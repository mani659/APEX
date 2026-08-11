import unittest
from unittest.mock import MagicMock
from simulation.api import APEXFramework
from simulation.runner import SimulationRunner
from simulation.walkforward import WalkForwardEngine
import simulation

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        self.framework = APEXFramework()

    def test_framework_factories(self):
        # We only verify that the factory properties instantiate and return the correct engine instances
        # passing mocks for their required arguments to avoid triggering inner validation.
        runner = self.framework.runner(
            strategy=MagicMock(),
            oms=MagicMock(),
            execution=MagicMock(),
            position=MagicMock(),
            portfolio=MagicMock()
        )
        self.assertIsInstance(runner, SimulationRunner)
        
        wf = self.framework.walkforward(
            strategy_factory=MagicMock(),
            config=MagicMock()
        )
        self.assertIsInstance(wf, WalkForwardEngine)
        
    def test_public_exports(self):
        # Check that __init__ exports what we expect based on __all__ in api.py
        self.assertTrue(hasattr(simulation, "APEXFramework"))
        self.assertTrue(hasattr(simulation, "SimulationRunner"))
        self.assertTrue(hasattr(simulation, "__version__"))
        self.assertTrue(hasattr(simulation, "load_json"))

if __name__ == '__main__':
    unittest.main()
