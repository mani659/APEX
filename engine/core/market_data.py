from dataclasses import dataclass
from collections import deque
import numpy as np
from typing import List

@dataclass(frozen=True)
class MarketSnapshot:
    current_price: float
    current_atr: float
    closes: List[float]
    opens: List[float]
    volumes: List[float]
    is_new_bar: bool

class MarketDataLayer:
    def __init__(self, atr_period: int = 14):
        self.atr_period = atr_period
        self.closes = deque(maxlen=atr_period + 1)
        self.opens = deque(maxlen=atr_period + 1)
        self.highs = deque(maxlen=atr_period + 1)
        self.lows = deque(maxlen=atr_period + 1)
        self.volumes = deque(maxlen=atr_period + 1)
        self.current_price = 0.0
        self.current_atr = 0.0
        self.is_new_bar = False

    def update_tick(self, price: float) -> MarketSnapshot:
        self.current_price = price
        self.is_new_bar = False
        return self._build_snapshot()

    def update_bar(self, open_price: float, high: float, low: float, close: float, volume: float) -> MarketSnapshot:
        self.opens.append(open_price)
        self.highs.append(high)
        self.lows.append(low)
        self.closes.append(close)
        self.volumes.append(volume)
        self.current_price = close
        self.is_new_bar = True
        self._calculate_atr()
        return self._build_snapshot()

    def _calculate_atr(self):
        if len(self.closes) < 2:
            self.current_atr = 0.0
            return
        
        trs = []
        for i in range(1, len(self.closes)):
            h = self.highs[i]
            l = self.lows[i]
            prev_c = self.closes[i-1]
            tr = max(h - l, abs(h - prev_c), abs(l - prev_c))
            trs.append(tr)
            
        if len(trs) > 0:
            self.current_atr = float(np.mean(trs[-self.atr_period:]))

    def _build_snapshot(self) -> MarketSnapshot:
        return MarketSnapshot(
            current_price=self.current_price,
            current_atr=self.current_atr,
            closes=list(self.closes),
            opens=list(self.opens),
            volumes=list(self.volumes),
            is_new_bar=self.is_new_bar
        )
