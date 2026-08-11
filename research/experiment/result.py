from dataclasses import dataclass, field
from types import MappingProxyType
from research.validation.report import ValidationReport
from research.analysis.result import FeatureAnalysisResult
from research.splitting.result import DatasetSplit

@dataclass(frozen=True)
class ExperimentRecord:
    experiment_name: str
    experiment_version: str
    created_timestamp: str
    validation_report: ValidationReport
    feature_analysis: FeatureAnalysisResult
    dataset_split: DatasetSplit
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
