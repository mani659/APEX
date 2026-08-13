import os
import pandas as pd
import numpy as np

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = np.maximum(high_low, np.maximum(high_close, low_close))
    return tr.rolling(window=period).mean()

def run_study():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data', 'm1')
    reports_dir = os.path.join(base_dir, 'reports')
    
    eurusd_path = os.path.join(data_dir, 'EURUSD_M1.parquet')
    
    print("Loading EURUSD M1...")
    df_m1 = pd.read_parquet(eurusd_path)
    df_m1['timestamp'] = pd.to_datetime(df_m1['timestamp'])
    
    tz_info = "Timezone aware" if df_m1['timestamp'].dt.tz is not None else "Naive timestamps"
    print(f"Timestamp format: {tz_info}")
    
    df_m1 = df_m1.sort_values('timestamp').reset_index(drop=True)
    
    print("Extracting EURUSD M1 Blocks...")
    df_m1['atr_14'] = calculate_atr(df_m1, 14)
    df_m1['block_range_15'] = df_m1['high'].rolling(15).max() - df_m1['low'].rolling(15).min()
    df_m1['block_ret_15'] = df_m1['close'] - df_m1['close'].shift(15)
    
    indexer_60 = pd.api.indexers.FixedForwardWindowIndexer(window_size=60)
    df_m1['fwd_high_60'] = df_m1['high'].shift(-1).rolling(window=indexer_60).max()
    df_m1['fwd_low_60'] = df_m1['low'].shift(-1).rolling(window=indexer_60).min()
    df_m1['fwd_close_60'] = df_m1['close'].shift(-60)
    
    indexer_240 = pd.api.indexers.FixedForwardWindowIndexer(window_size=240)
    df_m1['fwd_high_240'] = df_m1['high'].shift(-1).rolling(window=indexer_240).max()
    df_m1['fwd_low_240'] = df_m1['low'].shift(-1).rolling(window=indexer_240).min()
    df_m1['fwd_close_240'] = df_m1['close'].shift(-240)
    
    blocks = df_m1.iloc[15::15].copy().reset_index(drop=True)
    blocks['start_atr'] = blocks['atr_14'].shift(1)
    
    blocks['vol_pct_25'] = blocks['block_range_15'].rolling(480).quantile(0.25)
    blocks['vol_pct_75'] = blocks['block_range_15'].rolling(480).quantile(0.75)
    
    blocks['vol_state'] = np.where(blocks['block_range_15'] < blocks['vol_pct_25'], 'LOW_VOL',
                          np.where(blocks['block_range_15'] > blocks['vol_pct_75'], 'HIGH_VOL', 'NORMAL_VOL'))
    blocks['vol_state'] = np.where(blocks['vol_pct_25'].isna(), None, blocks['vol_state'])
                          
    blocks['norm_ret'] = blocks['block_ret_15'] / (blocks['start_atr'] + 1e-9)
    blocks['dir_state'] = np.where(blocks['norm_ret'] > 1.0, 'BULL',
                          np.where(blocks['norm_ret'] < -1.0, 'BEAR', 'FLAT'))
    blocks['dir_state'] = np.where(blocks['norm_ret'].isna(), None, blocks['dir_state'])
                          
    blocks['m1_state'] = blocks['vol_state'] + '_' + blocks['dir_state']
    
    blocks = blocks.dropna(subset=['vol_pct_25', 'fwd_close_240']).copy()
    
    blocks['ret_60'] = blocks['fwd_close_60'] - blocks['close']
    blocks['ret_240'] = blocks['fwd_close_240'] - blocks['close']
    blocks['mfe_60'] = blocks['fwd_high_60'] - blocks['close']
    blocks['mae_60'] = blocks['close'] - blocks['fwd_low_60']
    
    print("Constructing H4 Regime...")
    df_tmp = df_m1.set_index('timestamp')
    df_h4 = df_tmp.resample('4h', closed='left', label='left').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    }).dropna().reset_index()
    
    df_h4['atr_14'] = calculate_atr(df_h4, 14)
    df_h4['block_range_15'] = df_h4['high'].rolling(15).max() - df_h4['low'].rolling(15).min()
    df_h4['block_ret_15'] = df_h4['close'] - df_h4['close'].shift(15)
    df_h4['start_atr'] = df_h4['atr_14'].shift(15)
    
    df_h4['vol_pct_25'] = df_h4['block_range_15'].rolling(480).quantile(0.25)
    df_h4['vol_pct_75'] = df_h4['block_range_15'].rolling(480).quantile(0.75)
    
    df_h4['vol_state'] = np.where(df_h4['block_range_15'] < df_h4['vol_pct_25'], 'LOW_VOL',
                          np.where(df_h4['block_range_15'] > df_h4['vol_pct_75'], 'HIGH_VOL', 'NORMAL_VOL'))
    df_h4['vol_state'] = np.where(df_h4['vol_pct_25'].isna(), None, df_h4['vol_state'])
    
    df_h4['norm_ret'] = df_h4['block_ret_15'] / (df_h4['start_atr'] + 1e-9)
    df_h4['dir_state'] = np.where(df_h4['norm_ret'] > 1.0, 'BULL',
                          np.where(df_h4['norm_ret'] < -1.0, 'BEAR', 'FLAT'))
    df_h4['dir_state'] = np.where(df_h4['norm_ret'].isna(), None, df_h4['dir_state'])
                          
    df_h4['h4_state'] = df_h4['vol_state'] + '_' + df_h4['dir_state']
    
    df_h4 = df_h4.dropna(subset=['h4_state'])
    df_h4 = df_h4[df_h4['h4_state'].str.contains('None') == False]
    
    df_h4['h4_close_time'] = df_h4['timestamp'] + pd.Timedelta(hours=4)
    df_h4 = df_h4[['h4_close_time', 'h4_state']].copy()
    
    print("Merging M1 and H4 with Lookahead Protection...")
    blocks = blocks.sort_values('timestamp')
    df_h4 = df_h4.sort_values('h4_close_time')
    
    merged = pd.merge_asof(
        blocks,
        df_h4,
        left_on="timestamp",
        right_on="h4_close_time",
        direction="backward"
    )
    
    violations = (merged['h4_close_time'] > merged['timestamp']).sum()
    unmatched = merged['h4_state'].isna().sum()
    matched = len(merged) - unmatched
    
    print(f"Lookahead Audit violations: {violations}")
    if violations > 0:
        raise ValueError("LOOKAHEAD VIOLATION DETECTED!")
        
    merged['h4_state'] = merged['h4_state'].fillna("MISSING")
    
    analyze_and_report(merged, reports_dir, len(blocks), matched, unmatched, violations, tz_info)

def get_direction_metrics(df_sub):
    if len(df_sub) == 0: return 0.0, 0.0
    s_ret = np.sign(df_sub['ret_60'])
    s_block = np.sign(df_sub['block_ret_15'])
    valid = (s_ret != 0) & (s_block != 0)
    cont = (s_ret == s_block) & valid
    rev = (s_ret != s_block) & valid
    return cont.mean() * 100, rev.mean() * 100

def analyze_and_report(merged, reports_dir, total_m1, matched, unmatched, violations, tz_info):
    report_path = os.path.join(reports_dir, "RC009_Study_006_HTF_Regime_Analysis.md")
    
    df = merged[merged['h4_state'] != "MISSING"]
    
    m1_states = df['m1_state'].value_counts()
    
    model_a_stats = {}
    for state in sorted(m1_states.index):
        sub = df[df['m1_state'] == state]
        n = len(sub)
        cont_pct, rev_pct = get_direction_metrics(sub)
        model_a_stats[state] = {
            'n': n,
            'mean_60': sub['ret_60'].mean(),
            'std_60': sub['ret_60'].std(),
            'med_60': sub['ret_60'].median(),
            'mean_240': sub['ret_240'].mean(),
            'med_240': sub['ret_240'].median(),
            'mean_mfe': sub['mfe_60'].mean(),
            'mean_mae': sub['mae_60'].mean(),
            'cont': cont_pct,
            'rev': rev_pct
        }
        
    combinations = []
    for (m1_s, h4_s), sub in df.groupby(['m1_state', 'h4_state']):
        n = len(sub)
        base = model_a_stats[m1_s]
        
        if n > 1 and base['n'] > 1:
            mean_60 = sub['ret_60'].mean()
            std_60 = sub['ret_60'].std()
            pooled_std = np.sqrt(((n-1)*std_60**2 + (base['n']-1)*base['std_60']**2) / (n+base['n']-2))
            d = (mean_60 - base['mean_60']) / (pooled_std + 1e-9)
        else:
            mean_60 = sub['ret_60'].mean() if n > 0 else 0
            d = 0.0
            
        combinations.append({
            'M1_State': m1_s,
            'H4_State': h4_s,
            'N': n,
            'Mean_60': mean_60,
            'Med_60': sub['ret_60'].median() if n > 0 else 0,
            'Base_Mean': base['mean_60'],
            'Cohen_D': d,
            'Sub_Df': sub 
        })
        
    combinations.sort(key=lambda x: abs(x['Cohen_D']), reverse=True)
    
    total_eval = len(combinations)
    n_gte_100 = sum(1 for c in combinations if c['N'] >= 100)
    n_gte_500 = sum(1 for c in combinations if c['N'] >= 500)
    highlighted = sum(1 for c in combinations if c['N'] >= 500 and abs(c['Cohen_D']) >= 0.2)
    
    candidates = []
    for c in combinations:
        if c['N'] >= 500 and abs(c['Cohen_D']) >= 0.2:
            sub = c['Sub_Df'].sort_values('timestamp')
            third = len(sub) // 3
            m1 = sub.iloc[:third]['ret_60'].mean()
            m2 = sub.iloc[third:2*third]['ret_60'].mean()
            m3 = sub.iloc[2*third:]['ret_60'].mean()
            
            base_m = c['Base_Mean']
            sign1 = np.sign(m1 - base_m)
            sign2 = np.sign(m2 - base_m)
            sign3 = np.sign(m3 - base_m)
            
            stability = "Stable" if (sign1 == sign2 == sign3) else "Unstable"
            classification = "CANDIDATE" if stability == "Stable" else "EXPLORATORY"
            
            c['Stability'] = f"{m1:.5f} / {m2:.5f} / {m3:.5f} ({stability})"
            c['Classification'] = classification
            candidates.append(c)

    with open(report_path, 'w') as f:
        f.write("# RC009 Study 006 — HTF Regime Analysis\n\n")
        f.write("## 1. H4 Construction Methodology & Timezone\n")
        f.write("- **Resampling:** 4H boundaries (closed left, labeled left)\n")
        f.write(f"- **Timezone Format:** {tz_info}\n")
        f.write("- **Lookback Volatility Window:** 480 completed H4 bars\n")
        f.write("- **State:** 9-state (Vol/Dir) identically matched to M1\n\n")
        
        f.write("## 2. Lookahead Audit\n")
        f.write(f"- Total M1 Anchors: {total_m1}\n")
        f.write(f"- Matched H4 States: {matched}\n")
        f.write(f"- Unmatched (Missing): {unmatched}\n")
        f.write(f"- Lookahead Violations (h4_close_time > m1_timestamp): **{violations}**\n\n")
        
        f.write("## 3. Model A — M1 Baseline\n")
        f.write("| M1 State | N | Mean 60 | Med 60 | Mean 240 | Med 240 | Mean MFE | Mean MAE | Cont % | Rev % |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for state, s in model_a_stats.items():
            f.write(f"| {state} | {s['n']} | {s['mean_60']:.5f} | {s['med_60']:.5f} | {s['mean_240']:.5f} | {s['med_240']:.5f} | {s['mean_mfe']:.5f} | {s['mean_mae']:.5f} | {s['cont']:.1f}% | {s['rev']:.1f}% |\n")
        f.write("\n")
        
        f.write("## 4. Multiple-Testing Disclosure\n")
        f.write(f"- 9 M1 states, 9 H4 states, 81 theoretical combinations\n")
        f.write(f"- Number populated: {total_eval}\n")
        f.write(f"- Number with N >= 100: {n_gte_100}\n")
        f.write(f"- Number with N >= 500: {n_gte_500}\n")
        f.write(f"- Number highlighted (|d| >= 0.2 & N >= 500): {highlighted}\n\n")
        
        f.write("## 5. Candidate Register\n")
        if len(candidates) > 0:
            f.write("| M1 State | H4 State | N | Mean | Base Mean | Cohen D | Stability (P1/P2/P3) | Class |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for c in candidates:
                f.write(f"| {c['M1_State']} | {c['H4_State']} | {c['N']} | {c['Mean_60']:.5f} | {c['Base_Mean']:.5f} | {c['Cohen_D']:.3f} | {c['Stability']} | {c['Classification']} |\n")
        else:
            f.write("None.\n")
        f.write("\n")
        
        f.write("## 6. Top Exploratory / Limited Sample Combinations (100 <= N < 500)\n")
        exp = [c for c in combinations if 100 <= c['N'] < 500]
        if len(exp) > 0:
            f.write("| M1 State | H4 State | N | Mean | Base Mean | Cohen D |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for c in exp[:20]: 
                f.write(f"| {c['M1_State']} | {c['H4_State']} | {c['N']} | {c['Mean_60']:.5f} | {c['Base_Mean']:.5f} | {c['Cohen_D']:.3f} |\n")
        else:
            f.write("None.\n")
        f.write("\n")
        
        f.write("## 7. Rejected Register (N >= 500, |d| < 0.2)\n")
        rej = [c for c in combinations if c['N'] >= 500 and abs(c['Cohen_D']) < 0.2]
        if len(rej) > 0:
            f.write("| M1 State | H4 State | N | Mean | Base Mean | Cohen D |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for c in rej[:20]: 
                f.write(f"| {c['M1_State']} | {c['H4_State']} | {c['N']} | {c['Mean_60']:.5f} | {c['Base_Mean']:.5f} | {c['Cohen_D']:.3f} |\n")
        else:
            f.write("None.\n")
        f.write("\n")
        
        f.write("## 8. Final RC009 Decision\n")
        if len(candidates) > 0:
            f.write("**CANDIDATE FOR FUTURE VALIDATION**\n\n")
            f.write("The H4 regime materially changes the expected behavior of certain EURUSD M1 states. ")
            f.write("RC009 is now closed, and this finding will be advanced to an independent validation campaign.\n")
        else:
            f.write("**RC009 FINAL RESULT — NEGATIVE**\n\n")
            f.write("The H4 regime does NOT provide meaningful incremental predictive structure over the M1 state in isolation. ")
            f.write("All structural behavioral hypotheses tested under RC009 are rejected. The discovery campaign is permanently closed.\n")

    out_path = os.path.join(reports_dir, "RC009_Study_006_HTF_Regime_Dataset.parquet")
    merged.to_parquet(out_path, index=False)
    print("Done!")

if __name__ == "__main__":
    run_study()
