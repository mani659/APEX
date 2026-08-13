import pandas as pd
import numpy as np
import os
import json

def calculate_stats(series):
    s = pd.Series(series).dropna()
    if len(s) == 0:
        return {}
    return {
        'count': int(len(s)),
        'mean': float(s.mean()),
        'median': float(s.median()),
        'std': float(s.std()),
        'skew': float(s.skew()) if len(s) > 2 else 0,
        'q25': float(s.quantile(0.25)),
        'q75': float(s.quantile(0.75)),
        'max': float(s.max()),
        'min': float(s.min()),
        'p01': float(s.quantile(0.01)),
        'p05': float(s.quantile(0.05)),
        'p10': float(s.quantile(0.10)),
        'p95': float(s.quantile(0.95)),
        'p99': float(s.quantile(0.99))
    }

def calculate_drawdown(pnl_series):
    equity = pnl_series.cumsum()
    peak = equity.cummax()
    drawdown = peak - equity
    return float(drawdown.max())

def calculate_tail_loss(pnl_series):
    losses = pnl_series[pnl_series < 0]
    if len(losses) == 0:
        return {'w1': 0, 'w5': 0, 'w10': 0}
    
    total_loss = losses.sum()
    s_losses = losses.sort_values() # most negative first
    
    w1_count = max(1, int(len(losses) * 0.01))
    w5_count = max(1, int(len(losses) * 0.05))
    w10_count = max(1, int(len(losses) * 0.10))
    
    w1_sum = s_losses.iloc[:w1_count].sum()
    w5_sum = s_losses.iloc[:w5_count].sum()
    w10_sum = s_losses.iloc[:w10_count].sum()
    
    return {
        'w1_pct': float(w1_sum / total_loss) if total_loss != 0 else 0,
        'w5_pct': float(w5_sum / total_loss) if total_loss != 0 else 0,
        'w10_pct': float(w10_sum / total_loss) if total_loss != 0 else 0,
        'w1_sum': float(w1_sum),
        'w5_sum': float(w5_sum),
        'w10_sum': float(w10_sum),
        'total_loss': float(total_loss)
    }

def get_expectancy_excluding_tails(pnl_series):
    if len(pnl_series) == 0: return {}
    s = pnl_series.sort_values() # worst first
    n = len(s)
    
    w1_idx = max(1, int(n * 0.01))
    w5_idx = max(1, int(n * 0.05))
    w10_idx = max(1, int(n * 0.10))
    
    return {
        'excl_w1': float(s.iloc[w1_idx:].mean()),
        'excl_w5': float(s.iloc[w5_idx:].mean()),
        'excl_w10': float(s.iloc[w10_idx:].mean()),
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
    
    valid_data = m15[m15['vol_state'] == 'HIGH_VOL'].copy()
    validation = valid_data.loc['2024-07-01':].copy()
    
    signals = validation.iloc[::4]
    print(f"Executing Bounded Inventory Simulation for {len(signals)} signals...")
    
    results = []
    
    for t_m15, row in signals.iterrows():
        sig_close = row['close']
        D = row['D']
        
        if np.isnan(D):
            continue
            
        upper_trigger = sig_close + D
        lower_trigger = sig_close - D
        
        start_time = t_m15 + pd.Timedelta(minutes=15)
        end_time = t_m15 + pd.Timedelta(minutes=74)
        
        try:
            loc_start = df_m1.index.get_indexer([start_time], method='bfill')[0]
            loc_end = df_m1.index.get_indexer([end_time], method='ffill')[0]
            if loc_start == -1 or loc_end == -1:
                continue
        except KeyError:
            continue
            
        m1_high = df_m1['high'].values[loc_start:loc_end+1]
        m1_low = df_m1['low'].values[loc_start:loc_end+1]
        m1_close = df_m1['close'].values[loc_start:loc_end+1]
        
        if len(m1_close) < 10:
            continue
            
        direction = None
        u1_idx = -1
        u1_price = 0
        
        for i in range(len(m1_high)):
            if m1_high[i] >= upper_trigger and m1_low[i] <= lower_trigger:
                direction = 'AMBIGUOUS'
                break
            elif m1_high[i] >= upper_trigger:
                direction = 'LONG'
                u1_idx = i
                u1_price = m1_close[i]
                break
            elif m1_low[i] <= lower_trigger:
                direction = 'SHORT'
                u1_idx = i
                u1_price = m1_close[i]
                break
                
        if direction is None or direction == 'AMBIGUOUS':
            continue
            
        # Model A
        horizon_price = m1_close[-1]
        gross_pnl_A = (horizon_price - u1_price) if direction == 'LONG' else (u1_price - horizon_price)
        
        # Model B
        u2_trigger = u1_price - D if direction == 'LONG' else u1_price + D
        
        u2_idx = -1
        u2_price = 0
        
        for i in range(u1_idx + 1, len(m1_high)):
            if direction == 'LONG':
                if m1_low[i] <= u2_trigger:
                    u2_idx = i
                    u2_price = m1_close[i] # executing at close
                    break
            else: # SHORT
                if m1_high[i] >= u2_trigger:
                    u2_idx = i
                    u2_price = m1_close[i]
                    break
                    
        used_u2 = (u2_idx != -1)
        gross_pnl_B = gross_pnl_A
        if used_u2:
            gross_pnl_u2 = (horizon_price - u2_price) if direction == 'LONG' else (u2_price - horizon_price)
            gross_pnl_B += gross_pnl_u2
            
        # MFE / MAE of Basket A
        if direction == 'LONG':
            mfe_A_arr = np.maximum(0, m1_high[u1_idx:] - u1_price)
            mae_A_arr = np.maximum(0, u1_price - m1_low[u1_idx:])
        else:
            mfe_A_arr = np.maximum(0, u1_price - m1_low[u1_idx:])
            mae_A_arr = np.maximum(0, m1_high[u1_idx:] - u1_price)
            
        mfe_A = np.max(mfe_A_arr)
        mae_A = np.max(mae_A_arr)
        
        # Recovery Metrics for Model B (if u2 used)
        rec_mfe = 0
        time_to_rec = 0
        pnl_before_u2 = 0
        
        if used_u2:
            pnl_before_u2 = (u2_price - u1_price) if direction == 'LONG' else (u1_price - u2_price)
            # From u2 to end
            if direction == 'LONG':
                b_mfe_arr = np.maximum(0, (m1_high[u2_idx:] - u1_price) + (m1_high[u2_idx:] - u2_price))
            else:
                b_mfe_arr = np.maximum(0, (u1_price - m1_low[u2_idx:]) + (u2_price - m1_low[u2_idx:]))
                
            rec_mfe = np.max(b_mfe_arr)
            time_to_rec = np.argmax(b_mfe_arr)
            
        results.append({
            'timestamp': t_m15,
            'direction': direction,
            'gross_pnl_A': gross_pnl_A,
            'gross_pnl_B': gross_pnl_B,
            'used_u2': used_u2,
            'mfe_A': mfe_A,
            'mae_A': mae_A,
            'pnl_before_u2': pnl_before_u2,
            'rec_mfe': rec_mfe,
            'time_to_rec_mfe': time_to_rec
        })
        
    df_res = pd.DataFrame(results)
    
    def process_cost(f_val):
        df = df_res.copy()
        df['net_pnl_A'] = df['gross_pnl_A'] - f_val
        df['net_pnl_B'] = df['gross_pnl_B'] - np.where(df['used_u2'], f_val * 2, f_val)
        return df
        
    print("Generating Analysis...")
    
    def aggregate(df, f_val):
        if len(df) == 0: return {}
        
        d = process_cost(f_val)
        
        def run_stats(pnl_series, model_name):
            wins = pnl_series[pnl_series > 0]
            losses = pnl_series[pnl_series < 0]
            
            wr = len(wins) / len(pnl_series) if len(pnl_series) > 0 else 0
            lr = len(losses) / len(pnl_series) if len(pnl_series) > 0 else 0
            
            avg_win = wins.mean() if len(wins) > 0 else 0
            avg_loss = losses.mean() if len(losses) > 0 else 0
            payoff = abs(avg_win / avg_loss) if avg_loss != 0 else 0
            
            gross_win = wins.sum()
            gross_loss = abs(losses.sum())
            pf = gross_win / gross_loss if gross_loss != 0 else 0
            
            return {
                'expectancy': float(pnl_series.mean()),
                'median': float(pnl_series.median()),
                'win_rate': float(wr),
                'loss_rate': float(lr),
                'avg_win': float(avg_win),
                'avg_loss': float(avg_loss),
                'payoff': float(payoff),
                'profit_factor': float(pf),
                'tail_loss': calculate_tail_loss(pnl_series),
                'excl_tails': get_expectancy_excluding_tails(pnl_series)
            }
            
        stats_A = run_stats(d['net_pnl_A'], 'A')
        stats_B = run_stats(d['net_pnl_B'], 'B')
        
        longs_A = d[d['direction'] == 'LONG']['net_pnl_A']
        shorts_A = d[d['direction'] == 'SHORT']['net_pnl_A']
        longs_B = d[d['direction'] == 'LONG']['net_pnl_B']
        shorts_B = d[d['direction'] == 'SHORT']['net_pnl_B']
        
        stats_A['dd_long'] = calculate_drawdown(longs_A) if len(longs_A) > 0 else 0
        stats_A['dd_short'] = calculate_drawdown(shorts_A) if len(shorts_A) > 0 else 0
        stats_B['dd_long'] = calculate_drawdown(longs_B) if len(longs_B) > 0 else 0
        stats_B['dd_short'] = calculate_drawdown(shorts_B) if len(shorts_B) > 0 else 0
        
        u2_mask = d['used_u2'] == True
        u2_count = u2_mask.sum()
        u2_recovered = (d.loc[u2_mask, 'net_pnl_B'] > 0).sum()
        
        inv_stats = {
            'N': len(d),
            'avg_units_A': 1.0,
            'avg_units_B': 1.0 + (u2_count / len(d) if len(d) > 0 else 0),
            'pct_used_u2': float(u2_count / len(d)) if len(d) > 0 else 0,
            'u2_recovered_pct': float(u2_recovered / u2_count) if u2_count > 0 else 0,
            'mfe_A_mean': float(d['mfe_A'].mean()),
            'mae_A_mean': float(d['mae_A'].mean()),
            'rec_mfe_mean': float(d.loc[u2_mask, 'rec_mfe'].mean()) if u2_count > 0 else 0
        }
        
        return {
            'A': stats_A,
            'B': stats_B,
            'inventory': inv_stats
        }

    f1 = 1.0 * 0.0001
    f05 = 0.5 * 0.0001
    f2 = 2.0 * 0.0001
    
    val_early = df_res.iloc[:len(df_res)//2]
    val_late = df_res.iloc[len(df_res)//2:]
    
    final_report = {
        'cost_10': {
            'FULL': aggregate(df_res, f1),
            'EARLY': aggregate(val_early, f1),
            'LATE': aggregate(val_late, f1)
        },
        'cost_05': {
            'FULL': aggregate(df_res, f05)
        },
        'cost_20': {
            'FULL': aggregate(df_res, f2)
        }
    }
        
    with open('reports/RC012_Study_011_results.json', 'w') as f:
        json.dump(final_report, f, indent=2)
        
    df_res.to_parquet('reports/RC012_Study_011_Bounded_Inventory_Dataset.parquet')
    print("Done!")

if __name__ == '__main__':
    main()
