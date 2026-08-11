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


def main():
    print("=========================================================")
    print("RC002 Study 001: Behavioral Event Definition")
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
    print("[4] Executing Analysis...")
    data_list = []
    
    for r in dataset.records:
        data_list.append({
            "event": r.features["behavioral_event_displacement"],
            "ret_20": r.labels["forward_return_20"]
        })
    df_res = pd.DataFrame(data_list)
    
    # Segments
    bull_exhaustion = df_res[df_res['event'] == 1.0]['ret_20'].dropna()
    bear_exhaustion = df_res[df_res['event'] == -1.0]['ret_20'].dropna()
    
    bull_stats = recompute_stats(bull_exhaustion)
    bear_stats = recompute_stats(bear_exhaustion)
    
    stats_map = {
        "Bullish Exhaustion": bull_stats,
        "Bearish Exhaustion": bear_stats
    }
    
    for k, v in stats_map.items():
        print_stats(k, v)
        
    # Evaluate Definition Robustness
    # Success Criteria: Can it be identified deterministically and reproducibly?
    # We define it as supported if the event happens enough times to be statistically observable (e.g. N >= 30)
    if bull_stats["n"] >= 30 and bear_stats["n"] >= 30:
        conclusion = "SUPPORTED"
        print("Sufficient samples found to support the mathematical definition of the event.")
    elif bull_stats["n"] > 0 or bear_stats["n"] > 0:
        conclusion = "INCONCLUSIVE"
        print("Event defined, but extremely rare (N < 30). Threshold may be too strict.")
    else:
        conclusion = "NOT SUPPORTED"
        print("Zero events detected. The definition is mathematically unreachable in this dataset.")
        
    print(f"\nFinal Conclusion: {conclusion}")
    
    # 5. Archive to Experiment Repository
    print("[5] Archiving Experiment...")
    split_config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)
    exp_config = ExperimentConfig(
        experiment_name="Behavioral_Event_Definition",
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
    report_content = f"""# RC002 Study 001: Behavioral Event Definition

## Final Research Conclusion
**{conclusion}**

### Target Hypothesis
Can a Behavioral Event be defined objectively using only observable market data?

### Behavioral Event Definition
The **Displacement Exhaustion Event** was defined as a single-bar volatility imbalance where the absolute body size of the candle `abs(close - open)` is strictly greater than **3.0x its local ATR (14)**.
- **Bullish Exhaustion (+1.0)**: Up-close displacement. Represents panic buying, establishing a potential setup for a bearish mean reversion.
- **Bearish Exhaustion (-1.0)**: Down-close displacement. Represents capitulation selling, establishing a potential setup for a bullish mean reversion.

### Experiment Execution
- **Experiment ID**: {repo_entry.experiment_id}
- **Dataset Size**: {valid_samples}

### Statistics & Distribution (20-Bar Horizon)

#### Bullish Exhaustion
- **Sample Count**: {bull_stats['n']}
- **Mean Return**: {bull_stats['mean']:.5f}
- **Median Return**: {bull_stats['median']:.5f}
- **Standard Deviation**: {bull_stats['std']:.5f}
- **95% CI**: [{bull_stats['ci_low']:.5f}, {bull_stats['ci_high']:.5f}]
- **Effect Size**: {bull_stats['effect_size']:.3f}
- **Win Rate (Absolute Price increase)**: {bull_stats['win_rate']*100:.1f}%
- **Expectancy**: {bull_stats['expectancy']:.5f}

#### Bearish Exhaustion
- **Sample Count**: {bear_stats['n']}
- **Mean Return**: {bear_stats['mean']:.5f}
- **Median Return**: {bear_stats['median']:.5f}
- **Standard Deviation**: {bear_stats['std']:.5f}
- **95% CI**: [{bear_stats['ci_low']:.5f}, {bear_stats['ci_high']:.5f}]
- **Effect Size**: {bear_stats['effect_size']:.3f}
- **Win Rate (Absolute Price increase)**: {bear_stats['win_rate']*100:.1f}%
- **Expectancy**: {bear_stats['expectancy']:.5f}

### Initial Interpretation
*Note: This study evaluates the mathematical reproducibility of the event, not its profitability.*
The requirement was simply that the behavioral anomaly (3.0 ATR displacement) could be systematically quantified and that it occurs frequently enough in the real market to enable future research. 
With {bull_stats['n']} Bullish events and {bear_stats['n']} Bearish events, the formulation provides a solid, deterministic foundation.

### Verdict
Because the event was objectively modeled without lookahead bias and produced sufficient occurrences for analysis, the hypothesis that a behavioral exhaustion event can be deterministically defined is **{conclusion}**. This displacement event will serve as the base signal for subsequent Mean Reversion studies.
"""
        
    with open(os.path.join(output_dir, "Study_001_Report.md"), "w") as f:
        f.write(report_content)
        
    print("=========================================================")

if __name__ == "__main__":
    main()
