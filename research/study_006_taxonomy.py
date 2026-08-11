import os
import sys
import numpy as np
import pandas as pd
from types import MappingProxyType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.loader import load_data
from features.smart_money import build_smart_money_features

from simulation.market import MarketSnapshot
from simulation.context import TradingContext
from research.features.context import FeatureContext
from research.features.liquidity_sweep import LiquiditySweepFeature
from research.features.sweep_taxonomy import LiquiditySweepClassificationFeature
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
            "win_rate": 0, "expectancy": 0
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
    return {
        "n": n, "mean": m, "median": np.median(a) if n > 0 else 0,
        "std": std, "se": se, "ci_low": ci_low, "ci_high": ci_high,
        "effect_size": effect_size, "win_rate": win_rate,
        "expectancy": expectancy
    }

def print_stats(name, stats):
    if stats["n"] == 0:
        print(f"[{name}] N=0")
        return
    print(f"[{name}] N={stats['n']}")
    print(f"  Mean: {stats['mean']:.5f} | Std: {stats['std']:.5f} | Median: {stats['median']:.5f}")
    print(f"  95% CI: [{stats['ci_low']:.5f}, {stats['ci_high']:.5f}] | Effect Size: {stats['effect_size']:.3f}")
    print(f"  Win Rate: {stats['win_rate']*100:.1f}% | Expectancy: {stats['expectancy']:.5f}\n")

def evaluate_rules(stats_res, is_bullish):
    if stats_res["n"] < 200:
        return False
    ci_excludes_zero = (stats_res['ci_low'] > 0) if is_bullish else (stats_res['ci_high'] < 0)
    econ_sig = abs(stats_res['effect_size']) >= 0.05
    win_rate_ok = stats_res['win_rate'] >= 0.50
    return ci_excludes_zero and econ_sig and win_rate_ok

def main():
    print("=========================================================")
    print("APEX Research Study 006: Liquidity Sweep Taxonomy")
    print("=========================================================")
    
    # 1. Load Data
    print("[1] Loading historical XAUUSD data...")
    df = load_data("XAUUSD")
    
    print("    Computing legacy indicators...")
    sm_features = build_smart_money_features(df)
    
    limit = 100000
    if len(df) > limit:
        print(f"    Slicing data to most recent {limit} rows...")
        df = df.tail(limit).reset_index(drop=True)
        sm_features = sm_features.tail(limit).reset_index(drop=True)
        
    num_samples = len(df)
    print(f"    Total usable samples: {num_samples}")

    # 2. Setup Stores & Pipelines
    f_sweep = LiquiditySweepFeature()
    f_taxonomy = LiquiditySweepClassificationFeature()
    pipeline = FeaturePipeline([f_sweep, f_taxonomy])
    f_store = FeatureStore()
    
    horizons = [20]
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
    highs = df['high'].values
    lows = df['low'].values
    closes = df['close'].values
    volumes = df['volume'].values
    
    sweep_highs = sm_features['liquidity_sweep_high'].fillna(0).values
    sweep_lows = sm_features['liquidity_sweep_low'].fillna(0).values
    
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
            "liquidity_sweep_high": int(sweep_highs[i]),
            "liquidity_sweep_low": int(sweep_lows[i]),
            "open": float(opens[i]),
            "high": float(highs[i]),
            "low": float(lows[i]),
            "close": float(closes[i])
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
    print("[4] Executing Configured Subset Analysis...")
    data_list = []
    
    taxonomy_map = {
        0.0: "No Sweep",
        1.0: "Strong Rejection",
        2.0: "Weak Rejection"
    }
    
    for r in dataset.records:
        tax_val = r.features["sweep_rejection_class"]
        data_list.append({
            "sweep": r.features["liquidity_sweep_strength"],
            "taxonomy": taxonomy_map.get(tax_val, "Unknown"),
            "ret_20": r.labels["forward_return_20"]
        })
    df_res = pd.DataFrame(data_list)
    
    print("\nTaxonomy Distribution (Sweeps Only):")
    sweep_df = df_res[df_res['taxonomy'] != "No Sweep"]
    print(sweep_df['taxonomy'].value_counts())
    print("\n")
    
    # Segment configurations
    bull_sweeps = df_res[df_res['sweep'] > 0]
    bear_sweeps = df_res[df_res['sweep'] < 0]
    
    # Base
    bull_base = bull_sweeps['ret_20'].dropna()
    bear_base = bear_sweeps['ret_20'].dropna()
    base_bull_stats = recompute_stats(bull_base)
    base_bear_stats = recompute_stats(bear_base)
    
    classes = ["Strong Rejection", "Weak Rejection"]
    stats_map = {
        "Base (Bull)": base_bull_stats,
        "Base (Bear)": base_bear_stats
    }
    
    class_stats = {}
    
    for c in classes:
        bull_c = bull_sweeps[bull_sweeps['taxonomy'] == c]['ret_20'].dropna()
        bear_c = bear_sweeps[bear_sweeps['taxonomy'] == c]['ret_20'].dropna()
        
        bull_stats = recompute_stats(bull_c)
        bear_stats = recompute_stats(bear_c)
        
        stats_map[f"{c} (Bull)"] = bull_stats
        stats_map[f"{c} (Bear)"] = bear_stats
        
        class_stats[c] = {
            "bull": bull_stats,
            "bear": bear_stats,
            "bull_eval": evaluate_rules(bull_stats, is_bullish=True),
            "bear_eval": evaluate_rules(bear_stats, is_bullish=False)
        }
        
    for k, v in stats_map.items():
        print_stats(k, v)
        
    # Evaluate
    supported_classes = []
    for c in classes:
        if class_stats[c]["bull_eval"] and class_stats[c]["bear_eval"]:
            supported_classes.append(c)

    if len(supported_classes) > 0:
        conclusion = "SUPPORTED"
        print(f"Supported Classes: {supported_classes}")
    elif any(class_stats[c]["bull_eval"] or class_stats[c]["bear_eval"] for c in classes):
        conclusion = "INCONCLUSIVE"
        print("Some classes show partial support (FRAGILE).")
    else:
        conclusion = "NOT SUPPORTED"
        print("No taxonomy class significantly isolates the edge.")
        
    print(f"\nFinal Conclusion: {conclusion}")
    
    # 5. Archive to Experiment Repository
    print("[5] Archiving Experiment...")
    split_config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)
    exp_config = ExperimentConfig(
        experiment_name="Liquidity_Sweep_Taxonomy",
        experiment_version="1.0",
        split_config=split_config
    )
    experiment_record = run_experiment(dataset, exp_config)
    repo_path = os.path.join(os.path.dirname(__file__), "RC001_Continuation", "repository")
    repo_config = RepositoryConfig(repository_path=repo_path, overwrite_existing=True)
    repo = ExperimentRepository(repo_config)
    repo_entry = repo.save(experiment_record)
    
    # Report output
    output_dir = os.path.join(os.path.dirname(__file__), "RC001_Continuation")
    report_content = f"""# Research Study 006: Liquidity Sweep Taxonomy

## Final Research Conclusion
**{conclusion}**

### Target Hypothesis
Can liquidity sweeps be partitioned into distinct behavioral classes (Strong Rejection vs Weak Rejection), and does one class exhibit statistically meaningful predictive power?

### Experiment Execution
- **Experiment ID**: {repo_entry.experiment_id}
- **Dataset Size**: {valid_samples}
- **Taxonomy Method**: Rejection Strength (Candle close relative to high-low midpoint)

### Step-by-Step Edge Construction (20-Bar Horizon)

#### 1. Base Hypothesis (All Liquidity Sweeps)
- Bullish: Mean={stats_map['Base (Bull)']['mean']:.5f} | Effect Size={stats_map['Base (Bull)']['effect_size']:.3f} | Win Rate={stats_map['Base (Bull)']['win_rate']*100:.1f}% | 95% CI=[{stats_map['Base (Bull)']['ci_low']:.5f}, {stats_map['Base (Bull)']['ci_high']:.5f}]
- Bearish: Mean={stats_map['Base (Bear)']['mean']:.5f} | Effect Size={stats_map['Base (Bear)']['effect_size']:.3f} | Win Rate={stats_map['Base (Bear)']['win_rate']*100:.1f}% | 95% CI=[{stats_map['Base (Bear)']['ci_low']:.5f}, {stats_map['Base (Bear)']['ci_high']:.5f}]

#### 2. Taxonomy Classes
"""
    for c in classes:
        bull = stats_map[f"{c} (Bull)"]
        bear = stats_map[f"{c} (Bear)"]
        report_content += f"""
##### {c}
- **Bullish**: Mean={bull['mean']:.5f} | Effect={bull['effect_size']:.3f} | Win Rate={bull['win_rate']*100:.1f}% | CI=[{bull['ci_low']:.5f}, {bull['ci_high']:.5f}] | Sig={class_stats[c]['bull_eval']}
- **Bearish**: Mean={bear['mean']:.5f} | Effect={bear['effect_size']:.3f} | Win Rate={bear['win_rate']*100:.1f}% | CI=[{bear['ci_low']:.5f}, {bear['ci_high']:.5f}] | Sig={class_stats[c]['bear_eval']}
"""
    
    report_content += f"""
### Verdict
The taxonomy configuration was strictly evaluated against statistical significance (directional CI), economic significance (abs(Effect) >= 0.05), and sample adequacy.
Based on the rules, the hypothesis is **{conclusion}**.
"""
    if len(supported_classes) > 0:
        report_content += f"\nRecommendation: The {', '.join(supported_classes)} class(es) should be retained as the foundation for future continuation research, and the other classes should be discarded.\n"
    else:
        report_content += f"\nRecommendation: The taxonomy failed to isolate a strictly profitable directional edge. Re-evaluating the underlying continuation premise may be necessary.\n"
        
    with open(os.path.join(output_dir, "Study_006_Report.md"), "w") as f:
        f.write(report_content)
        
    print("=========================================================")

if __name__ == "__main__":
    main()
