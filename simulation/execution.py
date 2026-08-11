from dataclasses import dataclass
from typing import Optional
from simulation.order import Order, OrderType, OrderDirection, ExecutionReport, ExecutionStatus
from simulation.market import MarketSnapshot

@dataclass(frozen=True)
class ExecutionConfig:
    """
    Configuration for execution models.
    """
    spread_model: str = "fixed"      # options: "fixed", "market"
    fixed_spread: float = 0.0        # absolute value added to price
    
    slippage_model: str = "zero"     # options: "zero", "fixed", "directional"
    fixed_slippage: float = 0.0      # absolute value of slippage
    
    commission_model: str = "fixed"  # options: "fixed", "percentage"
    commission_rate: float = 0.0     # Fixed cost or percentage (e.g. 0.0001 for 1 bip)
    
    partial_fill_model: str = "full" # options: "full", "volume"
    partial_fill_ratio: float = 1.0  # percentage of available volume to consume
    
    latency_model: str = "zero"      # options: "zero", "fixed"
    fixed_latency: int = 0           # ms of latency to add

class ExecutionEngine:
    """
    The Execution Engine simulates physical market mechanics deterministically.
    It takes an active Order and MarketSnapshot and produces an immutable ExecutionReport.
    """
    def __init__(self, config: ExecutionConfig):
        self.config = config
        self._execution_counter = 0

    def evaluate_execution(self, order: Order, snapshot: MarketSnapshot) -> ExecutionReport:
        """
        Evaluates execution conditions based on the current market snapshot and models.
        """
        # Ensure symbol match
        if order.symbol != snapshot.symbol:
            return self._create_reject(order, snapshot, "Symbol mismatch")
            
        qty_to_fill = order.quantity - order.filled_quantity
        if qty_to_fill <= 0:
            return self._create_reject(order, snapshot, "Order already fully filled")

        # 1. Spread Model
        spread = 0.0
        if self.config.spread_model == "fixed":
            spread = self.config.fixed_spread
        elif self.config.spread_model == "market":
            spread = snapshot.ask - snapshot.bid
            
        if spread < 0:
            spread = 0.0

        # 2. Base Price Determination (Hitting the market)
        if order.direction == OrderDirection.LONG:
            # We pay the ask, or we take bid + fixed spread
            base_price = snapshot.ask if self.config.spread_model == "market" else snapshot.bid + spread
        elif order.direction == OrderDirection.SHORT:
            # We receive the bid
            base_price = snapshot.bid
        else:
            return self._create_reject(order, snapshot, "Invalid direction for execution")

        # 3. Slippage Model
        slippage = 0.0
        if self.config.slippage_model == "fixed" or self.config.slippage_model == "directional":
            slippage = self.config.fixed_slippage

        # Penalty to price
        fill_price = base_price
        if order.direction == OrderDirection.LONG:
            fill_price += slippage
        elif order.direction == OrderDirection.SHORT:
            fill_price -= slippage

        # 4. Limit/Stop Verification Post-Slippage
        if order.order_type == OrderType.LIMIT:
            if order.direction == OrderDirection.LONG and fill_price > order.desired_entry:
                return self._create_no_fill(order, snapshot, "Price exceeded limit after slippage/spread")
            if order.direction == OrderDirection.SHORT and fill_price < order.desired_entry:
                return self._create_no_fill(order, snapshot, "Price exceeded limit after slippage/spread")

        # 5. Partial Fill Model
        filled_qty = qty_to_fill
        status = ExecutionStatus.FILLED
        
        if self.config.partial_fill_model == "volume":
            max_qty = snapshot.volume * self.config.partial_fill_ratio
            if max_qty < qty_to_fill:
                filled_qty = max_qty
                if filled_qty > 0:
                    status = ExecutionStatus.PARTIALLY_FILLED
                else:
                    return self._create_no_fill(order, snapshot, "Insufficient volume")

        remaining_qty = order.quantity - (order.filled_quantity + filled_qty)

        # 6. Commission Model
        commission = 0.0
        if self.config.commission_model == "fixed":
            commission = self.config.commission_rate
        elif self.config.commission_model == "percentage":
            # For simplicity, treating rate as straight multiplier
            commission = fill_price * filled_qty * self.config.commission_rate

        self._execution_counter += 1
        
        return ExecutionReport(
            execution_id=f"EXEC_{self._execution_counter}",
            order_id=order.order_id,
            signal_id=order.signal_id,
            symbol=order.symbol,
            direction=order.direction,
            timestamp=snapshot.timestamp + self.config.fixed_latency,
            execution_status=status,
            fill_price=fill_price,
            requested_price=order.desired_entry,
            filled_quantity=filled_qty,
            remaining_quantity=remaining_qty,
            spread_paid=spread,
            slippage_paid=slippage,
            commission_paid=commission,
            latency=self.config.fixed_latency,
            rejection_reason=None
        )

    def _create_reject(self, order: Order, snapshot: MarketSnapshot, reason: str) -> ExecutionReport:
        self._execution_counter += 1
        return ExecutionReport(
            execution_id=f"EXEC_{self._execution_counter}",
            order_id=order.order_id,
            signal_id=order.signal_id,
            symbol=order.symbol,
            direction=order.direction,
            timestamp=snapshot.timestamp,
            execution_status=ExecutionStatus.REJECTED,
            fill_price=0.0,
            requested_price=order.desired_entry,
            filled_quantity=0.0,
            remaining_quantity=order.quantity - order.filled_quantity,
            spread_paid=0.0,
            slippage_paid=0.0,
            commission_paid=0.0,
            latency=0,
            rejection_reason=reason
        )

    def _create_no_fill(self, order: Order, snapshot: MarketSnapshot, reason: str) -> ExecutionReport:
        self._execution_counter += 1
        return ExecutionReport(
            execution_id=f"EXEC_{self._execution_counter}",
            order_id=order.order_id,
            signal_id=order.signal_id,
            symbol=order.symbol,
            direction=order.direction,
            timestamp=snapshot.timestamp,
            execution_status=ExecutionStatus.NO_FILL,
            fill_price=0.0,
            requested_price=order.desired_entry,
            filled_quantity=0.0,
            remaining_quantity=order.quantity - order.filled_quantity,
            spread_paid=0.0,
            slippage_paid=0.0,
            commission_paid=0.0,
            latency=0,
            rejection_reason=reason
        )
