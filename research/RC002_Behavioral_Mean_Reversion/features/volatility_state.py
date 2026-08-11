from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class VolatilityStateFeature(Feature):
    """
    VolatilityStateFeature

    Evaluates the volatility state based on the ATR rolling percentile.

    Returns:
    - 1.0  if atr_percentile > 0.75 (Expansion)
    - -1.0 if atr_percentile < 0.25 (Compression)
    - 0.0  otherwise (Normal)
    """

    @property
    def name(self) -> str:
        return "volatility_state"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["indicator_cache"])

    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        
        # Read atr_percentile from cache, default to 0.5 (Normal) if missing
        atr_pct = cache.get("atr_percentile", 0.5)

        if atr_pct < 0.25:
            state = -1.0
        elif atr_pct > 0.75:
            state = 1.0
        else:
            state = 0.0

        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(state),
            confidence=1.0,
            metadata=MappingProxyType({
                "atr_percentile": float(atr_pct)
            })
        )
