from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class LiquiditySweepFeature(Feature):
    """
    Computes institutional liquidity sweep utilizing prior quantitative research.
    Relies on `liquidity_sweep_high` and `liquidity_sweep_low` loaded into the 
    indicator cache by the legacy data pipeline.
    
    Returns a float representing sweep direction/strength:
      +1.0 for bullish sweep (liquidity_sweep_low)
      -1.0 for bearish sweep (liquidity_sweep_high)
       0.0 otherwise
    """
    
    @property
    def name(self) -> str:
        return "liquidity_sweep_strength"
        
    @property
    def version(self) -> str:
        return "2.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["market_snapshot", "indicator_cache"])
        
    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        
        sweep_high = cache.get("liquidity_sweep_high", 0)
        sweep_low = cache.get("liquidity_sweep_low", 0)
        
        sweep_strength = 0.0
        bullish_sweep = False
        bearish_sweep = False
        
        if sweep_low > 0:
            bullish_sweep = True
            sweep_strength = 1.0
        elif sweep_high > 0:
            bearish_sweep = True
            sweep_strength = -1.0
            
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(sweep_strength),
            confidence=1.0,
            metadata=MappingProxyType({
                "bullish_sweep": bullish_sweep,
                "bearish_sweep": bearish_sweep,
            })
        )
