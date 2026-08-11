from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable
from simulation.market import MarketSnapshot
from simulation.strategy import Strategy
from simulation.statistics import StatisticsSummary, StatisticsEngine
from simulation.runner import SimulationRunner
from simulation.order_manager import OrderManager
from simulation.execution import ExecutionEngine, ExecutionConfig
from simulation.position import PositionEngine, PositionConfig
from simulation.portfolio import PortfolioEngine
import math

@dataclass(frozen=True)
class WalkForwardConfig:
    """Configuration for Walk-Forward analysis."""
    train_size_bars: int
    test_size_bars: int
    step_size_bars: int
    # Allow passing engine configurations to ensure fresh state instantiation
    execution_config: ExecutionConfig = field(default_factory=ExecutionConfig)
    position_config: PositionConfig = field(default_factory=PositionConfig)
    initial_balance: float = 100000.0
    pass_criteria_net_profit: float = 0.0

@dataclass(frozen=True)
class WalkForwardWindow:
    window_id: str
    train_start_idx: int
    train_end_idx: int
    test_start_idx: int
    test_end_idx: int
    test_statistics: StatisticsSummary
    is_passed: bool

@dataclass(frozen=True)
class WalkForwardResult:
    windows: List[WalkForwardWindow]
    aggregate_statistics: Dict[str, float]
    stability_metrics: Dict[str, float]
    overall_pass: bool

class WalkForwardEngine:
    """
    Orchestrates multiple sequential simulations across historical data 
    using rolling training/testing windows.
    """
    def __init__(self, strategy_factory: Callable[[], Strategy], config: WalkForwardConfig):
        self.strategy_factory = strategy_factory
        self.config = config

    def _create_fresh_runner(self) -> SimulationRunner:
        """
        Instantiates a completely fresh set of isolated engines for a window run.
        Ensures absolutely zero state leakage between windows.
        """
        oms = OrderManager()
        execution = ExecutionEngine(self.config.execution_config)
        position = PositionEngine(self.config.position_config)
        portfolio = PortfolioEngine(initial_balance=self.config.initial_balance)
        
        # Ensure absolute state isolation by generating a new strategy instance for this specific run
        fresh_strategy = self.strategy_factory()
        
        return SimulationRunner(fresh_strategy, oms, execution, position, portfolio)

    def run(self, historical_snapshots: List[MarketSnapshot]) -> WalkForwardResult:
        windows = []
        total_bars = len(historical_snapshots)
        
        current_train_start = 0
        window_counter = 1
        
        # We only generate statistics on the TEST window, as the prompt specifies
        # Walk Forward Validation focuses on out-of-sample (OOS) testing.
        while True:
            train_end = current_train_start + self.config.train_size_bars
            test_start = train_end
            test_end = test_start + self.config.test_size_bars
            
            if test_end > total_bars:
                break
                
            # Actually run the Simulation on the TEST window to validate out-of-sample performance.
            # In a full Walk Forward Optimization, we would optimize parameters on the train window,
            # but since "no optimization" and "no parameter mutation" are mandated, 
            # we simply run the rigid Strategy on the test window to validate its robustness.
            test_snapshots = historical_snapshots[test_start:test_end]
            
            runner = self._create_fresh_runner()
            for idx, snapshot in enumerate(test_snapshots):
                runner.step(snapshot, bar_index=test_start + idx)
                
            stats = runner.generate_statistics()
            is_passed = stats.net_profit > self.config.pass_criteria_net_profit
            
            window = WalkForwardWindow(
                window_id=f"WFW_{window_counter}",
                train_start_idx=current_train_start,
                train_end_idx=train_end - 1,
                test_start_idx=test_start,
                test_end_idx=test_end - 1,
                test_statistics=stats,
                is_passed=is_passed
            )
            windows.append(window)
            
            current_train_start += self.config.step_size_bars
            window_counter += 1
            
        # Compute stability metrics
        net_profits = [w.test_statistics.net_profit for w in windows]
        win_rates = [w.test_statistics.win_rate for w in windows]
        
        if len(net_profits) == 0:
            return WalkForwardResult([], {}, {}, False)
            
        avg_profit = sum(net_profits) / len(net_profits)
        total_profit = sum(net_profits)
        avg_win_rate = sum(win_rates) / len(win_rates)
        
        # Calculate standard deviation of net profit
        variance = sum((p - avg_profit) ** 2 for p in net_profits) / len(net_profits)
        std_dev_profit = math.sqrt(variance)
        
        overall_pass = all(w.is_passed for w in windows)
        
        aggregate_stats = {
            "total_net_profit": total_profit,
            "average_net_profit": avg_profit,
            "average_win_rate": avg_win_rate
        }
        
        stability_metrics = {
            "net_profit_std_dev": std_dev_profit,
            "windows_passed": sum(1 for w in windows if w.is_passed),
            "total_windows": len(windows),
            "pass_rate": sum(1 for w in windows if w.is_passed) / len(windows)
        }
        
        return WalkForwardResult(
            windows=windows,
            aggregate_statistics=aggregate_stats,
            stability_metrics=stability_metrics,
            overall_pass=overall_pass
        )
