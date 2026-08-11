import unittest
from datetime import datetime, timezone
from types import MappingProxyType

from simulation.reporting import ReportGenerator, ReportConfig, ReportDocument
from simulation.statistics import StatisticsSummary
from simulation.portfolio import PortfolioSnapshot
from simulation.walkforward import WalkForwardResult
from simulation.montecarlo import MonteCarloResult
from simulation.optimization import OptimizationResult, OptimizationEvaluation
from simulation.experiment import ExperimentRecord, ResearchComponent, ExperimentComparison

def create_mock_stats(net_profit=100.0) -> StatisticsSummary:
    return StatisticsSummary(
        total_trades=10,
        winning_trades=5,
        losing_trades=5,
        win_rate=0.5,
        loss_rate=0.5,
        gross_profit=150.0,
        gross_loss=50.0,
        net_profit=net_profit,
        profit_factor=3.0,
        average_trade=10.0,
        average_win=30.0,
        average_loss=10.0,
        largest_win=30.0,
        largest_loss=10.0,
        expectancy=10.0,
        average_holding_period=2.0,
        maximum_drawdown=20.0,
        recovery_factor=net_profit / 20.0,
        number_of_long_trades=5,
        number_of_short_trades=5,
        metadata=None
    )

class TestReportGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = ReportGenerator()
        
    def test_empty_report(self):
        config = ReportConfig()
        result = self.generator.generate(config)
        self.assertIn("Executive Summary", result)
        self.assertNotIn("Performance Statistics", result) # because no stats provided
        
    def test_single_statistics_summary(self):
        config = ReportConfig()
        stats = create_mock_stats(100.0)
        
        result = self.generator.generate(config, stats=stats)
        self.assertIn("Performance Statistics", result)
        self.assertIn("Net Profit:** 100.00", result)
        self.assertNotIn("Monte Carlo Summary", result)
        
    def test_all_objects(self):
        config = ReportConfig()
        stats = create_mock_stats(100.0)
        snapshots = [PortfolioSnapshot(
            timestamp=0, 
            balance=1000.0, 
            equity=1000.0, 
            realized_pnl=0.0,
            floating_pnl=0.0,
            gross_profit=0.0,
            gross_loss=0.0,
            drawdown=0.0,
            max_drawdown=0.0,
            margin_used=0.0,
            free_margin=1000.0,
            exposure_long=0.0,
            exposure_short=0.0,
            net_exposure=0.0,
            number_open_positions=0,
            number_closed_trades=0
        )]
        
        opt_res = OptimizationResult(
            best_parameters={"a": 1},
            best_statistics=stats,
            objective_value=100.0,
            ranking=[],
            number_of_evaluations=1,
            runtime_seconds=1.0
        )
        
        mc_res = MonteCarloResult(
            number_of_runs=10,
            statistics_per_run=[stats],
            net_profit_distribution=[100.0],
            drawdown_distribution=[20.0],
            profit_factor_distribution=[3.0],
            expectancy_distribution=[10.0],
            win_rate_distribution=[0.5],
            recovery_factor_distribution=[5.0],
            aggregates={
                "net_profit": {"p50": 100.0},
                "maximum_drawdown": {"p99": 20.0}
            },
            prob_net_profit_positive=1.0,
            prob_drawdown_gt_threshold=0.0,
            prob_profit_factor_gt_one=1.0,
            prob_recovery_factor_gt_threshold=1.0
        )
        
        wf_res = WalkForwardResult(
            windows=[],
            aggregate_statistics={"net_profit": 100.0},
            stability_metrics={"robustness_ratio": 1.0},
            overall_pass=True
        )
        
        # Test markdown output
        result_md = self.generator.generate(
            config,
            stats=stats,
            snapshots=snapshots,
            opt_result=opt_res,
            mc_result=mc_res,
            wf_result=wf_res
        )
        
        self.assertIn("Optimization Summary", result_md)
        self.assertIn("Walk-Forward Summary", result_md)
        self.assertIn("Monte Carlo Summary", result_md)
        self.assertIn("Portfolio Summary", result_md)
        self.assertTrue(result_md.startswith("# Research Report"))
        
        # Test html output
        config_html = ReportConfig(output_format="html")
        result_html = self.generator.generate(
            config_html,
            stats=stats,
            snapshots=snapshots,
            opt_result=opt_res,
            mc_result=mc_res,
            wf_result=wf_res
        )
        
        self.assertIn("<h2>Optimization Summary</h2>", result_html)
        self.assertIn("<!DOCTYPE html>", result_html)
        
    def test_config_flags_omission(self):
        # Even if data provided, if config says no, it shouldn't be included
        config = ReportConfig(include_statistics=False)
        stats = create_mock_stats(100.0)
        
        result = self.generator.generate(config, stats=stats)
        self.assertNotIn("Performance Statistics", result)

if __name__ == '__main__':
    unittest.main()
