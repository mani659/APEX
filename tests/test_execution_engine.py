import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.core.execution_engine import ExecutionEngine, OrderDirection

class TestExecutionEngine(unittest.TestCase):
    def test_execute_trade(self):
        ee = ExecutionEngine(default_volume=0.1)
        
        pos1 = ee.execute_trade(OrderDirection.BUY, 100.5, 2.0)
        self.assertEqual(pos1.ticket, 1)
        self.assertEqual(pos1.direction, OrderDirection.BUY)
        self.assertEqual(pos1.entry_price, 100.5)
        self.assertEqual(pos1.volume, 0.1)
        
        pos2 = ee.execute_trade(OrderDirection.SELL, 98.0, 3.0)
        self.assertEqual(pos2.ticket, 2)
        self.assertEqual(pos2.direction, OrderDirection.SELL)

if __name__ == '__main__':
    unittest.main()
