from typing import Sequence
from types import MappingProxyType
from research.features.base import Feature
from research.features.context import FeatureContext
from research.pipeline.result import PipelineResult
from research.pipeline.errors import DuplicateFeatureError, FeatureExecutionError

class FeaturePipeline:
    """
    Executes registered research features in a deterministic sequence
    and produces a complete immutable feature vector mapping.
    """
    
    def __init__(self, features: Sequence[Feature]):
        self._validate_unique_names(features)
        self._features = tuple(features)
        
    def _validate_unique_names(self, features: Sequence[Feature]) -> None:
        seen = set()
        for f in features:
            if f.name in seen:
                raise DuplicateFeatureError(f"Duplicate feature name detected: '{f.name}'")
            seen.add(f.name)
            
    def run(self, context: FeatureContext) -> PipelineResult:
        """
        Executes all features exactly once, preserving registration order.
        Never skips, mutates, caches, or parallels execution.
        Fails immediately if one throws.
        """
        results = {}
        
        for feature in self._features:
            try:
                results[feature.name] = feature.compute(context)
            except Exception as ex:
                raise FeatureExecutionError(feature.name, ex) from ex
                
        return PipelineResult(
            timestamp=context.market_snapshot.timestamp,
            feature_results=MappingProxyType(results)
        )
