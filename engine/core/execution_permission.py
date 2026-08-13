from enum import Enum
from engine.core.market_data import MarketSnapshot
from engine.core.context_interpretation import ParticipationState

class PermissionState(Enum):
    WAIT = 1
    REJECT = 2
    EXECUTE = 3

class ExecutionPermission:
    def __init__(self, stabilization_threshold: float = 0.5):
        self.stabilization_threshold = stabilization_threshold

    def confirm_stabilization(self, snapshot: MarketSnapshot, participation: ParticipationState) -> PermissionState:
        if participation == ParticipationState.HIGH_ENTROPY:
            return PermissionState.REJECT
            
        if len(snapshot.closes) < 2:
            return PermissionState.WAIT
            
        if snapshot.is_new_bar:
            current_bar_body = abs(snapshot.opens[-1] - snapshot.closes[-1])
        else:
            current_bar_body = abs(snapshot.current_price - snapshot.closes[-1])
            
        if current_bar_body < (self.stabilization_threshold * snapshot.current_atr):
            return PermissionState.EXECUTE
            
        return PermissionState.WAIT
