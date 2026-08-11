from enum import Enum
from typing import List
import time
from engine.core.execution_engine import Position, OrderDirection

class InventoryDecision(Enum):
    HOLD = 1
    EXIT_PROFIT = 2
    AGING_EXIT = 3

class InventoryManagement:
    def __init__(self, initial_risk_r: float = 2.0, max_bars_hold: int = 10, bar_duration_sec: float = 3600):
        self.initial_risk_r = initial_risk_r
        self.max_bars_hold = max_bars_hold
        self.bar_duration_sec = bar_duration_sec

    def manage_inventory(self, positions: List[Position], current_price: float, current_atr: float, current_time: float) -> InventoryDecision:
        if not positions:
            return InventoryDecision.HOLD
            
        inventory_count = len(positions)
        avg_entry = sum(p.entry_price for p in positions) / inventory_count
        
        # Determine overall direction from the first position
        direction = positions[0].direction
        
        # R-Multiple Target: Target grows with deeper baskets (simple scaling)
        target_r = self.initial_risk_r + (inventory_count * 0.5)
        target_distance = target_r * current_atr
        
        if direction == OrderDirection.BUY:
            take_profit = avg_entry + target_distance
            if current_price >= take_profit:
                return InventoryDecision.EXIT_PROFIT
        else:
            take_profit = avg_entry - target_distance
            if current_price <= take_profit:
                return InventoryDecision.EXIT_PROFIT
                
        # Aging Exit
        oldest_pos = min(positions, key=lambda p: p.open_time)
        age_sec = current_time - oldest_pos.open_time
        if age_sec > (self.max_bars_hold * self.bar_duration_sec):
            return InventoryDecision.AGING_EXIT
            
        return InventoryDecision.HOLD
