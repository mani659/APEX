import unittest
from simulation.portfolio import PortfolioEngine
from simulation.position import Trade, ExitReason, OrderDirection

class TestPortfolioEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PortfolioEngine(initial_balance=100000.0)
        
    def _create_trade(self, net_pnl: float) -> Trade:
        return Trade(
            trade_id="TRD_1", position_id="POS_1", symbol="XAUUSD", direction=OrderDirection.LONG,
            entry_time=1000, exit_time=1001, entry_price=1900.0, exit_price=1900.0 + net_pnl,
            quantity=1.0, gross_pnl=net_pnl, net_pnl=net_pnl, commission=0.0,
            slippage=0.0, exit_reason=ExitReason.TAKE_PROFIT, bars_held=1
        )

    def test_initial_state(self):
        self.assertEqual(self.engine.balance, 100000.0)
        self.assertEqual(self.engine.equity, 100000.0)
        self.assertEqual(self.engine.peak_equity, 100000.0)
        self.assertEqual(self.engine.current_drawdown, 0.0)
        self.assertEqual(self.engine.max_drawdown, 0.0)
        
    def test_profitable_trade_updates(self):
        trade = self._create_trade(net_pnl=500.0)
        self.engine.process_trade(trade)
        
        self.assertEqual(self.engine.balance, 100500.0)
        self.assertEqual(self.engine.realized_pnl, 500.0)
        self.assertEqual(self.engine.gross_profit, 500.0)
        self.assertEqual(self.engine.gross_loss, 0.0)
        
        # High water marks should NOT update until commit
        self.assertEqual(self.engine.peak_equity, 100000.0)
        
        self.engine.commit_accounting_cycle(1000)
        
        self.assertEqual(self.engine.peak_equity, 100500.0)
        self.assertEqual(self.engine.current_drawdown, 0.0)
        self.assertEqual(self.engine.number_closed_trades, 1)

    def test_losing_trade_updates_drawdown(self):
        trade = self._create_trade(net_pnl=-1000.0)
        self.engine.process_trade(trade)
        self.engine.commit_accounting_cycle(1000)
        
        self.assertEqual(self.engine.balance, 99000.0)
        self.assertEqual(self.engine.gross_loss, 1000.0)
        self.assertEqual(self.engine.peak_equity, 100000.0)
        
        expected_dd = (100000.0 - 99000.0) / 100000.0
        self.assertEqual(self.engine.current_drawdown, expected_dd)
        self.assertEqual(self.engine.max_drawdown, expected_dd)
        
    def test_floating_state_updates(self):
        self.engine.update_floating_state(
            floating_pnl=1000.0,
            margin_used=5000.0,
            exposure_long=10.0,
            exposure_short=0.0,
            number_open_positions=1
        )
        self.engine.commit_accounting_cycle(1000)
        
        self.assertEqual(self.engine.equity, 101000.0) # 100k + 1k
        self.assertEqual(self.engine.free_margin, 96000.0) # 101k - 5k
        self.assertEqual(self.engine.peak_equity, 101000.0)
        self.assertEqual(self.engine.current_drawdown, 0.0)
        self.assertEqual(self.engine.net_exposure, 10.0)

    def test_max_drawdown_persistence(self):
        # 1. Float down by 10k
        self.engine.update_floating_state(floating_pnl=-10000.0, margin_used=0, exposure_long=0, exposure_short=0, number_open_positions=1)
        self.engine.commit_accounting_cycle(1000)
        self.assertEqual(self.engine.equity, 90000.0)
        self.assertEqual(self.engine.current_drawdown, 0.1)
        self.assertEqual(self.engine.max_drawdown, 0.1)
        
        # 2. Recover float to 0
        self.engine.update_floating_state(floating_pnl=0.0, margin_used=0, exposure_long=0, exposure_short=0, number_open_positions=0)
        self.engine.commit_accounting_cycle(1001)
        self.assertEqual(self.engine.equity, 100000.0)
        self.assertEqual(self.engine.current_drawdown, 0.0)
        
        # Max drawdown should persist!
        self.assertEqual(self.engine.max_drawdown, 0.1)

    def test_commit_accounting_cycle(self):
        trade = self._create_trade(net_pnl=100.0)
        self.engine.process_trade(trade)
        
        self.engine.update_floating_state(
            floating_pnl=-50.0, margin_used=1000.0, exposure_long=1.0, exposure_short=2.0, number_open_positions=3
        )
        
        snap = self.engine.commit_accounting_cycle(timestamp=2000, metadata={"tag": "test"})
        
        self.assertEqual(snap.timestamp, 2000)
        self.assertEqual(snap.balance, 100100.0)
        self.assertEqual(snap.equity, 100050.0) # 100100 - 50
        self.assertEqual(snap.floating_pnl, -50.0)
        self.assertEqual(snap.margin_used, 1000.0)
        self.assertEqual(snap.free_margin, 99050.0)
        self.assertEqual(snap.exposure_long, 1.0)
        self.assertEqual(snap.exposure_short, 2.0)
        self.assertEqual(snap.net_exposure, -1.0)
        self.assertEqual(snap.number_open_positions, 3)
        self.assertEqual(snap.number_closed_trades, 1)
        self.assertEqual(snap.metadata["tag"], "test")
        
        # Ensure metadata is fully immutable (types.MappingProxyType raises TypeError)
        with self.assertRaises(TypeError):
            snap.metadata["tag"] = "mutated"

if __name__ == '__main__':
    unittest.main()
