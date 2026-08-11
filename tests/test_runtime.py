import unittest
import sys
import os
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runtime import ApexRuntime
from engine.logger import EngineLogger

class TestApexRuntime(unittest.TestCase):
    def test_full_cycle(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            logger = EngineLogger(log_dir=tmpdirname)
            runtime = ApexRuntime(logger=logger)
            
            for _ in range(14):
                runtime.on_bar(100, 101, 99, 100, 100)
            
            runtime.on_bar(100, 100, 90, 90, 10) 
            
            runtime.on_bar(90.0, 90.1, 89.9, 90.1, 5) # Executed!
            
            self.assertEqual(len(runtime.active_positions), 1)
            self.assertEqual(runtime.active_positions[0].entry_price, 90.1)
            
            # Since the flawed logic resulted in a SELL, price going down hits TP.
            runtime.on_bar(90.1, 90.1, 80, 80, 50) # Should hit TP
            
            self.assertEqual(len(runtime.active_positions), 0)
            
            # Cleanup handlers
            for h in logger.logger.handlers[:]:
                h.close()
                logger.logger.removeHandler(h)

if __name__ == '__main__':
    unittest.main()
