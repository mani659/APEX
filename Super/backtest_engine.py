import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import talib
from datetime import datetime
import os

class BacktestEngine:
    def __init__(self, strategy, initial_balance=10000):
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.trades = []
        self.open_position = None
        
    def prepare_data(self, df):
        """Adds indicators required by the strategy"""
        df = df.copy()
        df['hl2'] = (df['high'] + df['low']) / 2
        df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=10)
        df['volume_ma'] = df['tick_volume'].rolling(window=20).mean()
        df['volatility'] = df['close'].rolling(window=10).std()
        df['norm_volatility'] = df['volatility'] / df['volatility'].rolling(window=50).mean()
        return df.dropna()

    def run_backtest(self, symbol, start_date, end_date, timeframe):
        rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
        if rates is None or len(rates) == 0:
            return f"Error: No data found for {symbol}."
            
        df_raw = pd.DataFrame(rates)
        df_raw['time'] = pd.to_datetime(df_raw['time'], unit='s')
        df = self.prepare_data(df_raw)
        
        balance = self.initial_balance
        equity_curve = []
        
        print(f"Starting backtest for {symbol}...")
        total_candles = len(df)
        print(f"Processing {total_candles} candles. This may take a few minutes...")
        for i in range(200, total_candles):
            # ADD THIS PROGRESS TRACKER:
            if i % 500 == 0:
                print(f"Progress: {i}/{total_candles} candles processed ({(i/total_candles)*100:.1f}%)")
            
            current_tick = df.iloc[i]
            
            # A. Check for SL/TP on open position
            if self.open_position:
                self.update_positions(current_tick)
                if self.open_position['status'] == 'closed':
                    balance += self.open_position['Profit']
                    self.trades.append(self.open_position)
                    self.open_position = None

            # B. Check for new signals
            if not self.open_position:
                current_df = df.iloc[:i+1].copy()
                signal = self.strategy.generate_signal(current_df)
                if signal:
                    self.place_virtual_trade(signal, current_tick, symbol)
            
            unrealized_pnl = 0
            if self.open_position:
                unrealized_pnl = self.calculate_pnl(self.open_position, current_tick, symbol)
            equity_curve.append(balance + unrealized_pnl)
            
        self.save_results_to_csv(symbol)
        return self.generate_backtest_report(equity_curve)

    def place_virtual_trade(self, signal, tick, symbol):
        direction = "Buy" if signal == 1 else "Sell"
        entry_price = tick['close']
        atr = tick['atr']
        
        sl_dist = atr * self.strategy.config.sl_multiplier
        tp_dist = atr * self.strategy.config.tp_multiplier

        # Keys now match the SMC Trade Log format where possible
        self.open_position = {
            'RowType': 'ENTRY',
            'Symbol': symbol,
            'Direction': direction,
            'Time': tick['time'],
            'EntryPrice': entry_price,
            'SL': entry_price - sl_dist if direction == "Buy" else entry_price + sl_dist,
            'TP': entry_price + tp_dist if direction == "Buy" else entry_price - tp_dist,
            'ATR': atr,
            'Volatility': round(tick['norm_volatility'], 4),
            'Volume_MA': round(tick['volume_ma'], 2),
            'status': 'open'
        }

    def update_positions(self, tick):
        pos = self.open_position
        # Gold logic: 100 contract size for XAUUSDm
        contract_size = 100 if "XAU" in pos['Symbol'] else 10000
        
        if pos['Direction'] == "Buy":
            if tick['low'] <= pos['SL']:
                pos.update({'status': 'closed', 'RowType': 'EXIT', 'ExitTime': tick['time'], 'ExitPrice': pos['SL'], 'ExitReason': 'SL_HIT', 
                            'Profit': round((pos['SL'] - pos['EntryPrice']) * contract_size, 2)})
            elif tick['high'] >= pos['TP']:
                pos.update({'status': 'closed', 'RowType': 'EXIT', 'ExitTime': tick['time'], 'ExitPrice': pos['TP'], 'ExitReason': 'TP_HIT', 
                            'Profit': round((pos['TP'] - pos['EntryPrice']) * contract_size, 2)})
        else:
            if tick['high'] >= pos['SL']:
                pos.update({'status': 'closed', 'RowType': 'EXIT', 'ExitTime': tick['time'], 'ExitPrice': pos['SL'], 'ExitReason': 'SL_HIT', 
                            'Profit': round((pos['EntryPrice'] - pos['SL']) * contract_size, 2)})
            elif tick['low'] <= pos['TP']:
                pos.update({'status': 'closed', 'RowType': 'EXIT', 'ExitTime': tick['time'], 'ExitPrice': pos['TP'], 'ExitReason': 'TP_HIT', 
                            'Profit': round((pos['EntryPrice'] - pos['TP']) * contract_size, 2)})

    def calculate_pnl(self, pos, tick, symbol):
        contract_size = 100 if "XAU" in symbol else 10000
        if pos['Direction'] == "Buy":
            return (tick['close'] - pos['EntryPrice']) * contract_size
        return (pos['EntryPrice'] - tick['close']) * contract_size

    def save_results_to_csv(self, symbol):
        if not self.trades:
            return
        
        df = pd.DataFrame(self.trades)
        # Final formatting to look like your SMC sample
        if 'status' in df.columns: df.drop(columns=['status'], inplace=True)
        
        filename = f"TradeLog_{symbol}_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"\n[SUCCESS] CSV Trade Log created: {filename}")

    def generate_backtest_report(self, equity_curve):
        if not self.trades:
            return "No trades triggered."
        total_profit = sum(t['Profit'] for t in self.trades)
        return f"\n=== BACKTEST COMPLETE ===\nNet Profit: ${total_profit:.2f}\nTrades: {len(self.trades)}"