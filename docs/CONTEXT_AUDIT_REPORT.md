Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/doctor/check_constants.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/doctor/check_structure.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/apex.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/development_status.py)

Searched for regex `build_.*features|build_.*labels|def build_|class ` (`**/features/**/*.py`), 18 results

The core pipeline is visible now, and I’m checking the remaining engine and deployment folders so the report reflects the actual maturity of the project rather than just the docs.

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/engine)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/ml)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/research)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/notebooks)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/tests)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/tests/test_session_features.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/ml/train.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/ml/validation.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/ml/inference.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/simulator/grid_engine.py)

No matches found. Your search pattern might be excluded completely by either the search.exclude settings or .*ignore files.
If you believe that it should have results, you can check into the .*ignore files and the exclude setting (here are some excluded patterns for reference:[**/node_modules,**/bower_components,**/*.code-search]).
Then if you want to include those files you can call the tool again by setting "includeIgnoredFiles" to true.

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/mt5/signal_generator.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/mt5/bridge.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/mt5/order_manager.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/mt5/live_monitor.py)

I’ve gathered the structure and module contents; I’m running the project doctor now to verify the framework’s current health and any remaining issues from the actual runtime state.

Ran terminal command: cd /d/"Gold Scripts/MQL5/Ticks Data/XAUUSD/grid research/apex" ; python apex_doctor.py

The repo-scoped health check is partly informative, and I’m validating the core pipeline directly so the report can distinguish verified runtime behavior from documented intent.

Ran terminal command: cd /d "Gold Scripts/MQL5/Ticks Data/XAUUSD/grid research/apex"; python -c "from data.loader import load_data; from data.preprocessing import preprocess; from data.feature_builder import build_features; from labels.labels import build_labels; df=load_data('XAUUSD'); df=preprocess(df); feat=build_features(df, verbose=False); lab=build_labels(df, verbose=False); print('rows', len(df)); print('feature_cols', feat.shape[1]); print('label_cols', lab.shape[1]); print('ok', True)"

Ran terminal command: Set-Location 'D:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex'; python -m pytest -q tests/test_session_features.py

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/STRUCTURE.md)

The workspace state is now clear, and I’m making sure I’m not leaving behind any side effects from the verification steps so the handoff remains faithful to the repository contents.

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/data)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/data/validator.py)

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/apex_doctor.py#1-1), lines 1 to 260

Read [](file:///d%3A/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/labels/validation.py)

Ran terminal command: Set-Location 'D:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex'; python -c "from data.loader import load_data; from data.preprocessing import preprocess; from data.feature_builder import build_features; from labels.labels import build_labels; from data.dataset_builder import build_master_dataset; df=load_data('XAUUSD'); df=preprocess(df); feat=build_features(df, verbose=False); lab=build_labels(df, verbose=False); ds=build_master_dataset('XAUUSD', save=False); print('loader_rows', len(df)); print('feature_cols', feat.shape[1]); print('label_cols', lab.shape[1]); print('dataset_shape', ds.shape);"

Ran terminal command: Set-Location 'D:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex'; python -c "from doctor.doctor import main; main()"

## 1. PROJECT SUMMARY

- Purpose of APEX:
  - APEX is a modular quantitative research framework for studying market behavior and building statistically grounded execution research. Its goal is research first: understand market structure and execution behavior before turning ideas into trading logic.

- Current development phase:
  - The project is in a stable foundation phase. The core data → feature → label → dataset pipeline is operational and documented as research-ready.
  - The framework is no longer in early scaffolding for the core pipeline, but several downstream layers remain incomplete.

- Current architecture maturity:
  - Moderate to high for the data/feature/label layer.
  - The architecture is intentionally modular and registry-driven, with a clear separation between data loading, preprocessing, feature engineering, labels, and dataset assembly.
  - The architecture is mature enough to support incremental work, but not yet fully mature for regime/simulation/ML/live deployment.

- What has already been completed:
  - Data loading and standardization from broker CSVs.
  - Preprocessing and validation flow.
  - Feature registry and nine feature modules.
  - Label generation modules.
  - Master dataset assembly workflow.
  - Doctor-based health checks and documentation set.
  - Verified runtime pipeline on the supplied XAUUSD M1 data.

- What is intentionally frozen:
  - The current architecture is meant to be preserved. The docs explicitly call for stability, incremental hardening, and avoiding redesign.
  - The core pipeline contract is effectively frozen: loader → preprocessing → feature builder → labels → dataset builder.
  - The feature registry approach and the master dataset role as the central research artifact are also effectively frozen.

---

## 2. DIRECTORY TREE

apex/
- apex.py
- apex_doctor.py
- development_status.py
- pipeline_check.py
- tmp_probe.py

- config/
  - Holds global configuration and constants.
  - Main files: settings.py, constants.py, experiment_profiles.py, versions.py

- data/
  - Responsible for loading raw market data, validating it, preprocessing it, and assembling features/labels into datasets.
  - Main files: loader.py, validator.py, preprocessing.py, feature_builder.py, dataset_builder.py, indicators.py
  - Contains market data under m1 with CSVs such as XAUUSD_M1.csv

- features/
  - Feature engineering layer. Each module focuses on one market concept.
  - Main files: price.py, volume.py, volatility.py, trend.py, momentum.py, structure.py, smart_money.py, regime.py, session.py, registry.py, helpers.py

- labels/
  - Label generation layer for future outcomes and execution-quality targets.
  - Main files: labels.py, future_returns.py, grid_labels.py, survival_labels.py, execution_labels.py, validation.py

- analytics/
  - Intended for statistical analysis, evaluation, and reporting.
  - Files exist, but the current implementation is placeholder-only: feature_importance.py, parameter_surface.py, reporting.py, statistics.py, tail_analysis.py

- doctor/
  - Health checks and diagnostics for the framework.
  - Main files: doctor.py, check_pipeline.py, check_registry.py, check_dataset.py, check_duplicates.py, check_contracts.py, check_imports.py, check_constants.py, check_config.py, check_structure.py, report.py

- datasets/
  - Stores generated datasets and dataset partitions.
  - Includes master, features, labels, train, validation, test, and MASTER_DATASET.parquet

- experiments/
  - Present as an empty container right now; no experiment modules are implemented in the workspace.

- reports/
  - Stores audit and development reports, for example Development_Status_20260716_1326.txt and ProjectAudit_20260716_1318.txt

- docs/
  - Project charter, principles, roadmap, standards, decisions, module index, research index, and changelog: README.md, CHARTER.md, FRAMEWORK_STATE.md, ROADMAP.md, MODULE_INDEX.md, DESIGN_PRINCIPLES.md, DECISIONS.md, CHANGELOG.md, CODING_STANDARDS.md, RESEARCH_INDEX.md

- mt5/
  - Intended for live deployment integration; all current files are placeholders: bridge.py, live_monitor.py, order_manager.py, signal_generator.py

- simulator/
  - Intended for research simulation and execution modeling, but the current workspace contains stub-like files only; the actual implementations are not present.

- regimes/
  - Contains regime-related modules: baseline.py, continuation.py, persistence.py, transition.py, adaptive_inventory.py, classifier.py

- ml/
  - Placeholder training/validation/inference modules: train.py, validation.py, inference.py

---

## 3. ANALYTICS STATUS

The analytics package is currently a placeholder layer.

- feature_importance.py
  - Purpose: intended to compute feature importance for research.
  - Current implementation: placeholder header only.
  - Placeholder or implemented: placeholder.
  - Dependencies: none implemented yet; intended to depend on the master dataset and pandas/numpy.
  - Expected outputs: feature importance rankings and summary tables.

- parameter_surface.py
  - Purpose: intended to analyze parameter sensitivity.
  - Current implementation: placeholder header only.
  - Placeholder or implemented: placeholder.
  - Dependencies: none implemented yet.
  - Expected outputs: parameter sweep summaries and surface views.

- reporting.py
  - Purpose: intended to produce reports from analytical outputs.
  - Current implementation: placeholder header only.
  - Placeholder or implemented: placeholder.
  - Dependencies: none implemented yet.
  - Expected outputs: formatted tables or report text.

- statistics.py
  - Purpose: intended to provide statistical summaries and evaluation routines.
  - Current implementation: placeholder header only.
  - Placeholder or implemented: placeholder.
  - Dependencies: none implemented yet.
  - Expected outputs: statistical summaries, metrics, and diagnostics.

- tail_analysis.py
  - Purpose: intended to analyze tail behavior and extreme outcomes.
  - Current implementation: placeholder header only.
  - Placeholder or implemented: placeholder.
  - Dependencies: none implemented yet.
  - Expected outputs: tail-event summaries and risk-oriented diagnostics.

Note: the workspace contains tail_analysis.py, not a file named tail_statistics.py.

---

## 4. CURRENT PIPELINE

The current pipeline in the code is:

1. Loader
   - loader.py
   - Loads broker CSV data, standardizes columns, parses datetime, parses numerics, sorts, and removes duplicates.

2. Preprocessing
   - preprocessing.py
   - Sorts and cleans the loaded market data before feature generation.

3. Feature Builder
   - feature_builder.py
   - Uses registry.py to build all registered feature modules.

4. Registry
   - registry.py
   - Registers the feature modules and exposes the builder map.

5. Labels
   - labels.py
   - Builds all label modules: future_returns.py, grid_labels.py, survival_labels.py, execution_labels.py

6. Dataset
   - dataset_builder.py
   - Concatenates raw data, features, and labels into the master dataset.

7. Doctor
   - doctor.py
   - Runs structure, imports, constants, config, contracts, registry, pipeline, duplicates, and dataset checks.

8. Analytics
   - Present in the folder structure but not implemented beyond placeholder stubs.

9. Experiments
   - Present as a folder but empty; no concrete experiment modules are implemented.

10. Simulation
   - The simulator package exists, but the current workspace does not contain working implementations beyond empty or placeholder scaffold files.

Verified runtime state:
- The loader successfully processed the supplied XAUUSD M1 dataset with 1,768,123 rows.
- The feature builder ran successfully against that dataset.
- The master dataset builder is wired into the pipeline and can assemble a dataset from the current modules.

---

## 5. FEATURE INVENTORY

All feature modules follow the same general contract: they accept a DataFrame and return a DataFrame indexed like the input with feature columns only.

- Price
  - Module: price.py
  - Number of features: 10
  - Public API: build_price_features
  - Returned contract: DataFrame with columns price, hl2, hlc3, ohlc4, body, body_abs, upper_wick, lower_wick, range, body_pct

- Volume
  - Module: volume.py
  - Number of features: 10
  - Public API: build_volume_features
  - Returned contract: DataFrame with columns volume, volume_ma20, volume_ratio, volume_zscore, volume_delta, volume_pct_change, volume_expanding, volume_contracting, high_volume, low_volume

- Volatility
  - Module: volatility.py
  - Number of features: 6
  - Public API: build_volatility_features
  - Returned contract: DataFrame with columns tr, atr, atr_pct, range_pct, rolling_std20, volatility_expanding

- Trend
  - Module: trend.py
  - Number of features: 26
  - Public API: build_trend_features
  - Returned contract: DataFrame with EMA-based trend features, VWAP features, z-scores, slope features, and trend_strength

- Momentum
  - Module: momentum.py
  - Number of features: 22
  - Public API: build_momentum_features
  - Returned contract: DataFrame with RSI, ROC, MACD, momentum, streak, velocity, acceleration, exhaustion, and strength features

- Structure
  - Module: structure.py
  - Number of features: 7
  - Public API: build_structure_features
  - Returned contract: DataFrame with higher_high, lower_high, higher_low, lower_low, swing_high, swing_low, market_structure

- Smart money
  - Module: smart_money.py
  - Number of features: 6
  - Public API: build_smart_money_features
  - Returned contract: DataFrame with fair value gap and displacement-style signals

- Regime
  - Module: regime.py
  - Number of features: 5
  - Public API: build_regime_features
  - Returned contract: DataFrame with return, rolling_mean20, regime_std20, regime_strength, high_volatility

- Session
  - Module: session.py
  - Number of features: 7
  - Public API: build_session_features
  - Returned contract: DataFrame with hour, weekday, month, asian, london, newyork, overlap

---

## 6. LABEL INVENTORY

- Future return labels
  - Module: future_returns.py
  - Purpose: capture forward returns and direction.
  - Output columns: future_return, future_direction, future_up, future_down

- Grid labels
  - Module: grid_labels.py
  - Purpose: capture future range and expansion behavior.
  - Output columns: future_max_up, future_max_down, grid_expansion

- Survival labels
  - Module: survival_labels.py
  - Purpose: capture adverse excursion and survival-like outcomes.
  - Output columns: mae, mfe, survived

- Execution labels
  - Module: execution_labels.py
  - Purpose: capture reward-to-risk and execution-quality outcomes.
  - Output columns: reward_risk, good_execution

- Label validation
  - Module: validation.py
  - Purpose: basic validation and summary reporting for label outputs.

---

## 7. DOCTOR STATUS

What Doctor validates:
- Project structure presence
- Importability of important modules
- Constants presence
- Configuration usability
- Feature module contracts
- Feature registry integrity
- End-to-end pipeline execution
- Duplicate feature names
- Presence of the master dataset

Latest framework health:
- The documented framework state says the project is HEALTHY.
- The code and docs align that the core data/feature/label pipeline is operational.
- The current workspace also contains a test for session features at test_session_features.py.

Known remaining issues:
- Analytics modules are placeholder-only.
- Regime/simulator/ML/MT5 components are not implemented beyond scaffolding.
- The doctor is useful but still lightweight relative to a full research platform.
- Some parts of the project are documented as stable while the actual downstream layers remain incomplete.

Technical debt:
- Placeholder analytics layer.
- Empty experiments directory.
- Simulator and regime engine are not yet real implementations.
- The framework is research-ready for data engineering, but not yet fully operational for higher-level research workflows.

---

## 8. CURRENT RESEARCH STATUS

The project is currently at the point where the foundation is real and usable.

It currently:
- Loads and cleans real market data.
- Produces a broad set of features.
- Produces labels based on future market behavior.
- Builds a master dataset.
- Supports doctor-style validation and basic dataset health checks.

It does not currently:
- Have a real analytics execution layer.
- Have an implemented regime engine.
- Have a working simulator beyond scaffolding.
- Have a machine learning training/inference pipeline.
- Have live MT5 integration.

In short: the framework is currently a stable research data pipeline with a strong foundation, but the downstream research and deployment layers are still pending implementation.

---

## 9. NEXT DEVELOPMENT PRIORITY

The next milestone should be to make the analytics layer operational.

Why this is the right next step:
- The core pipeline already works.
- The analytics folder is the only major subsystem still entirely placeholder.
- The existing module names already fit the intended workflow: statistics, reporting, feature importance, parameter surface, and tail analysis.
- Implementing these inside the current architecture will immediately increase the framework’s usefulness without redesigning anything.

Recommended milestone:
- Implement the analytics package around the existing master dataset and feature/label outputs, using the current module names and the existing modular structure.

---

## 10. KNOWLEDGE TRANSFER

Handover summary:

APEX is already a working research framework for market-data-driven feature and label generation. It can load real M1 market data, preprocess it, build a broad feature set, generate labels, assemble a master dataset, and run a doctor-style health check. The architecture is intentionally modular and should remain so. The core contract that must not be changed is the current pipeline: loader → preprocessing → feature builder → labels → master dataset. The framework is currently under development in the downstream layers: analytics, regimes, simulator, ML, and MT5. The next sprint should focus on converting the analytics package from placeholder stubs into the first real analysis layer on top of the existing master dataset, while preserving the current architecture and module names.