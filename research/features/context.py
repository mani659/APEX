from dataclasses import dataclass, field
from typing import Mapping, Any
from types import MappingProxyType
from simulation.market import MarketSnapshot
from simulation.context import TradingContext

@dataclass(frozen=True)
class FeatureContext:
    """
    Immutable context holding market information required by features.
    Guarantees no modifications to incoming snapshots or caches can occur.
    """
    market_snapshot: MarketSnapshot
    trading_context: TradingContext
    indicator_cache: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
