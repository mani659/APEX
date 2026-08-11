from typing import List
from simulation.market import MarketSnapshot
from simulation.context import TradingContext
from simulation.strategy import Strategy
from simulation.order_manager import OrderManager
from simulation.execution import ExecutionEngine
from simulation.position import PositionEngine, OrderDirection
from simulation.portfolio import PortfolioEngine
from simulation.statistics import StatisticsEngine, StatisticsSummary

class SimulationRunner:
    """
    The orchestrator of the entire simulation lifecycle.
    Responsible ONLY for passing data between the engines.
    Never performs financial math, optimization, or strategy logic.
    Deterministic and single-threaded.
    """
    
    def __init__(self, 
                 strategy: Strategy,
                 oms: OrderManager,
                 execution: ExecutionEngine,
                 position: PositionEngine,
                 portfolio: PortfolioEngine):
        self.strategy = strategy
        self.oms = oms
        self.execution = execution
        self.position = position
        self.portfolio = portfolio
        
        self.snapshots = []
        
    def _build_context(self, market_snapshot: MarketSnapshot, bar_index: int) -> TradingContext:
        """
        Assembles the read-only TradingContext for the Strategy.
        """
        long_pos, short_pos = self.position.get_position_counts()
        
        return TradingContext(
            timestamp=market_snapshot.timestamp,
            bar_index=bar_index,
            session="UNKNOWN",
            day_of_week=0,
            market_open=True,
            
            current_price=market_snapshot.bid,
            spread=market_snapshot.ask - market_snapshot.bid,
            volatility_regime="NORMAL",
            trend_regime="UNKNOWN",
            market_structure="UNKNOWN",
            atr=0.0,
            
            equity=self.portfolio.equity,
            balance=self.portfolio.balance,
            floating_pnl=self.portfolio.floating_pnl,
            closed_pnl=self.portfolio.realized_pnl,
            drawdown=self.portfolio.current_drawdown,
            daily_pnl=0.0,
            max_drawdown=self.portfolio.max_drawdown,
            
            open_positions=self.portfolio.number_open_positions,
            long_positions=long_pos,
            short_positions=short_pos,
            net_exposure=self.portfolio.net_exposure,
            margin_used=self.portfolio.margin_used,
            available_margin=self.portfolio.free_margin,
            
            daily_loss_limit_hit=False,
            risk_enabled=True,
            max_positions_reached=False,
            trading_paused=False,
            
            last_fill_price=0.0,
            last_slippage=0.0,
            last_commission=0.0,
            last_trade_time=0
        )

    def step(self, market_snapshot: MarketSnapshot, bar_index: int = 0):
        """
        Executes a single, deterministic tick of the simulation.
        The sequence is rigidly defined and must never be altered.
        """
        # 1. Build TradingContext
        context = self._build_context(market_snapshot, bar_index)
        
        # 2. Strategy produces Signal(s)
        signals = self.strategy.generate_signals(context)
        
        # 3. OMS receives Signal(s)
        if signals:
            for signal in signals:
                self.oms.receive_signal(signal)
            
        # 4. OMS activates executable orders
        self.oms.expire_orders(market_snapshot.timestamp)
        self.oms.activate_orders(market_snapshot) 
        executable_orders = self.oms.get_executable_orders()
        
        # 5. Execution Engine processes orders
        execution_reports = []
        for order in executable_orders:
            report = self.execution.evaluate_execution(order, market_snapshot)
            execution_reports.append(report)
        
        # 6. OMS receives ExecutionReports
        for report in execution_reports:
            self.oms.update_order_from_execution(report)
            
        # 7. Position Engine processes ExecutionReports
        for report in execution_reports:
            order = self.oms.get_order(report.order_id)
            if order:
                self.position.process_execution_report(
                    report, 
                    stop_loss=order.stop_loss, 
                    take_profit=order.take_profit
                )
            
        # 8. Position Engine evaluates open positions
        closed_trades = self.position.evaluate_positions(market_snapshot)
        
        # 9. Closed Trades / 10. Portfolio Engine processes Trades
        for trade in closed_trades:
            self.portfolio.process_trade(trade)
            
        # 11. Portfolio Engine updates floating state
        f_pnl, m_used, exp_long, exp_short, n_pos = self.position.calculate_floating_state(market_snapshot)
        self.portfolio.update_floating_state(
            floating_pnl=f_pnl,
            margin_used=m_used,
            exposure_long=exp_long,
            exposure_short=exp_short,
            number_open_positions=n_pos
        )
        
        # 12. Portfolio commits accounting cycle / 13. PortfolioSnapshot produced
        snapshot = self.portfolio.commit_accounting_cycle(timestamp=market_snapshot.timestamp)
        self.snapshots.append(snapshot)
        
    def generate_statistics(self) -> StatisticsSummary:
        """
        14. Statistics Engine consumes history.
        Must be called after all simulation steps are complete.
        """
        # Expose historical trades formally via public API later, 
        # but for now Runner just passes them deterministically.
        return StatisticsEngine.calculate(self.position._trades, self.snapshots)
