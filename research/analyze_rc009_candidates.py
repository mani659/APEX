import os
import pandas as pd
import numpy as np

def run_analysis():
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))
    events_path = os.path.join(reports_dir, "RC009_Discovery_Dataset.parquet")
    control_path = os.path.join(reports_dir, "RC009_Control_Dataset.parquet")
    baseline_path = os.path.join(reports_dir, "RC009_Baseline_Dataset.parquet")
    
    print("Loading datasets...")
    df_events = pd.read_parquet(events_path)
    df_control = pd.read_parquet(control_path)
    df_baseline = pd.read_parquet(baseline_path)
    
    report_path = os.path.join(reports_dir, "RC009_Candidate_Analysis.md")
    
    # Calculate Baseline A stats
    base_ret60_mean = df_baseline['ret_60'].mean()
    base_ret60_std = df_baseline['ret_60'].std()
    base_ret240_mean = df_baseline['ret_240'].mean()
    base_ret240_std = df_baseline['ret_240'].std()
    
    def calc_stats(df_subset):
        if len(df_subset) == 0:
            return None
        return {
            "count": len(df_subset),
            "freq": len(df_subset) / 2041613 * 100, # Approx frequency in % of bars
            "ret_60_mean": df_subset['ret_60'].mean(),
            "ret_60_med": df_subset['ret_60'].median(),
            "ret_60_std": df_subset['ret_60'].std(),
            "ret_240_mean": df_subset['ret_240'].mean(),
            "ret_240_med": df_subset['ret_240'].median(),
            "mfe_60_mean": df_subset['mfe_60'].mean(),
            "mae_60_mean": df_subset['mae_60'].mean(),
            "win_rate_60": (df_subset['ret_60'] > 0).mean() * 100
        }

    candidates = df_events['candidate'].unique()
    
    with open(report_path, "w") as f:
        f.write("# RC009 Study 001 Candidate Analysis\n\n")
        f.write(f"Total Evaluated Candidates: {len(candidates)}\n\n")
        
        f.write("## Baseline A: Unconditional (100k random samples)\n")
        f.write(f"- 60-bar Forward Return Mean: {base_ret60_mean:.5f} (Std: {base_ret60_std:.5f})\n")
        f.write(f"- 240-bar Forward Return Mean: {base_ret240_mean:.5f} (Std: {base_ret240_std:.5f})\n\n")
        
        rankings = []
        
        for cand in sorted(candidates):
            f.write(f"## Candidate: {cand}\n")
            c_ev = df_events[df_events['candidate'] == cand]
            c_ctrl = df_control[df_control['candidate'] == f"{cand}_Control"]
            
            stats_ev = calc_stats(c_ev)
            stats_ctrl = calc_stats(c_ctrl)
            
            if stats_ev is None:
                f.write("0 Occurrences detected.\n\n")
                continue
                
            # Effect size against Unconditional Baseline A
            if base_ret60_std > 0:
                d_base60 = (stats_ev['ret_60_mean'] - base_ret60_mean) / base_ret60_std
            else:
                d_base60 = 0.0
                
            # Effect size against Matched Control C
            d_ctrl60 = 0.0
            if stats_ctrl is not None:
                pooled_std = np.sqrt(((stats_ev['count']-1)*(stats_ev['ret_60_std']**2) + (stats_ctrl['count']-1)*(stats_ctrl['ret_60_std']**2)) / (stats_ev['count']+stats_ctrl['count']-2))
                if pooled_std > 0:
                    d_ctrl60 = (stats_ev['ret_60_mean'] - stats_ctrl['ret_60_mean']) / pooled_std
            
            f.write(f"- **Occurrence Count**: {stats_ev['count']}\n")
            f.write(f"- **Frequency**: {stats_ev['freq']:.4f}% of all bars\n")
            f.write(f"- **60-Bar Mean Return**: {stats_ev['ret_60_mean']:.5f} (Median: {stats_ev['ret_60_med']:.5f})\n")
            f.write(f"- **240-Bar Mean Return**: {stats_ev['ret_240_mean']:.5f} (Median: {stats_ev['ret_240_med']:.5f})\n")
            f.write(f"- **Mean MFE / MAE (60-bar)**: {stats_ev['mfe_60_mean']:.5f} / {stats_ev['mae_60_mean']:.5f}\n")
            f.write(f"- **Win Rate (60-bar)**: {stats_ev['win_rate_60']:.1f}%\n")
            f.write(f"- **Effect Size vs Baseline A (60-bar)**: {d_base60:.4f}\n")
            f.write(f"- **Effect Size vs Control C (60-bar)**: {d_ctrl60:.4f}\n\n")
            
            # Classification logic
            abs_d = max(abs(d_base60), abs(d_ctrl60))
            if stats_ev['count'] < 30:
                classification = "REJECTED (Insufficient Sample Size)"
            elif abs_d < 0.2:
                classification = "REJECTED (No Meaningful Effect Size)"
            elif abs_d >= 0.5:
                classification = "CANDIDATE (Requires Independent Validation)"
            else:
                classification = "EXPLORATORY (Weak Evidence)"
                
            f.write(f"**Classification**: {classification}\n\n---\n\n")
            rankings.append({
                "Candidate": cand,
                "Count": stats_ev['count'],
                "Effect Size (Base)": round(d_base60, 4),
                "Effect Size (Ctrl)": round(d_ctrl60, 4),
                "Classification": classification
            })
            
        f.write("## Candidate Ranking Table\n")
        df_rank = pd.DataFrame(rankings)
        if len(df_rank) > 0:
            df_rank = df_rank.sort_values(by="Effect Size (Base)", key=abs, ascending=False)
            f.write("| Candidate | Count | Effect Size (Base) | Effect Size (Ctrl) | Classification |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for _, row in df_rank.iterrows():
                f.write(f"| {row['Candidate']} | {row['Count']} | {row['Effect Size (Base)']} | {row['Effect Size (Ctrl)']} | {row['Classification']} |\n")
        else:
            f.write("No candidates to rank.\n")
            
        f.write("\n\n## Rejected Candidate Register\n")
        rejected = [r['Candidate'] for r in rankings if "REJECTED" in r['Classification']]
        if len(rejected) > 0:
            for r in rejected:
                f.write(f"- {r}\n")
        else:
            f.write("None.\n")
            
    print(f"Analysis saved to: {report_path}")

if __name__ == "__main__":
    run_analysis()
