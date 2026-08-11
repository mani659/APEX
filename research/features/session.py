from types import MappingProxyType
from typing import FrozenSet
import datetime

from research.features.base import Feature
from research.features.context import FeatureContext
from research.features.result import FeatureResult

class SessionFeature(Feature):
    """
    Classifies the market session based on the timestamp.
    Mapping:
    - 00:00 - 07:59: Asian
    - 08:00 - 12:59: London
    - 13:00 - 15:59: London/NY Overlap
    - 16:00 - 20:59: New York
    - 21:00 - 23:59: Other
    """
    
    @property
    def name(self) -> str:
        return "market_session"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["market_snapshot"])
        
    def compute(self, context: FeatureContext) -> FeatureResult:
        snap = context.market_snapshot
        
        # Determine UTC hour
        dt = datetime.datetime.utcfromtimestamp(snap.timestamp)
        hour = dt.hour
        
        if 0 <= hour < 8:
            session_id = 0  # Asian
        elif 8 <= hour < 13:
            session_id = 1  # London
        elif 13 <= hour < 16:
            session_id = 2  # London/NY Overlap
        elif 16 <= hour < 21:
            session_id = 3  # New York
        else:
            session_id = 4  # Other
            
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=float(session_id),
            confidence=1.0,
            metadata=MappingProxyType({
                "utc_hour": hour
            })
        )
