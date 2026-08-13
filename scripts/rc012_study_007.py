import pandas as pd
import numpy as np
import os
import json
from scipy.stats import skew

def calculate_drawdown(pnl_series):
    cum_pnl = pnl_series.cumsum()
    running_max = np.maximum.accumulate(cum_pnl)
    drawdowns = running_max - cum_pnl
    return float(drawdowns.max()) if len(drawdowns) > 0 else 0.0

def calc_trading_metrics(pnl_array):
    if len(pnl_array) == 0:
        return {}
    
    pnl = np.array(pnl_array)
    wins = pnl[pnl > 0]
    losses = pnl[pnl <= 0]
    
    win_rate = len(wins) / len(pnl)
    loss_rate = len(losses) / len(pnl)
    
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    
    payoff_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
    expectancy = pnl.mean()
    profit_factor = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else 0
    
    sorted_pnl = np.sort(pnl)
    total_losses = abs(losses.sum())
    
    def tail_metrics(pct):
        n_worst = max(1, int(len(pnl) * pct))
        worst_trades = sorted_pnl[:n_worst]
        worst_sum = abs(worst_trades.sum())
        tail_contrib = worst_sum / total_losses if total_losses != 0 else 0
        
        remaining_trades = sorted_pnl[n_worst:]
        rem_expectancy = remaining_trades.mean() if len(remaining_trades) > 0 else 0
        return float(tail_contrib), float(rem_expectancy)
        
    tail_1_contrib, rem_exp_1 = tail_metrics(0.01)
    tail_5_contrib, rem_exp_5 = tail_metrics(0.05)
    tail_10_contrib, rem_exp_10 = tail_metrics(0.10)
    
    return {
        'count': len(pnl),
        'win_rate': float(win_rate),
        'loss_rate': float(loss_rate),
        'avg_win': float(avg_win),
        'avg_loss': float(avg_loss),
        'payoff_ratio': float(payoff_ratio),
        'expectancy': float(expectancy),
        'profit_factor': float(profit_factor),
        'median': float(np.median(pnl)),
        'std_dev': float(np.std(pnl)),
        'skewness': float(skew(pnl)) if len(pnl) > 2 else 0.0,
        'max_loss': float(np.min(pnl)),
        'tail_contrib_1pct': tail_1_contrib,
        'tail_contrib_5pct': tail_5_contrib,
        'tail_contrib_10pct': tail_10_contrib,
        'leave_worst_1pct_exp': rem_exp_1,
        'leave_worst_5pct_exp': rem_exp_5,
        'leave_worst_10pct_exp': rem_exp_10
    }

def main():
    print("Loading data...")
    df = pd.read_parquet(r'data/m1/EURUSD_M1.parquet')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    print("Resampling to M15...")
    m15 = df.resample('15Min').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    m15.dropna(inplace=True)
    
    print("Calculating RV20...")
    m15['log_ret'] = np.log(m15['close'] / m15['close'].shift(1))
    m15['RV20'] = m15['log_ret'].shift(1).rolling(20).std()
    
    def calc_percentile(s):
        current = s[-1]
        prior = s[:-1]
        prior = prior[~np.isnan(prior)]
        if len(prior) < 400:
            return np.nan
        return (prior < current).mean() * 100
        
    m15['RV_percentile'] = m15['RV20'].rolling(481).apply(calc_percentile, raw=True)
    
    print("Assigning States...")
    m15['vol_state'] = 'UNCLASSIFIED'
    m15.loc[m15['RV_percentile'] < 20, 'vol_state'] = 'LOW_VOL'
    m15.loc[(m15['RV_percentile'] >= 20) & (m15['RV_percentile'] <= 80), 'vol_state'] = 'NORMAL_VOL'
    m15.loc[m15['RV_percentile'] > 80, 'vol_state'] = 'HIGH_VOL'
    
    valid_data = m15[m15['vol_state'] != 'UNCLASSIFIED'].copy()
    validation = valid_data.loc['2024-07-01':].copy()

    horizons = [4, 64]
    friction_pips = 1.0
    f_val = friction_pips * 0.0001
    
    for h in horizons:
        validation[f'close_fwd_{h}'] = validation['close'].shift(-h)
        validation[f'long_pnl_{h}'] = (validation[f'close_fwd_{h}'] - validation['close']) - f_val
        validation[f'short_pnl_{h}'] = (validation['close'] - validation[f'close_fwd_{h}']) - f_val
        
        future_highs = validation['high'].rolling(h).max().shift(-h)
        future_lows = validation['low'].rolling(h).min().shift(-h)
        validation[f'long_mfe_{h}'] = future_highs - validation['close']
        validation[f'long_mae_{h}'] = validation['close'] - future_lows
        validation[f'short_mfe_{h}'] = validation['close'] - future_lows
        validation[f'short_mae_{h}'] = future_highs - validation['close']

    print("Saving Validation Dataset...")
    os.makedirs('reports', exist_ok=True)
    validation.to_parquet('reports/RC012_Study_007_Volatility_Trading_Architecture_Dataset.parquet')

    def analyze_population(df_slice, h, state):
        if state != 'ALL':
            df_slice = df_slice[df_slice['vol_state'] == state]
            
        df_slice = df_slice.dropna(subset=[f'long_pnl_{h}'])
        if len(df_slice) == 0:
            return {}
            
        long_pnl = df_slice[f'long_pnl_{h}'].values
        short_pnl = df_slice[f'short_pnl_{h}'].values
        combined_pnl = np.concatenate([long_pnl, short_pnl])
        
        res = {
            'LONG': calc_trading_metrics(long_pnl),
            'SHORT': calc_trading_metrics(short_pnl),
            'COMBINED': calc_trading_metrics(combined_pnl),
            'long_drawdown': calculate_drawdown(long_pnl),
            'short_drawdown': calculate_drawdown(short_pnl),
            'long_mfe_mean': float(df_slice[f'long_mfe_{h}'].mean()),
            'long_mae_mean': float(df_slice[f'long_mae_{h}'].mean()),
            'short_mfe_mean': float(df_slice[f'short_mfe_{h}'].mean()),
            'short_mae_mean': float(df_slice[f'short_mae_{h}'].mean())
        }
        return res

    print("Generating Analysis...")
    analysis = {}
    
    val_early = validation.iloc[:len(validation)//2]
    val_late = validation.iloc[len(validation)//2:]

    def process_matrix(df_source, name):
        analysis[name] = {
            'ALL_4': analyze_population(df_source.iloc[::4], 4, 'ALL'),
            'HIGH_VOL_4': analyze_population(df_source.iloc[::4], 4, 'HIGH_VOL'),
            'ALL_64': analyze_population(df_source.iloc[::64], 64, 'ALL'),
            'LOW_VOL_64': analyze_population(df_source.iloc[::64], 64, 'LOW_VOL')
        }
        
    process_matrix(validation, 'FULL_VALIDATION')
    process_matrix(val_early, 'EARLY_VALIDATION')
    process_matrix(val_late, 'LATE_VALIDATION')
    
    with open('reports/RC012_Study_007_results.json', 'w') as f:
        json.dump(analysis, f, indent=2)
        
    print("Done!")

if __name__ == '__main__':
    main()
