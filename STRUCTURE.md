APEX Quant Research Framework

==========================================================
ROOT
==========================================================

apex/

│
├── config/
│   ├── settings.py
│   ├── constants.py
│   └── experiment_profiles.py
│
├── data/
│   ├── loader.py
│   ├── validator.py
│   ├── preprocessing.py
│   ├── indicators.py
│   ├── feature_builder.py
│   └── dataset_builder.py
│
├── features/
│   ├── helpers.py
│   ├── registry.py
│   ├── price.py
│   ├── volume.py
│   ├── session.py
│   ├── volatility.py
│   ├── trend.py
│   ├── momentum.py
│   ├── structure.py
│   ├── smart_money.py
│   └── regime.py
│
├── labels/
│   ├── labels.py
│   ├── future_returns.py
│   ├── grid_labels.py
│   ├── survival_labels.py
│   ├── execution_labels.py
│   └── validation.py
│
├── regimes/
│   ├── baseline.py
│   ├── continuation.py
│   ├── persistence.py
│   ├── transition.py
│   ├── adaptive_inventory.py
│   └── classifier.py
│
├── simulator/
│   ├── basket.py
│   ├── grid_engine.py
│   ├── payoff_engine.py
│   ├── execution.py
│   ├── inventory.py
│   ├── flash_events.py
│   └── monte_carlo.py
│
├── analytics/
│   ├── statistics.py
│   ├── parameter_surface.py
│   ├── feature_importance.py
│   ├── tail_analysis.py
│   └── reporting.py
│
├── ml/
│   ├── train.py
│   ├── validation.py
│   └── inference.py
│
├── mt5/
│   ├── signal_generator.py
│   ├── order_manager.py
│   ├── bridge.py
│   └── live_monitor.py
│
├── experiments/
│   ├── exp001_baseline.py
│   ├── exp002_flash.py
│   ├── exp003_inventory.py
│   └── ...
│
├── datasets/
│
├── reports/
│
├── docs/
│   ├── README.md
│   ├── CHARTER.md
│   ├── DESIGN_PRINCIPLES.md
│   ├── CODING_STANDARDS.md
│   ├── DECISIONS.md
│   ├── RESEARCH_INDEX.md
│   ├── ROADMAP.md
│   ├── MODULE_INDEX.md
│   └── CHANGELOG.md
│
├── development_status.py
├── apex_doctor.py
├── run_research.py
│
└── Structure.md

==========================================================
DATA FLOW
==========================================================

Raw CSV / Parquet
        │
        ▼
loader.py
        │
        ▼
validator.py
        │
        ▼
preprocessing.py
        │
        ▼
indicators.py
        │
        ▼
feature_builder.py
        │
        ▼
labels/
        │
        ▼
dataset_builder.py
        │
        ▼
Master Dataset
        │
        ▼
Regime Engine
        │
        ▼
Simulator
        │
        ▼
Analytics
        │
        ▼
Machine Learning
        │
        ▼
MT5 Live Execution