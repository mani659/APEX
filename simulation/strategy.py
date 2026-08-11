from abc import ABC, abstractmethod
from typing import List
from simulation.context import TradingContext
from simulation.order import Signal

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, context: TradingContext) -> List[Signal]:
        """
        Consumes the read-only TradingContext and outputs optional Trading Signals.
        """
        pass
