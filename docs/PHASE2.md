# Phase 2 — Research Operating System

Phase 2 replaces the initial simulation-focused architecture with a fully deterministic, immutable research operating system designed to strictly evaluate and validate trading logic.

## Frozen Architecture
The Phase 2 Research Infrastructure is officially frozen. It consists of 10 completed modules that operate sequentially in a strict unidirectional pipeline.

### 1. Research Feature Library
- **Purpose**: Defines pure mathematical feature transformations.
- **Responsibilities**: Computes stateless features based on provided market snapshots.
- **Public API**: `compute_features(snapshot)`
- **Inputs**: `MarketSnapshot`
- **Outputs**: `FeatureResult`
- **Dependencies**: None.
- **Architectural boundaries**: No access to historical state.
- **Immutability guarantees**: Features are frozen upon creation.
- **Determinism guarantees**: Absolute mathematical determinism.

### 2. Feature Pipeline
- **Purpose**: Orchestrates feature extraction sequentially.
- **Responsibilities**: Maps market snapshots sequentially through the feature library.
- **Public API**: `Pipeline`, `process(snapshot)`
- **Inputs**: `MarketSnapshot`
- **Outputs**: `PipelineResult`
- **Dependencies**: Research Feature Library
- **Architectural boundaries**: Connects data to features.
- **Immutability guarantees**: Produces frozen `PipelineResult`.
- **Determinism guarantees**: Executes features in strict, sorted deterministic order.

### 3. Feature Store
- **Purpose**: Caches feature vectors chronologically.
- **Responsibilities**: Stores and retrieves immutable pipeline results in memory.
- **Public API**: `FeatureStore.append()`, `FeatureStore.get_at()`, `FeatureStore.get_range()`
- **Inputs**: `PipelineResult`
- **Outputs**: `PipelineResult` list
- **Dependencies**: Feature Pipeline
- **Architectural boundaries**: Operates purely in-memory.
- **Immutability guarantees**: Rejects out-of-order appends; read-only retrieval.
- **Determinism guarantees**: Chronological integrity via timestamp enforcement.

### 4. Research Labeling Engine
- **Purpose**: Generates deterministic future-looking labels.
- **Responsibilities**: Looks ahead in the Feature Store to assign objective outcome classes.
- **Public API**: `generate_label(current_idx, feature_store, label_func)`
- **Inputs**: `FeatureStore`, Labeling Function
- **Outputs**: `LabelResult`
- **Dependencies**: Feature Store
- **Architectural boundaries**: Decoupled entirely from features.
- **Immutability guarantees**: Generated labels are deeply frozen.
- **Determinism guarantees**: Evaluates forward paths identically across runs.

### 5. Dataset Builder
- **Purpose**: Joins features and labels into research datasets.
- **Responsibilities**: Performs strict structural joining of features and labels, ensuring index alignment.
- **Public API**: `build_dataset(feature_results, label_results)`
- **Inputs**: List of `PipelineResult`, List of `LabelResult`
- **Outputs**: `Dataset`
- **Dependencies**: Feature Pipeline, Research Labeling Engine
- **Architectural boundaries**: Zero feature computation, purely structural.
- **Immutability guarantees**: Outputs deeply nested `@dataclass(frozen=True)` Datasets.
- **Determinism guarantees**: Strict sorting and alignment.

### 6. Dataset Validation Engine
- **Purpose**: Verifies dataset structural soundness.
- **Responsibilities**: Validates constraints without mutating or repairing datasets.
- **Public API**: `validate(dataset)`
- **Inputs**: `Dataset`
- **Outputs**: `ValidationReport`
- **Dependencies**: Dataset Builder
- **Architectural boundaries**: No data modification or filtering.
- **Immutability guarantees**: Returns a strictly frozen report.
- **Determinism guarantees**: Strict logic evaluations with no randomness.

### 7. Feature Analysis Engine
- **Purpose**: Evaluates statistical properties of features.
- **Responsibilities**: Calculates metrics (mean, median, variance, missing ratio) across features.
- **Public API**: `analyze(dataset)`
- **Inputs**: `Dataset`
- **Outputs**: `FeatureAnalysisResult`
- **Dependencies**: Dataset Builder
- **Architectural boundaries**: Read-only statistical review.
- **Immutability guarantees**: Preserves dataset integrity exactly.
- **Determinism guarantees**: Relies entirely on standard library statistical functions.

### 8. Dataset Split Engine
- **Purpose**: Partitions datasets chronologically.
- **Responsibilities**: Slices datasets into train/validation/test partitions without overlap or gaps.
- **Public API**: `split(dataset, config)`
- **Inputs**: `Dataset`, `SplitConfig`
- **Outputs**: `DatasetSplit`
- **Dependencies**: Dataset Builder
- **Architectural boundaries**: No data shuffling or class balancing.
- **Immutability guarantees**: Subsets maintain deep freezing.
- **Determinism guarantees**: Uses direct integer-index slice calculations.

### 9. Experiment Engine
- **Purpose**: Orchestrates complete research experiments.
- **Responsibilities**: Coordinates validation, analysis, and splitting sequentially without performing business logic itself.
- **Public API**: `run(dataset, config)`
- **Inputs**: `Dataset`, `ExperimentConfig`
- **Outputs**: `ExperimentRecord`
- **Dependencies**: Validation Engine, Analysis Engine, Split Engine
- **Architectural boundaries**: Strictly orchestration, no execution of simulations.
- **Immutability guarantees**: `ExperimentRecord` wraps all stage outputs immutably.
- **Determinism guarantees**: Halts execution identically on validation failure.

### 10. Experiment Repository
- **Purpose**: Archives research experiments permanently.
- **Responsibilities**: Performs deterministic JSON serialization/deserialization to/from the filesystem.
- **Public API**: `save(record)`, `load(id)`, `list()`, `exists(id)`
- **Inputs**: `ExperimentRecord`
- **Outputs**: `RepositoryEntry`
- **Dependencies**: Experiment Engine
- **Architectural boundaries**: Zero integration with databases.
- **Immutability guarantees**: Serialization operates non-destructively on `ExperimentRecord`.
- **Determinism guarantees**: Uses strictly deterministic dictionary conversions.
