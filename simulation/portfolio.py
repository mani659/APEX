import types
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from simulation.position import Trade

@dataclass(frozen=True)
class PortfolioSnapshot:
    """Immutable historical record of the portfolio state at a specific time."""
    timestamp: int
    balance: float
    equity: float
    realized_pnl: float
    floating_pnl: float
    gross_profit: float
    gross_loss: float
    drawdown: float
    max_drawdown: float
    margin_used: float
    free_margin: float
    exposure_long: float
    exposure_short: float
    net_exposure: float
    number_open_positions: int
    number_closed_trades: int
    metadata: Optional[types.MappingProxyType] = None

class PortfolioEngine:
    """
    Maintains account state, processes closed Trades for realized PnL,
    accepts floating updates, and generates immutable PortfolioSnapshots.
    """
    def __init__(self, initial_balance: float = 100000.0):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.realized_pnl = 0.0
        self.gross_profit = 0.0
        self.gross_loss = 0.0
        
        self.floating_pnl = 0.0
        self.margin_used = 0.0
        self.exposure_long = 0.0
        self.exposure_short = 0.0
        self.net_exposure = 0.0
        self.number_open_positions = 0
        
        self.peak_equity = initial_balance
        self.max_drawdown = 0.0
        
        self.number_closed_trades = 0

    @property
    def equity(self) -> float:
        return self.balance + self.floating_pnl

    @property
    def free_margin(self) -> float:
        return self.equity - self.margin_used

    @property
    def current_drawdown(self) -> float:
        if self.peak_equity > 0:
            return (self.peak_equity - self.equity) / self.peak_equity
        return 0.0

    def process_trade(self, trade: Trade):
        """Processes an immutable Trade to update realized balance and PnL."""
        self.number_closed_trades += 1
        
        net_pnl = trade.net_pnl
        self.realized_pnl += net_pnl
        self.balance += net_pnl
        
        if net_pnl > 0:
            self.gross_profit += net_pnl
        elif net_pnl < 0:
            self.gross_loss += abs(net_pnl)
            
        # Temporal Leakage Fix: High-water marks are NO LONGER updated here.
        # They are deferred to commit_accounting_cycle().

    def update_floating_state(self, 
                              floating_pnl: float, 
                              margin_used: float, 
                              exposure_long: float, 
                              exposure_short: float, 
                              number_open_positions: int):
        """
        Receives summarized floating values from active positions.
        The Simulation Runner calculates these and injects them here, 
        maintaining architectural separation so the PortfolioEngine doesn't own Positions.
        """
        self.floating_pnl = floating_pnl
        self.margin_used = margin_used
        self.exposure_long = exposure_long
        self.exposure_short = exposure_short
        self.net_exposure = exposure_long - exposure_short
        self.number_open_positions = number_open_positions
        
        # Temporal Leakage Fix: High-water marks are NO LONGER updated here.
        # They are deferred to commit_accounting_cycle().

    def commit_accounting_cycle(self, timestamp: int, metadata: Optional[Dict[str, Any]] = None) -> PortfolioSnapshot:
        """
        Executes the transactional accounting commit phase.
        Updates high-water marks and generates the immutable snapshot for the current tick.
        """
        current_eq = self.equity
        if current_eq > self.peak_equity:
            self.peak_equity = current_eq
            
        dd = self.current_drawdown
        if dd > self.max_drawdown:
            self.max_drawdown = dd
            
        # Ensure deep immutability of metadata
        frozen_metadata = types.MappingProxyType(metadata.copy()) if metadata else None
        
        return PortfolioSnapshot(
            timestamp=timestamp,
            balance=self.balance,
            equity=current_eq,
            realized_pnl=self.realized_pnl,
            floating_pnl=self.floating_pnl,
            gross_profit=self.gross_profit,
            gross_loss=self.gross_loss,
            drawdown=dd,
            max_drawdown=self.max_drawdown,
            margin_used=self.margin_used,
            free_margin=self.free_margin,
            exposure_long=self.exposure_long,
            exposure_short=self.exposure_short,
            net_exposure=self.net_exposure,
            number_open_positions=self.number_open_positions,
            number_closed_trades=self.number_closed_trades,
            metadata=frozen_metadata
        )
