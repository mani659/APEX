from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class LiquiditySweepClassificationFeature(Feature):
    """
    Classifies a liquidity sweep into behavioral categories based on Rejection Strength.
    
    Categories:
      0.0: No Sweep
      1.0: Strong Rejection (Close in the favorable half of the sweeping candle)
      2.0: Weak Rejection (Close in the unfavorable half of the sweeping candle)
      
    Requires 'open', 'high', 'low', 'close' in the indicator cache.
    """
    
    @property
    def name(self) -> str:
        return "sweep_rejection_class"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["market_snapshot", "indicator_cache"])
        
    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        
        sweep_high = cache.get("liquidity_sweep_high", 0)
        sweep_low = cache.get("liquidity_sweep_low", 0)
        
        c_open = cache.get("open", 0.0)
        c_high = cache.get("high", 0.0)
        c_low = cache.get("low", 0.0)
        c_close = cache.get("close", 0.0)
        
        taxonomy_class = 0.0 # No Sweep
        
        # Safe midpoint calculation
        if c_high > c_low:
            midpoint = (c_high + c_low) / 2.0
            
            if sweep_low > 0:
                # Bullish Sweep: We want a strong rejection (close >= midpoint)
                if c_close >= midpoint:
                    taxonomy_class = 1.0 # Strong Rejection
                else:
                    taxonomy_class = 2.0 # Weak Rejection
                    
            elif sweep_high > 0:
                # Bearish Sweep: We want a strong rejection (close <= midpoint)
                if c_close <= midpoint:
                    taxonomy_class = 1.0 # Strong Rejection
                else:
                    taxonomy_class = 2.0 # Weak Rejection
        else:
            # If high == low, it's a flat candle, can't be a strong rejection
            if sweep_low > 0 or sweep_high > 0:
                taxonomy_class = 2.0
                
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(taxonomy_class),
            confidence=1.0,
            metadata=MappingProxyType({
                "candle_high": float(c_high),
                "candle_low": float(c_low),
                "candle_close": float(c_close)
            })
        )
