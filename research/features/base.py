from abc import ABC, abstractmethod
from typing import FrozenSet
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class Feature(ABC):
    """
    Abstract base class for all research features.
    Features must be stateless, deterministic, and immutable.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the feature."""
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the feature."""
        pass
        
    @property
    @abstractmethod
    def required_inputs(self) -> FrozenSet[str]:
        """A frozenset of required input keys for this feature."""
        pass
        
    @abstractmethod
    def compute(self, context: FeatureContext) -> FeatureResult:
        """
        Compute the feature given the context.
        Must be side-effect free and deterministic.
        """
        pass
