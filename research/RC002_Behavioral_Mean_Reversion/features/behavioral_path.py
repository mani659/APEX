from types import MappingProxyType
from typing import FrozenSet
from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class BehavioralPathFeature(Feature):
    """
    Computes path dependency variables leading into the Behavioral Event.
    """
    
    @property
    def name(self) -> str:
        return "behavioral_path_data"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["indicator_cache"])
        
    def compute(self, ctx: FeatureContext) -> FeatureResult:
        cache = ctx.indicator_cache
        event_val = cache.get("event_val", 0.0)
        
        if event_val == 0.0:
            return FeatureResult(
                feature_name=self.name,
                feature_version=self.version,
                value=0.0,
                confidence=1.0,
                metadata=MappingProxyType({
                    "homogeneity": 0.0,
                    "expansion": 0.0,
                    "vol_slope": 0.0
                })
            )
            
        prev_5_dir = cache.get("prev_5_dir", 0.0)
        prev_5_atr = cache.get("prev_5_atr", 1.0)
        prev_15_atr = cache.get("prev_15_atr", 1.0)
        vol_slope = cache.get("prev_10_vol_slope", 0.0)
        
        homogeneity = prev_5_dir / 5.0
        
        expansion = 0.0
        if prev_15_atr > 0:
            expansion = prev_5_atr / prev_15_atr
            
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=1.0,
            confidence=1.0,
            metadata=MappingProxyType({
                "homogeneity": float(homogeneity),
                "expansion": float(expansion),
                "vol_slope": float(vol_slope)
            })
        )

