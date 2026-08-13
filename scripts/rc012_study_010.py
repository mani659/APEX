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
        'q25': float(s.quantile(0.25)),
        'q75': float(s.quantile(0.75)),
        'q90': float(s.quantile(0.90)),
        'q10': float(s.quantile(0.10))
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
    
    signals = validation.iloc[::4]
    print(f"Executing Diagnostic Simulation for {len(signals)} signals...")
    
    results = []
    
    f_val = 1.0 * 0.0001 # 1.0 pip primary friction
    
    for t_m15, row in signals.iterrows():
        sig_close = row['close']
        D = row['D']
        state = row['vol_state']
        
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
            
        p_len_arr = np.abs(np.diff(np.insert(m1_close, 0, sig_close)))
        path_length_full = np.sum(p_len_arr)
        
        direction = None
        entry_idx = -1
        entry_price = 0
        
        for i in range(len(m1_high)):
            if m1_high[i] >= upper_trigger and m1_low[i] <= lower_trigger:
                direction = 'AMBIGUOUS_TRIGGER'
                entry_idx = i
                entry_price = m1_close[i]
                break
            elif m1_high[i] >= upper_trigger:
                direction = 'LONG'
                entry_idx = i
                entry_price = m1_close[i]
                break
            elif m1_low[i] <= lower_trigger:
                direction = 'SHORT'
                entry_idx = i
                entry_price = m1_close[i]
                break
                
        if direction is None or direction == 'AMBIGUOUS_TRIGGER':
            continue
            
        sl = entry_price - D if direction == 'LONG' else entry_price + D
        tp = entry_price + D if direction == 'LONG' else entry_price - D
        
        exit_type = None
        exit_price = 0
        exit_idx = len(m1_high) - 1
        
        for i in range(entry_idx + 1, len(m1_high)):
            h = m1_high[i]
            l = m1_low[i]
            c = m1_close[i]
            
            if direction == 'LONG':
                if h >= tp and l <= sl:
                    exit_type = 'AMBIGUOUS_EXIT'
                    exit_price = c
                    exit_idx = i
                    break
                elif h >= tp:
                    exit_type = 'TP'
                    exit_price = c
                    exit_idx = i
                    break
                elif l <= sl:
                    exit_type = 'SL'
                    exit_price = c
                    exit_idx = i
                    break
            else: # SHORT
                if h >= sl and l <= tp:
                    exit_type = 'AMBIGUOUS_EXIT'
                    exit_price = c
                    exit_idx = i
                    break
                elif l <= tp:
                    exit_type = 'TP'
                    exit_price = c
                    exit_idx = i
                    break
                elif h >= sl:
                    exit_type = 'SL'
                    exit_price = c
                    exit_idx = i
                    break
                    
        if exit_type is None:
            exit_type = 'TIME'
            exit_price = m1_close[-1]
            exit_idx = len(m1_high) - 1
            
        if exit_type == 'AMBIGUOUS_EXIT':
            continue # drop ambiguous for cleaner path analysis
            
        gross_pnl = exit_price - entry_price if direction == 'LONG' else entry_price - exit_price
        
        active_close = m1_close[entry_idx:exit_idx+1]
        active_high = m1_high[entry_idx:exit_idx+1]
        active_low = m1_low[entry_idx:exit_idx+1]
        
        if len(active_close) == 0:
            continue
            
        act_p_len_arr = np.abs(np.diff(np.insert(active_close, 0, entry_price)))
        path_length_active = np.sum(act_p_len_arr)
        
        term_abs_disp = abs(exit_price - sig_close)
        
        if direction == 'LONG':
            mfe_arr = active_high - entry_price
            mae_arr = entry_price - active_low
        else:
            mfe_arr = entry_price - active_low
            mae_arr = active_high - entry_price
            
        mfe_arr = np.maximum(0, mfe_arr)
        mae_arr = np.maximum(0, mae_arr)
        
        mfe = np.max(mfe_arr)
        mae = np.max(mae_arr)
        
        idx_mfe = np.argmax(mfe_arr)
        idx_mae = np.argmax(mae_arr)
        
        time_to_mfe = idx_mfe # minutes from entry
        time_to_mae = idx_mae
        
        first_adv_idx = -1
        # defining meaningful adverse as > 1.0 pip (0.00010)
        adverse_threshold = 0.00010
        for idx in range(len(mae_arr)):
            if mae_arr[idx] >= adverse_threshold:
                first_adv_idx = idx
                break
                
        if first_adv_idx != -1:
            mfe_before_adv = np.max(mfe_arr[:first_adv_idx]) if first_adv_idx > 0 else 0
            mfe_after_adv = np.max(mfe_arr[first_adv_idx:]) if first_adv_idx < len(mfe_arr) else 0
            post_adv_expansion = mfe_after_adv - mfe_before_adv
        else:
            mfe_before_adv = mfe
            mfe_after_adv = mfe
            post_adv_expansion = 0
            
        path_eff_full = term_abs_disp / path_length_full if path_length_full > 0 else 0
        path_eff_active = abs(gross_pnl) / path_length_active if path_length_active > 0 else 0
        
        capture_ratio_full = abs(gross_pnl) / path_length_full if path_length_full > 0 else 0
        capture_ratio_active = abs(gross_pnl) / path_length_active if path_length_active > 0 else 0
        
        cost_decay_full = f_val / path_length_full if path_length_full > 0 else 0
        cost_decay_active = f_val / path_length_active if path_length_active > 0 else 0
        
        results.append({
            'timestamp': t_m15,
            'vol_state': state,
            'direction': direction,
            'exit_type': exit_type,
            'gross_pnl': gross_pnl,
            'term_abs_disp': term_abs_disp,
            'path_length_full': path_length_full,
            'path_length_active': path_length_active,
            'path_eff_full': path_eff_full,
            'path_eff_active': path_eff_active,
            'mfe': mfe,
            'mae': mae,
            'time_to_mfe': time_to_mfe,
            'time_to_mae': time_to_mae,
            'post_adv_expansion': post_adv_expansion,
            'capture_ratio_full': capture_ratio_full,
            'capture_ratio_active': capture_ratio_active,
            'cost_decay_full': cost_decay_full,
            'cost_decay_active': cost_decay_active
        })
        
    df_res = pd.DataFrame(results)
    print("Generating Analysis...")
    
    def aggregate(df_slice):
        if len(df_slice) == 0: return {}
        return {
            'N': len(df_slice),
            'gross_pnl': calculate_stats(df_slice['gross_pnl']),
            'term_abs_disp': calculate_stats(df_slice['term_abs_disp']),
            'path_length_full': calculate_stats(df_slice['path_length_full']),
            'path_length_active': calculate_stats(df_slice['path_length_active']),
            'path_eff_full': calculate_stats(df_slice['path_eff_full']),
            'path_eff_active': calculate_stats(df_slice['path_eff_active']),
            'mfe': calculate_stats(df_slice['mfe']),
            'mae': calculate_stats(df_slice['mae']),
            'time_to_mfe': calculate_stats(df_slice['time_to_mfe']),
            'time_to_mae': calculate_stats(df_slice['time_to_mae']),
            'post_adv_expansion': calculate_stats(df_slice['post_adv_expansion']),
            'capture_ratio_full': calculate_stats(df_slice['capture_ratio_full']),
            'capture_ratio_active': calculate_stats(df_slice['capture_ratio_active']),
            'cost_decay_full': calculate_stats(df_slice['cost_decay_full']),
            'cost_decay_active': calculate_stats(df_slice['cost_decay_active'])
        }

    final_report = {}
    
    for state in ['ALL', 'HIGH_VOL']:
        if state == 'ALL':
            df_s = df_res
        else:
            df_s = df_res[df_res['vol_state'] == state]
            
        final_report[state] = aggregate(df_s)
        
    with open('reports/RC012_Study_010_results.json', 'w') as f:
        json.dump(final_report, f, indent=2)
        
    df_res.to_parquet('reports/RC012_Study_010_Two_Sided_Path_Dataset.parquet')
    print("Done!")

if __name__ == '__main__':
    main()
