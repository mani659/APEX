from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class TradingContext:
    """
    Unified shared runtime state object exchanged between the Strategy layer 
    and the Simulation layer. Strictly read-only for Strategy.
    """
    # Clock
    timestamp: int
    bar_index: int
    session: str
    day_of_week: int
    market_open: bool

    # Market
    current_price: float
    spread: float
    volatility_regime: str
    trend_regime: str
    market_structure: str
    atr: float

    # Portfolio
    equity: float
    balance: float
    floating_pnl: float
    closed_pnl: float
    drawdown: float
    daily_pnl: float
    max_drawdown: float

    # Exposure
    open_positions: int
    long_positions: int
    short_positions: int
    net_exposure: float
    margin_used: float
    available_margin: float

    # Risk
    daily_loss_limit_hit: bool
    risk_enabled: bool
    max_positions_reached: bool
    trading_paused: bool

    # Execution
    last_fill_price: float
    last_slippage: float
    last_commission: float
    last_trade_time: int
