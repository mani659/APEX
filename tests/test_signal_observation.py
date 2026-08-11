import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.core.market_data import MarketSnapshot
from engine.core.signal_observation import SignalObservation

class TestSignalObservation(unittest.TestCase):
    def test_detect_event(self):
        so = SignalObservation(displacement_threshold=3.0)
        
        # Scenario 1: Not enough data
        snap_empty = MarketSnapshot(current_price=100, current_atr=0.0, closes=[], volumes=[], is_new_bar=False)
        self.assertFalse(so.detect_behavioral_event(snap_empty))
        
        # Scenario 2: No displacement
        snap_normal = MarketSnapshot(current_price=100, current_atr=2.0, closes=[99.0, 99.5], volumes=[], is_new_bar=False)
        self.assertFalse(so.detect_behavioral_event(snap_normal))
        
        # Scenario 3: Bullish displacement (3.0 * 2.0 = 6.0) -> current_price >= 99.5 + 6.0 = 105.5
        snap_bull = MarketSnapshot(current_price=105.5, current_atr=2.0, closes=[99.0, 99.5], volumes=[], is_new_bar=False)
        self.assertTrue(so.detect_behavioral_event(snap_bull))
        
        # Scenario 4: Bearish displacement (3.0 * 2.0 = 6.0) -> current_price <= 99.5 - 6.0 = 93.5
        snap_bear = MarketSnapshot(current_price=93.0, current_atr=2.0, closes=[99.0, 99.5], volumes=[], is_new_bar=False)
        self.assertTrue(so.detect_behavioral_event(snap_bear))

if __name__ == '__main__':
    unittest.main()
