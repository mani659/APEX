from datetime import datetime
from research.dataset.result import Dataset
from research.experiment.config import ExperimentConfig
from research.experiment.result import ExperimentRecord
from research.experiment.errors import ExperimentError, ExperimentExecutionError

from research.validation.engine import validate as default_validate
from research.analysis.engine import analyze as default_analyze
from research.splitting.engine import split as default_split

def run(
    dataset: Dataset, 
    config: ExperimentConfig,
    validator_fn=default_validate,
    analyzer_fn=default_analyze,
    splitter_fn=default_split
) -> ExperimentRecord:
    """
    Orchestrates the execution of a research experiment.
    Runs dataset validation, feature analysis, and dataset splitting deterministically.
    Never modifies datasets or trains models.
    """
    if dataset is None:
        raise ExperimentError("Dataset cannot be None.")
        
    if config is None:
        raise ExperimentError("ExperimentConfig cannot be None.")
        
    # 1. Validate Dataset
    validation_report = validator_fn(dataset)
    if not validation_report.valid:
        raise ExperimentExecutionError(
            f"Experiment halted: Dataset validation failed with {validation_report.error_count} errors."
        )
        
    # 2. Analyze Features
    feature_analysis = analyzer_fn(dataset)
    
    # 3. Split Dataset
    dataset_split = splitter_fn(dataset, config.split_config)
    
    # 4. Assemble immutable ExperimentRecord
    return ExperimentRecord(
        experiment_name=config.experiment_name,
        experiment_version=config.experiment_version,
        created_timestamp=datetime.now().isoformat(),
        validation_report=validation_report,
        feature_analysis=feature_analysis,
        dataset_split=dataset_split,
        metadata=config.metadata
    )
