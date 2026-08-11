from dataclasses import dataclass, field
from types import MappingProxyType
from research.features.result import FeatureResult

@dataclass(frozen=True)
class PipelineResult:
    """
    Immutable standard output object consumed by dataset builders.
    Preserves execution order naturally through dict insertion order within MappingProxyType.
    """
    timestamp: float
    feature_results: MappingProxyType[str, FeatureResult]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
