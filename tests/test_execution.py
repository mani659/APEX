import unittest
from simulation.order import Order, Signal, OrderType, OrderDirection, OrderState, ExecutionStatus
from simulation.market import MarketSnapshot
from simulation.execution import ExecutionEngine, ExecutionConfig

class TestExecutionEngine(unittest.TestCase):
    
    def setUp(self):
        self.signal = Signal("sig_1", "test", "1.0", 1000, OrderDirection.LONG, OrderType.MARKET, 0.0, 10.0, "XAUUSD")
        self.order = Order("ORD_sig_1", "sig_1", 1000, OrderDirection.LONG, OrderType.MARKET, 0.0, 10.0, "XAUUSD")
        self.order.transition_to(OrderState.PENDING)
        self.order.transition_to(OrderState.ACTIVE)
        
        self.snapshot = MarketSnapshot("XAUUSD", 1001, 1900.0, 1900.5, 100.0)
        
    def test_market_order_fixed_spread(self):
        config = ExecutionConfig(spread_model="fixed", fixed_spread=1.0)
        engine = ExecutionEngine(config)
        
        # Long market pays bid + spread (1900.0 + 1.0) = 1901.0
        report = engine.evaluate_execution(self.order, self.snapshot)
        
        self.assertEqual(report.execution_status, ExecutionStatus.FILLED)
        self.assertEqual(report.fill_price, 1901.0)
        self.assertEqual(report.spread_paid, 1.0)
        self.assertEqual(report.filled_quantity, 10.0)
        self.assertEqual(report.remaining_quantity, 0.0)

    def test_market_order_market_spread(self):
        config = ExecutionConfig(spread_model="market")
        engine = ExecutionEngine(config)
        
        # Long market pays ask (1900.5)
        report = engine.evaluate_execution(self.order, self.snapshot)
        
        self.assertEqual(report.execution_status, ExecutionStatus.FILLED)
        self.assertEqual(report.fill_price, 1900.5)
        self.assertEqual(report.spread_paid, 0.5)
        
    def test_short_order_pricing(self):
        config = ExecutionConfig(spread_model="market")
        engine = ExecutionEngine(config)
        short_order = Order("ORD_2", "sig_2", 1000, OrderDirection.SHORT, OrderType.MARKET, 0.0, 10.0, "XAUUSD")
        short_order.transition_to(OrderState.PENDING)
        short_order.transition_to(OrderState.ACTIVE)
        
        # Short market receives bid (1900.0)
        report = engine.evaluate_execution(short_order, self.snapshot)
        self.assertEqual(report.fill_price, 1900.0)

    def test_slippage_model(self):
        config = ExecutionConfig(spread_model="market", slippage_model="fixed", fixed_slippage=0.2)
        engine = ExecutionEngine(config)
        
        # Long market pays ask (1900.5) + slippage (0.2) = 1900.7
        report = engine.evaluate_execution(self.order, self.snapshot)
        
        self.assertEqual(report.fill_price, 1900.7)
        self.assertEqual(report.slippage_paid, 0.2)

    def test_limit_order_no_fill_due_to_slippage(self):
        config = ExecutionConfig(spread_model="market", slippage_model="fixed", fixed_slippage=1.0)
        engine = ExecutionEngine(config)
        
        # Limit at 1901.0. 
        # Base price = Ask = 1900.5. 
        # Slippage = 1.0. 
        # Fill price = 1901.5 (exceeds limit of 1901.0)
        limit_order = Order("ORD_3", "sig_3", 1000, OrderDirection.LONG, OrderType.LIMIT, 1901.0, 10.0, "XAUUSD")
        limit_order.transition_to(OrderState.PENDING)
        limit_order.transition_to(OrderState.ACTIVE)
        
        report = engine.evaluate_execution(limit_order, self.snapshot)
        
        self.assertEqual(report.execution_status, ExecutionStatus.NO_FILL)
        self.assertIn("Price exceeded limit", report.rejection_reason)

    def test_commission_model(self):
        config = ExecutionConfig(spread_model="market", commission_model="percentage", commission_rate=0.01)
        engine = ExecutionEngine(config)
        
        report = engine.evaluate_execution(self.order, self.snapshot)
        
        # fill_price = 1900.5
        # commission = 1900.5 * 10.0 * 0.01 = 190.05
        self.assertEqual(report.commission_paid, 190.05)
        
    def test_partial_fill(self):
        config = ExecutionConfig(partial_fill_model="volume", partial_fill_ratio=0.05)
        engine = ExecutionEngine(config)
        
        # Max fill = volume * ratio = 100 * 0.05 = 5.0. 
        # Order is 10.0. So partial fill of 5.0.
        report = engine.evaluate_execution(self.order, self.snapshot)
        
        self.assertEqual(report.execution_status, ExecutionStatus.PARTIALLY_FILLED)
        self.assertEqual(report.filled_quantity, 5.0)
        self.assertEqual(report.remaining_quantity, 5.0)

    def test_symbol_mismatch_rejection(self):
        engine = ExecutionEngine(ExecutionConfig())
        bad_snapshot = MarketSnapshot("EURUSD", 1001, 1.1, 1.1001, 100.0)
        
        report = engine.evaluate_execution(self.order, bad_snapshot)
        self.assertEqual(report.execution_status, ExecutionStatus.REJECTED)
        self.assertIn("Symbol mismatch", report.rejection_reason)

    def test_stop_order_execution(self):
        config = ExecutionConfig(spread_model="fixed", fixed_spread=1.0, slippage_model="fixed", fixed_slippage=0.5, commission_model="fixed", commission_rate=5.0)
        engine = ExecutionEngine(config)
        
        # Stop order at 1900.0 (Buy Stop)
        # Activated by OMS, becomes Market order conceptually
        # Base price = Bid + Spread = 1900.0 + 1.0 = 1901.0
        # Slippage = 0.5. Final Fill = 1901.5
        # Note: Stop orders do NOT reject if fill > limit, because they are market orders once triggered.
        stop_order = Order("ORD_4", "sig_4", 1000, OrderDirection.LONG, OrderType.STOP, 1900.0, 10.0, "XAUUSD")
        stop_order.transition_to(OrderState.PENDING)
        stop_order.transition_to(OrderState.ACTIVE)
        
        report = engine.evaluate_execution(stop_order, self.snapshot)
        
        self.assertEqual(report.execution_status, ExecutionStatus.FILLED)
        self.assertEqual(report.fill_price, 1901.5)
        self.assertEqual(report.slippage_paid, 0.5)
        self.assertEqual(report.commission_paid, 5.0)

    def test_latency_model(self):
        config = ExecutionConfig(latency_model="fixed", fixed_latency=50)
        engine = ExecutionEngine(config)
        
        report = engine.evaluate_execution(self.order, self.snapshot)
        
        self.assertEqual(report.timestamp, 1051) # 1001 + 50
        self.assertEqual(report.latency, 50)

if __name__ == '__main__':
    unittest.main()
