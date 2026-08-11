from enum import Enum
import numpy as np
from engine.core.market_data import MarketSnapshot

class ParticipationState(Enum):
    LOW_ENTROPY = 1
    HIGH_ENTROPY = 2

class ContextInterpretation:
    def __init__(self, volume_percentile_threshold: float = 25.0):
        self.volume_percentile_threshold = volume_percentile_threshold

    def evaluate_participation_state(self, snapshot: MarketSnapshot, event_triggered: bool) -> ParticipationState:
        if not event_triggered:
            return ParticipationState.HIGH_ENTROPY
            
        if len(snapshot.volumes) < 2:
            return ParticipationState.HIGH_ENTROPY
            
        current_volume = snapshot.volumes[-1]
        percentile = np.percentile(snapshot.volumes, self.volume_percentile_threshold)
        
        if current_volume < percentile:
            return ParticipationState.LOW_ENTROPY
            
        return ParticipationState.HIGH_ENTROPY
