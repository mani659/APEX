from enum import Enum
from dataclasses import dataclass, field
from engine.core.execution_engine import Position, OrderDirection

class ExitModel(Enum):
    MODEL_A_FIXED = "MODEL_A_FIXED"
    MODEL_B_ATR = "MODEL_B_ATR"
    MODEL_C_TIME = "MODEL_C_TIME"
    MODEL_D_OBSERVE = "MODEL_D_OBSERVE"

class ExperimentalExitDecision(Enum):
    HOLD = 1
    EXIT = 2

@dataclass
class ExperimentalConfig:
    model: ExitModel
    # Model A config
    fixed_sl_distance: float = 0.0  # in price units
    fixed_tp_distance: float = 0.0
    # Model B config
    atr_sl_multiplier: float = 2.0
    atr_tp_multiplier: float = 2.0
    # Model C config
    max_holding_bars: int = 10
    # Model D config
    observation_bars: int = 240

@dataclass
class ExperimentalState:
    entry_price: float = 0.0
    entry_atr: float = 0.0
    
    # Excursion Tracking
    mae: float = 0.0  # MAE is always >= 0, representing adverse distance
    mfe: float = 0.0  # MFE is always >= 0, representing favorable distance
    
    # Timing Tracking
    bars_held: int = 0
    time_to_mae_bars: int = 0
    time_to_mfe_bars: int = 0

class ExperimentalExitManager:
    def __init__(self, config: ExperimentalConfig):
        self.config = config
        self.states = {}  # ticket -> ExperimentalState

    def initialize_state(self, position: Position, current_atr: float):
        if position.ticket not in self.states:
            self.states[position.ticket] = ExperimentalState(
                entry_price=position.entry_price,
                entry_atr=current_atr
            )

    def evaluate(self, position: Position, current_price: float) -> tuple[ExperimentalExitDecision, str]:
        if position.ticket not in self.states:
            return ExperimentalExitDecision.HOLD, ""
            
        state = self.states[position.ticket]
        
        # Update metrics on the new bar/tick
        state.bars_held += 1
        
        if position.direction == OrderDirection.BUY:
            current_adverse = state.entry_price - current_price
            current_favorable = current_price - state.entry_price
        else:
            current_adverse = current_price - state.entry_price
            current_favorable = state.entry_price - current_price
            
        # Update MAE
        if current_adverse > state.mae:
            state.mae = current_adverse
            state.time_to_mae_bars = state.bars_held
            
        # Update MFE
        if current_favorable > state.mfe:
            state.mfe = current_favorable
            state.time_to_mfe_bars = state.bars_held
            
        # Evaluate Models
        if self.config.model == ExitModel.MODEL_A_FIXED:
            if state.mae >= self.config.fixed_sl_distance:
                return ExperimentalExitDecision.EXIT, "FIXED_SL"
            if state.mfe >= self.config.fixed_tp_distance:
                return ExperimentalExitDecision.EXIT, "FIXED_TP"
                
        elif self.config.model == ExitModel.MODEL_B_ATR:
            sl_distance = self.config.atr_sl_multiplier * state.entry_atr
            tp_distance = self.config.atr_tp_multiplier * state.entry_atr
            if state.mae >= sl_distance:
                return ExperimentalExitDecision.EXIT, "ATR_SL"
            if state.mfe >= tp_distance:
                return ExperimentalExitDecision.EXIT, "ATR_TP"
                
        elif self.config.model == ExitModel.MODEL_C_TIME:
            if state.bars_held >= self.config.max_holding_bars:
                return ExperimentalExitDecision.EXIT, "TIME_EXIT"
                
        elif self.config.model == ExitModel.MODEL_D_OBSERVE:
            if state.bars_held >= self.config.observation_bars:
                return ExperimentalExitDecision.EXIT, "OBSERVATION_WINDOW_EXPIRED"
            
        return ExperimentalExitDecision.HOLD, ""

    def clear_state(self, position: Position):
        if position.ticket in self.states:
            del self.states[position.ticket]
