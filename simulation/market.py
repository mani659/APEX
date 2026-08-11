from dataclasses import dataclass

@dataclass(frozen=True)
class MarketSnapshot:
    """
    Immutable representation of the physical market reality at a specific point in time.
    """
    symbol: str
    timestamp: int
    bid: float
    ask: float
    volume: float = 0.0
