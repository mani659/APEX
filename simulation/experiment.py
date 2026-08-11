import uuid
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Dict, Any, List, Optional, Tuple, Union

from simulation.statistics import StatisticsSummary

class ResearchComponent(Enum):
    SIMULATION = "Simulation"
    WALK_FORWARD = "WalkForward"
    MONTE_CARLO = "MonteCarlo"
    OPTIMIZATION = "Optimization"

@dataclass(frozen=True)
class ExperimentConfig:
    experiment_name: str
    description: str
    author: str
    strategy_name: str
    strategy_version: str
    random_seed: int
    tags: Tuple[str, ...] = field(default_factory=tuple)
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class ExperimentRecord:
    experiment_id: str
    timestamp_started: datetime
    timestamp_finished: datetime
    duration_seconds: float
    configuration_snapshot: ExperimentConfig
    research_component_used: ResearchComponent
    parameters_used: MappingProxyType
    statistics_summary: StatisticsSummary
    notes: str
    metadata: MappingProxyType

@dataclass(frozen=True)
class ExperimentComparison:
    baseline_experiment: ExperimentRecord
    candidate_experiment: ExperimentRecord
    metric_differences: Dict[str, float]
    winner: str # "baseline", "candidate", or "tie"
    metadata: MappingProxyType

class ExperimentManager:
    """
    Research orchestrator that records, stores, and compares experiments.
    It owns no simulation execution logic.
    """
    def __init__(self):
        self._records: Dict[str, ExperimentRecord] = {}

    def record_experiment(
        self,
        config: ExperimentConfig,
        timestamp_started: datetime,
        timestamp_finished: datetime,
        research_component: ResearchComponent,
        parameters_used: Dict[str, Any],
        statistics_summary: StatisticsSummary,
        notes: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> ExperimentRecord:
        
        duration = (timestamp_finished - timestamp_started).total_seconds()
        experiment_id = str(uuid.uuid4())
        
        safe_metadata = metadata or {}
        
        record = ExperimentRecord(
            experiment_id=experiment_id,
            timestamp_started=timestamp_started,
            timestamp_finished=timestamp_finished,
            duration_seconds=duration,
            configuration_snapshot=config,
            research_component_used=research_component,
            parameters_used=MappingProxyType(parameters_used.copy()),
            statistics_summary=statistics_summary,
            notes=notes,
            metadata=MappingProxyType(safe_metadata.copy())
        )
        
        self._records[experiment_id] = record
        return record

    def get_experiment(self, experiment_id: str) -> Optional[ExperimentRecord]:
        return self._records.get(experiment_id)
        
    def filter_experiments(
        self, 
        strategy_version: Optional[str] = None,
        tags: Optional[List[str]] = None,
        date_started: Optional[datetime] = None
    ) -> List[ExperimentRecord]:
        
        results = []
        for record in self._records.values():
            if strategy_version and record.configuration_snapshot.strategy_version != strategy_version:
                continue
                
            if tags:
                if not all(t in record.configuration_snapshot.tags for t in tags):
                    continue
                    
            if date_started:
                # Compare just the date part
                if record.timestamp_started.date() != date_started.date():
                    continue
                    
            results.append(record)
            
        return results

    def _extract_metric(self, stats: StatisticsSummary, metric: str) -> float:
        metric = metric.lower()
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
        else:
            raise ValueError(f"Unsupported metric: {metric}")

    def get_top_n(self, n: int, metric: str, maximize: bool = True) -> List[ExperimentRecord]:
        records_list = list(self._records.values())
        
        def sort_key(r: ExperimentRecord):
            return self._extract_metric(r.statistics_summary, metric)
            
        records_list.sort(key=sort_key, reverse=maximize)
        return records_list[:n]

    def compare_experiments(
        self, 
        baseline_id: str, 
        candidate_id: str, 
        primary_metric: str,
        maximize: bool = True
    ) -> ExperimentComparison:
        
        baseline = self.get_experiment(baseline_id)
        candidate = self.get_experiment(candidate_id)
        
        if not baseline or not candidate:
            raise ValueError("One or both experiment IDs not found.")
            
        metrics = ["net_profit", "profit_factor", "expectancy", "recovery_factor", "maximum_drawdown", "win_rate"]
        
        metric_differences = {}
        for m in metrics:
            base_val = self._extract_metric(baseline.statistics_summary, m)
            cand_val = self._extract_metric(candidate.statistics_summary, m)
            metric_differences[m] = cand_val - base_val
            
        base_primary = self._extract_metric(baseline.statistics_summary, primary_metric)
        cand_primary = self._extract_metric(candidate.statistics_summary, primary_metric)
        
        if cand_primary > base_primary:
            winner = "candidate" if maximize else "baseline"
        elif cand_primary < base_primary:
            winner = "baseline" if maximize else "candidate"
        else:
            winner = "tie"
            
        return ExperimentComparison(
            baseline_experiment=baseline,
            candidate_experiment=candidate,
            metric_differences=metric_differences,
            winner=winner,
            metadata=MappingProxyType({})
        )
