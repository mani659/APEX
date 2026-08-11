from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Any
from simulation.order import OrderDirection, ExecutionReport, ExecutionStatus
from simulation.market import MarketSnapshot

class ExitReason(Enum):
    STOP_LOSS = auto()
    TAKE_PROFIT = auto()
    MANUAL_CLOSE = auto()
    EXPIRATION = auto()

class PositionStatus(Enum):
    ACTIVE = auto()
    CLOSED = auto()

@dataclass
class PositionConfig:
    expiration_bars: Optional[int] = None
    allow_same_direction: bool = True
    allow_opposite_direction: bool = True

@dataclass
class Position:
    """Internal representation of an active position."""
    position_id: str
    symbol: str
    direction: OrderDirection
    entry_price: float
    entry_time: int
    quantity: float
    
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    
    status: PositionStatus = PositionStatus.ACTIVE
    remaining_quantity: float = field(init=False)
    commission_paid: float = 0.0
    entry_slippage: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    bars_held: int = 0
    
    def __post_init__(self):
        self.remaining_quantity = self.quantity

@dataclass(frozen=True)
class Trade:
    """Immutable record of a closed position (or partial close)."""
    trade_id: str
    position_id: str
    symbol: str
    direction: OrderDirection
    entry_time: int
    exit_time: int
    entry_price: float
    exit_price: float
    quantity: float
    gross_pnl: float
    net_pnl: float
    commission: float
    slippage: float
    exit_reason: ExitReason
    bars_held: int
    metadata: Optional[Dict[str, Any]] = None

class PositionEngine:
    """
    Manages active positions, evaluates exits against MarketSnapshots, 
    and produces immutable Trades upon closure.
    """
    def __init__(self, config: PositionConfig):
        self.config = config
        self._positions: Dict[str, Position] = {}
        self._trades: List[Trade] = []
        self._trade_counter = 0

    def process_execution_report(self, report: ExecutionReport, stop_loss: Optional[float] = None, take_profit: Optional[float] = None) -> Optional[Position]:
        """
        Creates or updates a position from an ExecutionReport.
        Assumes report is FILLED or PARTIALLY_FILLED.
        """
        if report.execution_status not in {ExecutionStatus.FILLED, ExecutionStatus.PARTIALLY_FILLED}:
            return None
            
        # For simplicity, treating every execution as a new independent position (no netting)
        pos_id = f"POS_{report.execution_id}"
        
        # We can extract direction from the ExecutionReport
        direction = report.direction
        
        position = Position(
            position_id=pos_id,
            symbol=report.symbol,
            direction=direction,
            entry_price=report.fill_price,
            entry_time=report.timestamp,
            quantity=report.filled_quantity,
            stop_loss=stop_loss,
            take_profit=take_profit,
            commission_paid=report.commission_paid,
            entry_slippage=report.slippage_paid
        )
        self._positions[pos_id] = position
        return position

    def evaluate_positions(self, snapshot: MarketSnapshot) -> List[Trade]:
        """
        Evaluates all active positions against the given snapshot for exits.
        Returns a list of trades generated from closed positions.
        """
        trades = []
        for pos_id, pos in list(self._positions.items()):
            if pos.status == PositionStatus.CLOSED:
                continue
            
            if pos.symbol != snapshot.symbol:
                continue

            pos.bars_held += 1
            exit_reason = None
            exit_price = 0.0

            # Exit Price logic: if Long, exit at Bid. If Short, exit at Ask.
            current_exit_price = snapshot.bid if pos.direction == OrderDirection.LONG else snapshot.ask

            # 1. Evaluate Stop Loss
            if pos.stop_loss is not None:
                if pos.direction == OrderDirection.LONG and current_exit_price <= pos.stop_loss:
                    exit_reason = ExitReason.STOP_LOSS
                    exit_price = current_exit_price
                elif pos.direction == OrderDirection.SHORT and current_exit_price >= pos.stop_loss:
                    exit_reason = ExitReason.STOP_LOSS
                    exit_price = current_exit_price

            # 2. Evaluate Take Profit (only if SL didn't hit)
            if not exit_reason and pos.take_profit is not None:
                if pos.direction == OrderDirection.LONG and current_exit_price >= pos.take_profit:
                    exit_reason = ExitReason.TAKE_PROFIT
                    exit_price = current_exit_price
                elif pos.direction == OrderDirection.SHORT and current_exit_price <= pos.take_profit:
                    exit_reason = ExitReason.TAKE_PROFIT
                    exit_price = current_exit_price

            # 3. Evaluate Expiration
            if not exit_reason and self.config.expiration_bars is not None:
                if pos.bars_held >= self.config.expiration_bars:
                    exit_reason = ExitReason.EXPIRATION
                    exit_price = current_exit_price

            # 4. Execute Close
            if exit_reason:
                trade = self._close_position(pos, exit_price, snapshot.timestamp, exit_reason)
                trades.append(trade)

        return trades

    def close_position_manually(self, position_id: str, snapshot: MarketSnapshot) -> Optional[Trade]:
        """Manually closes a specific position."""
        pos = self._positions.get(position_id)
        if not pos or pos.status == PositionStatus.CLOSED:
            return None
            
        exit_price = snapshot.bid if pos.direction == OrderDirection.LONG else snapshot.ask
        return self._close_position(pos, exit_price, snapshot.timestamp, ExitReason.MANUAL_CLOSE)

    def _close_position(self, pos: Position, exit_price: float, exit_time: int, reason: ExitReason) -> Trade:
        pos.status = PositionStatus.CLOSED
        
        # Calculate PnL
        if pos.direction == OrderDirection.LONG:
            gross_pnl = (exit_price - pos.entry_price) * pos.quantity
        else:
            gross_pnl = (pos.entry_price - exit_price) * pos.quantity
            
        net_pnl = gross_pnl - pos.commission_paid
        
        self._trade_counter += 1
        trade_id = f"TRD_{self._trade_counter}"
        
        trade = Trade(
            trade_id=trade_id,
            position_id=pos.position_id,
            symbol=pos.symbol,
            direction=pos.direction,
            entry_time=pos.entry_time,
            exit_time=exit_time,
            entry_price=pos.entry_price,
            exit_price=exit_price,
            quantity=pos.quantity,
            gross_pnl=gross_pnl,
            net_pnl=net_pnl,
            commission=pos.commission_paid, # Exit commissions not modeled here yet, could be added later
            slippage=0.0, # Exit slippage is 0 per simplified rules
            exit_reason=reason,
            bars_held=pos.bars_held,
            metadata=pos.metadata.copy()
        )
        self._trades.append(trade)
        
        # Remove closed position from active tracking
        del self._positions[pos.position_id]
        
        return trade

    def calculate_floating_state(self, snapshot: MarketSnapshot):
        """
        Calculates the floating state of all active positions.
        Returns: (floating_pnl, margin_used, exposure_long, exposure_short, number_open_positions)
        """
        floating_pnl = 0.0
        margin_used = 0.0
        exposure_long = 0.0
        exposure_short = 0.0
        number_open_positions = 0
        
        for pos in self._positions.values():
            number_open_positions += 1
            if pos.direction == OrderDirection.LONG:
                exposure_long += pos.quantity
                floating_pnl += (snapshot.bid - pos.entry_price) * pos.quantity
            else:
                exposure_short += pos.quantity
                floating_pnl += (pos.entry_price - snapshot.ask) * pos.quantity
                
        return floating_pnl, margin_used, exposure_long, exposure_short, number_open_positions

    def get_position_counts(self):
        """
        Returns a tuple of (long_count, short_count) for active positions.
        """
        long_count = 0
        short_count = 0
        for pos in self._positions.values():
            if pos.direction == OrderDirection.LONG:
                long_count += 1
            else:
                short_count += 1
        return long_count, short_count

