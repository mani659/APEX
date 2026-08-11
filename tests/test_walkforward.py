import unittest
from typing import List
from simulation.context import TradingContext
from simulation.market import MarketSnapshot
from simulation.order import Signal, OrderDirection, OrderType
from simulation.strategy import Strategy
from simulation.walkforward import WalkForwardEngine, WalkForwardConfig

class StatefulStrategy(Strategy):
    """
    A deliberately stateful strategy to prove state isolation.
    It counts its own internal trades. If state leaks across windows, 
    this count will increase beyond what is expected per window.
    """
    def __init__(self):
        self.internal_trade_count = 0

    def generate_signals(self, context: TradingContext) -> List[Signal]:
        # Trade exactly once per window life-cycle, on the very first bar we see
        # Because we only trade if internal_trade_count == 0.
        # If state leaks, Window 2 will start with internal_trade_count == 1 and never trade!
        if self.internal_trade_count == 0:
            self.internal_trade_count += 1
            return [
                Signal(
                    signal_id=f"SIG_{context.timestamp}", strategy_name="STATEFUL", strategy_version="1",
                    timestamp=context.timestamp, direction=OrderDirection.LONG,
                    entry_type=OrderType.MARKET, desired_entry=context.current_price,
                    quantity=1.0, take_profit=context.current_price + 2.0, stop_loss=context.current_price - 2.0
                )
            ]
        return []

class TestWalkForwardEngine(unittest.TestCase):
    def test_rolling_windows(self):
        # Create 100 fake snapshots representing an upward trending market
        snapshots = []
        for i in range(100):
            price = 100.0 + i  # Guaranteed to hit Take Profit of +2.0 every 2 bars
            snapshots.append(MarketSnapshot(symbol="XAUUSD", timestamp=1000 + i, bid=price, ask=price, volume=1.0))
            
        def strategy_factory() -> Strategy:
            return StatefulStrategy()
            
        # 10 bars train, 10 bars test, step 10
        config = WalkForwardConfig(
            train_size_bars=10,
            test_size_bars=10,
            step_size_bars=10,
            pass_criteria_net_profit=0.0
        )
        
        engine = WalkForwardEngine(strategy_factory, config)
        result = engine.run(snapshots)
        
        # 100 total bars = 9 full windows 
        self.assertEqual(len(result.windows), 9)
        
        for w in result.windows:
            # If the strategy was reused (leaked), Window 2+ would have internal_trade_count=1 
            # and generate 0 trades. The fact that EVERY window takes a trade proves 
            # the strategy was freshly instantiated for each window.
            self.assertEqual(w.test_statistics.total_trades, 1, f"Window {w.window_id} suffered state leakage!")
            self.assertTrue(w.is_passed)
            
        self.assertTrue(result.overall_pass)
        self.assertEqual(result.stability_metrics["total_windows"], 9)
        self.assertEqual(result.stability_metrics["windows_passed"], 9)

if __name__ == '__main__':
    unittest.main()
