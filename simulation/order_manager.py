from typing import List, Dict, Optional, Any
from simulation.order import Order, Signal, OrderState, OrderType, OrderDirection, ExecutionReport, ExecutionStatus
from simulation.market import MarketSnapshot

class OrderManager:
    """
    The Order Manager (OMS) owns the complete lifecycle of all pending orders.
    It receives Signals, creates Orders, tracks Order State, and activates orders
    based on the TradingContext. It is strictly deterministic.
    """
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
        self._order_history: List[Order] = []
        self._executable_queue: List[Order] = []
        
    def receive_signal(self, signal: Signal) -> Optional[Order]:
        """
        Receives a Signal and creates a NEW order or processes a CANCEL intent.
        
        Args:
            signal: The immutable Signal intent from Strategy.
            
        Returns:
            The created Order if applicable, otherwise None.
        """
        if signal.direction == OrderDirection.CANCEL:
            if not signal.reference_id:
                return None
            self._cancel_order(signal.reference_id)
            return None
            
        order_id = f"ORD_{signal.signal_id}"
        if order_id in self._orders:
            # Enforce unique IDs and queue integrity
            return None
            
        order = Order(
            order_id=order_id,
            signal_id=signal.signal_id,
            timestamp=signal.timestamp,
            direction=signal.direction,
            order_type=signal.entry_type,
            desired_entry=signal.desired_entry,
            quantity=signal.quantity,
            symbol=signal.symbol,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            expiration_time=signal.timestamp + signal.max_holding_period if signal.max_holding_period else None
        )
        self._orders[order.order_id] = order
        self._order_history.append(order)
        
        # Strict DAG compliance: NEW -> PENDING
        order.transition_to(OrderState.PENDING)
        
        # Market orders become immediately active
        if order.order_type == OrderType.MARKET:
            order.transition_to(OrderState.ACTIVE)
            self._executable_queue.append(order)
            
        return order
        
    def _cancel_order(self, original_signal_id: str) -> bool:
        """
        Transitions a pending or active order to CANCELLED state.
        Internal API only. Strategies must use receive_signal with CANCEL intent.
        """
        order_id = f"ORD_{original_signal_id}"
        order = self._orders.get(order_id)
        if order and not order.is_terminal():
            order.transition_to(OrderState.CANCELLED)
            if order in self._executable_queue:
                self._executable_queue.remove(order)
            return True
        return False
        
    def expire_orders(self, current_timestamp: int):
        """
        Transitions pending orders to EXPIRED if their time-in-force is breached.
        """
        for order in self._orders.values():
            if order.state == OrderState.PENDING and order.expiration_time is not None:
                if current_timestamp >= order.expiration_time:
                    order.transition_to(OrderState.EXPIRED)
                    
    def activate_orders(self, market_snapshot: MarketSnapshot):
        """
        Evaluates PENDING orders against the current MarketSnapshot.
        Transitions them to ACTIVE if conditions are met.
        """
        current_price = market_snapshot.bid
            
        for order in self._orders.values():
            if order.state != OrderState.PENDING:
                continue
                
            activated = False
            if order.order_type == OrderType.LIMIT:
                if order.direction == OrderDirection.LONG and current_price <= order.desired_entry:
                    activated = True
                elif order.direction == OrderDirection.SHORT and current_price >= order.desired_entry:
                    activated = True
            elif order.order_type == OrderType.STOP or order.order_type == OrderType.STOP_LIMIT:
                if order.direction == OrderDirection.LONG and current_price >= order.desired_entry:
                    activated = True
                elif order.direction == OrderDirection.SHORT and current_price <= order.desired_entry:
                    activated = True
                    
            if activated:
                order.transition_to(OrderState.ACTIVE)
                self._executable_queue.append(order)
                
    def update_order_from_execution(self, execution_report: ExecutionReport):
        """
        Receives immutable ExecutionReport from the Execution Engine.
        Updates ONLY the Order state.
        """
        order_id = execution_report.order_id
        order = self._orders.get(order_id)
        if not order or order.is_terminal():
            return
            
        if execution_report.execution_status == ExecutionStatus.FILLED:
            order.filled_quantity += execution_report.filled_quantity
            order.transition_to(OrderState.FILLED)
            if order in self._executable_queue:
                self._executable_queue.remove(order)
        elif execution_report.execution_status == ExecutionStatus.PARTIALLY_FILLED:
            order.filled_quantity += execution_report.filled_quantity
            order.transition_to(OrderState.PARTIALLY_FILLED)
        elif execution_report.execution_status == ExecutionStatus.NO_FILL:
            # Execution failed price/volume constraints but order remains valid
            if order not in self._executable_queue:
                self._executable_queue.append(order)
        elif execution_report.execution_status == ExecutionStatus.REJECTED:
            order.transition_to(OrderState.REJECTED)
            if order in self._executable_queue:
                self._executable_queue.remove(order)
                
    def get_executable_orders(self) -> List[Order]:
        """
        Returns the queue of ACTIVE orders ready for the Execution Engine.
        Clears the queue upon return to ensure one-time processing.
        """
        executable = self._executable_queue.copy()
        self._executable_queue.clear()
        return executable
        
    def get_pending_orders(self) -> List[Order]:
        """
        Returns a list of all currently PENDING orders.
        """
        return [order for order in self._orders.values() if order.state == OrderState.PENDING]
        
    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Retrieves a specific order by ID.
        """
        return self._orders.get(order_id)
        
    def get_statistics(self) -> Dict[str, int]:
        """
        Returns aggregate statistics of the OMS state.
        """
        stats = {state.name: 0 for state in OrderState}
        for order in self._orders.values():
            stats[order.state.name] += 1
        return stats
