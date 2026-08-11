import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.core.market_data import MarketSnapshot
from engine.core.context_interpretation import ParticipationState
from engine.core.execution_permission import ExecutionPermission, PermissionState

class TestExecutionPermission(unittest.TestCase):
    def test_confirm_stabilization(self):
        ep = ExecutionPermission(stabilization_threshold=0.5)
        
        # Scenario 1: Reject high entropy
        snap = MarketSnapshot(current_price=100, current_atr=2.0, closes=[99, 99], volumes=[], is_new_bar=False)
        self.assertEqual(ep.confirm_stabilization(snap, ParticipationState.HIGH_ENTROPY), PermissionState.REJECT)
        
        # Scenario 2: Wait (bar body >= 0.5 ATR)
        snap_wait = MarketSnapshot(current_price=100, current_atr=2.0, closes=[95, 98], volumes=[], is_new_bar=False)
        self.assertEqual(ep.confirm_stabilization(snap_wait, ParticipationState.LOW_ENTROPY), PermissionState.WAIT)
        
        # Scenario 3: Execute (bar body < 0.5 ATR)
        snap_exec = MarketSnapshot(current_price=100, current_atr=2.0, closes=[98, 99.5], volumes=[], is_new_bar=False)
        self.assertEqual(ep.confirm_stabilization(snap_exec, ParticipationState.LOW_ENTROPY), PermissionState.EXECUTE)

if __name__ == '__main__':
    unittest.main()
