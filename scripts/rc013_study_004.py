import pandas as pd
import numpy as np
import os

def calculate_stats(series):
    s = pd.Series(series).dropna()
    if len(s) == 0:
        return {}
    return {
        'count': int(len(s)),
        'mean': float(s.mean()),
        'median': float(s.median()),
        'std': float(s.std()),
        'q90': float(s.quantile(0.90)),
        'q95': float(s.quantile(0.95)),
        'q99': float(s.quantile(0.99))
    }

def main():
    print("Loading data...")
    df_m1 = pd.read_parquet(r'data/m1/EURUSD_M1.parquet')
    df_m1['datetime'] = pd.to_datetime(df_m1['datetime'] if 'datetime' in df_m1.columns else df_m1['timestamp'])
    
    if df_m1['datetime'].dt.tz is None:
        df_m1['datetime'] = df_m1['datetime'].dt.tz_localize('UTC')
        
    df_m1.set_index('datetime', inplace=True)
    df_m1.sort_index(inplace=True)
    df_m1 = df_m1[df_m1.index.dayofweek < 5]
    
    print("Assigning session states...")
    lon_time = df_m1.index.tz_convert('Europe/London')
    ny_time = df_m1.index.tz_convert('America/New_York')
    
    lon_float = lon_time.hour + lon_time.minute / 60.0
    ny_float = ny_time.hour + ny_time.minute / 60.0
    
    is_london = (lon_float >= 8.0) & (lon_float < 16.5)
    is_ny = (ny_float >= 8.0) & (ny_float < 17.0)
    
    is_asia = ~is_london & ~is_ny
    is_lpo = is_london & ~is_ny
    is_lno = is_london & is_ny
    is_atl_trans = (lon_float >= 7.0) & (lon_float < 9.0)
    
    dates = np.unique(lon_time.date)
    
    results = []
    
    m1_times = df_m1.index
    m1_closes = df_m1['close'].values
    
    print(f"Scanning {len(dates)} days for structural breakouts...")
    
    for d in dates:
        day_mask = lon_time.date == d
        df_day = df_m1[day_mask]
        
        # Candidate A: ASIA_TO_LONDON
        mask_ref_atl = is_asia[day_mask] & (lon_float[day_mask] < 7.0)
        mask_scan_atl = is_atl_trans[day_mask]
        
        ref_atl = df_day[mask_ref_atl]
        scan_atl = df_day[mask_scan_atl]
        
        if len(ref_atl) > 30 and len(scan_atl) > 0:
            high = ref_atl['high'].max()
            low = ref_atl['low'].min()
            
            for t, row in scan_atl.iterrows():
                direction = 0
                if row['close'] > high: direction = 1
                elif row['close'] < low: direction = -1
                
                if direction != 0:
                    entry_time = t
                    entry_price = row['close']
                    exit_time = entry_time + pd.Timedelta(hours=4)
                    
                    try:
                        exit_idx = m1_times.get_indexer([exit_time], method='ffill')[0]
                        if exit_idx != -1 and m1_times[exit_idx] > entry_time:
                            exit_price = m1_closes[exit_idx]
                            
                            # MAE/MFE Calculation
                            entry_idx = m1_times.get_indexer([entry_time], method='bfill')[0]
                            path = m1_closes[entry_idx:exit_idx+1]
                            
                            if direction == 1:
                                mfe = np.max(path) - entry_price
                                mae = np.min(path) - entry_price
                            else:
                                mfe = entry_price - np.min(path)
                                mae = entry_price - np.max(path)
                                
                            results.append({
                                'date': d,
                                'candidate': 'ASIA_TO_LONDON',
                                'trans_time': scan_atl.index[0],
                                'entry_time': entry_time,
                                'exit_time': m1_times[exit_idx],
                                'delay_mins': (entry_time - scan_atl.index[0]).total_seconds() / 60.0,
                                'direction': direction,
                                'entry_price': entry_price,
                                'exit_price': exit_price,
                                'raw_return': (exit_price - entry_price) * direction,
                                'mae': mae,
                                'mfe': mfe,
                                'range_size': high - low
                            })
                    except KeyError:
                        pass
                    break
                    
        # Candidate B: LONDON_NY_OVERLAP
        mask_ref_lno = is_lpo[day_mask]
        mask_scan_lno = is_lno[day_mask]
        
        ref_lno = df_day[mask_ref_lno]
        scan_lno = df_day[mask_scan_lno]
        
        if len(ref_lno) > 30 and len(scan_lno) > 0:
            high = ref_lno['high'].max()
            low = ref_lno['low'].min()
            
            for t, row in scan_lno.iterrows():
                direction = 0
                if row['close'] > high: direction = 1
                elif row['close'] < low: direction = -1
                
                if direction != 0:
                    entry_time = t
                    entry_price = row['close']
                    exit_time = entry_time + pd.Timedelta(hours=1)
                    
                    try:
                        exit_idx = m1_times.get_indexer([exit_time], method='ffill')[0]
                        if exit_idx != -1 and m1_times[exit_idx] > entry_time:
                            exit_price = m1_closes[exit_idx]
                            
                            entry_idx = m1_times.get_indexer([entry_time], method='bfill')[0]
                            path = m1_closes[entry_idx:exit_idx+1]
                            
                            if direction == 1:
                                mfe = np.max(path) - entry_price
                                mae = np.min(path) - entry_price
                            else:
                                mfe = entry_price - np.min(path)
                                mae = entry_price - np.max(path)
                                
                            results.append({
                                'date': d,
                                'candidate': 'LONDON_NY_OVERLAP',
                                'trans_time': scan_lno.index[0],
                                'entry_time': entry_time,
                                'exit_time': m1_times[exit_idx],
                                'delay_mins': (entry_time - scan_lno.index[0]).total_seconds() / 60.0,
                                'direction': direction,
                                'entry_price': entry_price,
                                'exit_price': exit_price,
                                'raw_return': (exit_price - entry_price) * direction,
                                'mae': mae,
                                'mfe': mfe,
                                'range_size': high - low
                            })
                    except KeyError:
                        pass
                    break
                    
    df_res = pd.DataFrame(results)
    df_res.set_index('entry_time', inplace=True)
    df_res.sort_index(inplace=True)
    
    print(f"Total Breakouts Executed: {len(df_res)}")
    
    val_early = df_res.loc['2024-01-01':'2025-03-31']
    val_late = df_res.loc['2025-04-01':]
    
    def generate_stats(df, cand_name, cost_pip=1.0):
        subset = df[df['candidate'] == cand_name].copy()
        if len(subset) == 0: return {}
        
        cost = cost_pip * 0.0001
        subset['net_return'] = subset['raw_return'] - cost
        
        wins = subset[subset['net_return'] > 0]
        losses = subset[subset['net_return'] <= 0]
        
        win_rate = len(wins) / len(subset) if len(subset) > 0 else 0
        avg_win = wins['net_return'].mean() if len(wins) > 0 else 0
        avg_loss = losses['net_return'].mean() if len(losses) > 0 else 0
        
        expectancy = subset['net_return'].mean()
        profit_factor = abs(wins['net_return'].sum() / losses['net_return'].sum()) if losses['net_return'].sum() != 0 else np.nan
        
        max_loss = subset['net_return'].min()
        q01 = subset['net_return'].quantile(0.01)
        q05 = subset['net_return'].quantile(0.05)
        q10 = subset['net_return'].quantile(0.10)
        
        total_loss = losses['net_return'].sum()
        loss_q01_sum = subset[subset['net_return'] <= q01]['net_return'].sum()
        loss_q05_sum = subset[subset['net_return'] <= q05]['net_return'].sum()
        
        longs = subset[subset['direction'] == 1]
        shorts = subset[subset['direction'] == -1]
        
        return {
            'N': len(subset),
            'longs': len(longs),
            'shorts': len(shorts),
            'win_rate': win_rate * 100,
            'avg_win': avg_win * 10000,
            'avg_loss': avg_loss * 10000,
            'expectancy': expectancy * 10000,
            'pf': profit_factor,
            'max_loss': max_loss * 10000,
            'q01': q01 * 10000,
            'q05': q05 * 10000,
            'tail_contrip_1p': (loss_q01_sum / total_loss * 100) if total_loss < 0 else 0,
            'tail_contrip_5p': (loss_q05_sum / total_loss * 100) if total_loss < 0 else 0,
            'long_exp': longs['net_return'].mean() * 10000 if len(longs) > 0 else 0,
            'short_exp': shorts['net_return'].mean() * 10000 if len(shorts) > 0 else 0,
            'mfe_mean': subset['mfe'].mean() * 10000,
            'mae_mean': subset['mae'].mean() * 10000
        }
        
    report = []
    report.append("# RC013 Study 004 - Session Breakout Monetization Analysis\n")
    
    for cand in ['ASIA_TO_LONDON', 'LONDON_NY_OVERLAP']:
        report.append(f"## {cand} Performance")
        st_10 = generate_stats(df_res, cand, cost_pip=1.0)
        st_05 = generate_stats(df_res, cand, cost_pip=0.5)
        st_20 = generate_stats(df_res, cand, cost_pip=2.0)
        
        if not st_10:
            report.append("No signals generated.")
            continue
            
        report.append(f"### Payoff (1.0 Pip Cost)")
        report.append(f"- Signals: {st_10['N']} (Long: {st_10['longs']} | Short: {st_10['shorts']})")
        report.append(f"- Expectancy: **{st_10['expectancy']:.2f} pips**")
        report.append(f"- Win Rate: {st_10['win_rate']:.1f}%")
        report.append(f"- Profit Factor: {st_10['pf']:.2f}")
        report.append(f"- Avg Win / Avg Loss: {st_10['avg_win']:.1f} / {st_10['avg_loss']:.1f}")
        report.append(f"- MFE / MAE: {st_10['mfe_mean']:.1f} / {st_10['mae_mean']:.1f}")
        
        report.append(f"### Directional Neutrality")
        report.append(f"- Long Expectancy: {st_10['long_exp']:.2f} pips")
        report.append(f"- Short Expectancy: {st_10['short_exp']:.2f} pips")
        
        report.append(f"### Tail Risk (No Stop Loss)")
        report.append(f"- Maximum Loss: {st_10['max_loss']:.1f} pips")
        report.append(f"- Worst 1% Threshold: {st_10['q01']:.1f} pips ({st_10['tail_contrip_1p']:.1f}% of total losses)")
        report.append(f"- Worst 5% Threshold: {st_10['q05']:.1f} pips ({st_10['tail_contrip_5p']:.1f}% of total losses)")
        
        report.append(f"### Cost Sensitivity (Expectancy)")
        report.append(f"- 0.5 Pip Cost: {st_05['expectancy']:.2f} pips")
        report.append(f"- 2.0 Pip Cost: {st_20['expectancy']:.2f} pips")
        
        report.append(f"### Temporal Stability (Out of Sample)")
        st_early = generate_stats(val_early, cand, cost_pip=1.0)
        st_late = generate_stats(val_late, cand, cost_pip=1.0)
        if st_early and st_late:
            report.append(f"- Early (2024-2025Q1): {st_early['expectancy']:.2f} pips (PF {st_early['pf']:.2f})")
            report.append(f"- Late (2025Q2-2026): {st_late['expectancy']:.2f} pips (PF {st_late['pf']:.2f})")
        report.append("\n---\n")

    report.append("## Relation to RC013 Study 003")
    report.append("The path geometry identified in Study 003 confirmed that these transitions produce efficient directional expansion. This breakout test directly monetizes that expansion. If expectancy is strongly positive, the structural path efficiency successfully overcomes the 1.0 pip transaction cost and the lack of a protective stop-loss. If expectancy is negative, the raw path expansion is absorbed by whipsaw tails or cost friction before the fixed horizon ends.")
    
    # Classification Logic
    def classify(st):
        if not st: return "REJECTED"
        if st['expectancy'] > 0 and st['pf'] > 1.05:
            return "CANDIDATE TRADING ARCHITECTURE"
        elif st['expectancy'] > -2.0:
            return "EXPLORATORY"
        else:
            return "REJECTED"
            
    c_atl = classify(generate_stats(df_res, 'ASIA_TO_LONDON', 1.0))
    c_lno = classify(generate_stats(df_res, 'LONDON_NY_OVERLAP', 1.0))
    
    report.append("## Candidate Classification")
    report.append(f"- **ASIA_TO_LONDON**: {c_atl}")
    report.append(f"- **LONDON_NY_OVERLAP**: {c_lno}")
    
    report.append("\n## Final Scientific Conclusion")
    report.append("This study measured whether a deterministic range breakout could convert the structural session edge into positive expectancy. The results demonstrate the raw economic value of the transition without complex exit engineering or arbitrary stop-losses.")
    
    report_path = 'reports/RC013_Study_004_Session_Breakout_Analysis.md'
    dataset_path = 'reports/RC013_Study_004_Session_Breakout_Dataset.parquet'
    
    with open(report_path, 'w') as f:
        f.write("\n".join(report))
        
    df_res.to_parquet(dataset_path)
    print(f"Artifacts saved to {report_path} and {dataset_path}")

if __name__ == '__main__':
    main()
