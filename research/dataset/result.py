from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Tuple, FrozenSet

@dataclass(frozen=True)
class DatasetRecord:
    """
    Immutable representation of a single aligned sample containing both features and labels.
    """
    timestamp: float
    features: MappingProxyType[str, float]
    labels: MappingProxyType[str, float]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class Dataset:
    """
    Immutable, deterministically aligned collection of DatasetRecords ready for machine learning.
    """
    records: Tuple[DatasetRecord, ...]
    feature_names: FrozenSet[str]
    label_names: FrozenSet[str]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
