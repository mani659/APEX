import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.mt5_interface import MT5Interface

class TestMT5Interface(unittest.TestCase):
    def test_connection(self):
        mt5 = MT5Interface()
        self.assertFalse(mt5.connected)
        
        mt5.connect()
        self.assertTrue(mt5.connected)
        
        # Test mock returns
        self.assertEqual(mt5.get_latest_tick(), 0.0)
        self.assertEqual(mt5.get_historical_bars(10), [])
        
        mt5.shutdown()
        self.assertFalse(mt5.connected)
        
        with self.assertRaises(ConnectionError):
            mt5.get_latest_tick()

if __name__ == '__main__':
    unittest.main()
