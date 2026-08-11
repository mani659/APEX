"""
=========================================================
APEX Quant Research Framework

Module      : analytics/hypothesis_engine.py
Version     : 1.0

Description : Hypothesis Engine module (Analytics V4).
              Automatically discovers two-condition market combinations,
              evaluates statistical edge, applies quality filters,
              computes transparent confidence & robustness scores,
              and ranks research hypotheses.
=========================================================
"""

from pathlib import Path
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from analytics.utils import (
    AnalyticsResult,
    df_to_markdown,
    ensure_dir,
    get_timestamp,
    write_csv,
    write_json,
    write_markdown,
)

# Outcome/Label columns to exclude from condition discovery
OUTCOME_COLS = [
    "return",
    "future_return",
    "future_direction",
    "future_up",
    "future_down",
    "future_max_up",
    "future_max_down",
    "mfe",
    "mae",
    "survived",
    "reward_risk",
    "good_execution",
    "bad_execution",
]

EXCLUDE_KEYWORDS = ["datetime", "date", "time", "row_id", "timestamp"]


def _discover_candidate_conditions(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Automatically discover atomic boolean, binary, and small-cardinality discrete conditions.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.

    Returns
    -------
    List[Dict[str, Any]]
        List of condition dicts with 'name', 'col', 'val', and 'mask'.
    """
    conditions = []
    cols = df.columns

    for col in cols:
        col_lower = col.lower()
        if any(k in col_lower for k in EXCLUDE_KEYWORDS) or col in OUTCOME_COLS:
            continue

        series = df[col].dropna()
        if series.empty:
            continue

        n_unique = series.nunique()

        # Check boolean or binary integer (<= 2 unique values)
        if pd.api.types.is_bool_dtype(df[col]) or n_unique <= 2:
            unique_vals = series.unique()
            for val in unique_vals:
                if val in [1, True, "1", "true", "True"]:
                    mask = df[col] == val
                    conditions.append(
                        {
                            "name": f"{col} == {val}",
                            "col": col,
                            "val": val,
                            "mask": mask,
                        }
                    )
        # Small cardinality categorical / discrete (3 to 10 unique values)
        elif 3 <= n_unique <= 10:
            unique_vals = series.unique()
            for val in unique_vals:
                mask = df[col] == val
                conditions.append(
                    {
                        "name": f"{col} == {val}",
                        "col": col,
                        "val": val,
                        "mask": mask,
                    }
                )

    return conditions


def _evaluate_hypothesis_pairs(
    df: pd.DataFrame,
    conditions: List[Dict[str, Any]],
    min_samples: int = 200,
    min_coverage_pct: float = 0.25,
) -> Tuple[pd.DataFrame, int, int]:
    """
    Generate and evaluate all 2-condition combinations against quality filters.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.
    conditions : List[Dict[str, Any]]
        Discovered atomic candidate conditions.
    min_samples : int
        Minimum row count filter (default 200).
    min_coverage_pct : float
        Minimum coverage percentage filter (default 0.25%).

    Returns
    -------
    Tuple[pd.DataFrame, int, int]
        - DataFrame of evaluated & accepted hypotheses.
        - Total pairs tested count.
        - Total pairs rejected count.
    """
    total_rows = len(df)
    n_cond = len(conditions)

    global_mean_fret = float(df["future_return"].mean()) if "future_return" in df.columns else 0.0
    global_std_fret = float(df["future_return"].std()) if "future_return" in df.columns else 1e-4
    global_mean_ret = float(df["return"].mean()) if "return" in df.columns else 0.0

    records = []
    pairs_tested = 0
    pairs_rejected = 0

    for i in range(n_cond):
        c1 = conditions[i]
        for j in range(i + 1, n_cond):
            c2 = conditions[j]

            # Enforce distinct columns
            if c1["col"] == c2["col"]:
                continue

            pairs_tested += 1

            # Vectorized bitwise AND
            pair_mask = c1["mask"] & c2["mask"]
            sample_count = int(pair_mask.sum())
            coverage_pct = float(sample_count / total_rows * 100) if total_rows > 0 else 0.0

            # Quality filters
            if sample_count < min_samples or coverage_pct < min_coverage_pct:
                pairs_rejected += 1
                continue

            sub_df = df.loc[pair_mask]
            pair_name = f"{c1['name']} AND {c2['name']}"

            # Return statistics
            mean_ret = float(sub_df["return"].mean()) if "return" in sub_df.columns else np.nan
            median_ret = float(sub_df["return"].median()) if "return" in sub_df.columns else np.nan
            ret_std = float(sub_df["return"].std()) if "return" in sub_df.columns else np.nan
            pos_ret_pct = (
                float((sub_df["return"] > 0).mean() * 100) if "return" in sub_df.columns else np.nan
            )
            neg_ret_pct = (
                float((sub_df["return"] < 0).mean() * 100) if "return" in sub_df.columns else np.nan
            )

            # Future return statistics
            mean_fret = (
                float(sub_df["future_return"].mean()) if "future_return" in sub_df.columns else np.nan
            )
            median_fret = (
                float(sub_df["future_return"].median()) if "future_return" in sub_df.columns else np.nan
            )
            fret_std = (
                float(sub_df["future_return"].std()) if "future_return" in sub_df.columns else 1e-4
            )

            # MFE & MAE
            mfe_col = "mfe" if "mfe" in sub_df.columns else ("future_max_up" if "future_max_up" in sub_df.columns else None)
            avg_mfe = float(sub_df[mfe_col].mean()) if mfe_col else np.nan

            mae_col = "mae" if "mae" in sub_df.columns else ("future_max_down" if "future_max_down" in sub_df.columns else None)
            avg_mae = float(sub_df[mae_col].mean()) if mae_col else np.nan

            # Confidence & Scoring Metrics
            target_mean = mean_fret if not np.isnan(mean_fret) else (mean_ret if not np.isnan(mean_ret) else 0.0)
            base_mean = global_mean_fret if not np.isnan(mean_fret) else global_mean_ret
            diff_mean = abs(target_mean - base_mean)

            # 1. Edge score (0-100 scale based on excess return magnitude)
            edge_score = max(0.0, min(100.0, (diff_mean / (global_std_fret + 1e-8)) * 5000.0))

            # 2. Sample quality score (0-100 scale)
            sample_quality_score = max(0.0, min(100.0, (sample_count / 1000.0) * 100.0))

            # 3. Confidence score (t-statistic based)
            t_stat = abs(target_mean) / ((fret_std / np.sqrt(sample_count)) + 1e-8)
            confidence_score = max(0.0, min(100.0, t_stat * 20.0))

            # 4. Robustness score
            robustness_score = 0.5 * sample_quality_score + 0.5 * confidence_score

            # 5. Overall hypothesis score
            overall_score = round(
                0.40 * edge_score + 0.30 * confidence_score + 0.30 * sample_quality_score, 2
            )

            records.append(
                {
                    "hypothesis": pair_name,
                    "condition_1": c1["name"],
                    "condition_2": c2["name"],
                    "sample_count": sample_count,
                    "coverage_pct": round(coverage_pct, 2),
                    "mean_return": round(mean_ret, 6) if not np.isnan(mean_ret) else np.nan,
                    "median_return": round(median_ret, 6) if not np.isnan(median_ret) else np.nan,
                    "pos_return_pct": round(pos_ret_pct, 2) if not np.isnan(pos_ret_pct) else np.nan,
                    "neg_return_pct": round(neg_ret_pct, 2) if not np.isnan(neg_ret_pct) else np.nan,
                    "mean_future_return": round(mean_fret, 6) if not np.isnan(mean_fret) else np.nan,
                    "median_future_return": round(median_fret, 6) if not np.isnan(median_fret) else np.nan,
                    "avg_mfe": round(avg_mfe, 6) if not np.isnan(avg_mfe) else np.nan,
                    "avg_mae": round(avg_mae, 6) if not np.isnan(avg_mae) else np.nan,
                    "edge_score": round(edge_score, 2),
                    "sample_quality_score": round(sample_quality_score, 2),
                    "confidence_score": round(confidence_score, 2),
                    "robustness_score": round(robustness_score, 2),
                    "overall_score": overall_score,
                }
            )

    hyp_df = pd.DataFrame(records)
    if not hyp_df.empty:
        hyp_df = hyp_df.sort_values(by="overall_score", ascending=False).reset_index(drop=True)

    return hyp_df, pairs_tested, pairs_rejected


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Perform Hypothesis Engine discovery and ranking on master dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame (read-only).
    output_dir : Union[str, Path]
        Target base report directory (e.g. reports/analytics/latest).
    verbose : bool
        Whether to log progress to stdout.

    Returns
    -------
    AnalyticsResult
        Standardized analytics result object.
    """
    start_time = time.time()
    out_path = Path(output_dir) / "hypotheses"
    ensure_dir(out_path)

    if df.empty:
        return AnalyticsResult(
            module="hypothesis_engine",
            success=False,
            rows=0,
            columns=0,
            files=0,
            metrics={
                "candidate_conditions": 0,
                "pairs_tested": 0,
                "pairs_rejected": 0,
                "accepted_hypotheses": 0,
                "best_hypothesis": "N/A",
                "average_edge_score": 0.0,
            },
            elapsed_seconds=time.time() - start_time,
            message="Input DataFrame is empty.",
        )

    n_rows, n_cols = df.shape

    # 1. Candidate Condition Discovery
    conditions = _discover_candidate_conditions(df)
    n_cond = len(conditions)

    # 2. Pairwise Evaluation & Quality Filtering
    hyp_df, pairs_tested, pairs_rejected = _evaluate_hypothesis_pairs(
        df, conditions, min_samples=200, min_coverage_pct=0.25
    )

    n_accepted = len(hyp_df)

    # 3. Output files generation
    top_50_df = hyp_df.head(50) if not hyp_df.empty else pd.DataFrame()
    bottom_50_df = hyp_df.tail(50) if not hyp_df.empty else pd.DataFrame()

    file_all = write_csv(hyp_df, out_path / "all_hypotheses.csv")
    file_top = write_csv(top_50_df, out_path / "top_hypotheses.csv")
    file_bottom = write_csv(bottom_50_df, out_path / "bottom_hypotheses.csv")

    # Summary metrics table
    avg_edge_score = float(hyp_df["edge_score"].mean()) if not hyp_df.empty else 0.0
    best_hypothesis_str = (
        f"{hyp_df.iloc[0]['hypothesis']} (overall_score: {hyp_df.iloc[0]['overall_score']})"
        if not hyp_df.empty
        else "N/A"
    )

    summary_records = [
        {"metric": "Candidate Conditions Discovered", "value": n_cond},
        {"metric": "Total 2-Condition Pairs Tested", "value": pairs_tested},
        {"metric": "Pairs Rejected by Quality Filters", "value": pairs_rejected},
        {"metric": "Accepted Valid Hypotheses", "value": n_accepted},
        {"metric": "Average Edge Score", "value": round(avg_edge_score, 2)},
        {"metric": "Top Hypothesis Overall Score", "value": hyp_df.iloc[0]["overall_score"] if not hyp_df.empty else 0.0},
    ]
    summary_df = pd.DataFrame(summary_records)
    file_summary_csv = write_csv(summary_df, out_path / "hypothesis_summary.csv")

    # 4. Generate hypothesis_report.md
    report_md = f"""# APEX Quant Research Framework - Hypothesis Discovery Report

**Generated:** {get_timestamp()}  
**Dataset Shape:** {n_rows:,} rows x {n_cols:,} columns  
**Candidate Conditions Discovered:** {n_cond}  
**Total Pairs Tested:** {pairs_tested:,} | **Accepted:** {n_accepted:,} | **Rejected:** {pairs_rejected:,}  

---

## 1. Executive Summary

This module automatically discovers two-condition market combinations, applies sample size & coverage filters, and evaluates statistical edge and confidence scores to generate hypothesis candidates for quantitative research.

- **Candidate Conditions Discovered:** {n_cond}
- **Total Condition Pairs Tested:** {pairs_tested:,}
- **Accepted Valid Hypotheses:** {n_accepted:,}
- **Best Rated Hypothesis:** {best_hypothesis_str}
- **Average Edge Score:** {avg_edge_score:.2f} / 100

---

## 2. Score Definitions & Formulas

Every hypothesis is ranked on a 0–100 scale using transparent statistical formulas:

1. **Edge Score**: Standardized excess return magnitude relative to dataset global return standard deviation.
2. **Sample Quality Score**: min(100.0, (sample_count / 1000) * 100).
3. **Confidence Score**: t-statistic scale relative to subgroup return variance.
4. **Robustness Score**: 0.5 * Sample Quality Score + 0.5 * Confidence Score.
5. **Overall Hypothesis Score**: 0.40 * Edge Score + 0.30 * Confidence Score + 0.30 * Sample Quality Score.

---

## 3. Top 10 High-Ranking Hypotheses

{df_to_markdown(top_50_df.head(10)[['hypothesis', 'sample_count', 'coverage_pct', 'mean_future_return', 'edge_score', 'confidence_score', 'overall_score']], max_rows=15)}

---

## 4. Weakest Hypotheses (Bottom 10)

{df_to_markdown(bottom_50_df.head(10)[['hypothesis', 'sample_count', 'coverage_pct', 'mean_future_return', 'edge_score', 'confidence_score', 'overall_score']], max_rows=15)}

---

## 5. Most Common Conditions in Top Hypotheses

"""
    if not top_50_df.empty:
        cond_counts = (
            pd.concat([top_50_df["condition_1"], top_50_df["condition_2"]])
            .value_counts()
            .reset_index()
        )
        cond_counts.columns = ["condition", "occurrences_in_top_50"]
        report_md += df_to_markdown(cond_counts.head(10), max_rows=15) + "\n\n"
    else:
        report_md += "_No hypotheses available for condition frequency breakdown._\n\n"

    report_md += "---\n\n## 6. Coverage & Quality Filter Summary\n\n"
    report_md += df_to_markdown(summary_df, max_rows=10)

    file_report_md = write_markdown(report_md, out_path / "hypothesis_report.md")

    # 5. Generate summary.json
    elapsed = time.time() - start_time
    metrics_dict = {
        "candidate_conditions": n_cond,
        "pairs_tested": pairs_tested,
        "pairs_rejected": pairs_rejected,
        "accepted_hypotheses": n_accepted,
        "best_hypothesis": best_hypothesis_str,
        "average_edge_score": round(avg_edge_score, 2),
    }

    summary_data = {
        "framework": "APEX Quant Research Framework",
        "module": "hypothesis_engine",
        "timestamp": get_timestamp(),
        "dataset_rows": n_rows,
        "dataset_columns": n_cols,
        "files_generated": [
            "top_hypotheses.csv",
            "bottom_hypotheses.csv",
            "all_hypotheses.csv",
            "hypothesis_summary.csv",
            "hypothesis_report.md",
            "summary.json",
        ],
        "metrics": metrics_dict,
        "elapsed_seconds": round(elapsed, 4),
        "message": f"Hypothesis discovery completed. Tested {pairs_tested} pairs, accepted {n_accepted} hypotheses.",
    }

    file_summary_json = write_json(summary_data, out_path / "summary.json")

    if verbose:
        print(
            f"[analytics.hypothesis_engine] Discovered {n_cond} conditions, tested {pairs_tested} pairs in {elapsed:.2f}s. "
            f"Accepted {n_accepted} valid hypotheses (Best score: {hyp_df.iloc[0]['overall_score'] if not hyp_df.empty else 0.0})."
        )

    return AnalyticsResult(
        module="hypothesis_engine",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=6,
        metrics=metrics_dict,
        elapsed_seconds=elapsed,
        message=f"Hypothesis discovery completed. Tested {pairs_tested} pairs, accepted {n_accepted} hypotheses.",
    )
