from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class ParticipationStateFeature(Feature):
    """
    ParticipationStateFeature

    Evaluates the participation state based on the volume rolling percentile.

    Returns:
    - 1.0  if volume_percentile > 0.75 (High Participation)
    - -1.0 if volume_percentile < 0.25 (Low Participation)
    - 0.0  otherwise (Normal)
    """

    @property
    def name(self) -> str:
        return "participation_state"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["indicator_cache"])

    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        
        # Read volume_percentile from cache, default to 0.5 (Normal) if missing
        vol_pct = cache.get("volume_percentile", 0.5)

        if vol_pct < 0.25:
            state = -1.0
        elif vol_pct > 0.75:
            state = 1.0
        else:
            state = 0.0

        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(state),
            confidence=1.0,
            metadata=MappingProxyType({
                "volume_percentile": float(vol_pct)
            })
        )
