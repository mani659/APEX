from dataclasses import dataclass, field
from typing import Any, Optional
from types import MappingProxyType

@dataclass(frozen=True)
class FeatureResult:
    """
    Frozen representation of a feature computation.
    Metadata is optional descriptive information only. Never read metadata inside strategy logic.
    """
    feature_name: str
    feature_version: str
    value: Any
    confidence: Optional[float]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
