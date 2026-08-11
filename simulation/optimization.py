import itertools
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional, Union

from simulation.statistics import StatisticsSummary

class ParameterDef(ABC):
    @abstractmethod
    def generate_grid(self) -> List[Any]:
        pass
        
    @abstractmethod
    def generate_random(self, rng: random.Random) -> Any:
        pass

@dataclass(frozen=True)
class IntegerParameter(ParameterDef):
    min_val: int
    max_val: int
    step: int = 1
    
    def generate_grid(self) -> List[Any]:
        return list(range(self.min_val, self.max_val + 1, self.step))
        
    def generate_random(self, rng: random.Random) -> Any:
        # random.randrange is exclusive of the upper bound, so we adjust
        return rng.randrange(self.min_val, self.max_val + 1, self.step)

@dataclass(frozen=True)
class FloatParameter(ParameterDef):
    min_val: float
    max_val: float
    step: float
    
    def generate_grid(self) -> List[Any]:
        # Avoid floating point accumulation errors
        grid = []
        current = self.min_val
        while current <= self.max_val + 1e-9: # tiny epsilon for float precision
            grid.append(current)
            current += self.step
        return grid
        
    def generate_random(self, rng: random.Random) -> Any:
        # Uniform sampling is standard for floats, though step could be enforced.
        # Enforcing step for random float:
        steps = int((self.max_val - self.min_val) / self.step)
        if steps <= 0:
            return self.min_val
        return self.min_val + rng.randint(0, steps) * self.step

@dataclass(frozen=True)
class BooleanParameter(ParameterDef):
    def generate_grid(self) -> List[Any]:
        return [True, False]
        
    def generate_random(self, rng: random.Random) -> Any:
        return rng.choice([True, False])

@dataclass(frozen=True)
class CategoricalParameter(ParameterDef):
    options: List[Any]
    
    def generate_grid(self) -> List[Any]:
        return list(self.options)
        
    def generate_random(self, rng: random.Random) -> Any:
        return rng.choice(self.options)

@dataclass(frozen=True)
class OptimizationConfig:
    optimization_method: str = "grid" # "grid", "random"
    parameter_space: Dict[str, ParameterDef] = field(default_factory=dict)
    objective_metric: Union[str, Callable[[StatisticsSummary], float]] = "net_profit"
    maximize: bool = True
    random_seed: int = 42
    max_iterations: int = 100
    parallel_enabled: bool = False # Placeholder for future

@dataclass(frozen=True)
class OptimizationEvaluation:
    parameters: Dict[str, Any]
    statistics: StatisticsSummary
    objective_value: float
    runtime_seconds: float

@dataclass(frozen=True)
class OptimizationResult:
    best_parameters: Dict[str, Any]
    best_statistics: StatisticsSummary
    objective_value: float
    ranking: List[OptimizationEvaluation]
    number_of_evaluations: int
    runtime_seconds: float
    
    def get_top_n(self, n: int) -> List[OptimizationEvaluation]:
        return self.ranking[:n]

class OptimizationEngine:
    """
    Research orchestrator that evaluates parameter sets by dispatching to a generic 
    evaluator callback. It does not own or modify any simulation logic.
    """
    def __init__(self, 
                 config: OptimizationConfig, 
                 evaluator: Callable[[Dict[str, Any]], StatisticsSummary]):
        self.config = config
        self.evaluator = evaluator
        
    def _extract_objective(self, stats: StatisticsSummary) -> float:
        if isinstance(self.config.objective_metric, str):
            # Known standard metrics
            metric = self.config.objective_metric.lower()
            if metric == "net_profit":
                return stats.net_profit
            elif metric == "profit_factor":
                return stats.profit_factor if stats.profit_factor != float('inf') else 999.0
            elif metric == "expectancy":
                return stats.expectancy
            elif metric == "recovery_factor":
                return stats.recovery_factor
            elif metric == "maximum_drawdown":
                return stats.maximum_drawdown
            elif metric == "win_rate":
                return stats.win_rate
            elif metric == "sharpe":
                # Placeholder for sharpe
                return stats.expectancy # Naive fallback
            else:
                raise ValueError(f"Unknown objective metric: {metric}")
        else:
            # Custom callback
            return self.config.objective_metric(stats)

    def _generate_grid_combinations(self) -> List[Dict[str, Any]]:
        keys = list(self.config.parameter_space.keys())
        if not keys:
            return [{}]
            
        value_lists = [self.config.parameter_space[k].generate_grid() for k in keys]
        combinations = []
        for combo in itertools.product(*value_lists):
            combinations.append(dict(zip(keys, combo)))
            
            # Bound grid search if needed, though usually grid search implies exhaustive
            if len(combinations) >= self.config.max_iterations:
                break
                
        return combinations
        
    def _generate_random_combinations(self) -> List[Dict[str, Any]]:
        keys = list(self.config.parameter_space.keys())
        if not keys:
            return [{}]
            
        rng = random.Random(self.config.random_seed)
        combinations = []
        
        for _ in range(self.config.max_iterations):
            params = {}
            for k in keys:
                params[k] = self.config.parameter_space[k].generate_random(rng)
            combinations.append(params)
            
        return combinations

    def run(self) -> OptimizationResult:
        start_time = time.time()
        
        if self.config.optimization_method == "grid":
            param_sets = self.generate_grid_combinations()
        elif self.config.optimization_method == "random":
            param_sets = self._generate_random_combinations()
        else:
            raise ValueError(f"Unknown optimization method: {self.config.optimization_method}")
            
        evaluations: List[OptimizationEvaluation] = []
        
        for params in param_sets:
            eval_start = time.time()
            
            # The evaluator is responsible for instantiating fresh Strategy, Runner, etc.
            stats = self.evaluator(params)
            
            eval_end = time.time()
            
            obj_val = self._extract_objective(stats)
            
            evaluation = OptimizationEvaluation(
                parameters=params,
                statistics=stats,
                objective_value=obj_val,
                runtime_seconds=eval_end - eval_start
            )
            evaluations.append(evaluation)
            
        # Sort ranking
        evaluations.sort(key=lambda e: e.objective_value, reverse=self.config.maximize)
        
        total_time = time.time() - start_time
        
        if not evaluations:
            # Fallback for empty param space
            return OptimizationResult(
                best_parameters={},
                best_statistics=None,
                objective_value=0.0,
                ranking=[],
                number_of_evaluations=0,
                runtime_seconds=total_time
            )
            
        best_eval = evaluations[0]
        
        return OptimizationResult(
            best_parameters=best_eval.parameters,
            best_statistics=best_eval.statistics,
            objective_value=best_eval.objective_value,
            ranking=evaluations,
            number_of_evaluations=len(evaluations),
            runtime_seconds=total_time
        )
        
    def generate_grid_combinations(self):
        return self._generate_grid_combinations()
