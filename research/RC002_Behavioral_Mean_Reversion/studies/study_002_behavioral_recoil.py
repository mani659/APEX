import os
import sys
import numpy as np
import pandas as pd
from types import MappingProxyType

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


def recompute_stats(data):
    a = 1.0 * np.array(data)
    n = len(a)
    if n == 0:
        return {
            "n": 0, "mean": 0, "median": 0, "std": 0, "se": 0,
            "ci_low": 0, "ci_high": 0, "effect_size": 0,
            "win_rate": 0, "expectancy": 0, "skew": 0, "kurt": 0
        }
    m = np.mean(a)
    std = np.std(a, ddof=1) if n > 1 else 0
    se = std / np.sqrt(n) if n > 0 else 0
    ci_low = m - 1.96 * se
    ci_high = m + 1.96 * se
    effect_size = m / std if std != 0 else 0
    
    pos_data = a[a > 0]
    neg_data = a[a < 0]
    win_rate = len(pos_data) / n if n > 0 else 0
    avg_win = np.mean(pos_data) if len(pos_data) > 0 else 0
    avg_loss = np.mean(neg_data) if len(neg_data) > 0 else 0
    expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)
    
    series = pd.Series(a)
    skew = series.skew()
    kurt = series.kurt()
    
    return {
        "n": n, "mean": m, "median": np.median(a) if n > 0 else 0,
        "std": std, "se": se, "ci_low": ci_low, "ci_high": ci_high,
        "effect_size": effect_size, "win_rate": win_rate,
        "expectancy": expectancy, "skew": skew, "kurt": kurt
    }

def print_stats(name, stats):
    if stats["n"] == 0:
        print(f"[{name}] N=0")
        return
    print(f"[{name}] N={stats['n']}")
    print(f"  Mean: {stats['mean']:.5f} | Std: {stats['std']:.5f} | Median: {stats['median']:.5f}")
    print(f"  95% CI: [{stats['ci_low']:.5f}, {stats['ci_high']:.5f}] | Effect Size: {stats['effect_size']:.3f}")
    print(f"  Win Rate: {stats['win_rate']*100:.1f}% | Expectancy: {stats['expectancy']:.5f}")
    print(f"  Skewness: {stats['skew']:.3f} | Kurtosis: {stats['kurt']:.3f}\n")


def main():
    print("=========================================================")
    print("RC002 Study 002: Behavioral Event Recoil Analysis")
    print("=========================================================")
    
    # 1. Load Data
    print("[1] Loading historical XAUUSD data...")
    df = load_data("XAUUSD")
    
    print("    Computing legacy indicators...")
    vol_features = build_volatility_features(df)
    
    limit = 100000
    if len(df) > limit:
        print(f"    Slicing data to most recent {limit} rows...")
        df = df.tail(limit).reset_index(drop=True)
        vol_features = vol_features.tail(limit).reset_index(drop=True)
        
    num_samples = len(df)
    print(f"    Total usable samples: {num_samples}")

    # 2. Setup Stores & Pipelines
    f_event = BehavioralEventFeature()
    pipeline = FeaturePipeline([f_event])
    f_store = FeatureStore()
    
    horizons = [5, 10, 20, 40]
    labels = [ForwardReturnLabel(horizon=h) for h in horizons]
    label_engine = LabelEngine(labels)
    l_store = LabelStore()
    
    print("[2] Executing FeaturePipeline & LabelEngine...")
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
    atrs = vol_features['atr'].fillna(1.0).values
    
    snapshots = []
    for i in range(num_samples):
        snapshots.append(MarketSnapshot(
            symbol="XAUUSD", timestamp=int(timestamps[i]), bid=float(closes[i]), ask=float(closes[i]) + 0.05, volume=float(volumes[i])
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
        
    # 3. Build Dataset
    print(f"[3] Building Dataset ({valid_samples} aligned records)...")
    dataset = build_dataset(f_store, l_store)
    
    # 4. Extract into DataFrame
    print("[4] Executing Analysis Across Horizons...")
    data_list = []
    
    for r in dataset.records:
        data_list.append({
            "event": r.features["behavioral_event_displacement"],
            "ret_5": r.labels["forward_return_5"],
            "ret_10": r.labels["forward_return_10"],
            "ret_20": r.labels["forward_return_20"],
            "ret_40": r.labels["forward_return_40"]
        })
    df_res = pd.DataFrame(data_list)
    
    # Segments
    bull_df = df_res[df_res['event'] == 1.0]
    bear_df = df_res[df_res['event'] == -1.0]
    
    results = {}
    for h in horizons:
        col = f"ret_{h}"
        bull_stats = recompute_stats(bull_df[col].dropna())
        bear_stats = recompute_stats(bear_df[col].dropna())
        
        results[h] = {
            "bull": bull_stats,
            "bear": bear_stats
        }
        
        print(f"\n--- HORIZON: {h} BARS ---")
        print_stats(f"Bullish Exhaustion H={h}", bull_stats)
        print_stats(f"Bearish Exhaustion H={h}", bear_stats)

    # Evaluate Recoil Development
    # We want negative returns for Bullish Exhaustion (bearish recoil)
    # We want positive returns for Bearish Exhaustion (bullish recoil)
    
    bullish_successes = 0
    bearish_successes = 0
    
    for h in horizons:
        bull_stat = results[h]["bull"]
        bear_stat = results[h]["bear"]
        
        if bull_stat["n"] >= 30:
            if bull_stat["ci_high"] < 0 and bull_stat["effect_size"] <= -0.05:
                bullish_successes += 1
                
        if bear_stat["n"] >= 30:
            if bear_stat["ci_low"] > 0 and bear_stat["effect_size"] >= 0.05:
                bearish_successes += 1

    if bullish_successes >= 2 and bearish_successes >= 2:
        conclusion = "SUPPORTED"
    elif bullish_successes > 0 or bearish_successes > 0:
        conclusion = "INCONCLUSIVE"
    else:
        conclusion = "NOT SUPPORTED"
        
    print(f"\nFinal Conclusion: {conclusion}")
    
    # 5. Archive to Experiment Repository
    print("[5] Archiving Experiment...")
    split_config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)
    exp_config = ExperimentConfig(
        experiment_name="Behavioral_Event_Recoil",
        experiment_version="1.0",
        split_config=split_config
    )
    experiment_record = run_experiment(dataset, exp_config)
    repo_path = os.path.join(os.path.dirname(__file__), "..", "repository")
    repo_config = RepositoryConfig(repository_path=repo_path, overwrite_existing=True)
    repo = ExperimentRepository(repo_config)
    repo_entry = repo.save(experiment_record)
    
    # Report output
    output_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    report_content = f"""# RC002 Study 002: Behavioral Event Recoil Analysis

## Final Research Conclusion
**{conclusion}**

### Target Hypothesis
After a Behavioral Exhaustion Event (3.0x ATR Displacement), does statistically significant mean reversion (recoil) occur?

### Experiment Execution
- **Experiment ID**: {repo_entry.experiment_id}
- **Dataset Size**: {valid_samples}
- **Horizons Analyzed**: 5, 10, 20, 40 bars

### Horizon Comparison

#### Bullish Exhaustion (Expecting Bearish Recoil / Negative Mean)
"""
    for h in horizons:
        stat = results[h]["bull"]
        report_content += f"- **H={h}**: Mean={stat['mean']:.4f} | 95% CI=[{stat['ci_low']:.4f}, {stat['ci_high']:.4f}] | Effect={stat['effect_size']:.3f} | Skew={stat['skew']:.2f} | Kurt={stat['kurt']:.2f}\n"

    report_content += "\n#### Bearish Exhaustion (Expecting Bullish Recoil / Positive Mean)\n"
    for h in horizons:
        stat = results[h]["bear"]
        report_content += f"- **H={h}**: Mean={stat['mean']:.4f} | 95% CI=[{stat['ci_low']:.4f}, {stat['ci_high']:.4f}] | Effect={stat['effect_size']:.3f} | Skew={stat['skew']:.2f} | Kurt={stat['kurt']:.2f}\n"

    report_content += f"""
### Behavioral Interpretation
- **Time Evolution**: By observing the means across 5, 10, 20, and 40 bars, we can see the time evolution of the mean reversion. 
- **Distribution Analysis**: High kurtosis indicates "fat tails" or explosive moves. Significant skewness indicates asymmetry in the payout.

### Verdict
The hypothesis is **{conclusion}**. Based on the strict requirement for robust CI excluding zero in the appropriate direction (negative for bullish exhaustion, positive for bearish exhaustion) and an absolute effect size > 0.05 on at least 2 horizons.
"""
        
    with open(os.path.join(output_dir, "Study_002_Report.md"), "w") as f:
        f.write(report_content)
        
    print("=========================================================")

if __name__ == "__main__":
    main()
