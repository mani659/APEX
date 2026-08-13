import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import HDBSCAN

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
    df_m1 = df_m1.sort_values('timestamp').reset_index(drop=True)
    
    print("Calculating Base Metrics...")
    df_m1['atr_14'] = calculate_atr(df_m1, 14)
    df_m1['block_high'] = df_m1['high'].rolling(15).max()
    df_m1['block_low'] = df_m1['low'].rolling(15).min()
    df_m1['block_range'] = df_m1['block_high'] - df_m1['block_low']
    df_m1['block_volume'] = df_m1['volume'].rolling(15).sum()
    df_m1['block_open'] = df_m1['open'].shift(14)
    
    indexer_60 = pd.api.indexers.FixedForwardWindowIndexer(window_size=60)
    df_m1['fwd_high_60'] = df_m1['high'].shift(-1).rolling(window=indexer_60).max()
    df_m1['fwd_low_60'] = df_m1['low'].shift(-1).rolling(window=indexer_60).min()
    df_m1['fwd_close_60'] = df_m1['close'].shift(-60)
    
    indexer_240 = pd.api.indexers.FixedForwardWindowIndexer(window_size=240)
    df_m1['fwd_high_240'] = df_m1['high'].shift(-1).rolling(window=indexer_240).max()
    df_m1['fwd_low_240'] = df_m1['low'].shift(-1).rolling(window=indexer_240).min()
    df_m1['fwd_close_240'] = df_m1['close'].shift(-240)
    
    print("Extracting Blocks...")
    blocks = df_m1.iloc[15::15].copy().reset_index(drop=True)
    blocks['start_atr'] = blocks['atr_14'].shift(1)
    
    blocks['path_15'] = (blocks['close'] - blocks['close'].shift(1)) / (blocks['start_atr'] + 1e-9)
    blocks['path_60'] = (blocks['close'] - blocks['close'].shift(4)) / (blocks['start_atr'] + 1e-9)
    
    print("Calculating Rolling Percentiles...")
    # Faster percentile implementation for pandas rolling
    blocks['vol_pct'] = blocks['block_range'].rolling(480).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=True)
    blocks['partic_pct'] = blocks['block_volume'].rolling(480).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=True)
    
    blocks['body_imbalance'] = np.abs(blocks['close'] - blocks['block_open']) / (blocks['block_range'] + 1e-9)
    
    blocks['ret_60'] = blocks['fwd_close_60'] - blocks['close']
    blocks['ret_240'] = blocks['fwd_close_240'] - blocks['close']
    blocks['mfe_60'] = blocks['fwd_high_60'] - blocks['close']
    blocks['mae_60'] = blocks['close'] - blocks['fwd_low_60']
    
    features = ['path_15', 'path_60', 'vol_pct', 'partic_pct', 'body_imbalance']
    
    blocks = blocks.dropna(subset=features + ['fwd_close_240']).copy()
    blocks = blocks[~blocks[features].isin([np.inf, -np.inf]).any(axis=1)]
    
    print(f"Valid blocks for clustering: {len(blocks)}")
    
    X = blocks[features].values
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("Running HDBSCAN...")
    clusterer = HDBSCAN(min_cluster_size=500, min_samples=50, metric='euclidean', n_jobs=-1)
    blocks['cluster'] = clusterer.fit_predict(X_scaled)
    
    print("Analyzing Clusters...")
    analyze_and_report(blocks, reports_dir, features)

def get_direction_metrics(df_sub):
    if len(df_sub) == 0: return 0.0, 0.0
    s_ret = np.sign(df_sub['ret_60'])
    s_block = np.sign(df_sub['path_15'])
    valid = (s_ret != 0) & (s_block != 0)
    cont = (s_ret == s_block) & valid
    rev = (s_ret != s_block) & valid
    return cont.mean() * 100, rev.mean() * 100

def analyze_and_report(blocks, reports_dir, features):
    report_path = os.path.join(reports_dir, "RC010_Study_001_HDBSCAN_Discovery.md")
    
    base_mean = blocks['ret_60'].mean()
    base_std = blocks['ret_60'].std()
    base_n = len(blocks)
    
    results = []
    
    total_len = len(blocks)
    third = total_len // 3
    
    cluster_labels = sorted(blocks['cluster'].unique())
    
    for c in cluster_labels:
        sub = blocks[blocks['cluster'] == c]
        n = len(sub)
        if c == -1:
            name = "Noise (-1)"
        else:
            name = f"Cluster {c}"
            
        mean_60 = sub['ret_60'].mean()
        std_60 = sub['ret_60'].std()
        med_60 = sub['ret_60'].median()
        mean_240 = sub['ret_240'].mean()
        med_240 = sub['ret_240'].median()
        mfe = sub['mfe_60'].mean()
        mae = sub['mae_60'].mean()
        cont, rev = get_direction_metrics(sub)
        
        pooled_std = np.sqrt(((n-1)*std_60**2 + (base_n-1)*base_std**2) / (n+base_n-2))
        d = (mean_60 - base_mean) / (pooled_std + 1e-9)
        
        sub_time = sub.sort_values('timestamp')
        
        # Calculate time distributions by splitting the overall dataset, not the subset
        # Wait, the prompt says "persistence across early / middle / recent history"
        # I should split the *overall* blocks into 3 chronological periods, and count how many cluster elements fall into each.
        overall_time = blocks.sort_values('timestamp')
        p1_end = overall_time.iloc[third]['timestamp']
        p2_end = overall_time.iloc[2*third]['timestamp']
        
        n_p1 = len(sub_time[sub_time['timestamp'] < p1_end])
        n_p2 = len(sub_time[(sub_time['timestamp'] >= p1_end) & (sub_time['timestamp'] < p2_end)])
        n_p3 = len(sub_time[sub_time['timestamp'] >= p2_end])
        
        dist_str = f"{n_p1/n*100:.0f}% / {n_p2/n*100:.0f}% / {n_p3/n*100:.0f}%"
        
        centroids = {f: sub[f].median() for f in features}
        
        results.append({
            'Cluster': name,
            'N': n,
            'Pct': n / base_n * 100,
            'Mean_60': mean_60,
            'Med_60': med_60,
            'Mean_240': mean_240,
            'Med_240': med_240,
            'MFE': mfe,
            'MAE': mae,
            'Cont': cont,
            'Rev': rev,
            'Cohen_D': d,
            'Dist': dist_str,
            'Centroids': centroids
        })
        
    results.sort(key=lambda x: abs(x['Cohen_D']), reverse=True)
    
    with open(report_path, 'w') as f:
        f.write("# RC010 Study 001 - Unsupervised Behavioral State Discovery\n\n")
        f.write("## 1. Methodology\n")
        f.write("- **Algorithm:** HDBSCAN\n")
        f.write("- **Min Cluster Size:** 500\n")
        f.write("- **Features (5):** `path_15`, `path_60`, `vol_pct`, `partic_pct`, `body_imbalance`\n")
        f.write("- **Preprocessing:** RobustScaler\n")
        f.write(f"- **Total Samples Analyzed:** {base_n}\n\n")
        
        f.write("## 2. Cluster Overview\n")
        f.write(f"Number of clusters found: {len(cluster_labels) - 1}\n\n")
        
        f.write("| Cluster | N | % of Pop | Mean 60 | Med 60 | Cohen D | Temporal Dist (P1/P2/P3) |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in results:
            f.write(f"| {r['Cluster']} | {r['N']} | {r['Pct']:.1f}% | {r['Mean_60']:.5f} | {r['Med_60']:.5f} | {r['Cohen_D']:.3f} | {r['Dist']} |\n")
        f.write("\n")
        
        f.write("## 3. Explaining Discovered Clusters\n")
        for r in results:
            if r['Cluster'] == "Noise (-1)": continue
            f.write(f"### {r['Cluster']} (N={r['N']})\n")
            f.write(f"- **Cohen D vs Baseline:** {r['Cohen_D']:.3f}\n")
            f.write("- **Feature Centroids (Medians):**\n")
            for feat, val in r['Centroids'].items():
                f.write(f"  - `{feat}`: {val:.3f}\n")
            f.write(f"- **Continuation Probability:** {r['Cont']:.1f}%\n")
            f.write(f"- **Reversal Probability:** {r['Rev']:.1f}%\n\n")
            
        f.write("## 4. Final Conclusion\n")
        candidates = [r for r in results if r['Cluster'] != "Noise (-1)" and abs(r['Cohen_D']) >= 0.2 and r['N'] >= 500]
        if len(candidates) > 0:
            f.write("**CANDIDATES IDENTIFIED**\n\n")
            f.write("HDBSCAN successfully discovered naturally occurring behavioral states with materially different forward outcome distributions. These clusters warrant deep-dive validation.\n")
        else:
            f.write("**NEGATIVE RESULT**\n\n")
            f.write("HDBSCAN did not discover any naturally occurring behavioral states with a strong predictive edge (Cohen's d >= 0.2). The market does not naturally separate into distinct, predictive behavioral clusters using these fundamental descriptors.\n")

    out_path = os.path.join(reports_dir, "RC010_Study_001_Dataset.parquet")
    blocks.to_parquet(out_path, index=False)
    print("Done!")

if __name__ == "__main__":
    run_study()
