import unittest
from simulation.order import OrderDirection, ExecutionReport, ExecutionStatus
from simulation.market import MarketSnapshot
from simulation.position import PositionEngine, PositionConfig, ExitReason, PositionStatus

class TestPositionEngine(unittest.TestCase):
    def setUp(self):
        self.config = PositionConfig(expiration_bars=5)
        self.engine = PositionEngine(self.config)
        self.snapshot1 = MarketSnapshot("XAUUSD", 1000, 1900.0, 1900.5, 100)
        
    def test_position_creation(self):
        report = ExecutionReport(
            execution_id="exec_1", order_id="ord_1", signal_id="sig_1", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1000, execution_status=ExecutionStatus.FILLED, fill_price=1900.5,
            requested_price=1900.0, filled_quantity=10.0, remaining_quantity=0.0,
            spread_paid=0.5, slippage_paid=0.0, commission_paid=5.0, latency=0
        )
        pos = self.engine.process_execution_report(report, stop_loss=1890.0, take_profit=1920.0)
        
        self.assertIsNotNone(pos)
        self.assertEqual(pos.position_id, "POS_exec_1")
        self.assertEqual(pos.status, PositionStatus.ACTIVE)
        self.assertEqual(pos.entry_price, 1900.5)
        self.assertEqual(len(self.engine._positions), 1)
        
    def test_position_stop_loss_long(self):
        report = ExecutionReport(
            execution_id="exec_sl", order_id="ord_1", signal_id="sig_1", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1000, execution_status=ExecutionStatus.FILLED, fill_price=1900.5,
            requested_price=1900.0, filled_quantity=10.0, remaining_quantity=0.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        self.engine.process_execution_report(report, stop_loss=1890.0)
        
        # Price drops below SL (Bid is 1889.0)
        snap = MarketSnapshot("XAUUSD", 1001, 1889.0, 1889.5, 10)
        trades = self.engine.evaluate_positions(snap)
        
        self.assertEqual(len(trades), 1)
        trade = trades[0]
        self.assertEqual(trade.exit_reason, ExitReason.STOP_LOSS)
        self.assertEqual(trade.exit_price, 1889.0)
        self.assertEqual(len(self.engine._positions), 0)
        
    def test_position_take_profit_short(self):
        report = ExecutionReport(
            execution_id="exec_tp", order_id="ord_2", signal_id="sig_2", symbol="XAUUSD", direction=OrderDirection.SHORT,
            timestamp=1000, execution_status=ExecutionStatus.FILLED, fill_price=1900.0,
            requested_price=1900.0, filled_quantity=10.0, remaining_quantity=0.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        self.engine.process_execution_report(report, take_profit=1880.0)
        
        # Price drops to TP (Ask is 1880.0)
        snap = MarketSnapshot("XAUUSD", 1001, 1879.5, 1880.0, 10)
        trades = self.engine.evaluate_positions(snap)
        
        self.assertEqual(len(trades), 1)
        trade = trades[0]
        self.assertEqual(trade.exit_reason, ExitReason.TAKE_PROFIT)
        self.assertEqual(trade.exit_price, 1880.0)
        self.assertGreater(trade.gross_pnl, 0)
        self.assertEqual(trade.gross_pnl, (1900.0 - 1880.0) * 10.0)
        
    def test_position_expiration(self):
        report = ExecutionReport(
            execution_id="exec_exp", order_id="ord_3", signal_id="sig_3", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1000, execution_status=ExecutionStatus.FILLED, fill_price=1900.5,
            requested_price=1900.0, filled_quantity=10.0, remaining_quantity=0.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        self.engine.process_execution_report(report)
        
        for i in range(4):
            snap = MarketSnapshot("XAUUSD", 1001 + i, 1900.0, 1900.5, 10)
            self.engine.evaluate_positions(snap)
            self.assertEqual(len(self.engine._positions), 1)
            
        snap5 = MarketSnapshot("XAUUSD", 1005, 1900.0, 1900.5, 10)
        trades = self.engine.evaluate_positions(snap5)
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].exit_reason, ExitReason.EXPIRATION)
        
    def test_manual_close(self):
        report = ExecutionReport(
            execution_id="exec_man", order_id="ord_4", signal_id="sig_4", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1000, execution_status=ExecutionStatus.FILLED, fill_price=1900.5,
            requested_price=1900.0, filled_quantity=10.0, remaining_quantity=0.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        pos = self.engine.process_execution_report(report)
        
        snap = MarketSnapshot("XAUUSD", 1001, 1905.0, 1905.5, 10)
        trade = self.engine.close_position_manually(pos.position_id, snap)
        
        self.assertIsNotNone(trade)
        self.assertEqual(trade.exit_reason, ExitReason.MANUAL_CLOSE)
        self.assertEqual(trade.exit_price, 1905.0)

    def test_multiple_positions_independent(self):
        report1 = ExecutionReport(
            execution_id="exec_m1", order_id="ord_m1", signal_id="sig_m1", symbol="XAUUSD", direction=OrderDirection.LONG,
            timestamp=1000, execution_status=ExecutionStatus.FILLED, fill_price=1900.0,
            requested_price=1900.0, filled_quantity=10.0, remaining_quantity=0.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        report2 = ExecutionReport(
            execution_id="exec_m2", order_id="ord_m2", signal_id="sig_m2", symbol="XAUUSD", direction=OrderDirection.SHORT,
            timestamp=1000, execution_status=ExecutionStatus.FILLED, fill_price=1900.0,
            requested_price=1900.0, filled_quantity=10.0, remaining_quantity=0.0,
            spread_paid=0.0, slippage_paid=0.0, commission_paid=0.0, latency=0
        )
        self.engine.process_execution_report(report1, stop_loss=1890.0)
        self.engine.process_execution_report(report2, stop_loss=1910.0)
        
        self.assertEqual(len(self.engine._positions), 2)
        
        # Price spikes up, stopping out the short position
        snap = MarketSnapshot("XAUUSD", 1001, 1910.0, 1910.5, 10)
        trades = self.engine.evaluate_positions(snap)
        
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].direction, OrderDirection.SHORT)
        self.assertEqual(len(self.engine._positions), 1) # Long still alive

if __name__ == '__main__':
    unittest.main()
