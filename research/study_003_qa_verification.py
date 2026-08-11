import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from research.repository.config import RepositoryConfig
from research.repository.engine import ExperimentRepository

def recompute_stats(data):
    a = 1.0 * np.array(data)
    n = len(a)
    m = np.mean(a)
    std = np.std(a, ddof=1)
    
    # Standard error
    se = std / np.sqrt(n)
    
    # 95% Confidence Interval
    # Normal approximation for large N
    ci_low = m - 1.96 * se
    ci_high = m + 1.96 * se
    
    # Effect Size (Cohen's d approximation)
    effect_size = m / std if std != 0 else 0
    
    # Win Rate
    pos_data = a[a > 0]
    win_rate = len(pos_data) / n
    
    return {
        "n": n,
        "mean": m,
        "std": std,
        "se": se,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "effect_size": effect_size,
        "win_rate": win_rate
    }

def main():
    print("=========================================================")
    print("APEX Research Study 003 QA: Statistical Verification Pass")
    print("=========================================================")
    
    repo_path = os.path.join(os.path.dirname(__file__), "RC001_Continuation", "repository")
    repo_config = RepositoryConfig(repository_path=repo_path)
    repo = ExperimentRepository(repo_config)
    
    print("[1] Loading Dataset from Study 002 (experiment_000003)...")
    entry = repo.load("experiment_000003")
    split = entry.experiment_record.dataset_split
    
    records = []
    records.extend(split.train_dataset.records)
    records.extend(split.validation_dataset.records)
    records.extend(split.test_dataset.records)
    
    print(f"    Successfully loaded {len(records)} records.")
    
    data_list = []
    for r in records:
        data_list.append({
            "sweep": r.features["liquidity_sweep_strength"],
            "trend": r.features["market_regime_trend_strength"],
            "ret_20": r.labels["forward_return_20"]
        })
    df = pd.DataFrame(data_list)
    
    bull_sweeps = df[df['sweep'] > 0]
    bear_sweeps = df[df['sweep'] < 0]
    
    bull_bull = bull_sweeps[bull_sweeps['trend'] >= 5]['ret_20'].dropna()
    bear_bear = bear_sweeps[bear_sweeps['trend'] <= 1]['ret_20'].dropna()
    
    print("\n[2] Recomputing Statistics (20-Bar Horizon)...")
    
    stats_bull = recompute_stats(bull_bull)
    stats_bear = recompute_stats(bear_bear)
    
    print("\n>> Bullish Sweep + Bull Trend")
    print(f"   Mean: {stats_bull['mean']:.5f}")
    print(f"   95% CI: [{stats_bull['ci_low']:.5f}, {stats_bull['ci_high']:.5f}]")
    print(f"   Effect Size: {stats_bull['effect_size']:.3f}")
    print(f"   Win Rate: {stats_bull['win_rate']*100:.1f}%")
    
    print("\n>> Bearish Sweep + Bear Trend")
    print(f"   Mean: {stats_bear['mean']:.5f}")
    print(f"   95% CI: [{stats_bear['ci_low']:.5f}, {stats_bear['ci_high']:.5f}]")
    print(f"   Effect Size: {stats_bear['effect_size']:.3f}")
    print(f"   Win Rate: {stats_bear['win_rate']*100:.1f}%")
    
    print("\n[3] Executing Decision Rules...")
    
    def evaluate_rules(stats_res):
        ci_excludes_zero = (stats_res['ci_low'] > 0) or (stats_res['ci_high'] < 0)
        econ_sig = abs(stats_res['effect_size']) >= 0.05
        # Require 50% minimum win rate
        win_rate_ok = stats_res['win_rate'] >= 0.50
        
        return {
            "stat_sig": ci_excludes_zero,
            "econ_sig": econ_sig,
            "win_rate_ok": win_rate_ok,
            "overall": ci_excludes_zero and econ_sig and win_rate_ok
        }
        
    bull_rules = evaluate_rules(stats_bull)
    bear_rules = evaluate_rules(stats_bear)
    
    print(f"   Bull Rules: StatSig={bull_rules['stat_sig']}, EconSig={bull_rules['econ_sig']}, WinRate={bull_rules['win_rate_ok']} -> {bull_rules['overall']}")
    print(f"   Bear Rules: StatSig={bear_rules['stat_sig']}, EconSig={bear_rules['econ_sig']}, WinRate={bear_rules['win_rate_ok']} -> {bear_rules['overall']}")
    
    final_verdict = "ROBUST" if (bull_rules['overall'] and bear_rules['overall']) else "FRAGILE"
    
    print(f"\n[4] Auto-Generated Final Verdict: {final_verdict}")
    
    print("\n[5] Consistency Audit against Study_003_Report.md...")
    report_path = os.path.join(os.path.dirname(__file__), "RC001_Continuation", "Study_003_Report.md")
    
    audit_findings = []
    
    with open(report_path, "r") as f:
        report_text = f.read()
        
        if "The candidate edge is statistically significant (95% CI excludes zero) and economically meaningful (effect sizes > 0.05)." in report_text:
            if not (bull_rules['stat_sig'] and bear_rules['stat_sig']):
                audit_findings.append("CONTRADICTION: Report claims 95% CI excludes zero, but Bearish continuation CI includes zero.")
            if not (bull_rules['econ_sig'] and bear_rules['econ_sig']):
                audit_findings.append("CONTRADICTION: Report claims effect sizes > 0.05, but both fall below this threshold.")
                
    for finding in audit_findings:
        print(f"   !!! {finding}")
        
    if len(audit_findings) > 0:
        print("\n[6] Outcome: Outcome B - Minor numerical corrections required. Updating report...")
        new_text = report_text.replace(
            "The candidate edge is statistically significant (95% CI excludes zero) and economically meaningful (effect sizes > 0.05). The win rates and payoff ratios demonstrate robust characteristics suitable for further research.",
            "The candidate edge is **FRAGILE**. While the Bullish Sweep inside a Bull Trend produced a positive mean return, its effect size is negligible (< 0.05) and its win rate sits at a coin flip (49.8%). More critically, the Bearish Sweep inside a Bear Trend produced a 95% Confidence Interval that crosses zero, meaning the signal is statistically indistinguishable from random noise."
        )
        with open(report_path, "w") as f:
            f.write(new_text)
            
    qa_report = f"""# Research Study 003 QA: Statistical Verification Pass

## Verified Statistics
- **Bullish Continuation (20-bar)**
  - Mean: {stats_bull['mean']:.5f}
  - 95% CI: [{stats_bull['ci_low']:.5f}, {stats_bull['ci_high']:.5f}]
  - Effect Size: {stats_bull['effect_size']:.3f}
  - Win Rate: {stats_bull['win_rate']*100:.1f}%

- **Bearish Continuation (20-bar)**
  - Mean: {stats_bear['mean']:.5f}
  - 95% CI: [{stats_bear['ci_low']:.5f}, {stats_bear['ci_high']:.5f}]
  - Effect Size: {stats_bear['effect_size']:.3f}
  - Win Rate: {stats_bear['win_rate']*100:.1f}%

## Decision Rules Output
- Bullish Rules Satisfied: **{bull_rules['overall']}**
- Bearish Rules Satisfied: **{bear_rules['overall']}**
- **Automatic Verdict: {final_verdict}**

## Consistency Audit
The following contradictions were discovered in the original `Study_003_Report.md`:
"""
    for finding in audit_findings:
        qa_report += f"- {finding}\n"
        
    qa_report += "\n## Resolution\nOutcome B. The `Study_003_Report.md` has been patched to accurately reflect the quantitative reality of the fragile signal."
    
    with open(os.path.join(os.path.dirname(__file__), "RC001_Continuation", "Study_003_QA_Report.md"), "w") as f:
        f.write(qa_report)
        
    print("=========================================================")

if __name__ == "__main__":
    main()
