from typing import Sequence
from types import MappingProxyType
from simulation.market import MarketSnapshot
from research.labeling.base import Label
from research.labeling.result import LabelResult

class ForwardReturnLabel(Label):
    """
    Computes deterministic future-return labels.
    Calculates the difference in bid price across a configurable horizon.
    """
    def __init__(self, horizon: int = 5):
        if horizon < 0:
            raise ValueError("Horizon must be >= 0")
        self._horizon = horizon
        
    @property
    def name(self) -> str:
        return f"forward_return_{self._horizon}"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_horizon(self) -> int:
        return self._horizon
        
    def compute(self, snapshots: Sequence[MarketSnapshot], index: int) -> LabelResult:
        if index + self.required_horizon >= len(snapshots):
            raise IndexError("Not enough forward snapshots to compute label.")
            
        current_bid = snapshots[index].bid
        future_bid = snapshots[index + self.required_horizon].bid
        
        future_return = future_bid - current_bid
        
        return LabelResult(
            label_name=self.name,
            label_version=self.version,
            value=float(future_return),
            confidence=1.0,
            horizon=self.required_horizon,
            metadata=MappingProxyType({"return_type": "absolute_bid_diff"})
        )
