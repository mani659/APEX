import unittest
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.core.execution_engine import Position, OrderDirection
from engine.core.inventory_management import InventoryManagement, InventoryDecision

class TestInventoryManagement(unittest.TestCase):
    def test_manage_inventory(self):
        im = InventoryManagement(initial_risk_r=2.0, max_bars_hold=10, bar_duration_sec=60)
        
        now = time.time()
        pos = Position(1, OrderDirection.BUY, 100.0, 0.1, now)
        
        # Scenario 1: Hold (price < TP, not aged)
        # Target R = 2.0 + 0.5 = 2.5. ATR = 2.0. Dist = 5.0. TP = 105.0.
        dec1 = im.manage_inventory([pos], 102.0, 2.0, now)
        self.assertEqual(dec1, InventoryDecision.HOLD)
        
        # Scenario 2: Exit Profit (price >= TP)
        dec2 = im.manage_inventory([pos], 105.1, 2.0, now)
        self.assertEqual(dec2, InventoryDecision.EXIT_PROFIT)
        
        # Scenario 3: Aging Exit
        # Max bars = 10, bar duration = 60s -> 600s max hold.
        dec3 = im.manage_inventory([pos], 100.0, 2.0, now + 601)
        self.assertEqual(dec3, InventoryDecision.AGING_EXIT)

if __name__ == '__main__':
    unittest.main()
