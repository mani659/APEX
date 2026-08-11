import random
import statistics
import types
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Any

from simulation.market import MarketSnapshot
from simulation.strategy import Strategy
from simulation.runner import SimulationRunner
from simulation.order_manager import OrderManager
from simulation.execution import ExecutionEngine, ExecutionConfig
from simulation.position import PositionEngine, PositionConfig, Trade
from simulation.portfolio import PortfolioEngine, PortfolioSnapshot
from simulation.statistics import StatisticsEngine, StatisticsSummary

@dataclass(frozen=True)
class MonteCarloConfig:
    number_of_runs: int = 100
    random_seed: int = 42
    
    # Perturbation toggles
    enable_trade_shuffle: bool = False
    enable_slippage_noise: bool = False
    enable_spread_noise: bool = False
    enable_commission_noise: bool = False
    enable_data_bootstrap: bool = False
    
    # Noise boundaries (defaults)
    spread_noise_bound: float = 1.0       # max absolute additive noise
    slippage_noise_bound: float = 1.0     # max absolute additive noise
    commission_noise_bound: float = 0.001 # max absolute additive noise
    
    initial_balance: float = 100000.0
    execution_config: ExecutionConfig = field(default_factory=ExecutionConfig)
    position_config: PositionConfig = field(default_factory=PositionConfig)

@dataclass(frozen=True)
class MonteCarloResult:
    number_of_runs: int
    statistics_per_run: List[StatisticsSummary]
    
    # Distributions (sorted for percentile extraction)
    net_profit_distribution: List[float]
    drawdown_distribution: List[float]
    profit_factor_distribution: List[float]
    expectancy_distribution: List[float]
    win_rate_distribution: List[float]
    recovery_factor_distribution: List[float]
    
    # Aggregates mapping: metric -> { mean, median, std, min, max, p5, p25, p50, p75, p95 }
    aggregates: Dict[str, Dict[str, float]]
    
    # Probabilities
    prob_net_profit_positive: float
    prob_drawdown_gt_threshold: float  # Uses 20% drawdown as default threshold
    prob_profit_factor_gt_one: float
    prob_recovery_factor_gt_threshold: float # Uses 1.0 as default threshold
    
class RecordingPortfolioEngine(PortfolioEngine):
    """
    Subclass that simply intercepts immutable Trades to fulfill Trade Sequence Shuffle 
    without accessing private variables or modifying SimulationRunner.
    """
    def __init__(self, initial_balance: float = 100000.0):
        super().__init__(initial_balance)
        self.recorded_trades: List[Trade] = []
        
    def process_trade(self, trade: Trade):
        self.recorded_trades.append(trade)
        super().process_trade(trade)

class MonteCarloEngine:
    """
    Research orchestrator that runs Monte Carlo simulations over the frozen Simulation Core.
    """
    def __init__(self, strategy_factory: Callable[[], Strategy], config: MonteCarloConfig):
        self.strategy_factory = strategy_factory
        self.config = config

    def _create_runner(self) -> tuple[SimulationRunner, RecordingPortfolioEngine]:
        oms = OrderManager()
        
        # Base exec config
        ec = self.config.execution_config
        
        # Apply perturbations
        spread = ec.fixed_spread
        spread_model = ec.spread_model
        if self.config.enable_spread_noise:
            spread += random.uniform(0, self.config.spread_noise_bound)
            spread_model = "fixed"
            
        slippage = ec.fixed_slippage
        slippage_model = ec.slippage_model
        if self.config.enable_slippage_noise:
            slippage += random.uniform(0, self.config.slippage_noise_bound)
            slippage_model = "fixed"
            
        commission = ec.commission_rate
        commission_model = ec.commission_model
        if self.config.enable_commission_noise:
            commission += random.uniform(0, self.config.commission_noise_bound)
            commission_model = "fixed"
            
        noisy_exec_config = ExecutionConfig(
            spread_model=spread_model,
            fixed_spread=spread,
            slippage_model=slippage_model,
            fixed_slippage=slippage,
            commission_model=commission_model,
            commission_rate=commission,
            partial_fill_model=ec.partial_fill_model,
            partial_fill_ratio=ec.partial_fill_ratio,
            latency_model=ec.latency_model,
            fixed_latency=ec.fixed_latency
        )
        
        execution = ExecutionEngine(noisy_exec_config)
        position = PositionEngine(self.config.position_config)
        portfolio = RecordingPortfolioEngine(initial_balance=self.config.initial_balance)
        
        fresh_strategy = self.strategy_factory()
        
        runner = SimulationRunner(fresh_strategy, oms, execution, position, portfolio)
        return runner, portfolio

    def run(self, historical_snapshots: List[MarketSnapshot]) -> MonteCarloResult:
        # 1. Determinism
        random.seed(self.config.random_seed)
        
        run_stats = []
        
        for _ in range(self.config.number_of_runs):
            # 2. Bootstrap data if required
            if self.config.enable_data_bootstrap and len(historical_snapshots) > 0:
                current_snapshots = random.choices(historical_snapshots, k=len(historical_snapshots))
            else:
                current_snapshots = historical_snapshots
                
            runner, recording_portfolio = self._create_runner()
            
            # 3. Execution
            for idx, snap in enumerate(current_snapshots):
                runner.step(snap, bar_index=idx)
                
            # 4. Handle Trade Sequence Shuffle
            if self.config.enable_trade_shuffle:
                shuffled_trades = list(recording_portfolio.recorded_trades)
                random.shuffle(shuffled_trades)
                
                # Re-run strict accounting to get exact drawdown given the new equity curve
                calc_portfolio = PortfolioEngine(self.config.initial_balance)
                new_snapshots = []
                for t in shuffled_trades:
                    calc_portfolio.process_trade(t)
                    # We just need to commit to generate the snapshot for drawdown calculation.
                    # Timestamp doesn't technically matter for max drawdown computation
                    new_snapshots.append(calc_portfolio.commit_accounting_cycle(t.exit_time))
                    
                stats = StatisticsEngine.calculate(shuffled_trades, new_snapshots)
            else:
                stats = runner.generate_statistics()
                
            run_stats.append(stats)
            
        return self._aggregate_results(run_stats)

    def _aggregate_results(self, run_stats: List[StatisticsSummary]) -> MonteCarloResult:
        def extract(metric_func) -> List[float]:
            vals = [metric_func(s) for s in run_stats]
            # Replace infinities from profit factor
            return [v if v != float('inf') else 999.0 for v in vals]
            
        np_dist = extract(lambda s: s.net_profit)
        dd_dist = extract(lambda s: s.maximum_drawdown)
        pf_dist = extract(lambda s: s.profit_factor)
        ex_dist = extract(lambda s: s.expectancy)
        wr_dist = extract(lambda s: s.win_rate)
        rf_dist = extract(lambda s: s.recovery_factor)
        
        distributions = {
            "net_profit": np_dist,
            "drawdown": dd_dist,
            "profit_factor": pf_dist,
            "expectancy": ex_dist,
            "win_rate": wr_dist,
            "recovery_factor": rf_dist
        }
        
        aggregates = {}
        for name, dist in distributions.items():
            sorted_dist = sorted(dist)
            n = len(sorted_dist)
            
            if n == 0:
                aggregates[name] = {k: 0.0 for k in ["mean", "median", "std", "min", "max", "p5", "p25", "p50", "p75", "p95"]}
                continue
                
            def p(pct):
                idx = int((pct / 100.0) * (n - 1))
                return sorted_dist[idx]
                
            mean = statistics.mean(dist)
            median = statistics.median(dist)
            std = statistics.stdev(dist) if n > 1 else 0.0
            
            aggregates[name] = {
                "mean": mean,
                "median": median,
                "std": std,
                "min": sorted_dist[0],
                "max": sorted_dist[-1],
                "p5": p(5),
                "p25": p(25),
                "p50": p(50),
                "p75": p(75),
                "p95": p(95),
            }
            
        # Probabilities
        n_runs = len(run_stats)
        if n_runs > 0:
            p_np_pos = sum(1 for v in np_dist if v > 0) / n_runs
            p_dd_gt = sum(1 for v in dd_dist if v > 0.20) / n_runs # threshold 0.20
            p_pf_gt = sum(1 for v in pf_dist if v > 1.0) / n_runs
            p_rf_gt = sum(1 for v in rf_dist if v > 1.0) / n_runs
        else:
            p_np_pos = p_dd_gt = p_pf_gt = p_rf_gt = 0.0
            
        return MonteCarloResult(
            number_of_runs=n_runs,
            statistics_per_run=run_stats,
            net_profit_distribution=np_dist,
            drawdown_distribution=dd_dist,
            profit_factor_distribution=pf_dist,
            expectancy_distribution=ex_dist,
            win_rate_distribution=wr_dist,
            recovery_factor_distribution=rf_dist,
            aggregates=aggregates,
            prob_net_profit_positive=p_np_pos,
            prob_drawdown_gt_threshold=p_dd_gt,
            prob_profit_factor_gt_one=p_pf_gt,
            prob_recovery_factor_gt_threshold=p_rf_gt
        )
