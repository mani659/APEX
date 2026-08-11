from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class ExpansionConfirmationFeature(Feature):
    """
    Measures immediate price expansion relative to volatility.
    Calculates (current_close - previous_close) / atr.
    Requires `atr` and `previous_close` to be injected into the indicator cache.
    """
    
    @property
    def name(self) -> str:
        return "normalized_expansion"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["market_snapshot", "indicator_cache"])
        
    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        snap = context.market_snapshot
        
        atr = cache.get("atr", 1.0)
        # Avoid division by zero
        if atr <= 0:
            atr = 1.0
            
        previous_close = cache.get("previous_close", snap.bid)
        current_close = snap.bid
        
        normalized_expansion = (current_close - previous_close) / atr
            
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(normalized_expansion),
            confidence=1.0,
            metadata=MappingProxyType({
                "atr_reference": float(atr),
                "absolute_expansion": float(current_close - previous_close)
            })
        )
