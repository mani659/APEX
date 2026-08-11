import unittest
from typing import List
from simulation.context import TradingContext
from simulation.market import MarketSnapshot
from simulation.order import Signal, OrderDirection, OrderType
from simulation.strategy import Strategy
from simulation.montecarlo import MonteCarloEngine, MonteCarloConfig, MonteCarloResult

class StatefulStrategy(Strategy):
    """
    Deliberately trades once on the very first bar it sees.
    Used to prove state isolation.
    """
    def __init__(self):
        self.internal_trade_count = 0

    def generate_signals(self, context: TradingContext) -> List[Signal]:
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

class MultiTradeStrategy(Strategy):
    """
    Trades multiple times to test Trade Sequence Shuffle.
    Buys at 100, closes at 105. Short at 110, close at 105.
    """
    def __init__(self):
        self.trades = 0

    def generate_signals(self, context: TradingContext) -> List[Signal]:
        # Just fire a signal every 5 bars.
        if context.bar_index % 5 == 0 and self.trades < 5:
            self.trades += 1
            return [
                Signal(
                    signal_id=f"SIG_{context.timestamp}", strategy_name="MULTI", strategy_version="1",
                    timestamp=context.timestamp, direction=OrderDirection.LONG,
                    entry_type=OrderType.MARKET, desired_entry=context.current_price,
                    quantity=1.0, take_profit=context.current_price + 2.0, stop_loss=context.current_price - 2.0
                )
            ]
        return []

class TestMonteCarloEngine(unittest.TestCase):
    def setUp(self):
        self.snapshots = []
        for i in range(100):
            price = 100.0 + i  # Guaranteed to hit Take Profit of +2.0 every 2 bars
            self.snapshots.append(MarketSnapshot(symbol="XAUUSD", timestamp=1000 + i, bid=price, ask=price, volume=1.0))

    def test_deterministic_replay(self):
        def sf(): return StatefulStrategy()
        config = MonteCarloConfig(number_of_runs=2, random_seed=42)
        engine = MonteCarloEngine(sf, config)
        result = engine.run(self.snapshots)
        
        self.assertEqual(result.number_of_runs, 2)
        
        # In a purely deterministic setting (no perturbations), all runs should be identical.
        stats1 = result.statistics_per_run[0]
        stats2 = result.statistics_per_run[1]
        self.assertEqual(stats1.net_profit, stats2.net_profit)
        self.assertEqual(stats1.total_trades, stats2.total_trades)
        
        # Prove state isolation: if state leaked, run 2 would have 0 trades.
        self.assertEqual(stats1.total_trades, 1)
        self.assertEqual(stats2.total_trades, 1)
        
    def test_trade_shuffle(self):
        def sf(): return MultiTradeStrategy()
        # Enable trade shuffle
        config = MonteCarloConfig(number_of_runs=10, random_seed=42, enable_trade_shuffle=True)
        engine = MonteCarloEngine(sf, config)
        result = engine.run(self.snapshots)
        
        self.assertEqual(result.number_of_runs, 10)
        
        # All runs should have the same total net profit, but max drawdown could vary 
        # (Though with this specific strategy, all trades are winners, so drawdown is 0)
        np_dist = result.net_profit_distribution
        # Since the strategy makes 5 trades, and each trade is a winner of 2.0 (gross 2.0)
        self.assertEqual(np_dist[0], np_dist[-1])
        
    def test_bootstrap(self):
        def sf(): return MultiTradeStrategy()
        # Enable bootstrap
        config = MonteCarloConfig(number_of_runs=5, random_seed=123, enable_data_bootstrap=True)
        engine = MonteCarloEngine(sf, config)
        result = engine.run(self.snapshots)
        
        # Bootstrap changes the sequence of prices, meaning the number of trades or their outcome will vary.
        # Check that standard deviation of net profit is > 0
        self.assertGreater(result.aggregates["net_profit"]["std"], 0.0)
        
    def test_execution_noise(self):
        def sf(): return StatefulStrategy()
        # Enable noise
        config = MonteCarloConfig(
            number_of_runs=10, 
            random_seed=42, 
            enable_slippage_noise=True, 
            slippage_noise_bound=0.5
        )
        engine = MonteCarloEngine(sf, config)
        result = engine.run(self.snapshots)
        
        # Slippage noise should cause net profit to vary
        self.assertGreater(result.aggregates["net_profit"]["std"], 0.0)
        
    def test_percentile_correctness(self):
        def sf(): return StatefulStrategy()
        # Force variation via noise to test percentiles
        config = MonteCarloConfig(
            number_of_runs=100, 
            random_seed=999, 
            enable_slippage_noise=True, 
            slippage_noise_bound=2.0
        )
        engine = MonteCarloEngine(sf, config)
        result = engine.run(self.snapshots)
        
        agg = result.aggregates["net_profit"]
        self.assertLessEqual(agg["min"], agg["p5"])
        self.assertLessEqual(agg["p5"], agg["p25"])
        self.assertLessEqual(agg["p25"], agg["p50"])
        self.assertLessEqual(agg["p50"], agg["p75"])
        self.assertLessEqual(agg["p75"], agg["p95"])
        self.assertLessEqual(agg["p95"], agg["max"])

if __name__ == '__main__':
    unittest.main()
