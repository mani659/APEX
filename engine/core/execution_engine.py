from dataclasses import dataclass
from enum import Enum
import time

class OrderDirection(Enum):
    BUY = 1
    SELL = 2

@dataclass
class Position:
    ticket: int
    direction: OrderDirection
    entry_price: float
    volume: float
    open_time: float
    trace_id: str = ""

class ExecutionEngine:
    def __init__(self, default_volume: float = 0.01):
        self.default_volume = default_volume
        self.next_ticket = 1

    def execute_trade(self, direction: OrderDirection, entry_price: float, grid_distance: float) -> Position:
        # In a real environment, this would call MT5. 
        # In the reference engine, it deterministically simulates the position generation.
        pos = Position(
            ticket=self.next_ticket,
            direction=direction,
            entry_price=entry_price,
            volume=self.default_volume,
            open_time=time.time()
        )
        self.next_ticket += 1
        return pos
