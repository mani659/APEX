import os
import pandas as pd
import numpy as np

def run_analysis():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'RC008_Context_Dataset.parquet'))
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'RC008_Context_Comparison_Report.md'))
    
    df = pd.read_parquet(data_path)
    
    # Define groups
    fav = df[df['is_favorable'] == 1]
    unfav = df[df['is_favorable'] == 0]
    
    print(f"Total Events: {len(df)}")
    print(f"Favorable: {len(fav)}")
    print(f"Unfavorable: {len(unfav)}")
    
    variables = {
        'Volatility Context: 1-Week ATR Percentile': 'vol_pct',
        'Trend Context: Distance from 24h Mean (ATRs)': 'dist_1440',
        'Trend Context: 240-bar Return (ATRs)': 'ret_240',
        'Liquidity Context: 240-bar Volume Z-Score': 'volume_z',
        'Path Context: 60-bar Momentum (ATRs)': 'mom_60',
        'Temporal Context: Hour of Day': 'hour'
    }
    
    with open(report_path, "w") as f:
        f.write("# RC008 Context Comparison Report\n\n")
        f.write(f"Total Events: {len(df)} | Favorable (Isolated PnL > 0): {len(fav)} | Unfavorable: {len(unfav)}\n\n")
        
        for name, col in variables.items():
            f.write(f"## {name}\n")
            
            # Handle Hour as categorical/binned differently if needed, but mean/median still works
            fav_vals = fav[col].dropna()
            unfav_vals = unfav[col].dropna()
            
            if len(fav_vals) == 0 or len(unfav_vals) == 0:
                f.write("Insufficient data.\n\n")
                continue
            
            # Basic stats
            fav_mean = fav_vals.mean()
            fav_med = fav_vals.median()
            unfav_mean = unfav_vals.mean()
            unfav_med = unfav_vals.median()
            
            # Effect size (Cohen's d)
            pooled_std = np.sqrt(((len(fav_vals)-1)*fav_vals.var() + (len(unfav_vals)-1)*unfav_vals.var()) / (len(fav_vals)+len(unfav_vals)-2))
            if pooled_std > 0:
                cohens_d = (fav_mean - unfav_mean) / pooled_std
            else:
                cohens_d = 0.0
                
            f.write(f"- **Favorable**: Mean = {fav_mean:.4f}, Median = {fav_med:.4f}\n")
            f.write(f"- **Unfavorable**: Mean = {unfav_mean:.4f}, Median = {unfav_med:.4f}\n")
            f.write(f"- **Effect Size (Cohen's d)**: {cohens_d:.4f}\n\n")
            
            # Binned conditional expectancy
            f.write("### Conditional Expectancy by Quartiles\n")
            f.write("| Quartile | Range | Sample Count | Win Rate | Mean PnL (Isolated) |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            
            try:
                df['quartile'], bins = pd.qcut(df[col], q=4, retbins=True, duplicates='drop')
                for i, interval in enumerate(sorted(df['quartile'].dropna().unique())):
                    subset = df[df['quartile'] == interval]
                    count = len(subset)
                    win_rate = (subset['is_favorable'].mean()) * 100
                    mean_pnl = subset['m1_pnl'].mean()
                    f.write(f"| Q{i+1} | {interval} | {count} | {win_rate:.1f}% | {mean_pnl:.5f} |\n")
            except ValueError:
                f.write("| N/A | Could not compute quartiles (too few unique values) | - | - | - |\n")
                
            f.write("\n")
            
            # Interpretation categorization
            abs_d = abs(cohens_d)
            if abs_d < 0.2:
                status = "No Evidence"
            elif abs_d >= 0.5:
                status = "Promising / Requires Independent Validation"
            else:
                status = "Weak / Exploratory"
                
            f.write(f"**Classification**: {status}\n\n")
            f.write("---\n\n")

    print(f"Analysis complete. Report saved to: {report_path}")

if __name__ == "__main__":
    run_analysis()
