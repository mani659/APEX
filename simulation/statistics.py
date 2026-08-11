import types
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from simulation.position import Trade, OrderDirection
from simulation.portfolio import PortfolioSnapshot

@dataclass(frozen=True)
class StatisticsSummary:
    """Immutable record of computed statistics."""
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    loss_rate: float
    gross_profit: float
    gross_loss: float
    net_profit: float
    profit_factor: float
    average_trade: float
    average_win: float
    average_loss: float
    largest_win: float
    largest_loss: float
    expectancy: float
    average_holding_period: float
    maximum_drawdown: float
    recovery_factor: float
    number_of_long_trades: int
    number_of_short_trades: int
    metadata: Optional[types.MappingProxyType] = None

class StatisticsEngine:
    """
    Pure analytics consumer.
    Computes deterministic statistics from immutable Trades and PortfolioSnapshots.
    Does NOT mutate any simulation state.
    """

    @staticmethod
    def calculate(trades: List[Trade], snapshots: List[PortfolioSnapshot], metadata: Optional[Dict[str, Any]] = None) -> StatisticsSummary:
        total_trades = len(trades)
        
        if total_trades == 0:
            return StatisticsEngine._create_empty_summary(snapshots, metadata)

        winning_trades = 0
        losing_trades = 0
        gross_profit = 0.0
        gross_loss = 0.0
        largest_win = 0.0
        largest_loss = 0.0
        total_holding_bars = 0
        number_of_long_trades = 0
        number_of_short_trades = 0

        for trade in trades:
            if trade.direction == OrderDirection.LONG:
                number_of_long_trades += 1
            else:
                number_of_short_trades += 1
                
            total_holding_bars += trade.bars_held
            pnl = trade.net_pnl
            
            if pnl > 0:
                winning_trades += 1
                gross_profit += pnl
                if pnl > largest_win:
                    largest_win = pnl
            elif pnl < 0:
                losing_trades += 1
                gross_loss += abs(pnl)
                if pnl < largest_loss:
                    largest_loss = pnl
            else:
                # Breakeven trades
                pass

        net_profit = gross_profit - gross_loss
        win_rate = winning_trades / total_trades if total_trades > 0 else 0.0
        loss_rate = losing_trades / total_trades if total_trades > 0 else 0.0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        
        average_trade = net_profit / total_trades
        average_win = (gross_profit / winning_trades) if winning_trades > 0 else 0.0
        average_loss = (-gross_loss / losing_trades) if losing_trades > 0 else 0.0
        
        expectancy = (win_rate * average_win) + (loss_rate * average_loss)
        average_holding_period = total_holding_bars / total_trades
        
        # Max drawdown extraction from snapshots
        max_drawdown = 0.0
        if snapshots:
            max_drawdown = max(snap.max_drawdown for snap in snapshots)
            
        recovery_factor = (net_profit / max_drawdown) if max_drawdown > 0 else net_profit

        frozen_metadata = types.MappingProxyType(metadata.copy()) if metadata else None

        return StatisticsSummary(
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            loss_rate=loss_rate,
            gross_profit=gross_profit,
            gross_loss=gross_loss,
            net_profit=net_profit,
            profit_factor=profit_factor,
            average_trade=average_trade,
            average_win=average_win,
            average_loss=average_loss,
            largest_win=largest_win,
            largest_loss=largest_loss,
            expectancy=expectancy,
            average_holding_period=average_holding_period,
            maximum_drawdown=max_drawdown,
            recovery_factor=recovery_factor,
            number_of_long_trades=number_of_long_trades,
            number_of_short_trades=number_of_short_trades,
            metadata=frozen_metadata
        )

    @staticmethod
    def _create_empty_summary(snapshots: List[PortfolioSnapshot], metadata: Optional[Dict[str, Any]]) -> StatisticsSummary:
        max_drawdown = 0.0
        if snapshots:
            max_drawdown = max(snap.max_drawdown for snap in snapshots)
            
        frozen_metadata = types.MappingProxyType(metadata.copy()) if metadata else None
        
        return StatisticsSummary(
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            loss_rate=0.0,
            gross_profit=0.0,
            gross_loss=0.0,
            net_profit=0.0,
            profit_factor=0.0,
            average_trade=0.0,
            average_win=0.0,
            average_loss=0.0,
            largest_win=0.0,
            largest_loss=0.0,
            expectancy=0.0,
            average_holding_period=0.0,
            maximum_drawdown=max_drawdown,
            recovery_factor=0.0,
            number_of_long_trades=0,
            number_of_short_trades=0,
            metadata=frozen_metadata
        )
