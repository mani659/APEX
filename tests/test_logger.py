import unittest
import sys
import os
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.logger import EngineLogger, LogEventType

class TestEngineLogger(unittest.TestCase):
    def test_logging(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            logger_instance = EngineLogger(log_dir=tmpdirname)
            
            logger_instance.log_event(LogEventType.REJECTION, "High Entropy")
            logger_instance.log_event(LogEventType.EXECUTION, "Bought 0.1 XAUUSD")
            
            log_file = os.path.join(tmpdirname, 'engine.log')
            self.assertTrue(os.path.exists(log_file))
            
            # Close handlers so Windows can delete the file
            for handler in logger_instance.logger.handlers[:]:
                handler.close()
                logger_instance.logger.removeHandler(handler)
            
            with open(log_file, 'r') as f:
                logs = f.read()
                self.assertIn("[REJECTION] High Entropy", logs)
                self.assertIn("[EXECUTION] Bought 0.1 XAUUSD", logs)

if __name__ == '__main__':
    unittest.main()
