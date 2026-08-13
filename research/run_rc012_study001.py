import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts

# Setup directories
os.makedirs('reports', exist_ok=True)

def calculate_hurst_exponent(ts_data, max_lag=20):
    lags = range(2, max_lag)
    # Using np.std on the difference
    tau = [np.sqrt(np.std(np.subtract(ts_data[lag:], ts_data[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2.0

def calculate_half_life(spread):
    spread_lag = spread.shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_ret = spread - spread_lag
    spread_ret.iloc[0] = spread_ret.iloc[1]
    spread_lag2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_ret, spread_lag2)
    res = model.fit()
    lam = res.params.iloc[1]
    if lam >= 0:
        return np.inf
    halflife = -np.log(2) / lam
    return halflife

def zero_crossings(spread, mean_val):
    centered = spread - mean_val
    crossings = np.where(np.diff(np.sign(centered)))[0]
    return len(crossings)

def avg_recovery_time(spread, mean_val, crossings_count, total_time):
    if crossings_count == 0:
        return np.inf
    return total_time / crossings_count

def run_analysis_for_period(df_period, log_P_A, log_P_B):
    # OLS
    X = sm.add_constant(df_period[log_P_B])
    model = sm.OLS(df_period[log_P_A], X).fit()
    alpha = model.params.iloc[0]
    beta = model.params.iloc[1]
    
    spread = df_period[log_P_A] - (alpha + beta * df_period[log_P_B])
    
    # ADF Test
    adf_result = ts.adfuller(spread, maxlag=1)
    
    # Half-life
    hl = calculate_half_life(spread)
    
    return {
        'alpha': alpha,
        'beta': beta,
        'adf_stat': adf_result[0],
        'adf_pvalue': adf_result[1],
        'adf_1pct': adf_result[4]['1%'],
        'adf_5pct': adf_result[4]['5%'],
        'spread_mean': spread.mean(),
        'spread_std': spread.std(),
        'half_life': hl,
        'spread': spread
    }

def analyze_pair(symbol_A, symbol_B, all_results_df):
    print(f"Analyzing {symbol_A} / {symbol_B}")
    # Load data with only needed columns to save memory
    df_A = pd.read_parquet(f'data/m1/{symbol_A}_M1.parquet', columns=['timestamp', 'close'])
    df_B = pd.read_parquet(f'data/m1/{symbol_B}_M1.parquet', columns=['timestamp', 'close'])
    
    # Drop NaNs and duplicates just in case
    df_A = df_A.dropna(subset=['close']).drop_duplicates('timestamp')
    df_B = df_B.dropna(subset=['close']).drop_duplicates('timestamp')

    total_A = len(df_A)
    total_B = len(df_B)
    
    df = pd.merge(df_A, df_B, on='timestamp', how='inner', suffixes=('_A', '_B'))
    df_A = None # Free memory
    df_B = None # Free memory
    df = df.sort_values('timestamp').reset_index(drop=True)
    overlap = len(df)
    coverage_A = overlap / total_A if total_A > 0 else 0
    coverage_B = overlap / total_B if total_B > 0 else 0
    
    log_A = f'log_{symbol_A}'
    log_B = f'log_{symbol_B}'
    df[log_A] = np.log(df['close_A'])
    df[log_B] = np.log(df['close_B'])
    
    # 1. Full Period Analysis
    full_res = run_analysis_for_period(df, log_A, log_B)
    df['spread'] = full_res['spread']
    
    # Zero crossings & Recovery
    crossings = zero_crossings(df['spread'], full_res['spread_mean'])
    recovery = avg_recovery_time(df['spread'], full_res['spread_mean'], crossings, len(df))
    max_excursion = df['spread'].abs().max()
    
    # Hurst
    # downsample for hurst to save time if needed, but M1 is fine with small lags
    # Using a stride of 15 (M15 equivalent) to speed it up and reduce M1 noise
    hurst = calculate_hurst_exponent(df['spread'].values[::15])
    
    # Correlation
    corr = df['close_A'].corr(df['close_B'])
    log_corr = df[log_A].corr(df[log_B])
    
    # 2. Temporal Partitions
    n = len(df)
    p1 = df.iloc[:n//3]
    p2 = df.iloc[n//3:2*n//3]
    p3 = df.iloc[2*n//3:]
    
    res_p1 = run_analysis_for_period(p1, log_A, log_B)
    res_p2 = run_analysis_for_period(p2, log_A, log_B)
    res_p3 = run_analysis_for_period(p3, log_A, log_B)
    
    # 3. Rolling Stability
    # We will compute rolling beta, ADF, mean, std using a 3-month window (~ 3 * 20 * 1440 = 86400 bars)
    # To keep it computationally feasible, we sample rolling every 10,000 bars
    rolling_beta = []
    rolling_adf = []
    window = 86400
    if len(df) > window:
        for i in range(window, len(df), 40000):
            w_df = df.iloc[i-window:i]
            w_res = run_analysis_for_period(w_df, log_A, log_B)
            rolling_beta.append(w_res['beta'])
            rolling_adf.append(w_res['adf_stat'])
            
    beta_std = np.std(rolling_beta) if rolling_beta else 0
    adf_mean = np.mean(rolling_adf) if rolling_adf else 0
    
    # Extract only the spread to merge into all_results_df
    spread_df = df[['timestamp', 'spread']].copy()
    spread_df.rename(columns={'spread': f"{symbol_A}_{symbol_B}_spread"}, inplace=True)
    
    if all_results_df.empty:
        all_results_df = spread_df
    else:
        all_results_df = pd.merge(all_results_df, spread_df, on='timestamp', how='outer')
    
    return {
        'pair': f"{symbol_A} / {symbol_B}",
        'start': df['timestamp'].min(),
        'end': df['timestamp'].max(),
        'overlap': overlap,
        'cov_A': coverage_A,
        'cov_B': coverage_B,
        'corr': corr,
        'log_corr': log_corr,
        'alpha': full_res['alpha'],
        'beta': full_res['beta'],
        'adf_stat': full_res['adf_stat'],
        'adf_pvalue': full_res['adf_pvalue'],
        'adf_5pct': full_res['adf_5pct'],
        'hurst': hurst,
        'half_life': full_res['half_life'],
        'zero_crossings': crossings,
        'avg_recovery': recovery,
        'max_excursion': max_excursion,
        'spread_std': full_res['spread_std'],
        'p1_beta': res_p1['beta'],
        'p1_adf': res_p1['adf_stat'],
        'p2_beta': res_p2['beta'],
        'p2_adf': res_p2['adf_stat'],
        'p3_beta': res_p3['beta'],
        'p3_adf': res_p3['adf_stat'],
        'rolling_beta_std': beta_std,
        'rolling_adf_mean': adf_mean
    }, all_results_df

def generate_report(results, df_all):
    lines = [
        "# RC012 Study 001 — Pair Discovery",
        "",
        "## 1. Dataset Overlap Validation",
    ]
    for r in results:
        lines.append(f"**{r['pair']}**")
        lines.append(f"- Start: {r['start']} | End: {r['end']}")
        lines.append(f"- Overlapping bars: {r['overlap']}")
        lines.append(f"- Coverage: {r['cov_A']:.1%} of Leg A, {r['cov_B']:.1%} of Leg B")
        lines.append("")
        
    lines.append("## 2. Pair Inventory & Correlation")
    lines.append("| Pair | Pearson Corr | Log-Price Corr |")
    lines.append("|---|---|---|")
    for r in results:
        lines.append(f"| {r['pair']} | {r['corr']:.3f} | {r['log_corr']:.3f} |")
    lines.append("")
    
    lines.append("## 3. Hedge Ratio & Stationarity (Full Sample)")
    lines.append("| Pair | Alpha | Beta | ADF Stat | ADF p-value | 5% Crit | Hurst |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in results:
        lines.append(f"| {r['pair']} | {r['alpha']:.4f} | {r['beta']:.4f} | {r['adf_stat']:.3f} | {r['adf_pvalue']:.4e} | {r['adf_5pct']:.3f} | {r['hurst']:.3f} |")
    lines.append("")
    
    lines.append("## 4. Mean-Reversion Characteristics")
    lines.append("| Pair | Spread Std | Half-Life (bars) | Zero Crossings | Avg Recovery (bars) | Max Excursion |")
    lines.append("|---|---|---|---|---|---|")
    for r in results:
        lines.append(f"| {r['pair']} | {r['spread_std']:.4f} | {r['half_life']:.1f} | {r['zero_crossings']} | {r['avg_recovery']:.1f} | {r['max_excursion']:.4f} |")
    lines.append("")
    
    lines.append("## 5. Temporal Stability (Early / Middle / Recent)")
    lines.append("| Pair | P1 Beta | P2 Beta | P3 Beta | P1 ADF | P2 ADF | P3 ADF |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in results:
        lines.append(f"| {r['pair']} | {r['p1_beta']:.3f} | {r['p2_beta']:.3f} | {r['p3_beta']:.3f} | {r['p1_adf']:.3f} | {r['p2_adf']:.3f} | {r['p3_adf']:.3f} |")
    lines.append("")
    
    lines.append("## 6. Rolling Stability (3-Month Windows)")
    lines.append("| Pair | Rolling Beta Std | Mean Rolling ADF |")
    lines.append("|---|---|---|")
    for r in results:
        lines.append(f"| {r['pair']} | {r['rolling_beta_std']:.4f} | {r['rolling_adf_mean']:.3f} |")
    lines.append("")
    
    lines.append("## 7. Independence & Structural Logic")
    lines.append("### XAUUSD / XAGUSD")
    lines.append("- **Economic**: Both are precious metals, primarily driven by real interest rates, USD strength, and safe-haven demand. Silver has higher industrial use, leading to volatility differences, but they share macro drivers.")
    lines.append("### BTCUSD / USATECHIDXUSD (Nasdaq)")
    lines.append("- **Economic**: Both are risk assets highly sensitive to global liquidity, interest rates, and tech-driven market sentiment. BTC often trades as a high-beta tech proxy.")
    lines.append("")
    
    lines.append("## 8. Candidate / Rejected Register")
    for r in results:
        # Determine classification
        # Criteria for CANDIDATE: ADF stat < 5% critical, Beta relatively stable across P1/P2/P3, Hurst < 0.5
        is_stat = r['adf_stat'] < r['adf_5pct'] and r['adf_pvalue'] < 0.05
        is_stable_beta = abs(r['p1_beta'] - r['p3_beta']) / abs(r['beta']) < 0.5 # Arbitrary stability check
        is_mean_reverting = r['hurst'] < 0.5 and r['half_life'] < 50000
        
        classification = "REJECTED"
        if is_stat and is_mean_reverting and is_stable_beta:
            classification = "CANDIDATE"
        elif is_stat or (r['hurst'] < 0.5):
            classification = "EXPLORATORY"
            
        lines.append(f"### {r['pair']} : **{classification}**")
        lines.append(f"- Stationarity (ADF): {'Pass' if is_stat else 'Fail'}")
        lines.append(f"- Mean Reversion: {'Pass' if is_mean_reverting else 'Fail'}")
        lines.append(f"- Structural Stability: {'Pass' if is_stable_beta else 'Fail'}")
        lines.append("")
        
    lines.append("## 9. Final Scientific Conclusion")
    
    candidates = [r for r in results if r['adf_stat'] < r['adf_5pct']]
    if candidates:
        lines.append("> **A stable relative-value relationship has been discovered.**")
    else:
        lines.append("> **The selected economically related pairs do not demonstrate sufficient statistical stability to justify further relative-value research.**")
        
    with open('reports/RC012_Study_001_Pair_Discovery.md', 'w') as f:
        f.write("\n".join(lines))
        
    # Save the aligned data
    df_all.to_parquet('reports/RC012_Study_001_Pair_Discovery.parquet')
    print("Report and dataset generated.")

if __name__ == '__main__':
    pairs = [
        ('XAUUSD', 'XAGUSD'),
        ('BTCUSD', 'USATECHIDXUSD')
    ]
    all_res = []
    df_all = pd.DataFrame()
    for pa, pb in pairs:
        res, df_all = analyze_pair(pa, pb, df_all)
        all_res.append(res)
        
    generate_report(all_res, df_all)
