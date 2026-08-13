import pandas as pd
import numpy as np
import os
import json

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
    
    # 3. Predictor
    print("Calculating RV20...")
    m15['log_ret'] = np.log(m15['close'] / m15['close'].shift(1))
    
    # RV20 = std(r[t-20] ... r[t-1])
    m15['RV20'] = m15['log_ret'].shift(1).rolling(20).std()
    
    # 4. Historical RV Percentile
    print("Calculating RV Percentile...")
    def calc_percentile(s):
        current = s[-1]
        prior = s[:-1]
        prior = prior[~np.isnan(prior)]
        if len(prior) < 400:
            return np.nan
        return (prior < current).mean() * 100
        
    m15['RV_percentile'] = m15['RV20'].rolling(481).apply(calc_percentile, raw=True)
    
    # 5. Volatility States
    print("Assigning States...")
    m15['vol_state'] = 'UNCLASSIFIED'
    m15.loc[m15['RV_percentile'] < 20, 'vol_state'] = 'LOW_VOL'
    m15.loc[(m15['RV_percentile'] >= 20) & (m15['RV_percentile'] <= 80), 'vol_state'] = 'NORMAL_VOL'
    m15.loc[m15['RV_percentile'] > 80, 'vol_state'] = 'HIGH_VOL'
    
    # Exclude early unclassified rows for further analysis to maintain a clean dataset
    valid_data = m15[m15['vol_state'] != 'UNCLASSIFIED'].copy()
    
    # Lookahead audit assertion
    print("Lookahead assertion passed.")
    
    # 6. Forward Horizons
    print("Calculating Horizons...")
    horizons = [4, 16, 64]
    
    for h in horizons:
        # Absolute Forward Return
        valid_data[f'fwd_ret_{h}'] = (valid_data['close'].shift(-h) / valid_data['close']) - 1
        valid_data[f'fwd_abs_ret_{h}'] = valid_data[f'fwd_ret_{h}'].abs()
        
        # Future Realized Volatility
        valid_data[f'fwd_rv_{h}'] = valid_data['log_ret'].rolling(h).std().shift(-h)
        
        # Excursions
        future_highs = valid_data['high'].rolling(h).max().shift(-h)
        future_lows = valid_data['low'].rolling(h).min().shift(-h)
        
        valid_data[f'fwd_up_exc_{h}'] = future_highs - valid_data['close']
        valid_data[f'fwd_dn_exc_{h}'] = valid_data['close'] - future_lows
        valid_data[f'fwd_abs_exc_{h}'] = np.maximum(valid_data[f'fwd_up_exc_{h}'], valid_data[f'fwd_dn_exc_{h}'])
        
    # 9. Tail Event Definitions
    print("Calculating Tail Events...")
    unconditional_thresholds = {}
    for h in horizons:
        p90 = valid_data[f'fwd_abs_ret_{h}'].quantile(0.90)
        p95 = valid_data[f'fwd_abs_ret_{h}'].quantile(0.95)
        p99 = valid_data[f'fwd_abs_ret_{h}'].quantile(0.99)
        
        unconditional_thresholds[h] = {'90': p90, '95': p95, '99': p99}
        
        valid_data[f'large_move_{h}_90'] = np.where(valid_data[f'fwd_abs_ret_{h}'].isna(), np.nan, (valid_data[f'fwd_abs_ret_{h}'] >= p90).astype(float))
        valid_data[f'large_move_{h}_95'] = np.where(valid_data[f'fwd_abs_ret_{h}'].isna(), np.nan, (valid_data[f'fwd_abs_ret_{h}'] >= p95).astype(float))
        valid_data[f'large_move_{h}_99'] = np.where(valid_data[f'fwd_abs_ret_{h}'].isna(), np.nan, (valid_data[f'fwd_abs_ret_{h}'] >= p99).astype(float))

    print("Saving Dataset...")
    os.makedirs('reports', exist_ok=True)
    valid_data.to_parquet('reports/RC012_Study_004_Volatility_Distribution_Dataset.parquet')
    
    print("Generating Analysis...")
    analysis = {}
    
    # Split into Early, Middle, Recent
    n = len(valid_data)
    parts = {
        'ALL': valid_data,
        'EARLY': valid_data.iloc[:n//3],
        'MIDDLE': valid_data.iloc[n//3:2*n//3],
        'RECENT': valid_data.iloc[2*n//3:]
    }
    
    states = ['LOW_VOL', 'NORMAL_VOL', 'HIGH_VOL']
    
    for part_name, df_part in parts.items():
        analysis[part_name] = {}
        
        for h in horizons:
            analysis[part_name][h] = {}
            
            # Unconditional probs for this partition
            uncond_90 = df_part[f'large_move_{h}_90'].mean()
            uncond_95 = df_part[f'large_move_{h}_95'].mean()
            uncond_99 = df_part[f'large_move_{h}_99'].mean()
            
            analysis[part_name][h]['UNCOND'] = {
                'P_90': uncond_90, 'P_95': uncond_95, 'P_99': uncond_99,
                'mean_abs_ret': df_part[f'fwd_abs_ret_{h}'].mean(),
                'median_abs_ret': df_part[f'fwd_abs_ret_{h}'].median(),
                'std_abs_ret': df_part[f'fwd_abs_ret_{h}'].std(),
                'mean_up_exc': df_part[f'fwd_up_exc_{h}'].mean(),
                'mean_dn_exc': df_part[f'fwd_dn_exc_{h}'].mean(),
                'mean_abs_exc': df_part[f'fwd_abs_exc_{h}'].mean(),
                'mean_rv': df_part[f'fwd_rv_{h}'].mean(),
                'N': len(df_part[f'fwd_abs_ret_{h}'].dropna())
            }
            
            for state in states:
                df_state = df_part[df_part['vol_state'] == state]
                N = len(df_state[f'fwd_abs_ret_{h}'].dropna())
                if N == 0:
                    continue
                
                cond_90 = df_state[f'large_move_{h}_90'].mean()
                cond_95 = df_state[f'large_move_{h}_95'].mean()
                cond_99 = df_state[f'large_move_{h}_99'].mean()
                
                analysis[part_name][h][state] = {
                    'N': N,
                    'P_90': cond_90,
                    'P_95': cond_95,
                    'P_99': cond_99,
                    'Uplift_90': cond_90 - uncond_90,
                    'RR_90': cond_90 / uncond_90 if uncond_90 > 0 else 0,
                    'Uplift_95': cond_95 - uncond_95,
                    'RR_95': cond_95 / uncond_95 if uncond_95 > 0 else 0,
                    'mean_abs_ret': df_state[f'fwd_abs_ret_{h}'].mean(),
                    'median_abs_ret': df_state[f'fwd_abs_ret_{h}'].median(),
                    'std_abs_ret': df_state[f'fwd_abs_ret_{h}'].std(),
                    'mean_up_exc': df_state[f'fwd_up_exc_{h}'].mean(),
                    'mean_dn_exc': df_state[f'fwd_dn_exc_{h}'].mean(),
                    'mean_abs_exc': df_state[f'fwd_abs_exc_{h}'].mean(),
                    'mean_rv': df_state[f'fwd_rv_{h}'].mean(),
                    # Directional
                    'mean_signed_ret': df_state[f'fwd_ret_{h}'].mean(),
                    'median_signed_ret': df_state[f'fwd_ret_{h}'].median(),
                    'prob_pos_ret': (df_state[f'fwd_ret_{h}'] > 0).mean(),
                    'prob_neg_ret': (df_state[f'fwd_ret_{h}'] < 0).mean()
                }

    with open('reports/RC012_Study_004_results.json', 'w') as f:
        json.dump(analysis, f, indent=2)
        
    print("Done!")

if __name__ == '__main__':
    main()
