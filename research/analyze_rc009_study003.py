import os
import pandas as pd
import numpy as np

def run_analysis():
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))
    dataset_path = os.path.join(reports_dir, "RC009_Study_003_Sequence_Dataset.parquet")
    
    print("Loading sequence dataset...")
    df = pd.read_parquet(dataset_path)
    
    report_path = os.path.join(reports_dir, "RC009_Study_003_Sequence_Analysis.md")
    
    with open(report_path, "w") as f:
        f.write("# RC009 Study 003 Sequence Analysis\n\n")
        
        # Multiple Testing Disclosure
        f.write("## Multiple-Testing Disclosure\n")
        f.write(f"- **Number of state dimensions**: 2 (Volatility, Direction)\n")
        f.write(f"- **Number of composite states**: 9\n")
        f.write(f"- **Sequence lengths tested**: N=3, N=5\n")
        f.write(f"- **Unique N=3 sequences observed**: {df['seq_3'].nunique()}\n")
        f.write(f"- **Unique N=5 sequences observed**: {df['seq_5'].nunique()}\n")
        f.write(f"- **Number of outcome metrics**: 4 (ret_60, ret_240, mfe_60, mae_60)\n")
        f.write("The exploratory nature of this search means these findings must be validated independently.\n\n")
        
        # State Frequency
        f.write("## State Frequency Table\n")
        state_counts = df['state'].value_counts()
        total_blocks = len(df)
        f.write("| State | Count | Frequency |\n")
        f.write("| :--- | :--- | :--- |\n")
        for state, count in state_counts.items():
            f.write(f"| {state} | {count} | {count/total_blocks*100:.1f}% |\n")
        f.write("\n")
        
        # Transition Matrix
        f.write("## State Transition Matrix (Probability of Next State)\n")
        df['next_state'] = df['state'].shift(-1)
        # Drop the very last row which will have NaN next_state
        trans_df = df.dropna(subset=['next_state'])
        trans_matrix = pd.crosstab(trans_df['state'], trans_df['next_state'], normalize='index')
        f.write("| Current State | " + " | ".join(trans_matrix.columns) + " |\n")
        f.write("| :--- | " + " | ".join(["---"] * len(trans_matrix.columns)) + " |\n")
        for idx, row in trans_matrix.iterrows():
            formatted_row = " | ".join([f"{val*100:.1f}%" for val in row])
            f.write(f"| {idx} | {formatted_row} |\n")
        f.write("\n")
        
        # Baseline A
        base_a_mean = df['ret_60'].mean()
        base_a_std = df['ret_60'].std()
        
        # Analysis Function
        def analyze_sequences(seq_col, label):
            f.write(f"## {label} Sequence Analysis\n")
            counts = df[seq_col].value_counts()
            
            # Filter to sufficiently populated sequences (e.g. N > 1000)
            valid_seqs = counts[counts > 1000].index
            f.write(f"Evaluating {len(valid_seqs)} highly populated sequences (N > 1000).\n\n")
            
            results = []
            
            for seq in valid_seqs:
                subset = df[df[seq_col] == seq]
                n = len(subset)
                mean_ret = subset['ret_60'].mean()
                std_ret = subset['ret_60'].std()
                
                # Get final state from sequence
                final_state = seq.split(' -> ')[-1]
                final_dir = final_state.split('_')[-1] # BULL, BEAR, or FLAT
                
                # Baseline B: Same direction
                base_b = df[df['dir_state'] == final_dir]
                # Baseline C: Same composite state
                base_c = df[df['state'] == final_state]
                
                # Effect size vs Baseline C (Primary control)
                if len(base_c) > 1 and n > 1:
                    pooled_std = np.sqrt(((n-1)*std_ret**2 + (len(base_c)-1)*base_c['ret_60'].std()**2) / (n+len(base_c)-2))
                    d_ctrl = (mean_ret - base_c['ret_60'].mean()) / (pooled_std + 1e-9)
                else:
                    d_ctrl = 0.0
                    
                abs_d = abs(d_ctrl)
                if abs_d < 0.1:
                    classification = "REJECTED (No Edge)"
                elif abs_d < 0.2:
                    classification = "EXPLORATORY (Weak Edge)"
                else:
                    classification = "CANDIDATE"
                    
                results.append({
                    "Sequence": seq,
                    "Count": n,
                    "Mean Ret": mean_ret,
                    "Ctrl Mean": base_c['ret_60'].mean(),
                    "Effect Size": d_ctrl,
                    "Classification": classification
                })
                
            res_df = pd.DataFrame(results, columns=["Sequence", "Count", "Mean Ret", "Ctrl Mean", "Effect Size", "Classification"])
            if len(res_df) > 0:
                res_df = res_df.sort_values(by="Effect Size", key=abs, ascending=False).head(30) # Show top 30
                f.write("| Sequence | Count | Mean Ret | Ctrl Mean | Effect Size (vs Ctrl) | Classification |\n")
                f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
                for _, row in res_df.iterrows():
                    f.write(f"| {row['Sequence']} | {row['Count']} | {row['Mean Ret']:.5f} | {row['Ctrl Mean']:.5f} | {row['Effect Size']:.4f} | {row['Classification']} |\n")
            else:
                f.write("No sequences met the population criteria.\n")
            f.write("\n")
            
            return res_df
            
        res_3 = analyze_sequences('seq_3', "N=3")
        res_5 = analyze_sequences('seq_5', "N=5")
        
        f.write("## Candidate Register\n")
        candidates = []
        if res_3 is not None:
            candidates.extend(res_3[res_3['Classification'] == 'CANDIDATE']['Sequence'].tolist())
        if res_5 is not None:
            candidates.extend(res_5[res_5['Classification'] == 'CANDIDATE']['Sequence'].tolist())
            
        if len(candidates) > 0:
            for c in candidates:
                f.write(f"- {c}\n")
        else:
            f.write("None.\n")
            
        f.write("\n## Conclusion\n")
        if len(candidates) > 0:
            f.write("**Status:** Positive. We found sequences where the historical path meaningfully alters the expected outcome compared to evaluating the final state in isolation.\n")
        else:
            f.write("**Status:** Negative. The sequence of states does NOT contain meaningful predictive information beyond the final state itself. All sequences converged back to their baseline distributions.\n")
            
    print(f"Analysis saved to: {report_path}")

if __name__ == "__main__":
    run_analysis()
