import unittest
import random
from typing import List, Dict, Any
from simulation.optimization import (
    OptimizationEngine, OptimizationConfig, OptimizationResult,
    IntegerParameter, FloatParameter, BooleanParameter, CategoricalParameter
)
from simulation.statistics import StatisticsSummary
from simulation.position import Trade
from simulation.portfolio import PortfolioSnapshot

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

class TestOptimizationEngine(unittest.TestCase):
    def setUp(self):
        # We define a dummy evaluator that simply calculates a net profit based on parameters
        # to prove the engine correctly ranks and evaluates them.
        self.call_count = 0
        def dummy_evaluator(params: Dict[str, Any]) -> StatisticsSummary:
            self.call_count += 1
            # A dummy formula for net profit based on parameters
            # Let's say we want to maximize: (param_int * param_float) + (10 if param_bool else 0)
            val_int = params.get("param_int", 0)
            val_float = params.get("param_float", 1.0)
            val_bool = params.get("param_bool", False)
            val_cat = params.get("param_cat", "A")
            
            base_profit = (val_int * val_float) + (10.0 if val_bool else 0.0)
            if val_cat == "B":
                base_profit *= 2
                
            # Drawdown could be inversely related
            max_dd = 0.1 * val_int
            
            return create_mock_stats(net_profit=base_profit, max_dd=max_dd)
            
        self.evaluator = dummy_evaluator

    def test_parameter_spaces_types(self):
        rng = random.Random(42)
        
        int_param = IntegerParameter(1, 5, 2)
        self.assertEqual(int_param.generate_grid(), [1, 3, 5])
        self.assertIn(int_param.generate_random(rng), [1, 3, 5])
        
        float_param = FloatParameter(0.0, 1.0, 0.5)
        self.assertEqual(float_param.generate_grid(), [0.0, 0.5, 1.0])
        self.assertIn(float_param.generate_random(rng), [0.0, 0.5, 1.0])
        
        bool_param = BooleanParameter()
        self.assertEqual(bool_param.generate_grid(), [True, False])
        self.assertIn(bool_param.generate_random(rng), [True, False])
        
        cat_param = CategoricalParameter(["A", "B", "C"])
        self.assertEqual(cat_param.generate_grid(), ["A", "B", "C"])
        self.assertIn(cat_param.generate_random(rng), ["A", "B", "C"])

    def test_grid_search_maximize(self):
        space = {
            "param_int": IntegerParameter(1, 2), # 2
            "param_float": FloatParameter(1.0, 2.0, 1.0), # 2 (1.0, 2.0)
            "param_bool": BooleanParameter(), # 2
            "param_cat": CategoricalParameter(["A", "B"]) # 2
        }
        
        # Total combinations: 2 * 2 * 2 * 2 = 16
        config = OptimizationConfig(
            optimization_method="grid",
            parameter_space=space,
            objective_metric="net_profit",
            maximize=True
        )
        
        engine = OptimizationEngine(config, self.evaluator)
        result = engine.run()
        
        self.assertEqual(result.number_of_evaluations, 16)
        self.assertEqual(self.call_count, 16)
        self.assertEqual(len(result.ranking), 16)
        
        # Maximize Net Profit:
        # Best params should be: int=2, float=2.0, bool=True, cat=B
        # Profit = ((2 * 2.0) + 10.0) * 2 = 28.0
        self.assertEqual(result.best_objective_value if hasattr(result, 'best_objective_value') else result.objective_value, 28.0)
        self.assertEqual(result.best_parameters["param_int"], 2)
        self.assertEqual(result.best_parameters["param_float"], 2.0)
        self.assertEqual(result.best_parameters["param_bool"], True)
        self.assertEqual(result.best_parameters["param_cat"], "B")

    def test_grid_search_minimize(self):
        space = {
            "param_int": IntegerParameter(1, 2)
        }
        
        # Total combinations: 2
        config = OptimizationConfig(
            optimization_method="grid",
            parameter_space=space,
            objective_metric="maximum_drawdown",
            maximize=False  # Minimize drawdown
        )
        
        engine = OptimizationEngine(config, self.evaluator)
        result = engine.run()
        
        self.assertEqual(result.number_of_evaluations, 2)
        
        # Minimize Max Drawdown (which is 0.1 * param_int)
        # Should pick param_int = 1
        self.assertEqual(result.best_parameters["param_int"], 1)
        self.assertEqual(result.objective_value, 0.1)

    def test_random_search(self):
        space = {
            "param_int": IntegerParameter(1, 100),
            "param_float": FloatParameter(0.0, 10.0, 0.1)
        }
        
        config = OptimizationConfig(
            optimization_method="random",
            parameter_space=space,
            objective_metric="net_profit",
            maximize=True,
            random_seed=42,
            max_iterations=10
        )
        
        engine = OptimizationEngine(config, self.evaluator)
        result = engine.run()
        
        self.assertEqual(result.number_of_evaluations, 10)
        self.assertEqual(len(result.ranking), 10)
        
        # Test determinism
        self.call_count = 0
        engine2 = OptimizationEngine(config, self.evaluator)
        result2 = engine2.run()
        
        self.assertEqual(result.best_parameters, result2.best_parameters)
        self.assertEqual(result.objective_value, result2.objective_value)

    def test_top_n_retrieval(self):
        space = {
            "param_int": IntegerParameter(1, 10) # 10 options
        }
        config = OptimizationConfig(
            optimization_method="grid",
            parameter_space=space,
            objective_metric="net_profit",
            maximize=True
        )
        
        engine = OptimizationEngine(config, self.evaluator)
        result = engine.run()
        
        top_3 = result.get_top_n(3)
        self.assertEqual(len(top_3), 3)
        
        # Best should be 10, then 9, then 8
        self.assertEqual(top_3[0].parameters["param_int"], 10)
        self.assertEqual(top_3[1].parameters["param_int"], 9)
        self.assertEqual(top_3[2].parameters["param_int"], 8)
        
    def test_custom_metric_callback(self):
        space = {
            "param_int": IntegerParameter(1, 2) # max_dd is 0.1 * param_int
        }
        
        def custom_metric(stats: StatisticsSummary) -> float:
            return stats.maximum_drawdown * 100.0 # Return as percentage
            
        config = OptimizationConfig(
            optimization_method="grid",
            parameter_space=space,
            objective_metric=custom_metric,
            maximize=True # We maximize max drawdown (weird but valid for testing)
        )
        
        engine = OptimizationEngine(config, self.evaluator)
        result = engine.run()
        
        self.assertEqual(result.best_parameters["param_int"], 2)
        self.assertEqual(result.objective_value, 20.0) # 0.1 * 2 * 100


if __name__ == '__main__':
    unittest.main()
