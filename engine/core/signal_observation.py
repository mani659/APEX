from engine.core.market_data import MarketSnapshot

class SignalObservation:
    def __init__(self, displacement_threshold: float = 3.0):
        self.displacement_threshold = displacement_threshold

    def detect_behavioral_event(self, snapshot: MarketSnapshot) -> bool:
        if len(snapshot.closes) < 2 or snapshot.current_atr == 0.0:
            return False
            
        if snapshot.is_new_bar:
            last_close = snapshot.closes[-2]
        else:
            last_close = snapshot.closes[-1]
            
        displacement = abs(snapshot.current_price - last_close)
        
        return displacement >= (self.displacement_threshold * snapshot.current_atr)
