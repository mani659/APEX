from typing import Any

from simulation.runner import SimulationRunner
from simulation.walkforward import WalkForwardEngine
from simulation.montecarlo import MonteCarloEngine
from simulation.optimization import OptimizationEngine
from simulation.experiment import ExperimentManager as ExperimentTracker
from simulation.reporting import ReportGenerator
from simulation.visualization import VisualizationEngine
from simulation.data_exporter import DataExporter
from simulation.version import __version__, get_framework_info

__all__ = [
    "APEXFramework",
    "SimulationRunner",
    "WalkForwardEngine",
    "MonteCarloEngine",
    "OptimizationEngine",
    "ExperimentTracker",
    "ReportGenerator",
    "VisualizationEngine",
    "DataExporter",
    "__version__",
]

class APEXFramework:
    """
    Primary entry point for the APEX framework.
    Provides factory methods to instantiate internal engines without exposing their mechanics.
    Performs NO calculations.
    """
    
    def runner(self, *args, **kwargs) -> SimulationRunner:
        return SimulationRunner(*args, **kwargs)
        
    def walkforward(self, *args, **kwargs) -> WalkForwardEngine:
        return WalkForwardEngine(*args, **kwargs)
        
    def montecarlo(self, *args, **kwargs) -> MonteCarloEngine:
        return MonteCarloEngine(*args, **kwargs)
        
    def optimization(self, *args, **kwargs) -> OptimizationEngine:
        return OptimizationEngine(*args, **kwargs)
        
    def experiment(self, *args, **kwargs) -> ExperimentTracker:
        return ExperimentTracker(*args, **kwargs)
        
    def report(self, *args, **kwargs) -> ReportGenerator:
        return ReportGenerator(*args, **kwargs)
        
    def visualization(self, *args, **kwargs) -> VisualizationEngine:
        return VisualizationEngine(*args, **kwargs)
        
    def exporter(self, *args, **kwargs) -> DataExporter:
        return DataExporter(*args, **kwargs)
