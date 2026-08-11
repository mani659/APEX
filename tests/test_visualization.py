import unittest
from types import MappingProxyType

from simulation.visualization import VisualizationEngine, VisualizationConfig
from simulation.portfolio import PortfolioSnapshot
from simulation.montecarlo import MonteCarloResult
from simulation.statistics import StatisticsSummary

class TestVisualizationEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = VisualizationEngine()
        self.config_svg = VisualizationConfig(format="svg", theme="dark")
        self.config_html = VisualizationConfig(format="html", theme="light")
        
        self.snapshots = [
            PortfolioSnapshot(timestamp=1, balance=100.0, equity=100.0, realized_pnl=0.0, floating_pnl=0.0, gross_profit=0.0, gross_loss=0.0, drawdown=0.0, max_drawdown=0.0, margin_used=0.0, free_margin=100.0, exposure_long=0.0, exposure_short=0.0, net_exposure=0.0, number_open_positions=0, number_closed_trades=0),
            PortfolioSnapshot(timestamp=2, balance=100.0, equity=110.0, realized_pnl=0.0, floating_pnl=10.0, gross_profit=0.0, gross_loss=0.0, drawdown=0.0, max_drawdown=0.0, margin_used=10.0, free_margin=90.0, exposure_long=0.0, exposure_short=0.0, net_exposure=0.0, number_open_positions=0, number_closed_trades=0),
            PortfolioSnapshot(timestamp=3, balance=100.0, equity=105.0, realized_pnl=0.0, floating_pnl=5.0, gross_profit=0.0, gross_loss=0.0, drawdown=5.0, max_drawdown=5.0, margin_used=10.0, free_margin=90.0, exposure_long=0.0, exposure_short=0.0, net_exposure=0.0, number_open_positions=0, number_closed_trades=0)
        ]
        
        self.mc_result = MonteCarloResult(
            number_of_runs=100,
            statistics_per_run=[],
            net_profit_distribution=[10.0, 15.0, 10.0, -5.0, 20.0, 10.0, 15.0],
            drawdown_distribution=[],
            profit_factor_distribution=[],
            expectancy_distribution=[],
            win_rate_distribution=[],
            recovery_factor_distribution=[],
            aggregates={},
            prob_net_profit_positive=0.9,
            prob_drawdown_gt_threshold=0.1,
            prob_profit_factor_gt_one=0.8,
            prob_recovery_factor_gt_threshold=0.5
        )

    def test_equity_curve_svg(self):
        result = self.engine.visualize_equity_curve(self.snapshots, self.config_svg)
        
        self.assertEqual(result.format, "svg")
        self.assertEqual(result.definition.title, "Equity Curve")
        self.assertEqual(result.definition.chart_type, "line")
        
        svg_str = result.data.decode('utf-8')
        self.assertTrue(svg_str.startswith("<svg"))
        self.assertTrue("</svg>" in svg_str)
        self.assertTrue("Equity Curve" in svg_str)

    def test_drawdown_curve_html(self):
        result = self.engine.visualize_drawdown_curve(self.snapshots, self.config_html)
        
        self.assertEqual(result.format, "html")
        html_str = result.data.decode('utf-8')
        self.assertTrue(html_str.startswith("<div><svg"))
        self.assertTrue("</svg></div>" in html_str)
        self.assertTrue("Drawdown Curve" in html_str)

    def test_monte_carlo_histogram(self):
        result = self.engine.visualize_monte_carlo_distribution(self.mc_result, self.config_svg)
        
        self.assertEqual(result.definition.chart_type, "histogram")
        svg_str = result.data.decode('utf-8')
        self.assertTrue("<rect" in svg_str)
        
    def test_empty_snapshots(self):
        result = self.engine.visualize_equity_curve([], self.config_svg)
        self.assertEqual(result.definition.chart_type, "empty")
        svg_str = result.data.decode('utf-8')
        self.assertTrue("No data" in svg_str)

    def test_empty_monte_carlo(self):
        empty_mc = MonteCarloResult(
            number_of_runs=0,
            statistics_per_run=[],
            net_profit_distribution=[],
            drawdown_distribution=[],
            profit_factor_distribution=[],
            expectancy_distribution=[],
            win_rate_distribution=[],
            recovery_factor_distribution=[],
            aggregates={},
            prob_net_profit_positive=0.0,
            prob_drawdown_gt_threshold=0.0,
            prob_profit_factor_gt_one=0.0,
            prob_recovery_factor_gt_threshold=0.0
        )
        result = self.engine.visualize_monte_carlo_distribution(empty_mc, self.config_svg)
        self.assertEqual(result.definition.chart_type, "empty")
        
    def test_determinism(self):
        r1 = self.engine.visualize_equity_curve(self.snapshots, self.config_svg)
        r2 = self.engine.visualize_equity_curve(self.snapshots, self.config_svg)
        
        self.assertEqual(r1.data, r2.data)

if __name__ == '__main__':
    unittest.main()
