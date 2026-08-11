from abc import ABC, abstractmethod
from typing import Sequence
from simulation.market import MarketSnapshot
from research.labeling.context import LabelContext
from research.labeling.result import LabelResult

class Label(ABC):
    """
    Abstract base class for all research labels.
    Labels compute future outcomes deterministically using only historical snapshots.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the label."""
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the label."""
        pass
        
    @property
    @abstractmethod
    def required_horizon(self) -> int:
        """Number of forward snapshots required. Must be >= 0."""
        pass
        
    @abstractmethod
    def compute(self, snapshots: Sequence[MarketSnapshot], index: int) -> LabelResult:
        """
        Compute the label outcome for the given index in the snapshot sequence.
        Must be stateless and deeply immutable.
        """
        pass
