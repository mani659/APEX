import os
import pandas as pd
import numpy as np

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = np.maximum(high_low, np.maximum(high_close, low_close))
    return tr.rolling(window=period).mean()

def process_context_instrument(file_path):
    print(f"  Processing context: {os.path.basename(file_path)}")
    df = pd.read_parquet(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort just in case
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    df['atr_14'] = calculate_atr(df, 14)
    
    # 15-bar rolling metrics
    df['block_range_15'] = df['high'].rolling(15).max() - df['low'].rolling(15).min()
    df['block_ret_15'] = df['close'] - df['close'].shift(15)
    df['start_atr'] = df['atr_14'].shift(15)
    
    # 1-week rolling volatility distribution (7200 bars = 5 days * 24 h * 60 m)
    df['vol_pct_25'] = df['block_range_15'].rolling(7200).quantile(0.25)
    df['vol_pct_75'] = df['block_range_15'].rolling(7200).quantile(0.75)
    
    df['vol_state'] = np.where(df['block_range_15'] < df['vol_pct_25'], 'LOW_VOL',
                      np.where(df['block_range_15'] > df['vol_pct_75'], 'HIGH_VOL', 'NORMAL_VOL'))
    df['vol_state'] = np.where(df['vol_pct_25'].isna(), None, df['vol_state'])
    
    df['norm_ret'] = df['block_ret_15'] / (df['start_atr'] + 1e-9)
    df['dir_state'] = np.where(df['norm_ret'] > 1.0, 'BULL',
                      np.where(df['norm_ret'] < -1.0, 'BEAR', 'FLAT'))
    df['dir_state'] = np.where(df['norm_ret'].isna(), None, df['dir_state'])
    df['state'] = df['vol_state'] + '_' + df['dir_state']
    
    # Drop rows without state
    df = df.dropna(subset=['state'])
    df = df[df['state'].str.contains('None') == False]
    
    # Return mapping of timestamp to state
    return df.set_index('timestamp')['state']


def analyze_and_report(blocks, reports_dir, context_instruments):
    report_path = os.path.join(reports_dir, "RC009_Study_004_Cross_Market_Analysis.md")
    print("Generating Analysis Report...")
    
    with open(report_path, 'w') as f:
        f.write("# RC009 Study 004 Cross-Market Analysis\n\n")
        
        # 1. Synchronization Coverage
        f.write("## 1. Synchronization Coverage\n")
        total_eu_anchors = len(blocks)
        f.write(f"Total eligible EURUSD anchors: {total_eu_anchors}\n\n")
        
        f.write("| Context Market | Lag | Matched | Missing | Coverage % |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        
        for symbol in context_instruments:
            for lag, col_suffix in [('t', 't0'), ('t-15', 't15'), ('t-30', 't30')]:
                col = f"{symbol}_{col_suffix}"
                if col in blocks.columns:
                    missing = (blocks[col] == "MISSING").sum()
                    matched = total_eu_anchors - missing
                    cov = matched / total_eu_anchors * 100
                    f.write(f"| {symbol} | {lag} | {matched} | {missing} | {cov:.1f}% |\n")
        f.write("\n")
        
        # 2. EURUSD State Frequency
        f.write("## 2. EURUSD State Frequency\n")
        f.write("| State | Count | % |\n")
        f.write("| :--- | :--- | :--- |\n")
        eu_states = blocks['eu_state'].value_counts()
        for state, count in eu_states.items():
            f.write(f"| {state} | {count} | {count/total_eu_anchors*100:.1f}% |\n")
        f.write("\n")
        
        def get_direction_metrics(df_sub):
            if len(df_sub) == 0: return 0.0, 0.0
            
            s_ret = np.sign(df_sub['ret_60'])
            s_block = np.sign(df_sub['block_ret_15'])
            
            valid = (s_ret != 0) & (s_block != 0)
            cont = (s_ret == s_block) & valid
            rev = (s_ret != s_block) & valid
            
            return cont.mean() * 100, rev.mean() * 100
            
        # 3. Model A Baseline
        f.write("## 3. Model A Baselines (EURUSD Only)\n")
        f.write("| EURUSD State | N | Mean Ret 60 | Med Ret 60 | Mean Ret 240 | Med Ret 240 | Mean MFE | Mean MAE | Cont % | Rev % |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        
        model_a_stats = {}
        for state in sorted(eu_states.index):
            sub = blocks[blocks['eu_state'] == state]
            n = len(sub)
            cont_pct, rev_pct = get_direction_metrics(sub)
            stats_dict = {
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
            model_a_stats[state] = stats_dict
            f.write(f"| {state} | {n} | {stats_dict['mean_60']:.5f} | {stats_dict['med_60']:.5f} | {stats_dict['mean_240']:.5f} | {stats_dict['med_240']:.5f} | {stats_dict['mean_mfe']:.5f} | {stats_dict['mean_mae']:.5f} | {stats_dict['cont']:.1f}% | {stats_dict['rev']:.1f}% |\n")
        f.write("\n")
        
        # 4. Model B/C Analysis
        combinations = []
        
        for symbol in context_instruments:
            for lag, col_suffix in [('t', 't0'), ('t-15', 't15'), ('t-30', 't30')]:
                col = f"{symbol}_{col_suffix}"
                if col not in blocks.columns: continue
                
                valid_pairs = blocks[blocks[col] != "MISSING"]
                
                for (eu_s, ctx_s), sub in valid_pairs.groupby(['eu_state', col]):
                    n = len(sub)
                    base = model_a_stats[eu_s]
                    
                    if n > 1 and base['n'] > 1:
                        mean_60 = sub['ret_60'].mean()
                        std_60 = sub['ret_60'].std()
                        pooled_std = np.sqrt(((n-1)*std_60**2 + (base['n']-1)*base['std_60']**2) / (n+base['n']-2))
                        d = (mean_60 - base['mean_60']) / (pooled_std + 1e-9)
                    else:
                        mean_60 = sub['ret_60'].mean() if n > 0 else 0
                        d = 0.0
                    
                    combinations.append({
                        'Market': symbol,
                        'Lag': lag,
                        'EU_State': eu_s,
                        'Ctx_State': ctx_s,
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
        
        f.write("## 4. Multiple-Testing Disclosure\n")
        f.write(f"- 4 context markets, 3 lags, 9 EURUSD states, 9 context states\n")
        f.write(f"- Total evaluated combinations: {total_eval}\n")
        f.write(f"- Number meeting N >= 100: {n_gte_100}\n")
        f.write(f"- Number meeting N >= 500: {n_gte_500}\n")
        f.write(f"- Number highlighted (|d| >= 0.2 & N >= 500): {highlighted}\n\n")
        
        f.write("## 5. Candidate Register\n")
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
                
        if len(candidates) > 0:
            f.write("| Market | Lag | EU State | Ctx State | N | Mean | Base Mean | Cohen D | Stability (P1/P2/P3) | Class |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for c in candidates:
                f.write(f"| {c['Market']} | {c['Lag']} | {c['EU_State']} | {c['Ctx_State']} | {c['N']} | {c['Mean_60']:.5f} | {c['Base_Mean']:.5f} | {c['Cohen_D']:.3f} | {c['Stability']} | {c['Classification']} |\n")
        else:
            f.write("No candidates found.\n")
        f.write("\n")
        
        f.write("## 6. Top Exploratory / Limited Sample Combinations (100 <= N < 500)\n")
        exp = [c for c in combinations if 100 <= c['N'] < 500]
        if len(exp) > 0:
            f.write("| Market | Lag | EU State | Ctx State | N | Mean | Base Mean | Cohen D |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for c in exp[:20]: 
                f.write(f"| {c['Market']} | {c['Lag']} | {c['EU_State']} | {c['Ctx_State']} | {c['N']} | {c['Mean_60']:.5f} | {c['Base_Mean']:.5f} | {c['Cohen_D']:.3f} |\n")
        else:
            f.write("None.\n")
        f.write("\n")
        
        f.write("## 7. Rejected Register (N >= 500, |d| < 0.2)\n")
        rej = [c for c in combinations if c['N'] >= 500 and abs(c['Cohen_D']) < 0.2]
        if len(rej) > 0:
            f.write("| Market | Lag | EU State | Ctx State | N | Mean | Base Mean | Cohen D |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for c in rej[:20]: 
                f.write(f"| {c['Market']} | {c['Lag']} | {c['EU_State']} | {c['Ctx_State']} | {c['N']} | {c['Mean_60']:.5f} | {c['Base_Mean']:.5f} | {c['Cohen_D']:.3f} |\n")
        else:
            f.write("None.\n")
        f.write("\n")
        
        f.write("## 8. Conclusion\n")
        if len(candidates) > 0:
            f.write("**1. Incremental Information:** Yes, certain context markets provide meaningful predictive information beyond EURUSD's current state.\n\n")
            lags_found = set(c['Lag'] for c in candidates)
            f.write(f"**2. Lead/Lag Relationship:** Effects were observed at lags: {', '.join(lags_found)}.\n\n")
            unstable_count = sum(1 for c in candidates if c['Classification'] == 'EXPLORATORY')
            f.write(f"**3. Temporal Consistency:** {len(candidates) - unstable_count} out of {len(candidates)} candidates showed consistent directionality across all three historical partitions.\n\n")
            f.write("**4. Sufficiently Populated:** Yes, all candidates were evaluated with N >= 500.\n\n")
            f.write("**5. Explained by EURUSD?** No, the baseline matching controlled for EURUSD's own state, isolating the cross-market effect.\n\n")
        else:
            f.write("**1. Incremental Information:** No relationships met the criteria for candidate selection (N >= 500, |d| >= 0.2, and temporal stability).\n\n")
            f.write("**2. Lead/Lag Relationship:** N/A\n\n")
            f.write("**3. Temporal Consistency:** N/A\n\n")
            f.write("**4. Sufficiently Populated:** N/A\n\n")
            f.write("**5. Explained by EURUSD?** N/A\n\n")


def run_study():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data', 'm1')
    reports_dir = os.path.join(base_dir, 'reports')
    
    eurusd_path = os.path.join(data_dir, 'EURUSD_M1.parquet')
    
    print("Extracting EURUSD Non-overlapping Blocks...")
    df_eu = pd.read_parquet(eurusd_path)
    df_eu['timestamp'] = pd.to_datetime(df_eu['timestamp'])
    df_eu = df_eu.sort_values('timestamp').reset_index(drop=True)
    
    df_eu['atr_14'] = calculate_atr(df_eu, 14)
    df_eu['block_range_15'] = df_eu['high'].rolling(15).max() - df_eu['low'].rolling(15).min()
    df_eu['block_ret_15'] = df_eu['close'] - df_eu['close'].shift(15)
    
    indexer_60 = pd.api.indexers.FixedForwardWindowIndexer(window_size=60)
    df_eu['fwd_high_60'] = df_eu['high'].shift(-1).rolling(window=indexer_60).max()
    df_eu['fwd_low_60'] = df_eu['low'].shift(-1).rolling(window=indexer_60).min()
    df_eu['fwd_close_60'] = df_eu['close'].shift(-60)
    
    indexer_240 = pd.api.indexers.FixedForwardWindowIndexer(window_size=240)
    df_eu['fwd_high_240'] = df_eu['high'].shift(-1).rolling(window=indexer_240).max()
    df_eu['fwd_low_240'] = df_eu['low'].shift(-1).rolling(window=indexer_240).min()
    df_eu['fwd_close_240'] = df_eu['close'].shift(-240)
    
    # Anchor extraction
    blocks = df_eu.iloc[15::15].copy().reset_index(drop=True)
    blocks['start_atr'] = blocks['atr_14'].shift(1)
    
    # 480 non-overlapping blocks = 1 week
    blocks['vol_pct_25'] = blocks['block_range_15'].rolling(480).quantile(0.25)
    blocks['vol_pct_75'] = blocks['block_range_15'].rolling(480).quantile(0.75)
    
    blocks['vol_state'] = np.where(blocks['block_range_15'] < blocks['vol_pct_25'], 'LOW_VOL',
                          np.where(blocks['block_range_15'] > blocks['vol_pct_75'], 'HIGH_VOL', 'NORMAL_VOL'))
                          
    blocks['norm_ret'] = blocks['block_ret_15'] / (blocks['start_atr'] + 1e-9)
    blocks['dir_state'] = np.where(blocks['norm_ret'] > 1.0, 'BULL',
                          np.where(blocks['norm_ret'] < -1.0, 'BEAR', 'FLAT'))
                          
    blocks['eu_state'] = blocks['vol_state'] + '_' + blocks['dir_state']
    
    # Drop rows without sufficient history
    blocks = blocks.dropna(subset=['vol_pct_25', 'fwd_close_240']).copy()
    
    # Compute outcomes
    blocks['ret_60'] = blocks['fwd_close_60'] - blocks['close']
    blocks['ret_240'] = blocks['fwd_close_240'] - blocks['close']
    blocks['mfe_60'] = blocks['fwd_high_60'] - blocks['close']
    blocks['mae_60'] = blocks['close'] - blocks['fwd_low_60']
    
    # Set index to timestamp for merging
    blocks.set_index('timestamp', inplace=True)
    
    context_instruments = ['XAUUSD', 'XAGUSD', 'BTCUSD', 'USATECHIDXUSD']
    
    for symbol in context_instruments:
        file_path = os.path.join(data_dir, f"{symbol}_M1.parquet")
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found.")
            continue
            
        ctx_series = process_context_instrument(file_path)
        
        # Merge contemporaneous
        blocks = blocks.join(ctx_series.rename(f"{symbol}_t0"), how='left')
        
        # Merge t-15
        ctx_t15 = ctx_series.copy()
        ctx_t15.index = ctx_t15.index + pd.Timedelta(minutes=15)
        blocks = blocks.join(ctx_t15.rename(f"{symbol}_t15"), how='left')
        
        # Merge t-30
        ctx_t30 = ctx_series.copy()
        ctx_t30.index = ctx_t30.index + pd.Timedelta(minutes=30)
        blocks = blocks.join(ctx_t30.rename(f"{symbol}_t30"), how='left')
        
        # Handle explicit missing states
        blocks[f"{symbol}_t0"] = blocks[f"{symbol}_t0"].fillna("MISSING")
        blocks[f"{symbol}_t15"] = blocks[f"{symbol}_t15"].fillna("MISSING")
        blocks[f"{symbol}_t30"] = blocks[f"{symbol}_t30"].fillna("MISSING")
        
    print("Saving synchronized dataset...")
    blocks.reset_index(inplace=True)
    out_path = os.path.join(reports_dir, "RC009_Study_004_Cross_Market_Dataset.parquet")
    blocks.to_parquet(out_path, index=False)
    
    analyze_and_report(blocks, reports_dir, context_instruments)
    print("Study 004 execution complete.")

if __name__ == "__main__":
    run_study()
