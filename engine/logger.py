import logging
from enum import Enum
import os

class LogEventType(Enum):
    MARKET = 'MARKET'
    DECISION = 'DECISION'
    REJECTION = 'REJECTION'
    EXECUTION = 'EXECUTION'
    EXIT = 'EXIT'
    ERROR = 'ERROR'

class EngineLogger:
    def __init__(self, log_dir: str = 'logs', log_level=logging.INFO):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        self.logger = logging.getLogger('ApexEngine')
        self.logger.setLevel(log_level)
        self.logger.propagate = False
        
        # Prevent adding handlers multiple times in tests
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            
            fh = logging.FileHandler(os.path.join(log_dir, 'engine.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def log_event(self, event_type: LogEventType, message: str):
        full_message = f"[{event_type.value}] {message}"
        if event_type == LogEventType.ERROR:
            self.logger.error(full_message)
        else:
            self.logger.info(full_message)
