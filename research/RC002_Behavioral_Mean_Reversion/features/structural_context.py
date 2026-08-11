from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class StructuralContextFeature(Feature):
    """
    StructuralContextFeature

    Evaluates the structural context based on the rolling range position.

    Returns:
    - 1.0  if rolling_range_position < 0.10 or rolling_range_position > 0.90 (Structural Extreme)
    - -1.0 if 0.40 <= rolling_range_position <= 0.60 (Structural Neutral)
    - 0.0  otherwise
    """

    @property
    def name(self) -> str:
        return "structural_context"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["indicator_cache"])

    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        
        # Read rolling_range_position from cache
        rr_pos = cache.get("rolling_range_position", 0.5)

        if rr_pos < 0.10 or rr_pos > 0.90:
            state = 1.0
        elif 0.40 <= rr_pos <= 0.60:
            state = -1.0
        else:
            state = 0.0

        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(state),
            confidence=1.0,
            metadata=MappingProxyType({
                "rolling_range_position": float(rr_pos)
            })
        )
