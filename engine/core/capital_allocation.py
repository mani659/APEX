class CapitalAllocation:
    def __init__(self, base_atr_multiplier: float = 1.0, inventory_scaling: float = 0.5):
        self.base_atr_multiplier = base_atr_multiplier
        self.inventory_scaling = inventory_scaling

    def calculate_grid_spacing(self, current_atr: float, current_inventory_count: int) -> float:
        if current_atr <= 0:
            return 0.0
            
        scaling_factor = 1.0 + (current_inventory_count * self.inventory_scaling)
        next_distance = current_atr * self.base_atr_multiplier * scaling_factor
        return next_distance
