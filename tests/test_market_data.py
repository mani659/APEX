import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.core.market_data import MarketDataLayer

class TestMarketDataLayer(unittest.TestCase):
    def test_update_bar_and_tick(self):
        md = MarketDataLayer(atr_period=2)
        md.update_bar(100, 102, 98, 101, 10)
        snap = md.update_bar(101, 105, 100, 104, 15)
        self.assertTrue(snap.is_new_bar)
        self.assertEqual(snap.current_price, 104)
        self.assertTrue(snap.current_atr > 0)
        
        snap2 = md.update_tick(104.5)
        self.assertFalse(snap2.is_new_bar)
        self.assertEqual(snap2.current_price, 104.5)
        self.assertEqual(snap2.current_atr, snap.current_atr)

if __name__ == '__main__':
    unittest.main()
