from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Tuple

@dataclass(frozen=True)
class FeatureMetrics:
    feature_name: str
    sample_count: int
    mean: float
    median: float
    minimum: float
    maximum: float
    variance: float
    standard_deviation: float
    missing_ratio: float
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class FeatureAnalysisResult:
    feature_count: int
    analyzed_timestamp: str
    feature_metrics: Tuple[FeatureMetrics, ...]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
