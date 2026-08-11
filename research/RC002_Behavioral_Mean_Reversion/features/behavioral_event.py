from types import MappingProxyType
from typing import FrozenSet
import sys
import os

# Ensure the base feature classes can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class BehavioralEventFeature(Feature):
    """
    Defines a deterministic Behavioral Exhaustion event based on Displacement.
    
    A Displacement Exhaustion occurs when the body size of a single candle 
    is extremely large relative to its local volatility (ATR).
    
    Condition: abs(close - open) > 3.0 * atr
    
    Returns:
      +1.0: Bullish Displacement (Panic buying, expecting a bearish mean reversion)
      -1.0: Bearish Displacement (Panic selling, expecting a bullish mean reversion)
       0.0: No event
    """
    
    @property
    def name(self) -> str:
        return "behavioral_event_displacement"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["market_snapshot", "indicator_cache"])
        
    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        
        c_open = cache.get("open", 0.0)
        c_close = cache.get("close", 0.0)
        atr = cache.get("atr", 1.0)
        
        if atr <= 0:
            atr = 1.0
            
        body_size = abs(c_close - c_open)
        
        event_value = 0.0
        
        if body_size > 3.0 * atr:
            if c_close > c_open:
                event_value = 1.0 # Bullish exhaustion
            elif c_close < c_open:
                event_value = -1.0 # Bearish exhaustion
                
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(event_value),
            confidence=1.0,
            metadata=MappingProxyType({
                "body_size": float(body_size),
                "atr": float(atr)
            })
        )
