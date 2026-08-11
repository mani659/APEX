from dataclasses import dataclass, field
from typing import Any, Optional
from types import MappingProxyType

@dataclass(frozen=True)
class LabelResult:
    """
    Frozen representation of a label computation mapping future market outcomes.
    """
    label_name: str
    label_version: str
    value: Any
    confidence: Optional[float]
    horizon: int
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
