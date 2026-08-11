import unittest
from typing import List
from simulation.context import TradingContext
from simulation.market import MarketSnapshot
from simulation.order import Signal, OrderDirection, OrderType
from simulation.strategy import Strategy
from simulation.order_manager import OrderManager
from simulation.execution import ExecutionEngine, ExecutionConfig
from simulation.position import PositionEngine, PositionConfig
from simulation.portfolio import PortfolioEngine
from simulation.runner import SimulationRunner

class DummyStrategy(Strategy):
    def __init__(self):
        self.signaled = False
        
    def generate_signals(self, context: TradingContext) -> List[Signal]:
        if not self.signaled and context.timestamp == 1000:
            self.signaled = True
            return [
                Signal(
                    signal_id="SIG_1", strategy_name="DUMMY", strategy_version="1",
                    timestamp=context.timestamp, direction=OrderDirection.LONG,
                    entry_type=OrderType.MARKET, desired_entry=context.current_price,
                    quantity=1.0, take_profit=105.0, stop_loss=95.0
                )
            ]
        return []

class TestSimulationRunner(unittest.TestCase):
    def setUp(self):
        self.strategy = DummyStrategy()
        self.oms = OrderManager()
        self.execution = ExecutionEngine(ExecutionConfig(slippage_model="ZERO", commission_model="ZERO"))
        self.position = PositionEngine(PositionConfig())
        self.portfolio = PortfolioEngine(initial_balance=10000.0)
        
        self.runner = SimulationRunner(
            self.strategy, self.oms, self.execution, self.position, self.portfolio
        )

    def test_full_pipeline_lifecycle(self):
        # Step 1: Market opens at 100. Strategy fires MARKET LONG.
        snap1 = MarketSnapshot(symbol="XAUUSD", timestamp=1000, bid=100.0, ask=100.0, volume=1.0)
        self.runner.step(snap1, bar_index=1)
        
        # After step 1: 
        # - Signal received by OMS -> Order ACTIVE -> Execution Engine fills it -> OMS updates it -> Position opens
        # - PnL floating = 0
        self.assertEqual(self.portfolio.number_open_positions, 1)
        longs, shorts = self.position.get_position_counts()
        self.assertEqual(longs + shorts, 1)
        
        # Step 2: Price moves up to 102.
        snap2 = MarketSnapshot(symbol="XAUUSD", timestamp=1001, bid=102.0, ask=102.0, volume=1.0)
        self.runner.step(snap2, bar_index=2)
        
        # After step 2: 
        # - Position still open, floating PnL should be +2.0
        self.assertEqual(self.portfolio.floating_pnl, 2.0)
        self.assertEqual(self.portfolio.equity, 10002.0)
        self.assertEqual(self.portfolio.peak_equity, 10002.0)
        
        # Step 3: Price hits take profit at 105.
        snap3 = MarketSnapshot(symbol="XAUUSD", timestamp=1002, bid=105.0, ask=105.0, volume=1.0)
        self.runner.step(snap3, bar_index=3)
        
        # After step 3:
        # - Position Engine evaluates and hits take profit -> Closes trade -> Portfolio realizes 5.0
        # - floating PnL = 0
        self.assertEqual(self.portfolio.number_open_positions, 0)
        self.assertEqual(self.portfolio.balance, 10005.0)
        self.assertEqual(self.portfolio.realized_pnl, 5.0)
        self.assertEqual(self.portfolio.equity, 10005.0)
        
        # Step 4: Generate Stats
        stats = self.runner.generate_statistics()
        self.assertEqual(stats.total_trades, 1)
        self.assertEqual(stats.winning_trades, 1)
        self.assertEqual(stats.net_profit, 5.0)
        self.assertEqual(stats.win_rate, 1.0)
        self.assertEqual(stats.maximum_drawdown, 0.0)

if __name__ == '__main__':
    unittest.main()
