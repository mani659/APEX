import os
import json
from datetime import datetime
from types import MappingProxyType
from typing import Tuple

from research.dataset.result import Dataset, DatasetRecord
from research.splitting.config import SplitConfig
from research.splitting.result import DatasetSplit
from research.validation.report import ValidationReport, ValidationIssue, Severity
from research.analysis.result import FeatureAnalysisResult, FeatureMetrics
from research.experiment.result import ExperimentRecord

from research.repository.config import RepositoryConfig
from research.repository.result import RepositoryEntry
from research.repository.errors import (
    RepositoryError, DuplicateExperimentError, 
    RepositoryReadError, RepositoryWriteError
)

# --- Deterministic Serialization ---

def _convert_to_dict(o: any) -> any:
    if hasattr(o, '__dataclass_fields__'):
        return {k: _convert_to_dict(getattr(o, k)) for k in o.__dataclass_fields__}
    elif isinstance(o, (frozenset, set)):
        return sorted(list(o))
    elif isinstance(o, MappingProxyType):
        return {k: _convert_to_dict(v) for k, v in o.items()}
    elif isinstance(o, (tuple, list)):
        return [_convert_to_dict(i) for i in o]
    elif isinstance(o, dict):
        return {k: _convert_to_dict(v) for k, v in o.items()}
    elif hasattr(o, 'value'): # Handle Enum
        return o.value
    else:
        return o

def _dict_to_dataset_record(d: dict) -> DatasetRecord:
    return DatasetRecord(
        timestamp=float(d["timestamp"]),
        features=MappingProxyType(d["features"]),
        labels=MappingProxyType(d["labels"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_dataset(d: dict) -> Dataset:
    return Dataset(
        records=tuple(_dict_to_dataset_record(r) for r in d["records"]),
        feature_names=frozenset(d["feature_names"]),
        label_names=frozenset(d["label_names"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_split_config(d: dict) -> SplitConfig:
    return SplitConfig(
        train_ratio=float(d["train_ratio"]),
        validation_ratio=float(d["validation_ratio"]),
        test_ratio=float(d["test_ratio"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_dataset_split(d: dict) -> DatasetSplit:
    return DatasetSplit(
        train_dataset=_dict_to_dataset(d["train_dataset"]),
        validation_dataset=_dict_to_dataset(d["validation_dataset"]),
        test_dataset=_dict_to_dataset(d["test_dataset"]),
        configuration=_dict_to_split_config(d["configuration"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_validation_issue(d: dict) -> ValidationIssue:
    return ValidationIssue(
        severity=Severity(d["severity"]),
        category=d["category"],
        message=d["message"],
        record_index=d.get("record_index"),
        feature_name=d.get("feature_name"),
        label_name=d.get("label_name"),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_validation_report(d: dict) -> ValidationReport:
    return ValidationReport(
        valid=bool(d["valid"]),
        issue_count=int(d["issue_count"]),
        error_count=int(d["error_count"]),
        warning_count=int(d["warning_count"]),
        issues=tuple(_dict_to_validation_issue(i) for i in d["issues"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_feature_metrics(d: dict) -> FeatureMetrics:
    return FeatureMetrics(
        feature_name=d["feature_name"],
        sample_count=int(d["sample_count"]),
        mean=float(d["mean"]),
        median=float(d["median"]),
        minimum=float(d["minimum"]),
        maximum=float(d["maximum"]),
        variance=float(d["variance"]),
        standard_deviation=float(d["standard_deviation"]),
        missing_ratio=float(d["missing_ratio"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_feature_analysis(d: dict) -> FeatureAnalysisResult:
    return FeatureAnalysisResult(
        feature_count=int(d["feature_count"]),
        analyzed_timestamp=d["analyzed_timestamp"],
        feature_metrics=tuple(_dict_to_feature_metrics(m) for m in d["feature_metrics"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_experiment_record(d: dict) -> ExperimentRecord:
    return ExperimentRecord(
        experiment_name=d["experiment_name"],
        experiment_version=d["experiment_version"],
        created_timestamp=d["created_timestamp"],
        validation_report=_dict_to_validation_report(d["validation_report"]),
        feature_analysis=_dict_to_feature_analysis(d["feature_analysis"]),
        dataset_split=_dict_to_dataset_split(d["dataset_split"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

def _dict_to_repository_entry(d: dict) -> RepositoryEntry:
    return RepositoryEntry(
        experiment_id=d["experiment_id"],
        created_timestamp=d["created_timestamp"],
        experiment_record=_dict_to_experiment_record(d["experiment_record"]),
        metadata=MappingProxyType(d.get("metadata", {}))
    )

# --- Engine ---

class ExperimentRepository:
    """
    Immutable storage archive for research experiments.
    """
    def __init__(self, config: RepositoryConfig):
        self.config = config
        os.makedirs(self.config.repository_path, exist_ok=True)
        
    def _get_path(self, exp_id: str) -> str:
        return os.path.join(self.config.repository_path, f"{exp_id}.json")
        
    def list(self) -> Tuple[str, ...]:
        files = [f for f in os.listdir(self.config.repository_path) if f.endswith(".json")]
        # experiment_000001.json -> experiment_000001
        ids = [f[:-5] for f in files]
        return tuple(sorted(ids))
        
    def exists(self, experiment_id: str) -> bool:
        return os.path.exists(self._get_path(experiment_id))
        
    def save(self, record: ExperimentRecord) -> RepositoryEntry:
        existing_ids = self.list()
        
        # Calculate next ID deterministically based on layout
        max_num = 0
        for eid in existing_ids:
            if eid.startswith("experiment_"):
                try:
                    num = int(eid.split("_")[1])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
                    
        next_id_num = max_num + 1
        exp_id = f"experiment_{next_id_num:06d}"
        
        file_path = self._get_path(exp_id)
        if os.path.exists(file_path) and not self.config.overwrite_existing:
            raise DuplicateExperimentError(f"Experiment {exp_id} already exists.")
            
        entry = RepositoryEntry(
            experiment_id=exp_id,
            created_timestamp=datetime.now().isoformat(),
            experiment_record=record,
            metadata=MappingProxyType({})
        )
        
        try:
            entry_dict = _convert_to_dict(entry)
            json_str = json.dumps(entry_dict, indent=2)
            with open(file_path, "w") as f:
                f.write(json_str)
        except Exception as e:
            raise RepositoryWriteError(f"Failed to write {exp_id}: {str(e)}")
            
        return entry
        
    def load(self, experiment_id: str) -> RepositoryEntry:
        file_path = self._get_path(experiment_id)
        if not os.path.exists(file_path):
            raise RepositoryReadError(f"Experiment {experiment_id} not found.")
            
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return _dict_to_repository_entry(data)
        except Exception as e:
            raise RepositoryReadError(f"Failed to load {experiment_id}: {str(e)}")
