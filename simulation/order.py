from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional

class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()
    STOP = auto()
    STOP_LIMIT = auto()

class OrderState(Enum):
    NEW = auto()
    PENDING = auto()
    ACTIVE = auto()
    PARTIALLY_FILLED = auto()
    FILLED = auto()
    CANCELLED = auto()
    EXPIRED = auto()
    REJECTED = auto()

class OrderDirection(Enum):
    LONG = auto()
    SHORT = auto()
    CANCEL = auto() 

class ExecutionStatus(Enum):
    FILLED = auto()
    PARTIALLY_FILLED = auto()
    NO_FILL = auto()
    REJECTED = auto()
    EXPIRED = auto()
    CANCELLED = auto()

@dataclass(frozen=True)
class Signal:
    signal_id: str
    strategy_name: str
    strategy_version: str
    timestamp: int
    direction: OrderDirection
    entry_type: OrderType
    desired_entry: float
    quantity: float
    symbol: str = "XAUUSD"
    risk_percent: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    trailing_stop: Optional[float] = None
    max_holding_period: Optional[int] = None
    confidence_score: Optional[float] = None
    reference_id: Optional[str] = None 

@dataclass(frozen=True)
class ExecutionReport:
    execution_id: str
    order_id: str
    signal_id: str
    symbol: str
    direction: OrderDirection
    timestamp: int
    execution_status: ExecutionStatus
    fill_price: float
    requested_price: float
    filled_quantity: float
    remaining_quantity: float
    spread_paid: float
    slippage_paid: float
    commission_paid: float
    latency: int
    rejection_reason: Optional[str] = None
    metadata: Optional[dict] = None

@dataclass
class Order:
    order_id: str
    signal_id: str
    timestamp: int
    direction: OrderDirection
    order_type: OrderType
    desired_entry: float
    quantity: float
    
    symbol: str = "XAUUSD"
    state: OrderState = OrderState.NEW
    filled_quantity: float = 0.0
    
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    expiration_time: Optional[int] = None
    
    _locked: bool = field(default=False, repr=False)
    
    def is_terminal(self) -> bool:
        return self.state in {
            OrderState.FILLED, 
            OrderState.CANCELLED, 
            OrderState.EXPIRED, 
            OrderState.REJECTED
        }

    def transition_to(self, new_state: OrderState):
        """
        Transitions the order to a new state following a strict DAG.
        Raises ValueError if transition is illegal.
        """
        if self._locked:
            raise ValueError(f"Order {self.order_id} is locked in terminal state {self.state}")
            
        allowed = False
        if self.state == OrderState.NEW:
            allowed = new_state == OrderState.PENDING
        elif self.state == OrderState.PENDING:
            allowed = new_state in {OrderState.ACTIVE, OrderState.CANCELLED, OrderState.EXPIRED, OrderState.REJECTED}
        elif self.state == OrderState.ACTIVE:
            allowed = new_state in {OrderState.PARTIALLY_FILLED, OrderState.FILLED, OrderState.CANCELLED, OrderState.REJECTED}
        elif self.state == OrderState.PARTIALLY_FILLED:
            allowed = new_state in {OrderState.PARTIALLY_FILLED, OrderState.FILLED, OrderState.CANCELLED, OrderState.REJECTED}
            
        if not allowed:
            raise ValueError(f"Illegal transition from {self.state} to {new_state}")
            
        self.state = new_state
        if self.is_terminal():
            self._locked = True
