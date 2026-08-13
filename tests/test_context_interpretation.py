import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.core.market_data import MarketSnapshot
from engine.core.context_interpretation import ContextInterpretation, ParticipationState

class TestContextInterpretation(unittest.TestCase):
    def test_evaluate_participation(self):
        ci = ContextInterpretation(volume_percentile_threshold=25.0)
        
        # Scenario 1: No event triggered
        snap_no_event = MarketSnapshot(current_price=100, current_atr=2.0, closes=[], opens=[], volumes=[10, 20, 30], is_new_bar=False)
        self.assertEqual(ci.evaluate_participation_state(snap_no_event, False), ParticipationState.HIGH_ENTROPY)
        
        # Scenario 2: Event triggered, but volume is high (not a vacuum)
        snap_high_vol = MarketSnapshot(current_price=100, current_atr=2.0, closes=[], opens=[], volumes=[100, 100, 100, 200], is_new_bar=False)
        # 25th percentile of [100, 100, 100, 200] is 100. Current is 200 (not < 100).
        self.assertEqual(ci.evaluate_participation_state(snap_high_vol, True), ParticipationState.HIGH_ENTROPY)
        
        # Scenario 3: Event triggered, volume is low (vacuum)
        snap_low_vol = MarketSnapshot(current_price=100, current_atr=2.0, closes=[], opens=[], volumes=[100, 100, 100, 10], is_new_bar=False)
        # 25th percentile of [100, 100, 100, 10] is 77.5. Current is 10 (< 77.5).
        self.assertEqual(ci.evaluate_participation_state(snap_low_vol, True), ParticipationState.LOW_ENTROPY)

if __name__ == '__main__':
    unittest.main()
