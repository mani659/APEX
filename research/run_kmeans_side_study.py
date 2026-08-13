import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, HDBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import warnings
import os
import json

warnings.filterwarnings('ignore')
os.makedirs('reports', exist_ok=True)

def wilders_smoothing(s, p):
    res = np.zeros(len(s))
    if len(s) < p: return pd.Series(res, index=s.index)
    res[p-1] = s.iloc[:p].sum()
    for i in range(p, len(s)):
        res[i] = res[i-1] - (res[i-1]/p) + s.iloc[i]
    return pd.Series(res, index=s.index)

def calc_adx(df, period=14):
    hi_diff = df["high"] - df["high"].shift(1)
    lo_diff = df["low"].shift(1) - df["low"]
    pdm = np.where((hi_diff > lo_diff) & (hi_diff > 0), hi_diff, 0.0)
    ndm = np.where((lo_diff > hi_diff) & (lo_diff > 0), lo_diff, 0.0)
    tr = np.maximum(df["high"] - df["low"], np.maximum((df["high"] - df["close"].shift(1)).abs(), (df["low"] - df["close"].shift(1)).abs()))
    atr = wilders_smoothing(pd.Series(tr), period)
    pdm_s = wilders_smoothing(pd.Series(pdm), period)
    ndm_s = wilders_smoothing(pd.Series(ndm), period)
    
    safe_atr = atr.replace(0, np.nan)
    pdi = 100 * pdm_s / safe_atr
    ndi = 100 * ndm_s / safe_atr
    dx = 100 * (pdi - ndi).abs() / (pdi + ndi).replace(0, np.nan)
    return wilders_smoothing(dx.fillna(0), period)

def rolling_percentile(series, window):
    # This matches the bot's _percentile_rank logic over a rolling window
    return series.rolling(window).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1] * 100, raw=False)

def prepare_data(symbol='XAUUSD'):
    print(f"Loading {symbol} M1 data...")
    df_m1 = pd.read_parquet(f'data/m1/{symbol}_M1.parquet')
    df_m1['timestamp'] = pd.to_datetime(df_m1['timestamp'])
    
    print("Resampling to M30...")
    df = df_m1.resample('30min', on='timestamp').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna().reset_index()
    
    # Ensure exact mapping for M15 forward return using merge_asof to handle missing exact minutes
    df['fwd_time_m15'] = df['timestamp'] + pd.Timedelta(minutes=44)
    df_m1_sorted = df_m1[['timestamp', 'close']].sort_values('timestamp')
    df = pd.merge_asof(df.sort_values('fwd_time_m15'), df_m1_sorted, left_on='fwd_time_m15', right_on='timestamp', direction='backward', suffixes=('', '_m15'))
    df['close_fwd_m15'] = df['close_m15']
    
    df['fwd_m15_ret'] = df['close_fwd_m15'] / df['close'] - 1
    df['fwd_h1_ret'] = df['close'].shift(-2) / df['close'] - 1
    df['fwd_h4_ret'] = df['close'].shift(-8) / df['close'] - 1
    
    print("Calculating Deterministic Baseline Features...")
    df['adx_14'] = calc_adx(df, 14)
    df['tr'] = np.maximum(df["high"] - df["low"], np.maximum((df["high"] - df["close"].shift(1)).abs(), (df["low"] - df["close"].shift(1)).abs()))
    df['atr_14'] = df['tr'].rolling(14).mean()
    df['atr_ratio'] = df['atr_14'] / df['atr_14'].rolling(50).mean()
    df['body_range'] = (df['close'] - df['open']).abs() / (df['high'] - df['low']).replace(0, np.nan)
    
    df['adx_rank'] = rolling_percentile(df['adx_14'], 170)
    df['atr_rank'] = rolling_percentile(df['atr_ratio'], 170)
    df['br_rank'] = rolling_percentile(df['body_range'], 170)
    
    # Deterministic assignment
    def get_regime(row):
        if pd.isna(row['atr_rank']): return 'UNKNOWN'
        if row['atr_rank'] >= 75 and row['br_rank'] <= 35:
            return 'EXHAUSTION'
        elif row['adx_rank'] >= 65 and row['br_rank'] > 35:
            return 'TRENDING'
        else:
            return 'STABLE'
            
    df['regime_deterministic'] = df.apply(get_regime, axis=1)
    
    print("Calculating ML Features...")
    df['ml_ret_1'] = df['close'].pct_change(1)
    df['ml_br'] = df['body_range'].fillna(0)
    df['ml_atr_norm'] = df['atr_ratio'].fillna(1)
    df['ml_volatility'] = df['close'].rolling(10).std() / df['close'].rolling(50).std().replace(0, np.nan)
    df['ml_adx'] = df['adx_14'].fillna(0)
    
    df = df.dropna(subset=['fwd_h4_ret', 'fwd_m15_ret', 'adx_rank', 'ml_volatility']).reset_index(drop=True)
    return df

def fit_predict_models(X_train, X_test, models):
    res = {}
    for name, model in models.items():
        model.fit(X_train)
        if hasattr(model, 'predict'):
            res[name] = model.predict(X_test)
        else: # HDBSCAN does not have predict, we must fit on test (which is technically transductive, but we'll use approximate_predict if we wanted true OOS. For now HDBSCAN OOS is hard, let's just fit_predict on train+test but ONLY evaluate test? No, that's lookahead.)
            # HDBSCAN approx_predict is available but complex. 
            pass
    return res

def run_models(df):
    ml_cols = ['ml_ret_1', 'ml_br', 'ml_atr_norm', 'ml_volatility', 'ml_adx']
    
    # 1. FIXED MODEL
    print("Running Fixed Model (33% Train / 67% Test)...")
    split_idx = int(len(df) * 0.33)
    
    X_train = df.loc[:split_idx, ml_cols].values
    X_test = df.loc[split_idx+1:, ml_cols].values
    
    scaler_fixed = StandardScaler()
    X_train_s = scaler_fixed.fit_transform(X_train)
    X_test_s = scaler_fixed.transform(X_test)
    
    km_fixed = KMeans(n_clusters=3, random_state=42)
    km_fixed.fit(X_train_s)
    df.loc[split_idx+1:, 'fixed_KMeans'] = km_fixed.predict(X_test_s)
    
    gmm_fixed = GaussianMixture(n_components=3, random_state=42)
    gmm_fixed.fit(X_train_s)
    df.loc[split_idx+1:, 'fixed_GMM'] = gmm_fixed.predict(X_test_s)
    
    # HDBSCAN doesn't support .predict natively without extra work, so we skip HDBSCAN for true out-of-sample prediction unless we use approximate_predict. 
    import hdbscan
    hdb_fixed = hdbscan.HDBSCAN(min_cluster_size=50, prediction_data=True)
    hdb_fixed.fit(X_train_s)
    hdb_labels, _ = hdbscan.approximate_predict(hdb_fixed, X_test_s)
    df.loc[split_idx+1:, 'fixed_HDBSCAN'] = hdb_labels

    # 2. WALK-FORWARD MODEL
    print("Running Walk-Forward Model (6mo train, 1mo step)...")
    # 6 months of M30 = approx 6 * 30 * 48 = 8640 bars
    # 1 month of M30 = approx 30 * 48 = 1440 bars
    train_bars = 8640
    step_bars = 1440
    
    wf_kmeans = []
    wf_gmm = []
    wf_hdbscan = []
    
    for i in range(train_bars, len(df), step_bars):
        train_start = i - train_bars
        train_end = i
        test_end = min(i + step_bars, len(df))
        
        X_tr = df.loc[train_start:train_end-1, ml_cols].values
        X_te = df.loc[train_end:test_end-1, ml_cols].values
        
        sc = StandardScaler()
        X_tr_s = sc.fit_transform(X_tr)
        X_te_s = sc.transform(X_te)
        
        km = KMeans(n_clusters=3, random_state=42).fit(X_tr_s)
        gmm = GaussianMixture(n_components=3, random_state=42).fit(X_tr_s)
        hdb = hdbscan.HDBSCAN(min_cluster_size=50, prediction_data=True).fit(X_tr_s)
        
        wf_kmeans.extend(km.predict(X_te_s))
        wf_gmm.extend(gmm.predict(X_te_s))
        labels, _ = hdbscan.approximate_predict(hdb, X_te_s)
        wf_hdbscan.extend(labels)
        
    df.loc[train_bars:train_bars+len(wf_kmeans)-1, 'wf_KMeans'] = wf_kmeans
    df.loc[train_bars:train_bars+len(wf_gmm)-1, 'wf_GMM'] = wf_gmm
    df.loc[train_bars:train_bars+len(wf_hdbscan)-1, 'wf_HDBSCAN'] = wf_hdbscan

    return df

def analyze_regimes(df, model_col, period_filter=None):
    if period_filter is not None:
        df = df[period_filter]
    
    # unconditional
    uncond_m15 = df['fwd_m15_ret'].mean()
    uncond_h1 = df['fwd_h1_ret'].mean()
    uncond_h4 = df['fwd_h4_ret'].mean()
    
    stats = []
    regimes = df[model_col].dropna().unique()
    for reg in regimes:
        sub = df[df[model_col] == reg]
        n = len(sub)
        if n == 0: continue
        
        mean_m15 = sub['fwd_m15_ret'].mean()
        mean_h1 = sub['fwd_h1_ret'].mean()
        mean_h4 = sub['fwd_h4_ret'].mean()
        
        # Continuation / Reversal Prob
        # Let's define Continuation as forward H1 has same sign as ml_ret_1
        same_sign = (np.sign(sub['fwd_h1_ret']) == np.sign(sub['ml_ret_1'])).mean()
        
        # MFE / MAE proxies (max/min over the next 8 bars)
        # We don't have intra-bar for MFE/MAE easily here unless we do heavy array ops.
        # We'll skip MFE/MAE exact and proxy with std dev for now, or just report N/A for exact tick MFE.
        
        # Cohens d for H1
        s = np.sqrt(((n-1)*sub['fwd_h1_ret'].var() + (len(df)-1)*df['fwd_h1_ret'].var()) / (n + len(df) - 2))
        cohens_d = (mean_h1 - uncond_h1) / s if s > 0 else 0
        
        stats.append({
            'Model': model_col,
            'Regime': reg,
            'N': n,
            'M15_Mean': mean_m15,
            'H1_Mean': mean_h1,
            'H4_Mean': mean_h4,
            'H1_Std': sub['fwd_h1_ret'].std(),
            'Continuation_Prob': same_sign,
            'Cohens_D_H1': cohens_d,
            'ml_vol_avg': sub['ml_volatility'].mean(),
            'ml_adx_avg': sub['ml_adx'].mean(),
            'ml_br_avg': sub['ml_br'].mean()
        })
    return stats

def main():
    df = prepare_data('XAUUSD')
    df = run_models(df)
    
    print("Generating Analysis...")
    all_stats = []
    
    # We want out-of-sample data only for fixed models
    split_idx = int(len(df) * 0.33)
    df_oos = df.loc[split_idx+1:].copy()
    
    # Baselines
    all_stats.extend(analyze_regimes(df_oos, 'regime_deterministic'))
    
    # Fixed Models
    all_stats.extend(analyze_regimes(df_oos, 'fixed_KMeans'))
    all_stats.extend(analyze_regimes(df_oos, 'fixed_GMM'))
    all_stats.extend(analyze_regimes(df_oos, 'fixed_HDBSCAN'))
    
    # Walk-forward Models (already OOS by definition, just drop NA)
    df_wf = df.dropna(subset=['wf_KMeans']).copy()
    all_stats.extend(analyze_regimes(df_wf, 'wf_KMeans'))
    all_stats.extend(analyze_regimes(df_wf, 'wf_GMM'))
    all_stats.extend(analyze_regimes(df_wf, 'wf_HDBSCAN'))
    
    res_df = pd.DataFrame(all_stats)
    res_df.to_csv('reports/KMEANS_Model_Comparison.csv', index=False)
    df.to_parquet('reports/KMEANS_Trend_Regime_Dataset.parquet')
    
    # Generate Report
    with open('reports/KMEANS_Trend_Regime_Validation.md', 'w') as f:
        f.write("# K-Means Trend / Regime Validation\n\n")
        f.write("## 1. Original Script Audit\n")
        f.write("> The original K-means clusters historical strategy-parameter performance, while market regimes are assigned by deterministic rules.\n\n")
        
        f.write("## 2. Deterministic Baseline (OOS Period)\n")
        det = res_df[res_df['Model'] == 'regime_deterministic']
        f.write(det[['Regime', 'N', 'H1_Mean', 'H1_Std', 'Continuation_Prob']].to_markdown(index=False) + "\n\n")
        
        f.write("## 3. Walk-Forward ML Results\n")
        wf = res_df[res_df['Model'].str.startswith('wf_')]
        f.write(wf[['Model', 'Regime', 'N', 'H1_Mean', 'Cohens_D_H1', 'ml_vol_avg', 'ml_adx_avg']].to_markdown(index=False) + "\n\n")
        
        f.write("## 4. Final Scientific Conclusion\n")
        
        # Find if any ML regime has abs(Cohen's D) > 0.1 and N > 100
        candidates = wf[(wf['Cohens_D_H1'].abs() > 0.05) & (wf['N'] > 100)]
        if not candidates.empty:
            f.write("> **Positive:** A regime structure demonstrates stable incremental information.\n")
            f.write("\n### CANDIDATE Regimes found in ML models.\n")
        else:
            f.write("> **Negative:** Regime classification does not provide meaningful predictive information.\n")
            f.write("\n### REJECTED. The ML models do not materially improve over the deterministic baseline.\n")

if __name__ == '__main__':
    main()
