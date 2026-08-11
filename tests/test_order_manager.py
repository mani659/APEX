import unittest
from simulation.order import Signal, OrderType, OrderDirection, OrderState, ExecutionReport, ExecutionStatus
from simulation.market import MarketSnapshot
from simulation.order_manager import OrderManager

class TestOrderManager(unittest.TestCase):
    
    def setUp(self):
        self.oms = OrderManager()
        
    def test_market_order_creation(self):
        signal = Signal(
            signal_id="sig_1", strategy_name="test", strategy_version="1.0",
            timestamp=1000, direction=OrderDirection.LONG, entry_type=OrderType.MARKET,
            desired_entry=0.0, quantity=1.0
        )
        order = self.oms.receive_signal(signal)
        self.assertIsNotNone(order)
        self.assertEqual(order.state, OrderState.ACTIVE)
        
        exec_orders = self.oms.get_executable_orders()
        self.assertEqual(len(exec_orders), 1)
        self.assertEqual(exec_orders[0].order_id, "ORD_sig_1")
        
        # Ensure queue is cleared
        self.assertEqual(len(self.oms.get_executable_orders()), 0)
        
    def test_limit_order_creation_and_activation(self):
        signal = Signal(
            signal_id="sig_2", strategy_name="test", strategy_version="1.0",
            timestamp=1000, direction=OrderDirection.LONG, entry_type=OrderType.LIMIT,
            desired_entry=1900.0, quantity=1.0
        )
        order = self.oms.receive_signal(signal)
        self.assertEqual(order.state, OrderState.PENDING)
        
        snap1 = MarketSnapshot(symbol="XAUUSD", timestamp=1001, bid=1950.0, ask=1950.0)
        self.oms.activate_orders(snap1)
        self.assertEqual(order.state, OrderState.PENDING)
        
        snap2 = MarketSnapshot(symbol="XAUUSD", timestamp=1002, bid=1900.0, ask=1900.0)
        self.oms.activate_orders(snap2)
        self.assertEqual(order.state, OrderState.ACTIVE)
        
        exec_orders = self.oms.get_executable_orders()
        self.assertEqual(len(exec_orders), 1)
        
    def test_stop_order_activation(self):
        signal = Signal(
            signal_id="sig_3", strategy_name="test", strategy_version="1.0",
            timestamp=1000, direction=OrderDirection.LONG, entry_type=OrderType.STOP,
            desired_entry=1950.0, quantity=1.0
        )
        order = self.oms.receive_signal(signal)
        self.assertEqual(order.state, OrderState.PENDING)
        
        snap1 = MarketSnapshot(symbol="XAUUSD", timestamp=1001, bid=1900.0, ask=1900.0)
        self.oms.activate_orders(snap1)
        self.assertEqual(order.state, OrderState.PENDING)
        
        snap2 = MarketSnapshot(symbol="XAUUSD", timestamp=1002, bid=1960.0, ask=1960.0)
        self.oms.activate_orders(snap2)
        self.assertEqual(order.state, OrderState.ACTIVE)
        
    def test_order_cancellation(self):
        signal = Signal(
            signal_id="sig_4", strategy_name="test", strategy_version="1.0",
            timestamp=1000, direction=OrderDirection.LONG, entry_type=OrderType.LIMIT,
            desired_entry=1900.0, quantity=1.0
        )
        order = self.oms.receive_signal(signal)
        
        cancel_signal = Signal(
            signal_id="sig_cancel", strategy_name="test", strategy_version="1.0",
            timestamp=1050, direction=OrderDirection.CANCEL, entry_type=OrderType.MARKET,
            desired_entry=0.0, quantity=0.0, reference_id="sig_4"
        )
        result_order = self.oms.receive_signal(cancel_signal)
        self.assertIsNone(result_order) 
        
        self.assertEqual(order.state, OrderState.CANCELLED)
        
    def test_order_expiration(self):
        signal = Signal(
            signal_id="sig_5", strategy_name="test", strategy_version="1.0",
            timestamp=1000, direction=OrderDirection.LONG, entry_type=OrderType.LIMIT,
            desired_entry=1900.0, quantity=1.0, max_holding_period=500
        )
        order = self.oms.receive_signal(signal)
        self.assertEqual(order.state, OrderState.PENDING)
        
        self.oms.expire_orders(1400)
        self.assertEqual(order.state, OrderState.PENDING)
        
        self.oms.expire_orders(1500)
        self.assertEqual(order.state, OrderState.EXPIRED)

    # --- New Revision Tests ---

    def test_dag_transitions(self):
        signal = Signal("sig_dag", "test", "1.0", 1000, OrderDirection.LONG, OrderType.LIMIT, 1900.0, 1.0)
        order = self.oms.receive_signal(signal)
        
        # NEW -> PENDING handled automatically in receive_signal
        self.assertEqual(order.state, OrderState.PENDING)
        
        # Illegal backward transition
        with self.assertRaises(ValueError):
            order.transition_to(OrderState.NEW)
            
        # PENDING -> ACTIVE is allowed
        order.transition_to(OrderState.ACTIVE)
        
        # ACTIVE -> PENDING is illegal
        with self.assertRaises(ValueError):
            order.transition_to(OrderState.PENDING)
            
        # ACTIVE -> PARTIALLY_FILLED is allowed
        order.transition_to(OrderState.PARTIALLY_FILLED)
        
        # PARTIALLY_FILLED -> FILLED is allowed
        order.transition_to(OrderState.FILLED)
        
        # FILLED is terminal, further transitions fail
        with self.assertRaises(ValueError):
            order.transition_to(OrderState.CANCELLED)

    def test_duplicate_id_protection(self):
        signal = Signal("sig_dup", "test", "1.0", 1000, OrderDirection.LONG, OrderType.MARKET, 0.0, 1.0)
        self.oms.receive_signal(signal)
        
        # Same signal ID again
        res = self.oms.receive_signal(signal)
        self.assertIsNone(res) # Should be rejected
        
        stats = self.oms.get_statistics()
        self.assertEqual(stats["ACTIVE"], 1)

    def test_execution_feedback(self):
        signal = Signal("sig_exec", "test", "1.0", 1000, OrderDirection.LONG, OrderType.MARKET, 0.0, 10.0)
        order = self.oms.receive_signal(signal)
        
        self.assertEqual(order.state, OrderState.ACTIVE)
        
        report1 = ExecutionReport(
            execution_id="exec_1", order_id="ORD_sig_exec", signal_id="sig_exec", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1001, execution_status=ExecutionStatus.PARTIALLY_FILLED, fill_price=1900.0,
            requested_price=1900.0, filled_quantity=4.0, remaining_quantity=6.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        self.oms.update_order_from_execution(report1)
        self.assertEqual(order.state, OrderState.PARTIALLY_FILLED)
        self.assertEqual(order.filled_quantity, 4.0)
        
        report2 = ExecutionReport(
            execution_id="exec_2", order_id="ORD_sig_exec", signal_id="sig_exec", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1002, execution_status=ExecutionStatus.FILLED, fill_price=1900.0,
            requested_price=1900.0, filled_quantity=6.0, remaining_quantity=0.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        self.oms.update_order_from_execution(report2)
        self.assertEqual(order.state, OrderState.FILLED)
        self.assertEqual(order.filled_quantity, 10.0)
        
        # Terminal state lock
        report3 = ExecutionReport(
            execution_id="exec_3", order_id="ORD_sig_exec", signal_id="sig_exec", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1003, execution_status=ExecutionStatus.REJECTED, fill_price=0.0,
            requested_price=0.0, filled_quantity=0.0, remaining_quantity=0.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        self.oms.update_order_from_execution(report3)
        self.assertEqual(order.state, OrderState.FILLED) # Unchanged

    def test_cancel_queue_integrity(self):
        signal = Signal("sig_cancel_queue", "test", "1.0", 1000, OrderDirection.LONG, OrderType.MARKET, 0.0, 1.0)
        order = self.oms.receive_signal(signal)
        
        # It's in the executable queue
        self.assertIn(order, self.oms._executable_queue)
        
        cancel_signal = Signal("sig_cancel_q2", "test", "1.0", 1050, OrderDirection.CANCEL, OrderType.MARKET, 0.0, 0.0, reference_id="sig_cancel_queue")
        self.oms.receive_signal(cancel_signal)
        
        # Should be removed from queue
        self.assertNotIn(order, self.oms._executable_queue)
        self.assertEqual(order.state, OrderState.CANCELLED)

    def test_no_fill_feedback(self):
        signal = Signal("sig_nofill", "test", "1.0", 1000, OrderDirection.LONG, OrderType.LIMIT, 1900.0, 1.0)
        order = self.oms.receive_signal(signal)
        snap1 = MarketSnapshot(symbol="XAUUSD", timestamp=1001, bid=1900.0, ask=1900.0)
        self.oms.activate_orders(snap1)
        
        # In queue
        self.assertIn(order, self.oms._executable_queue)
        # Pull from queue (simulating runner)
        exec_orders = self.oms.get_executable_orders()
        self.assertNotIn(order, self.oms._executable_queue)
        
        # Simulate Execution Engine NO_FILL
        report = ExecutionReport(
            execution_id="exec_nf", order_id=order.order_id, signal_id="sig_nofill", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1001, execution_status=ExecutionStatus.NO_FILL, fill_price=0.0,
            requested_price=1900.0, filled_quantity=0.0, remaining_quantity=1.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        self.oms.update_order_from_execution(report)
        
        # State remains ACTIVE
        self.assertEqual(order.state, OrderState.ACTIVE)
        # Should be back in queue for next tick
        self.assertIn(order, self.oms._executable_queue)

if __name__ == '__main__':
    unittest.main()
