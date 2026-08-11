import unittest
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

from simulation.experiment import (
    ExperimentManager, ExperimentConfig, ResearchComponent
)
from simulation.statistics import StatisticsSummary

def create_mock_stats(net_profit: float, max_dd: float) -> StatisticsSummary:
    return StatisticsSummary(
        total_trades=10,
        winning_trades=5,
        losing_trades=5,
        win_rate=0.5,
        loss_rate=0.5,
        gross_profit=100.0,
        gross_loss=50.0,
        net_profit=net_profit,
        profit_factor=2.0,
        average_trade=10.0,
        average_win=20.0,
        average_loss=10.0,
        largest_win=20.0,
        largest_loss=10.0,
        expectancy=5.0,
        average_holding_period=2.0,
        maximum_drawdown=max_dd,
        recovery_factor=net_profit / max_dd if max_dd > 0 else net_profit,
        number_of_long_trades=5,
        number_of_short_trades=5,
        metadata=None
    )

class TestExperimentManager(unittest.TestCase):
    def setUp(self):
        self.manager = ExperimentManager()
        
        self.config1 = ExperimentConfig(
            experiment_name="Exp1",
            description="Test Exp 1",
            author="Tester",
            strategy_name="Grid",
            strategy_version="v1.0",
            random_seed=42,
            tags=("test", "baseline")
        )
        
        self.config2 = ExperimentConfig(
            experiment_name="Exp2",
            description="Test Exp 2",
            author="Tester",
            strategy_name="Grid",
            strategy_version="v1.1",
            random_seed=42,
            tags=("test", "candidate")
        )

    def test_record_experiment(self):
        now = datetime.now(timezone.utc)
        finish = now + timedelta(minutes=5)
        
        record = self.manager.record_experiment(
            config=self.config1,
            timestamp_started=now,
            timestamp_finished=finish,
            research_component=ResearchComponent.SIMULATION,
            parameters_used={"param1": 10},
            statistics_summary=create_mock_stats(net_profit=100.0, max_dd=10.0),
            notes="Initial run"
        )
        
        self.assertIsNotNone(record.experiment_id)
        self.assertEqual(record.duration_seconds, 300.0)
        self.assertEqual(record.research_component_used, ResearchComponent.SIMULATION)
        self.assertEqual(record.parameters_used["param1"], 10)
        
        # Test immutability via MappingProxyType
        with self.assertRaises(TypeError):
            record.parameters_used["param1"] = 20

    def test_filter_experiments(self):
        now = datetime.now(timezone.utc)
        
        self.manager.record_experiment(
            config=self.config1,
            timestamp_started=now,
            timestamp_finished=now,
            research_component=ResearchComponent.SIMULATION,
            parameters_used={},
            statistics_summary=create_mock_stats(100.0, 10.0)
        )
        
        self.manager.record_experiment(
            config=self.config2,
            timestamp_started=now,
            timestamp_finished=now,
            research_component=ResearchComponent.OPTIMIZATION,
            parameters_used={},
            statistics_summary=create_mock_stats(200.0, 20.0)
        )
        
        v1_records = self.manager.filter_experiments(strategy_version="v1.0")
        self.assertEqual(len(v1_records), 1)
        self.assertEqual(v1_records[0].configuration_snapshot.strategy_version, "v1.0")
        
        tag_records = self.manager.filter_experiments(tags=["test"])
        self.assertEqual(len(tag_records), 2)
        
        cand_records = self.manager.filter_experiments(tags=["test", "candidate"])
        self.assertEqual(len(cand_records), 1)

    def test_get_top_n(self):
        now = datetime.now(timezone.utc)
        
        self.manager.record_experiment(
            config=self.config1,
            timestamp_started=now,
            timestamp_finished=now,
            research_component=ResearchComponent.SIMULATION,
            parameters_used={},
            statistics_summary=create_mock_stats(100.0, 10.0)
        )
        
        self.manager.record_experiment(
            config=self.config2,
            timestamp_started=now,
            timestamp_finished=now,
            research_component=ResearchComponent.OPTIMIZATION,
            parameters_used={},
            statistics_summary=create_mock_stats(200.0, 20.0)
        )
        
        # Maximize net profit
        top_profit = self.manager.get_top_n(n=2, metric="net_profit", maximize=True)
        self.assertEqual(top_profit[0].statistics_summary.net_profit, 200.0)
        self.assertEqual(top_profit[1].statistics_summary.net_profit, 100.0)
        
        # Minimize max drawdown
        top_dd = self.manager.get_top_n(n=2, metric="maximum_drawdown", maximize=False)
        self.assertEqual(top_dd[0].statistics_summary.maximum_drawdown, 10.0)
        self.assertEqual(top_dd[1].statistics_summary.maximum_drawdown, 20.0)

    def test_compare_experiments(self):
        now = datetime.now(timezone.utc)
        
        rec1 = self.manager.record_experiment(
            config=self.config1,
            timestamp_started=now,
            timestamp_finished=now,
            research_component=ResearchComponent.SIMULATION,
            parameters_used={},
            statistics_summary=create_mock_stats(100.0, 10.0)
        )
        
        rec2 = self.manager.record_experiment(
            config=self.config2,
            timestamp_started=now,
            timestamp_finished=now,
            research_component=ResearchComponent.OPTIMIZATION,
            parameters_used={},
            statistics_summary=create_mock_stats(200.0, 20.0)
        )
        
        comp = self.manager.compare_experiments(
            baseline_id=rec1.experiment_id,
            candidate_id=rec2.experiment_id,
            primary_metric="net_profit",
            maximize=True
        )
        
        self.assertEqual(comp.winner, "candidate")
        self.assertEqual(comp.metric_differences["net_profit"], 100.0) # 200 - 100
        self.assertEqual(comp.metric_differences["maximum_drawdown"], 10.0) # 20 - 10
        
        comp_dd = self.manager.compare_experiments(
            baseline_id=rec1.experiment_id,
            candidate_id=rec2.experiment_id,
            primary_metric="maximum_drawdown",
            maximize=False
        )
        
        self.assertEqual(comp_dd.winner, "baseline") # baseline has 10.0, candidate has 20.0


if __name__ == '__main__':
    unittest.main()
