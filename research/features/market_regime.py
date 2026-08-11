from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class MarketRegimeFeature(Feature):
    """
    Computes institutional market regime utilizing prior quantitative research.
    Relies on `trend_strength` and `high_volatility` loaded into the 
    indicator cache by the legacy data pipeline.
    
    Returns a float representing trend strength:
      0.0 to 1.0 -> Strong Bearish
      2.0 to 4.0 -> Ranging / Mixed
      5.0 to 6.0 -> Strong Bullish
    """
    
    @property
    def name(self) -> str:
        return "market_regime_trend_strength"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["market_snapshot", "indicator_cache"])
        
    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        
        trend_strength = cache.get("trend_strength", 3.0) # default to ranging
        high_volatility = cache.get("high_volatility", 0.0)
        
        regime_class = "RANGING"
        if trend_strength >= 5:
            regime_class = "TRENDING_BULL"
        elif trend_strength <= 1:
            regime_class = "TRENDING_BEAR"
            
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(trend_strength),
            confidence=1.0,
            metadata=MappingProxyType({
                "high_volatility": bool(high_volatility),
                "regime_class": regime_class
            })
        )
