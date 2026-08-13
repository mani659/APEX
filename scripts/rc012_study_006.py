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
    
    # Predictor
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
    
    horizons = [4, 16, 64]
    
    print("Calculating Movement and Excursions...")
    for h in horizons:
        m15[f'fwd_move_raw_{h}'] = m15['close'].shift(-h) - m15['close']
        m15[f'gross_movement_{h}'] = m15[f'fwd_move_raw_{h}'].abs()
        
        future_highs = m15['high'].rolling(h).max().shift(-h)
        future_lows = m15['low'].rolling(h).min().shift(-h)
        
        m15[f'fwd_up_exc_{h}'] = future_highs - m15['close']
        m15[f'fwd_dn_exc_{h}'] = m15['close'] - future_lows
        m15[f'fwd_abs_exc_{h}'] = np.maximum(m15[f'fwd_up_exc_{h}'], m15[f'fwd_dn_exc_{h}'])

    valid_data = m15[m15['vol_state'] != 'UNCLASSIFIED'].copy()

    discovery = valid_data.loc[:'2024-06-30'].copy()
    validation = valid_data.loc['2024-07-01':].copy()

    print("Calculating Discovery Baselines...")
    baselines = {}
    for h in horizons:
        # Baseline Movement = mean(Gross Movement) on Discovery Set
        base_mean = discovery[f'gross_movement_{h}'].mean()
        baselines[h] = base_mean
        
        # Calculate Excess Movement for Validation
        validation[f'excess_movement_{h}'] = validation[f'gross_movement_{h}'] - base_mean
        
        # Calculate Net Edge for different friction assumptions
        for f_pips in [0.5, 1.0, 2.0]:
            f_val = f_pips * 0.0001
            validation[f'net_edge_{h}_{f_pips}'] = validation[f'excess_movement_{h}'] - f_val

    print("Saving Validation Dataset...")
    os.makedirs('reports', exist_ok=True)
    validation.to_parquet('reports/RC012_Study_006_Volatility_Monetization_Dataset.parquet')

    def calc_metrics(df_part, h):
        states = ['ALL', 'LOW_VOL', 'NORMAL_VOL', 'HIGH_VOL']
        res = {}
        for state in states:
            if state == 'ALL':
                df_state = df_part
            else:
                df_state = df_part[df_part['vol_state'] == state]
                
            df_state = df_state.dropna(subset=[f'gross_movement_{h}'])
            N = len(df_state)
            if N == 0:
                continue
                
            pos_moves = df_state[df_state[f'fwd_move_raw_{h}'] > 0]
            neg_moves = df_state[df_state[f'fwd_move_raw_{h}'] < 0]

            res[state] = {
                'N': N,
                'mean_gross': df_state[f'gross_movement_{h}'].mean(),
                'median_gross': df_state[f'gross_movement_{h}'].median(),
                'baseline_movement': baselines[h],
                'mean_excess': df_state[f'excess_movement_{h}'].mean(),
                
                'mean_net_1.0': df_state[f'net_edge_{h}_1.0'].mean(),
                'median_net_1.0': df_state[f'net_edge_{h}_1.0'].median(),
                'prob_pos_net_1.0': (df_state[f'net_edge_{h}_1.0'] > 0).mean(),
                'std_net_1.0': df_state[f'net_edge_{h}_1.0'].std(),
                'p90_net_1.0': df_state[f'net_edge_{h}_1.0'].quantile(0.90),
                'p95_net_1.0': df_state[f'net_edge_{h}_1.0'].quantile(0.95),
                'p99_net_1.0': df_state[f'net_edge_{h}_1.0'].quantile(0.99),
                
                'mean_net_0.5': df_state[f'net_edge_{h}_0.5'].mean(),
                'mean_net_2.0': df_state[f'net_edge_{h}_2.0'].mean(),

                'mean_up_exc': df_state[f'fwd_up_exc_{h}'].mean(),
                'mean_dn_exc': df_state[f'fwd_dn_exc_{h}'].mean(),
                'mean_abs_exc': df_state[f'fwd_abs_exc_{h}'].mean(),
                
                'pos_term_prob': len(pos_moves)/N if N>0 else 0,
                'neg_term_prob': len(neg_moves)/N if N>0 else 0,
                'mean_pos_term_mag': pos_moves[f'gross_movement_{h}'].mean() if len(pos_moves)>0 else 0,
                'mean_neg_term_mag': neg_moves[f'gross_movement_{h}'].mean() if len(neg_moves)>0 else 0
            }
        return res

    print("Generating Analysis...")
    analysis = {}
    
    # 1. Validation Inferential (Non-Overlapping)
    analysis['VALIDATION_INFERENTIAL'] = {}
    for h in horizons:
        val_thinned = validation.iloc[::h]
        analysis['VALIDATION_INFERENTIAL'][h] = calc_metrics(val_thinned, h)
        
    # 2. Temporal Stability (Early vs Late)
    val_early = validation.iloc[:len(validation)//2]
    val_late = validation.iloc[len(validation)//2:]

    analysis['EARLY'] = {}
    analysis['LATE'] = {}
    
    for h in horizons:
        val_early_thinned = val_early.iloc[::h]
        val_late_thinned = val_late.iloc[::h]
        analysis['EARLY'][h] = calc_metrics(val_early_thinned, h)
        analysis['LATE'][h] = calc_metrics(val_late_thinned, h)

    with open('reports/RC012_Study_006_results.json', 'w') as f:
        json.dump(analysis, f, indent=2)
        
    print("Done!")

if __name__ == '__main__':
    main()
