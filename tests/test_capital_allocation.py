import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.core.capital_allocation import CapitalAllocation

class TestCapitalAllocation(unittest.TestCase):
    def test_calculate_grid_spacing(self):
        ca = CapitalAllocation(base_atr_multiplier=1.0, inventory_scaling=0.5)
        
        # Scenario 1: No inventory (count = 0) -> distance = 1.0 * ATR
        dist_0 = ca.calculate_grid_spacing(current_atr=2.0, current_inventory_count=0)
        self.assertEqual(dist_0, 2.0)
        
        # Scenario 2: 1 open position -> distance = (1.0 + 0.5) * ATR = 1.5 * 2.0 = 3.0
        dist_1 = ca.calculate_grid_spacing(current_atr=2.0, current_inventory_count=1)
        self.assertEqual(dist_1, 3.0)
        
        # Scenario 3: 2 open positions -> distance = (1.0 + 1.0) * ATR = 2.0 * 2.0 = 4.0
        dist_2 = ca.calculate_grid_spacing(current_atr=2.0, current_inventory_count=2)
        self.assertEqual(dist_2, 4.0)

if __name__ == '__main__':
    unittest.main()
