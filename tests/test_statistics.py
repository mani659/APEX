import unittest
import types
from simulation.statistics import StatisticsEngine
from simulation.position import Trade, ExitReason, OrderDirection
from simulation.portfolio import PortfolioSnapshot

class TestStatisticsEngine(unittest.TestCase):
    def _create_trade(self, net_pnl: float, direction: OrderDirection, bars_held: int) -> Trade:
        return Trade(
            trade_id="TRD_1", position_id="POS_1", symbol="XAUUSD", direction=direction,
            entry_time=1000, exit_time=1001, entry_price=1900.0, exit_price=1900.0 + net_pnl,
            quantity=1.0, gross_pnl=net_pnl, net_pnl=net_pnl, commission=0.0,
            slippage=0.0, exit_reason=ExitReason.TAKE_PROFIT, bars_held=bars_held
        )
        
    def _create_snapshot(self, max_dd: float) -> PortfolioSnapshot:
        return PortfolioSnapshot(
            timestamp=1000, balance=100000.0, equity=100000.0, realized_pnl=0.0,
            floating_pnl=0.0, gross_profit=0.0, gross_loss=0.0, drawdown=0.0,
            max_drawdown=max_dd, margin_used=0.0, free_margin=100000.0,
            exposure_long=0.0, exposure_short=0.0, net_exposure=0.0,
            number_open_positions=0, number_closed_trades=0
        )

    def test_zero_trades(self):
        summary = StatisticsEngine.calculate([], [])
        self.assertEqual(summary.total_trades, 0)
        self.assertEqual(summary.net_profit, 0.0)
        self.assertEqual(summary.win_rate, 0.0)
        self.assertEqual(summary.maximum_drawdown, 0.0)

    def test_single_winner(self):
        trade = self._create_trade(100.0, OrderDirection.LONG, 5)
        summary = StatisticsEngine.calculate([trade], [])
        
        self.assertEqual(summary.total_trades, 1)
        self.assertEqual(summary.winning_trades, 1)
        self.assertEqual(summary.win_rate, 1.0)
        self.assertEqual(summary.net_profit, 100.0)
        self.assertEqual(summary.profit_factor, float('inf'))
        self.assertEqual(summary.average_holding_period, 5.0)
        self.assertEqual(summary.number_of_long_trades, 1)

    def test_single_loser(self):
        trade = self._create_trade(-50.0, OrderDirection.SHORT, 3)
        summary = StatisticsEngine.calculate([trade], [])
        
        self.assertEqual(summary.total_trades, 1)
        self.assertEqual(summary.losing_trades, 1)
        self.assertEqual(summary.loss_rate, 1.0)
        self.assertEqual(summary.net_profit, -50.0)
        self.assertEqual(summary.profit_factor, 0.0)
        self.assertEqual(summary.number_of_short_trades, 1)

    def test_mixed_trades_and_expectancy(self):
        trades = [
            self._create_trade(200.0, OrderDirection.LONG, 10),
            self._create_trade(100.0, OrderDirection.SHORT, 5),
            self._create_trade(-50.0, OrderDirection.LONG, 2),
            self._create_trade(-10.0, OrderDirection.SHORT, 3)
        ]
        snap = self._create_snapshot(max_dd=0.1)
        
        summary = StatisticsEngine.calculate(trades, [snap], metadata={"test": True})
        
        self.assertEqual(summary.total_trades, 4)
        self.assertEqual(summary.winning_trades, 2)
        self.assertEqual(summary.losing_trades, 2)
        self.assertEqual(summary.win_rate, 0.5)
        self.assertEqual(summary.loss_rate, 0.5)
        
        self.assertEqual(summary.gross_profit, 300.0)
        self.assertEqual(summary.gross_loss, 60.0)
        self.assertEqual(summary.net_profit, 240.0)
        self.assertEqual(summary.profit_factor, 5.0)
        
        self.assertEqual(summary.average_win, 150.0)
        self.assertEqual(summary.average_loss, -30.0)
        
        expected_expectancy = (0.5 * 150.0) + (0.5 * -30.0)
        self.assertEqual(summary.expectancy, expected_expectancy)
        self.assertEqual(summary.average_trade, 60.0) # 240 / 4 = 60
        
        self.assertEqual(summary.largest_win, 200.0)
        self.assertEqual(summary.largest_loss, -50.0)
        
        self.assertEqual(summary.average_holding_period, 20.0 / 4)
        
        self.assertEqual(summary.maximum_drawdown, 0.1)
        self.assertEqual(summary.recovery_factor, 240.0 / 0.1)
        
        self.assertEqual(summary.number_of_long_trades, 2)
        self.assertEqual(summary.number_of_short_trades, 2)
        
        self.assertIsInstance(summary.metadata, types.MappingProxyType)
        self.assertTrue(summary.metadata["test"])

if __name__ == '__main__':
    unittest.main()
