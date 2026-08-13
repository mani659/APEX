import pandas as pd
import numpy as np
import os
import json
from scipy.stats import skew

def calc_trading_metrics(pnl_array, trigger_count, tp_count, sl_count, time_count, ambig_count):
    if trigger_count == 0:
        return {}
        
    pnl = np.array(pnl_array)
    wins = pnl[pnl > 0]
    losses = pnl[pnl <= 0]
    
    win_rate = len(wins) / len(pnl) if len(pnl) > 0 else 0
    loss_rate = len(losses) / len(pnl) if len(pnl) > 0 else 0
    
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    
    payoff_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
    expectancy = pnl.mean() if len(pnl) > 0 else 0
    profit_factor = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else 0
    
    sorted_pnl = np.sort(pnl) if len(pnl) > 0 else np.array([])
    total_losses = abs(losses.sum())
    
    def tail_metrics(pct):
        if len(pnl) == 0: return 0.0, 0.0
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

    cum_pnl = pnl.cumsum() if len(pnl) > 0 else np.array([])
    running_max = np.maximum.accumulate(cum_pnl) if len(cum_pnl) > 0 else np.array([])
    drawdowns = running_max - cum_pnl if len(cum_pnl) > 0 else np.array([])
    max_dd = float(drawdowns.max()) if len(drawdowns) > 0 else 0.0
    
    return {
        'count': len(pnl),
        'trigger_rate': trigger_count / (trigger_count + len(pnl_array) - trigger_count) if trigger_count > 0 else 0, # not perfectly accurate here as N is trades, not signals, but handled in aggregate
        'tp_rate': tp_count / trigger_count if trigger_count > 0 else 0,
        'sl_rate': sl_count / trigger_count if trigger_count > 0 else 0,
        'time_rate': time_count / trigger_count if trigger_count > 0 else 0,
        'ambig_rate': ambig_count / trigger_count if trigger_count > 0 else 0,
        'win_rate': float(win_rate),
        'loss_rate': float(loss_rate),
        'avg_win': float(avg_win),
        'avg_loss': float(avg_loss),
        'payoff_ratio': float(payoff_ratio),
        'expectancy': float(expectancy),
        'profit_factor': float(profit_factor),
        'median': float(np.median(pnl)) if len(pnl) > 0 else 0,
        'std_dev': float(np.std(pnl)) if len(pnl) > 0 else 0,
        'skewness': float(skew(pnl)) if len(pnl) > 2 else 0.0,
        'max_loss': float(np.min(pnl)) if len(pnl) > 0 else 0,
        'max_dd': max_dd,
        'tail_contrib_1pct': tail_1_contrib,
        'tail_contrib_5pct': tail_5_contrib,
        'tail_contrib_10pct': tail_10_contrib,
        'leave_worst_1pct_exp': rem_exp_1,
        'leave_worst_5pct_exp': rem_exp_5,
        'leave_worst_10pct_exp': rem_exp_10
    }

def main():
    print("Loading data...")
    df_m1 = pd.read_parquet(r'data/m1/EURUSD_M1.parquet')
    df_m1['timestamp'] = pd.to_datetime(df_m1['timestamp'])
    df_m1.set_index('timestamp', inplace=True)
    df_m1.sort_index(inplace=True)
    
    print("Resampling to M15...")
    m15 = df_m1.resample('15Min').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    m15.dropna(inplace=True)
    
    print("Calculating RV20 and ATR20...")
    m15['log_ret'] = np.log(m15['close'] / m15['close'].shift(1))
    m15['RV20'] = m15['log_ret'].shift(1).rolling(20).std()
    
    m15['tr1'] = m15['high'] - m15['low']
    m15['tr2'] = (m15['high'] - m15['close'].shift(1)).abs()
    m15['tr3'] = (m15['low'] - m15['close'].shift(1)).abs()
    m15['TR'] = m15[['tr1', 'tr2', 'tr3']].max(axis=1)
    
    # ATR from completed bars before signal
    m15['ATR20'] = m15['TR'].shift(1).rolling(20).mean()
    m15['D'] = 0.5 * m15['ATR20']
    
    def calc_percentile(s):
        current = s[-1]
        prior = s[:-1]
        prior = prior[~np.isnan(prior)]
        if len(prior) < 400:
            return np.nan
        return (prior < current).mean() * 100
        
    m15['RV_percentile'] = m15['RV20'].rolling(481).apply(calc_percentile, raw=True)
    
    m15['vol_state'] = 'UNCLASSIFIED'
    m15.loc[m15['RV_percentile'] < 20, 'vol_state'] = 'LOW_VOL'
    m15.loc[(m15['RV_percentile'] >= 20) & (m15['RV_percentile'] <= 80), 'vol_state'] = 'NORMAL_VOL'
    m15.loc[m15['RV_percentile'] > 80, 'vol_state'] = 'HIGH_VOL'
    
    valid_data = m15[m15['vol_state'] != 'UNCLASSIFIED'].copy()
    validation = valid_data.loc['2024-07-01':].copy()
    
    # Use 4-bar spacing for signals
    signals = validation.iloc[::4]
    
    print(f"Executing M1 Simulation for {len(signals)} signals...")
    
    results = []
    
    # Pre-fetch M1 data indexing for faster access
    m1_idx = df_m1.index
    
    for t_m15, row in signals.iterrows():
        sig_close = row['close']
        D = row['D']
        state = row['vol_state']
        
        if np.isnan(D):
            continue
            
        upper_trigger = sig_close + D
        lower_trigger = sig_close - D
        
        # M1 slice is exactly [t_m15 + 15m, t_m15 + 74m]
        start_time = t_m15 + pd.Timedelta(minutes=15)
        end_time = t_m15 + pd.Timedelta(minutes=74)
        
        try:
            loc_start = df_m1.index.get_indexer([start_time], method='bfill')[0]
            loc_end = df_m1.index.get_indexer([end_time], method='ffill')[0]
            if loc_start == -1 or loc_end == -1:
                continue
        except KeyError:
            continue
            
        m1_slice_high = df_m1['high'].values[loc_start:loc_end+1]
        m1_slice_low = df_m1['low'].values[loc_start:loc_end+1]
        m1_slice_close = df_m1['close'].values[loc_start:loc_end+1]
        
        direction = None
        entry_idx = -1
        entry_price = 0
        
        for i in range(len(m1_slice_high)):
            h = m1_slice_high[i]
            l = m1_slice_low[i]
            c = m1_slice_close[i]
            
            if h >= upper_trigger and l <= lower_trigger:
                direction = 'AMBIGUOUS_TRIGGER'
                entry_idx = i
                entry_price = c
                break
            elif h >= upper_trigger:
                direction = 'LONG'
                entry_idx = i
                entry_price = c
                break
            elif l <= lower_trigger:
                direction = 'SHORT'
                entry_idx = i
                entry_price = c
                break
                
        if direction is None:
            results.append({
                'timestamp': t_m15,
                'vol_state': state,
                'direction': 'NO_TRIGGER',
                'pnl': 0.0,
                'exit_type': 'NONE'
            })
            continue
            
        if direction == 'AMBIGUOUS_TRIGGER':
            # Assign -1R roughly
            results.append({
                'timestamp': t_m15,
                'vol_state': state,
                'direction': 'AMBIGUOUS',
                'pnl': -D,
                'exit_type': 'AMBIGUOUS'
            })
            continue
            
        # OCO Executed. Find SL/TP
        if direction == 'LONG':
            sl = entry_price - D
            tp = entry_price + D
        else:
            sl = entry_price + D
            tp = entry_price - D
            
        exit_type = None
        exit_price = 0
        
        for i in range(entry_idx + 1, len(m1_slice_high)):
            h = m1_slice_high[i]
            l = m1_slice_low[i]
            c = m1_slice_close[i]
            
            if direction == 'LONG':
                if h >= tp and l <= sl:
                    exit_type = 'AMBIGUOUS_EXIT'
                    exit_price = c
                    break
                elif h >= tp:
                    exit_type = 'TP'
                    exit_price = c
                    break
                elif l <= sl:
                    exit_type = 'SL'
                    exit_price = c
                    break
            else: # SHORT
                if h >= sl and l <= tp:
                    exit_type = 'AMBIGUOUS_EXIT'
                    exit_price = c
                    break
                elif l <= tp:
                    exit_type = 'TP'
                    exit_price = c
                    break
                elif h >= sl:
                    exit_type = 'SL'
                    exit_price = c
                    break
                    
        if exit_type is None:
            exit_type = 'TIME'
            exit_price = m1_slice_close[-1]
            
        if exit_type == 'AMBIGUOUS_EXIT':
            gross_pnl = -D # conservative
        else:
            if direction == 'LONG':
                gross_pnl = exit_price - entry_price
            else:
                gross_pnl = entry_price - exit_price
                
        results.append({
            'timestamp': t_m15,
            'vol_state': state,
            'direction': direction,
            'gross_pnl': gross_pnl,
            'exit_type': exit_type
        })
        
    df_res = pd.DataFrame(results)
    
    print("Generating Analysis...")
    def aggregate(df_slice, friction):
        f_val = friction * 0.0001
        
        df_trig = df_slice[~df_slice['direction'].isin(['NO_TRIGGER'])]
        total_signals = len(df_slice)
        total_triggers = len(df_trig)
        
        if total_triggers == 0: return {}
        
        pnl = df_trig['gross_pnl'] - f_val
        
        tp_c = len(df_trig[df_trig['exit_type'] == 'TP'])
        sl_c = len(df_trig[df_trig['exit_type'] == 'SL'])
        time_c = len(df_trig[df_trig['exit_type'] == 'TIME'])
        ambig_c = len(df_trig[df_trig['exit_type'].str.contains('AMBIGUOUS')])
        
        stats = calc_trading_metrics(pnl.values, total_triggers, tp_c, sl_c, time_c, ambig_c)
        stats['signal_count'] = total_signals
        stats['trigger_rate_global'] = total_triggers / total_signals if total_signals > 0 else 0
        return stats
        
    final_report = {}
    
    val_early = df_res.iloc[:len(df_res)//2]
    val_late = df_res.iloc[len(df_res)//2:]
    
    for f in [0.5, 1.0, 2.0]:
        f_key = f"{f}_pip"
        final_report[f_key] = {
            'ALL': {
                'FULL': aggregate(df_res, f),
                'EARLY': aggregate(val_early, f),
                'LATE': aggregate(val_late, f),
                'LONG_ONLY': aggregate(df_res[df_res['direction'] == 'LONG'], f),
                'SHORT_ONLY': aggregate(df_res[df_res['direction'] == 'SHORT'], f),
            },
            'HIGH_VOL': {
                'FULL': aggregate(df_res[df_res['vol_state'] == 'HIGH_VOL'], f),
                'EARLY': aggregate(val_early[val_early['vol_state'] == 'HIGH_VOL'], f),
                'LATE': aggregate(val_late[val_late['vol_state'] == 'HIGH_VOL'], f),
                'LONG_ONLY': aggregate(df_res[(df_res['vol_state'] == 'HIGH_VOL') & (df_res['direction'] == 'LONG')], f),
                'SHORT_ONLY': aggregate(df_res[(df_res['vol_state'] == 'HIGH_VOL') & (df_res['direction'] == 'SHORT')], f),
            }
        }
        
    with open('reports/RC012_Study_008_results.json', 'w') as f:
        json.dump(final_report, f, indent=2)
        
    df_res.to_parquet('reports/RC012_Study_008_Volatility_OCO_Dataset.parquet')
    print("Done!")

if __name__ == '__main__':
    main()
