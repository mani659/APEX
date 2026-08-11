from dataclasses import dataclass, field
from typing import Sequence
from types import MappingProxyType
from simulation.market import MarketSnapshot

@dataclass(frozen=True)
class LabelContext:
    """
    Immutable context holding a sequence of market snapshots and the current evaluation index.
    Restricts labels from accessing execution state, portfolios, or features.
    """
    snapshots: Sequence[MarketSnapshot]
    index: int
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
