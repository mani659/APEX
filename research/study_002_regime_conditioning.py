import os
import sys
import json
from typing import Sequence
from types import MappingProxyType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.loader import load_data
from features.smart_money import build_smart_money_features
from features.trend import build_trend_features
from features.regime import build_regime_features

from simulation.market import MarketSnapshot
from simulation.context import TradingContext
from research.features.context import FeatureContext
from research.features.liquidity_sweep import LiquiditySweepFeature
from research.features.market_regime import MarketRegimeFeature
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

def main():
    print("=========================================================")
    print("APEX Research Study 002: Liquidity Sweep + Market Regime")
    print("=========================================================")
    
    # 1. Load Data
    print("[1] Loading historical XAUUSD data...")
    df = load_data("XAUUSD")
    
    # Pre-calculate legacy features
    print("    Computing legacy indicators...")
    sm_features = build_smart_money_features(df)
    
    print("    Computing trend indicators (this may take a moment)...")
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        trend_features = build_trend_features(df)
        regime_features = build_regime_features(df)
    
    # Limit to most recent 100,000 rows to ensure timely execution
    limit = 100000
    if len(df) > limit:
        print(f"    Slicing data to most recent {limit} rows...")
        df = df.tail(limit).reset_index(drop=True)
        sm_features = sm_features.tail(limit).reset_index(drop=True)
        trend_features = trend_features.tail(limit).reset_index(drop=True)
        regime_features = regime_features.tail(limit).reset_index(drop=True)
        
    num_samples = len(df)
    print(f"    Total usable samples: {num_samples}")

    # 2. Setup Stores & Pipelines
    f_sweep = LiquiditySweepFeature()
    f_regime = MarketRegimeFeature()
    pipeline = FeaturePipeline([f_sweep, f_regime])
    f_store = FeatureStore()
    
    horizons = [5, 10, 20]
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
    
    print("    Building MarketSnapshots...")
    import pandas as pd
    timestamps = ((df['datetime'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1s')).values
    bids = df['close'].values
    asks = df['close'].values + 0.05
    volumes = df['volume'].values
    
    sweep_highs = sm_features['liquidity_sweep_high'].fillna(0).values
    sweep_lows = sm_features['liquidity_sweep_low'].fillna(0).values
    trend_strengths = trend_features['trend_strength'].fillna(3).values
    high_vols = regime_features['high_volatility'].fillna(0).values
    
    snapshots = []
    for i in range(num_samples):
        snapshots.append(MarketSnapshot(
            symbol="XAUUSD",
            timestamp=int(timestamps[i]),
            bid=float(bids[i]),
            ask=float(asks[i]),
            volume=float(volumes[i])
        ))
    snapshots_tuple = tuple(snapshots)
        
    print("    Running pipelines...")
    max_horizon = max(horizons)
    valid_samples = num_samples - max_horizon
    
    for i in range(valid_samples):
        snap = snapshots_tuple[i]
        
        # Features
        ind_cache = MappingProxyType({
            "liquidity_sweep_high": int(sweep_highs[i]),
            "liquidity_sweep_low": int(sweep_lows[i]),
            "trend_strength": float(trend_strengths[i]),
            "high_volatility": float(high_vols[i])
        })
        
        f_ctx = FeatureContext(market_snapshot=snap, trading_context=mock_tc, indicator_cache=ind_cache)
        f_res = pipeline.run(f_ctx)
        f_store.add(f_res)
        
        # Labels
        l_ctx = LabelContext(snapshots=snapshots_tuple, index=i)
        l_dict = label_engine.generate(l_ctx)
        l_res = LabelStoreResult(
            timestamp=snap.timestamp,
            label_results=MappingProxyType(l_dict)
        )
        l_store.add(l_res)
        
    # 3. Build Dataset
    print(f"[3] Building Dataset ({valid_samples} aligned records)...")
    dataset = build_dataset(f_store, l_store)
    
    # 4. Run Experiment
    print("[4] Executing ExperimentEngine...")
    split_config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)
    exp_config = ExperimentConfig(
        experiment_name="Liquidity_Sweep_Market_Regime",
        experiment_version="1.0",
        split_config=split_config
    )
    
    experiment_record = run_experiment(dataset, exp_config)
    
    # 5. Archive
    print("[5] Archiving Experiment...")
    repo_path = os.path.join(os.path.dirname(__file__), "RC001_Continuation", "repository")
    repo_config = RepositoryConfig(repository_path=repo_path, overwrite_existing=True)
    repo = ExperimentRepository(repo_config)
    repo_entry = repo.save(experiment_record)
    
    # 6. Deliverables Generation
    print("\n[6] Study Deliverables Generated:")
    print("---------------------------------")
    val_report = experiment_record.validation_report
    print(f"1. Dataset summary  : {len(dataset.records)} records valid: {val_report.valid}")
    print(f"2. Label summary    : Generated {dataset.label_names}")
    
    print("\n[ Conditional Regime Analysis ]")
    
    # Categorize subsets
    bullish_sweeps = [r for r in dataset.records if r.features["liquidity_sweep_strength"] > 0]
    bearish_sweeps = [r for r in dataset.records if r.features["liquidity_sweep_strength"] < 0]
    
    def get_subset(records, min_trend, max_trend):
        return [r for r in records if min_trend <= r.features["market_regime_trend_strength"] <= max_trend]
        
    # Regimes
    # Strong Bullish Trend: trend_strength >= 5
    # Strong Bearish Trend: trend_strength <= 1
    # Ranging/Mixed: 2 <= trend_strength <= 4
    
    bull_sweeps_bull_trend = get_subset(bullish_sweeps, 5, 6)
    bull_sweeps_bear_trend = get_subset(bullish_sweeps, 0, 1)
    bull_sweeps_ranging = get_subset(bullish_sweeps, 2, 4)
    
    bear_sweeps_bear_trend = get_subset(bearish_sweeps, 0, 1)
    bear_sweeps_bull_trend = get_subset(bearish_sweeps, 5, 6)
    bear_sweeps_ranging = get_subset(bearish_sweeps, 2, 4)
    
    def print_return(subset, name):
        count = len(subset)
        if count == 0:
            print(f"   {name} [n=0] -> N/A")
            return 0.0
        r20 = sum(r.labels["forward_return_20"] for r in subset) / count
        print(f"   {name} [n={count}] -> Mean 20-bar Return: {r20:.5f}")
        return r20
        
    print("\n>> Bullish Sweeps Conditioned on Regime:")
    r_bull_in_bull = print_return(bull_sweeps_bull_trend, "Bull Sweep in Strong Bull Trend")
    r_bull_in_bear = print_return(bull_sweeps_bear_trend, "Bull Sweep in Strong Bear Trend")
    r_bull_in_rng  = print_return(bull_sweeps_ranging,    "Bull Sweep in Ranging Market     ")
    
    print("\n>> Bearish Sweeps Conditioned on Regime:")
    r_bear_in_bear = print_return(bear_sweeps_bear_trend, "Bear Sweep in Strong Bear Trend")
    r_bear_in_bull = print_return(bear_sweeps_bull_trend, "Bear Sweep in Strong Bull Trend")
    r_bear_in_rng  = print_return(bear_sweeps_ranging,    "Bear Sweep in Ranging Market     ")
    
    conclusion = "INCONCLUSIVE"
    # Does Market Regime materially improve the predictive value?
    # If a Bull Sweep has significantly better returns in a Bull trend than in a Bear trend
    # Or if a Bear Sweep has significantly more negative returns in a Bear trend than in a Bull trend
    
    diff_bull = r_bull_in_bull - r_bull_in_bear
    diff_bear = r_bear_in_bear - r_bear_in_bull # Should be negative if bear sweep in bear trend drops more
    
    if diff_bull > 0.05 and diff_bear < -0.05:
        conclusion = "SUPPORTED"
        strongest = "Trend Continuation (Bull sweep in Bull trend, Bear sweep in Bear trend)"
    elif r_bull_in_bear > r_bull_in_bull and r_bear_in_bull < r_bear_in_bear:
        conclusion = "SUPPORTED"
        strongest = "Reversal (Bull sweep in Bear trend, Bear sweep in Bull trend)"
    else:
        strongest = "N/A"
        
    print(f"\n7. Final Conclusion : {conclusion}")
    
    # Report output
    output_dir = os.path.join(os.path.dirname(__file__), "RC001_Continuation")
    report_content = f"""# Research Study 002: Liquidity Sweep + Market Regime

## Final Research Conclusion
**{conclusion}**

### Results Summary
- **Experiment ID**: {repo_entry.experiment_id}
- **Dataset Size**: {len(dataset.records)} records
- **Validation**: {'PASSED' if val_report.valid else 'FAILED'}
- **Features Evaluated**: liquidity_sweep_strength, market_regime_trend_strength
- **Target Horizons**: 5, 10, 20 bars

### Conditional Return Analysis (Horizon=20)
| Condition | Sample Size | Mean Forward Return |
|-----------|-------------|---------------------|
| Bull Sweep in Bull Trend | {len(bull_sweeps_bull_trend)} | {r_bull_in_bull:.5f} |
| Bull Sweep in Ranging | {len(bull_sweeps_ranging)} | {r_bull_in_rng:.5f} |
| Bull Sweep in Bear Trend | {len(bull_sweeps_bear_trend)} | {r_bull_in_bear:.5f} |
| Bear Sweep in Bear Trend | {len(bear_sweeps_bear_trend)} | {r_bear_in_bear:.5f} |
| Bear Sweep in Ranging | {len(bear_sweeps_ranging)} | {r_bear_in_rng:.5f} |
| Bear Sweep in Bull Trend | {len(bear_sweeps_bull_trend)} | {r_bear_in_bull:.5f} |

### Findings
The conditioning variable (Market Regime) produced the strongest effect under: **{strongest}**.

### Archival Status
Successfully written to Phase 2 Experiment Repository at `{repo_path}`.
"""
    with open(os.path.join(output_dir, "Study_002_Report.md"), "w") as f:
        f.write(report_content)
        
    print("=========================================================")

if __name__ == "__main__":
    main()
