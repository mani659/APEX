from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class BehavioralArchetypeFeature(Feature):
    """
    BehavioralArchetypeFeature

    Evaluates the archetype of the Behavioral Exhaustion event based on the 
    preceding 3 candles' momentum.

    Returns:
    - 1.0: Single-Candle Shock (prev 3 bars absolute body sum < 1.0 * ATR)
    - 2.0: Multi-Candle Acceleration (prev 3 bars directional body sum matches event direction and > 2.0 * ATR)
    - 0.0: Standard Exhaustion
    """

    @property
    def name(self) -> str:
        return "behavioral_archetype"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["indicator_cache"])

    def compute(self, context: FeatureContext) -> FeatureResult:
        cache = context.indicator_cache
        
        atr = cache.get("atr", 1.0)
        if atr <= 0:
            atr = 1.0
            
        event_val = cache.get("event_val", 0.0) # Passed from study script or pipeline
        prev_3_abs_body = cache.get("prev_3_abs_body", 0.0)
        prev_3_dir_body = cache.get("prev_3_dir_body", 0.0)
        
        state = 0.0
        if event_val != 0.0:
            if prev_3_abs_body < 1.0 * atr:
                state = 1.0 # Shock
            else:
                # Directional check
                if event_val == 1.0 and prev_3_dir_body > 2.0 * atr:
                    state = 2.0 # Bullish Acceleration
                elif event_val == -1.0 and prev_3_dir_body < -2.0 * atr:
                    state = 2.0 # Bearish Acceleration
                    
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(state),
            confidence=1.0,
            metadata=MappingProxyType({
                "prev_3_abs_body": float(prev_3_abs_body),
                "prev_3_dir_body": float(prev_3_dir_body)
            })
        )
