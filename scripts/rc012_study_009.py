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
    
    m15['vol_state'] = 'UNCLASSIFIED'
    m15.loc[m15['RV_percentile'] < 20, 'vol_state'] = 'LOW_VOL'
    m15.loc[(m15['RV_percentile'] >= 20) & (m15['RV_percentile'] <= 80), 'vol_state'] = 'NORMAL_VOL'
    m15.loc[m15['RV_percentile'] > 80, 'vol_state'] = 'HIGH_VOL'
    
    valid_data = m15[m15['vol_state'] != 'UNCLASSIFIED'].copy()
    validation = valid_data.loc['2024-07-01':].copy()
    
    # 4-bar thin
    signals = validation.iloc[::4]
    
    print(f"Executing Path Analysis for {len(signals)} signals...")
    
    results = []
    
    for t_m15, row in signals.iterrows():
        C0 = row['close']
        state = row['vol_state']
        
        start_time = t_m15 + pd.Timedelta(minutes=1) # 60 minutes after the close
        end_time = t_m15 + pd.Timedelta(minutes=60)
        
        try:
            loc_start = df_m1.index.get_indexer([start_time], method='bfill')[0]
            loc_end = df_m1.index.get_indexer([end_time], method='ffill')[0]
            if loc_start == -1 or loc_end == -1:
                continue
        except KeyError:
            continue
            
        m1_close = df_m1['close'].values[loc_start:loc_end+1]
        
        if len(m1_close) < 5: # data gap
            continue
            
        # extract M15 R1..R4 directly from the m15 dataframe if possible, but m1 is safer for exact alignment
        # R1 = 15m, R2 = 30m, R3 = 45m, R4 = 60m
        # Using M1 array (assuming roughly continuous, but let's use exact time matching or just get it from m15)
        try:
            t_r1 = t_m15 + pd.Timedelta(minutes=15)
            t_r2 = t_m15 + pd.Timedelta(minutes=30)
            t_r3 = t_m15 + pd.Timedelta(minutes=45)
            t_r4 = t_m15 + pd.Timedelta(minutes=60)
            c_r1 = m15.loc[t_r1, 'close']
            c_r2 = m15.loc[t_r2, 'close']
            c_r3 = m15.loc[t_r3, 'close']
            c_r4 = m15.loc[t_r4, 'close']
        except KeyError:
            # gap in M15
            continue
            
        initial_return = c_r1 - C0
        if initial_return > 0:
            init_dir = 1
        elif initial_return < 0:
            init_dir = -1
        else:
            init_dir = 0
            
        # Directional Persistence
        r_rets = [c_r1 - C0, c_r2 - c_r1, c_r3 - c_r2, c_r4 - c_r3]
        dirs = [1 if r > 0 else (-1 if r < 0 else 0) for r in r_rets]
        directional_count = sum([1 for d in dirs if d != 0])
        match_count = sum([1 for d in dirs if d == init_dir and d != 0])
        
        persistence = match_count / directional_count if directional_count > 0 else np.nan
        
        # Excursions
        if init_dir != 0:
            signed_moves = (m1_close - C0) * init_dir
            init_excursion = max(0, np.max(signed_moves))
            counter_moves = (C0 - m1_close) * init_dir
            rev_excursion = max(0, np.max(counter_moves))
            whipsaw = rev_excursion / init_excursion if init_excursion > 0 else np.nan
        else:
            init_excursion = np.nan
            rev_excursion = np.nan
            whipsaw = np.nan
            
        # Path Efficiency
        net_displacement = abs(c_r4 - C0)
        # path length = sum(abs(C_i - C_i-1))
        p_len_arr = np.abs(np.diff(np.insert(m1_close, 0, C0)))
        path_length = np.sum(p_len_arr)
        
        path_efficiency = net_displacement / path_length if path_length > 0 else np.nan
        
        term_return = c_r4 - C0
        if term_return > 0:
            term_dir = 1
        elif term_return < 0:
            term_dir = -1
        else:
            term_dir = 0
            
        if init_dir == 0:
            term_match = 'NEUTRAL'
        elif term_dir == init_dir:
            term_match = 'SAME'
        elif term_dir == 0:
            term_match = 'NEUTRAL'
        else:
            term_match = 'OPPOSITE'
            
        results.append({
            'timestamp': t_m15,
            'vol_state': state,
            'initial_direction': init_dir,
            'directional_persistence': persistence,
            'initial_excursion': init_excursion,
            'reversal_excursion': rev_excursion,
            'whipsaw_ratio': whipsaw,
            'net_displacement': net_displacement,
            'total_path_length': path_length,
            'path_efficiency': path_efficiency,
            'terminal_return': term_return,
            'terminal_absolute_return': abs(term_return),
            'terminal_match': term_match
        })
        
    df_res = pd.DataFrame(results)
    print("Generating Analysis...")
    
    def aggregate(df_slice):
        if len(df_slice) == 0: return {}
        
        same = len(df_slice[df_slice['terminal_match'] == 'SAME'])
        oppo = len(df_slice[df_slice['terminal_match'] == 'OPPOSITE'])
        neut = len(df_slice[df_slice['terminal_match'] == 'NEUTRAL'])
        tot = same + oppo + neut
        
        return {
            'N': len(df_slice),
            'terminal_same_pct': same / tot if tot > 0 else 0,
            'terminal_oppo_pct': oppo / tot if tot > 0 else 0,
            'persistence': calculate_stats(df_slice['directional_persistence']),
            'initial_excursion': calculate_stats(df_slice['initial_excursion']),
            'reversal_excursion': calculate_stats(df_slice['reversal_excursion']),
            'whipsaw_ratio': calculate_stats(df_slice['whipsaw_ratio']),
            'net_displacement': calculate_stats(df_slice['net_displacement']),
            'total_path_length': calculate_stats(df_slice['total_path_length']),
            'path_efficiency': calculate_stats(df_slice['path_efficiency']),
            'terminal_absolute_return': calculate_stats(df_slice['terminal_absolute_return'])
        }

    final_report = {}
    
    val_early = df_res.iloc[:len(df_res)//2]
    val_late = df_res.iloc[len(df_res)//2:]
    
    for state in ['ALL', 'HIGH_VOL', 'LOW_VOL']:
        if state == 'ALL':
            df_s = df_res
            df_e = val_early
            df_l = val_late
        else:
            df_s = df_res[df_res['vol_state'] == state]
            df_e = val_early[val_early['vol_state'] == state]
            df_l = val_late[val_late['vol_state'] == state]
            
        final_report[state] = {
            'FULL': aggregate(df_s),
            'EARLY': aggregate(df_e),
            'LATE': aggregate(df_l)
        }
        
    with open('reports/RC012_Study_009_results.json', 'w') as f:
        json.dump(final_report, f, indent=2)
        
    df_res.to_parquet('reports/RC012_Study_009_HIGH_VOL_Path_Dataset.parquet')
    print("Done!")

if __name__ == '__main__':
    main()
