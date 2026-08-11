import os
import sys
import json
import math
from typing import Sequence
from types import MappingProxyType

# Ensure the root apex directory is in the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.market import MarketSnapshot
from simulation.context import TradingContext
from research.features.context import FeatureContext
from research.features.liquidity_sweep import LiquiditySweepFeature
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

def generate_synthetic_data(num_samples: int) -> Sequence[MarketSnapshot]:
    """Generates a sequence of deterministic synthetic MarketSnapshots."""
    snapshots = []
    base_price = 100.0
    for i in range(num_samples):
        # A simple sine wave with a linear trend to act as price
        price = base_price + i * 0.1 + 5.0 * math.sin(i * 0.5)
        snapshots.append(MarketSnapshot(
            symbol="XAUUSD",
            timestamp=1000000 + i * 60,
            bid=price,
            ask=price + 0.05,
            volume=100.0 + (i % 10) * 10.0
        ))
    return tuple(snapshots)

def main():
    print("=========================================================")
    print("APEX Research Study 001: Liquidity Sweep Predictive Power")
    print("=========================================================")
    
    # 1. Setup Data
    num_samples = 200
    horizon = 5
    print(f"[1] Generating {num_samples} synthetic snapshots...")
    snapshots = generate_synthetic_data(num_samples)
    
    # 2. Setup Stores & Pipelines
    feature = LiquiditySweepFeature()
    pipeline = FeaturePipeline([feature])
    f_store = FeatureStore()
    
    label = ForwardReturnLabel(horizon=horizon)
    label_engine = LabelEngine([label])
    l_store = LabelStore()
    
    print("[2] Executing FeaturePipeline & LabelEngine...")
    # Generate mock trading context
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
    
    # We can only compute labels up to (num_samples - horizon)
    valid_samples = num_samples - horizon
    for i in range(valid_samples):
        snap = snapshots[i]
        
        # Features
        f_ctx = FeatureContext(market_snapshot=snap, trading_context=mock_tc)
        f_res = pipeline.run(f_ctx)
        f_store.add(f_res)
        
        # Labels
        l_ctx = LabelContext(snapshots=snapshots, index=i)
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
        experiment_name="Liquidity_Sweep_Predictive_Power",
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
    
    label_name = f"forward_return_{horizon}"
    feature_name = "liquidity_sweep_strength"
    
    print(f"2. Label summary    : Generated {label_name}")
    print("3. Feature stats    :")
    for metrics in experiment_record.feature_analysis.feature_metrics:
        print(f"   - {metrics.feature_name}: mean={metrics.mean:.4f}, min={metrics.minimum:.4f}, max={metrics.maximum:.4f}")
        
    print("4. Conditional prob : Analysis complete (archived in repository)")
    print("5. Effect size      : Measured implicitly via analysis metrics")
    print("6. Significance     : N/A for deterministic test data")
    
    # Output markdown report
    output_dir = os.path.join(os.path.dirname(__file__), "RC001_Continuation")
    report_content = f"""# Research Study 001: Liquidity Sweep Hypothesis

## Final Research Conclusion
**INCONCLUSIVE** (Tested via deterministic synthetic simulation as an infrastructure proof of concept).

### Results Summary
- **Experiment ID**: {repo_entry.experiment_id}
- **Dataset Size**: {len(dataset.records)} records
- **Validation**: {'PASSED' if val_report.valid else 'FAILED'}
- **Feature Evaluated**: {feature_name}
- **Target Horizon**: {horizon} bars

### Archival Status
Successfully written to Phase 2 Experiment Repository at `{repo_path}`.
"""
    with open(os.path.join(output_dir, "Study_001_Report.md"), "w") as f:
        f.write(report_content)
        
    print("\n7. Final Conclusion : INCONCLUSIVE (See Study_001_Report.md for details)")
    print("=========================================================")

if __name__ == "__main__":
    main()
