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
    
    # Forward Horizons
    horizons = [4, 16, 64]
    
    for h in horizons:
        m15[f'fwd_ret_{h}'] = (m15['close'].shift(-h) / m15['close']) - 1
        m15[f'fwd_abs_ret_{h}'] = m15[f'fwd_ret_{h}'].abs()
        m15[f'fwd_rv_{h}'] = m15['log_ret'].rolling(h).std().shift(-h)
        future_highs = m15['high'].rolling(h).max().shift(-h)
        future_lows = m15['low'].rolling(h).min().shift(-h)
        m15[f'fwd_up_exc_{h}'] = future_highs - m15['close']
        m15[f'fwd_dn_exc_{h}'] = m15['close'] - future_lows
        m15[f'fwd_abs_exc_{h}'] = np.maximum(m15[f'fwd_up_exc_{h}'], m15[f'fwd_dn_exc_{h}'])

    valid_data = m15[m15['vol_state'] != 'UNCLASSIFIED'].copy()

    # Split Discovery and Validation
    discovery = valid_data.loc[:'2024-06-30'].copy()
    validation = valid_data.loc['2024-07-01':].copy()

    assert discovery.index.max() <= pd.to_datetime('2024-06-30 23:59:59')
    assert validation.index.min() >= pd.to_datetime('2024-07-01 00:00:00')

    # Calculate Tail Thresholds ONLY on Discovery
    print("Calculating Tail Thresholds on Discovery Set...")
    thresholds = {}
    for h in horizons:
        p90 = discovery[f'fwd_abs_ret_{h}'].quantile(0.90)
        p95 = discovery[f'fwd_abs_ret_{h}'].quantile(0.95)
        p99 = discovery[f'fwd_abs_ret_{h}'].quantile(0.99)
        thresholds[h] = {'90': p90, '95': p95, '99': p99}

        # Apply flags to Discovery
        discovery[f'large_move_{h}_90'] = np.where(discovery[f'fwd_abs_ret_{h}'].isna(), np.nan, (discovery[f'fwd_abs_ret_{h}'] >= p90).astype(float))
        discovery[f'large_move_{h}_95'] = np.where(discovery[f'fwd_abs_ret_{h}'].isna(), np.nan, (discovery[f'fwd_abs_ret_{h}'] >= p95).astype(float))
        discovery[f'large_move_{h}_99'] = np.where(discovery[f'fwd_abs_ret_{h}'].isna(), np.nan, (discovery[f'fwd_abs_ret_{h}'] >= p99).astype(float))

        # Apply flags to Validation using Discovery thresholds
        validation[f'large_move_{h}_90'] = np.where(validation[f'fwd_abs_ret_{h}'].isna(), np.nan, (validation[f'fwd_abs_ret_{h}'] >= p90).astype(float))
        validation[f'large_move_{h}_95'] = np.where(validation[f'fwd_abs_ret_{h}'].isna(), np.nan, (validation[f'fwd_abs_ret_{h}'] >= p95).astype(float))
        validation[f'large_move_{h}_99'] = np.where(validation[f'fwd_abs_ret_{h}'].isna(), np.nan, (validation[f'fwd_abs_ret_{h}'] >= p99).astype(float))

    print("Saving Validation Dataset...")
    os.makedirs('reports', exist_ok=True)
    validation.to_parquet('reports/RC012_Study_005_Volatility_Validation_Dataset.parquet')

    # Analysis Helper
    def calc_metrics(df_part, h):
        states = ['LOW_VOL', 'NORMAL_VOL', 'HIGH_VOL']
        res = {}
        # Unconditional
        uncond_90 = df_part[f'large_move_{h}_90'].mean()
        uncond_95 = df_part[f'large_move_{h}_95'].mean()
        uncond_99 = df_part[f'large_move_{h}_99'].mean()
        
        res['UNCOND'] = {
            'P_90': uncond_90, 'P_95': uncond_95, 'P_99': uncond_99,
            'mean_abs_ret': df_part[f'fwd_abs_ret_{h}'].mean(),
            'median_abs_ret': df_part[f'fwd_abs_ret_{h}'].median(),
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
            
            res[state] = {
                'N': N,
                'P_90': cond_90,
                'P_95': cond_95,
                'P_99': cond_99,
                'Uplift_90': cond_90 - uncond_90,
                'RR_90': cond_90 / uncond_90 if uncond_90 > 0 else 0,
                'Uplift_95': cond_95 - uncond_95,
                'RR_95': cond_95 / uncond_95 if uncond_95 > 0 else 0,
                'Uplift_99': cond_99 - uncond_99,
                'RR_99': cond_99 / uncond_99 if uncond_99 > 0 else 0,
                'mean_abs_ret': df_state[f'fwd_abs_ret_{h}'].mean(),
                'median_abs_ret': df_state[f'fwd_abs_ret_{h}'].median(),
                'mean_up_exc': df_state[f'fwd_up_exc_{h}'].mean(),
                'mean_dn_exc': df_state[f'fwd_dn_exc_{h}'].mean(),
                'mean_abs_exc': df_state[f'fwd_abs_exc_{h}'].mean(),
                'mean_rv': df_state[f'fwd_rv_{h}'].mean(),
                'mean_signed_ret': df_state[f'fwd_ret_{h}'].mean(),
                'median_signed_ret': df_state[f'fwd_ret_{h}'].median(),
                'prob_pos_ret': (df_state[f'fwd_ret_{h}'] > 0).mean(),
                'prob_neg_ret': (df_state[f'fwd_ret_{h}'] < 0).mean()
            }
        return res

    # Generate Analysis
    print("Generating Analysis...")
    analysis = {}
    
    # 1. Discovery Reference (Non-Overlapping)
    analysis['DISCOVERY'] = {}
    for h in horizons:
        # Thin the discovery set by h
        disc_thinned = discovery.iloc[::h].dropna(subset=[f'fwd_abs_ret_{h}'])
        analysis['DISCOVERY'][h] = calc_metrics(disc_thinned, h)

    # 2. Validation Descriptive (Full-Resolution)
    analysis['VALIDATION_DESCRIPTIVE'] = {}
    for h in horizons:
        val_full = validation.dropna(subset=[f'fwd_abs_ret_{h}'])
        analysis['VALIDATION_DESCRIPTIVE'][h] = calc_metrics(val_full, h)

    # 3. Validation Inferential (Non-Overlapping)
    analysis['VALIDATION_INFERENTIAL'] = {}
    for h in horizons:
        val_thinned = validation.iloc[::h].dropna(subset=[f'fwd_abs_ret_{h}'])
        analysis['VALIDATION_INFERENTIAL'][h] = calc_metrics(val_thinned, h)
        
    # 4. Temporal Stability (Validation Inferential Split)
    analysis['VALIDATION_INFERENTIAL_EARLY'] = {}
    analysis['VALIDATION_INFERENTIAL_LATE'] = {}
    
    val_early = validation.iloc[:len(validation)//2]
    val_late = validation.iloc[len(validation)//2:]

    for h in horizons:
        val_early_thinned = val_early.iloc[::h].dropna(subset=[f'fwd_abs_ret_{h}'])
        val_late_thinned = val_late.iloc[::h].dropna(subset=[f'fwd_abs_ret_{h}'])
        analysis['VALIDATION_INFERENTIAL_EARLY'][h] = calc_metrics(val_early_thinned, h)
        analysis['VALIDATION_INFERENTIAL_LATE'][h] = calc_metrics(val_late_thinned, h)

    with open('reports/RC012_Study_005_results.json', 'w') as f:
        json.dump(analysis, f, indent=2)
        
    print("Done!")

if __name__ == '__main__':
    main()
