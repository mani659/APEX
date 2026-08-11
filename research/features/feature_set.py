from typing import List, Dict
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class FeatureSet:
    """
    Lightweight orchestrator for executing a collection of features.
    Execution order equals insertion order. No dependency graph.
    """
    def __init__(self, features: List[Feature]):
        self._features = features
        
    def compute(self, context: FeatureContext) -> Dict[str, FeatureResult]:
        """
        Iterates synchronously and returns the results.
        No caching, no optimization. Just orchestration.
        """
        results = {}
        for feature in self._features:
            results[feature.name] = feature.compute(context)
        return results
