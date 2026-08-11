import os
import sys
import numpy as np
import pandas as pd
from types import MappingProxyType
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from data.loader import load_data
from features.volatility import build_volatility_features

from simulation.market import MarketSnapshot
from simulation.context import TradingContext
from research.features.context import FeatureContext
from research.RC002_Behavioral_Mean_Reversion.features.behavioral_event import BehavioralEventFeature
from research.pipeline.pipeline import FeaturePipeline
from research.store.store import FeatureStore

from research.labeling.context import LabelContext
from research.labels.forward_return import ForwardReturnLabel
from research.labeling.engine import LabelEngine
from research.store.label_store import LabelStore, LabelStoreResult

from research.dataset.builder import build_dataset
from research.experiment.config import ExperimentConfig
from research.splitting.config import SplitConfig
from research.experiment.engine import run as run_experiment
from research.repository.config import RepositoryConfig
from research.repository.engine import ExperimentRepository

def calculate_entropy(counts):
    total = sum(counts)
    if total == 0:
        return 0.0
    entropy = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            entropy -= p * math.log2(p)
    return entropy

def classify(event_val, ret_5, ret_20, atr):
    if event_val == 0.0:
        return None
    expected_dir = -1.0 if event_val == 1.0 else 1.0
    recoil_5 = ret_5 * expected_dir
    recoil_20 = ret_20 * expected_dir
    threshold = atr * 1.0
    
    if recoil_5 > threshold:
        return "Immediate Recoil"
    elif recoil_20 > threshold:
        return "Delayed Recoil"
    elif recoil_20 < -threshold:
        return "Momentum Continuation"
    else:
        return "Volatility Absorption"

def main():
    print("=========================================================")
    print("RC002 Study 005: Entropy Reduction Through Pre-Event Context")
    print("=========================================================")
    
    symbols = ["XAUUSD", "XAGUSD", "EURUSD", "BTCUSD", "NAS100"]
    horizons = [5, 20]
    
    all_data = []
    
    repo_path = os.path.join(os.path.dirname(__file__), "..", "repository")
    repo_config = RepositoryConfig(repository_path=repo_path, overwrite_existing=True)
    repo = ExperimentRepository(repo_config)
    
    for symbol in symbols:
        print(f"\n[Loading Data for {symbol}]")
        try:
            df = load_data(symbol)
        except Exception as e:
            print(f"Failed to load {symbol}: {e}")
            continue
            
        print("    Computing legacy indicators & SMA 50...")
        vol_features = build_volatility_features(df)
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        limit = 100000
        if len(df) > limit:
            df = df.tail(limit).reset_index(drop=True)
            vol_features = vol_features.tail(limit).reset_index(drop=True)
            
        num_samples = len(df)
        print(f"    Total usable samples: {num_samples}")

        f_event = BehavioralEventFeature()
        pipeline = FeaturePipeline([f_event])
        f_store = FeatureStore()
        
        labels = [ForwardReturnLabel(horizon=h) for h in horizons]
        label_engine = LabelEngine(labels)
        l_store = LabelStore()
        
        mock_tc = TradingContext(
            timestamp=0, bar_index=0, session="NYC", day_of_week=1, market_open=True,
            current_price=100.0, spread=0.05, volatility_regime="LOW", trend_regime="FLAT",
            market_structure="RANGE", atr=1.0, equity=10000.0, balance=10000.0,
            floating_pnl=0.0, closed_pnl=0.0, drawdown=0.0, daily_pnl=0.0, max_drawdown=0.0,
            open_positions=0, long_positions=0, short_positions=0, net_exposure=0.0,
            margin_used=0.0, available_margin=10000.0, daily_loss_limit_hit=False,
            risk_enabled=True, max_positions_reached=False, trading_paused=False,
            last_fill_price=0.0, last_slippage=0.0, last_commission=0.0, last_trade_time=0
        )
        
        timestamps = ((df['datetime'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1s')).values
        opens = df['open'].values
        closes = df['close'].values
        volumes = df['volume'].values
        smas = df['sma_50'].bfill().values
        atrs = vol_features['atr'].fillna(1.0).values
        
        snapshots = []
        for i in range(num_samples):
            snapshots.append(MarketSnapshot(
                symbol=symbol, timestamp=int(timestamps[i]), bid=float(closes[i]), ask=float(closes[i]) + 0.05, volume=float(volumes[i])
            ))
        snapshots_tuple = tuple(snapshots)
            
        print("    Running pipelines...")
        max_horizon = max(horizons)
        valid_samples = num_samples - max_horizon
        
        for i in range(valid_samples):
            snap = snapshots_tuple[i]
            
            ind_cache = MappingProxyType({
                "open": float(opens[i]),
                "close": float(closes[i]),
                "atr": float(atrs[i])
            })
            
            f_ctx = FeatureContext(market_snapshot=snap, trading_context=mock_tc, indicator_cache=ind_cache)
            f_res = pipeline.run(f_ctx)
            f_store.add(f_res)
            
            l_ctx = LabelContext(snapshots=snapshots_tuple, index=i)
            l_dict = label_engine.generate(l_ctx)
            l_res = LabelStoreResult(timestamp=snap.timestamp, label_results=MappingProxyType(l_dict))
            l_store.add(l_res)
            
        print(f"    Building Dataset & Classifying Context...")
        dataset = build_dataset(f_store, l_store)
        
        sym_data = []
        for i, r in enumerate(dataset.records):
            event_val = r.features["behavioral_event_displacement"]
            if event_val == 0.0:
                continue
                
            ret_5 = r.labels["forward_return_5"]
            ret_20 = r.labels["forward_return_20"]
            atr = atrs[i] if atrs[i] > 0 else 1.0
            
            response = classify(event_val, ret_5, ret_20, atr)
            distance_from_mean = abs(closes[i] - smas[i]) / atr
            
            # Context state
            is_extended = distance_from_mean > 1.5
            
            sym_data.append({
                "symbol": symbol,
                "event": event_val,
                "ret_5": ret_5,
                "ret_20": ret_20,
                "atr": atr,
                "distance": distance_from_mean,
                "is_extended": is_extended,
                "response": response
            })
            
        all_data.extend(sym_data)
        
        # Archive experiment independently
        df_sym = pd.DataFrame(sym_data)
        split_config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)
        exp_config = ExperimentConfig(
            experiment_name=f"Behavioral_Entropy_{symbol}",
            experiment_version="1.0",
            split_config=split_config
        )
        experiment_record = run_experiment(dataset, exp_config)
        repo.save(experiment_record)

    df_res = pd.DataFrame(all_data)
    total_events = len(df_res)
    
    print(f"\nTotal Events Evaluated: {total_events}")
    
    categories = ["Immediate Recoil", "Delayed Recoil", "Momentum Continuation", "Volatility Absorption"]
    max_entropy = math.log2(4) # 2.0
    
    # 1. Baseline Entropy
    baseline_counts = df_res['response'].value_counts()
    base_counts_arr = [baseline_counts.get(cat, 0) for cat in categories]
    base_entropy = calculate_entropy(base_counts_arr)
    
    # 2. Conditioned Entropy (Extended Subset)
    df_extended = df_res[df_res['is_extended'] == True]
    ext_counts = df_extended['response'].value_counts()
    ext_counts_arr = [ext_counts.get(cat, 0) for cat in categories]
    ext_entropy = calculate_entropy(ext_counts_arr)
    
    # Calculation
    abs_reduction = base_entropy - ext_entropy
    rel_reduction = (abs_reduction / base_entropy * 100) if base_entropy > 0 else 0
    
    print(f"Baseline Entropy: {base_entropy:.4f}")
    print(f"Conditioned Entropy: {ext_entropy:.4f}")
    print(f"Absolute Reduction: {abs_reduction:.4f}")
    print(f"Relative Reduction: {rel_reduction:.2f}%")
    
    # Cross Market Analysis
    market_metrics = []
    for sym in symbols:
        df_s = df_res[df_res['symbol'] == sym]
        if len(df_s) == 0: continue
        b_cnts = [df_s['response'].value_counts().get(c, 0) for c in categories]
        b_ent = calculate_entropy(b_cnts)
        
        df_s_ext = df_s[df_s['is_extended'] == True]
        if len(df_s_ext) == 0: continue
        e_cnts = [df_s_ext['response'].value_counts().get(c, 0) for c in categories]
        e_ent = calculate_entropy(e_cnts)
        
        red = (b_ent - e_ent) / b_ent * 100 if b_ent > 0 else 0
        market_metrics.append((sym, b_ent, e_ent, red))
        
    # Verdict logic
    # To be "SUPPORTED", we require at least a 10% relative entropy reduction globally, 
    # indicating meaningful information gain.
    if rel_reduction > 10.0:
        conclusion = "SUPPORTED"
    elif rel_reduction > 3.0:
        conclusion = "PARTIALLY SUPPORTED"
    else:
        conclusion = "NOT SUPPORTED"
        
    print(f"\nFinal Conclusion: {conclusion}")
    
    # Output Report
    output_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    report_content = f"""# RC002 Study 005: Entropy Reduction Through Pre-Event Context

## Final Research Conclusion
**{conclusion}**

### Target Hypothesis
Can one deterministic contextual variable (Distance from Local Mean > 1.5 ATR) significantly reduce Behavioral Response entropy?

---

## 1. Primary Metrics

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **Baseline Shannon Entropy** | {base_entropy:.4f} | Represents the unconditioned uncertainty of the taxonomy (Max 2.0). |
| **Conditioned Shannon Entropy** | {ext_entropy:.4f} | Represents uncertainty when conditioned on the 'Extended' state. |
| **Absolute Entropy Reduction** | {abs_reduction:.4f} | Information Gain provided by the contextual variable. |
| **Relative Entropy Reduction** | {rel_reduction:.2f}% | The percentage improvement in predictability. |

## 2. Response Frequency Comparison

How did the transition matrix shift when we only looked at Extreme Displacements occurring far away from the mean?

| Response Class | Baseline (N={len(df_res)}) | Conditioned (N={len(df_extended)}) | Shift |
| :--- | :--- | :--- | :--- |
"""
    base_probs = {cat: (base_counts_arr[i]/len(df_res))*100 for i, cat in enumerate(categories)} if len(df_res) > 0 else {}
    ext_probs = {cat: (ext_counts_arr[i]/len(df_extended))*100 for i, cat in enumerate(categories)} if len(df_extended) > 0 else {}
    
    for cat in categories:
        shift = ext_probs.get(cat, 0) - base_probs.get(cat, 0)
        report_content += f"| {cat} | {base_probs.get(cat, 0):.1f}% | {ext_probs.get(cat, 0):.1f}% | {shift:+.1f}% |\n"

    report_content += """
## 3. Cross-Market Information Gain

Does this entropy reduction generalize across different asset classes?

| Market | Baseline Entropy | Conditioned Entropy | Entropy Reduction (%) |
| :--- | :--- | :--- | :--- |
"""
    for sym, b_ent, e_ent, red in market_metrics:
        report_content += f"| {sym} | {b_ent:.4f} | {e_ent:.4f} | {red:+.1f}% |\n"
        
    report_content += f"""
## 4. Contextual Interpretation

- **Did it meaningfully partition responses?** If the conditioned matrix heavily skews toward Immediate/Delayed Recoil while crushing Momentum Continuation, it proves that exhaustion requires spatial extension.
- **Statistical Significance**: A {rel_reduction:.2f}% reduction in entropy indicates the variable's predictive power.

### Verdict
The hypothesis that pre-event context reduces the entropy of the Behavioral Response Taxonomy is **{conclusion}**. 
"""

    with open(os.path.join(output_dir, "Study_005_Report.md"), "w", encoding='utf-8') as f:
        f.write(report_content)
        
    print("=========================================================")

if __name__ == "__main__":
    main()
