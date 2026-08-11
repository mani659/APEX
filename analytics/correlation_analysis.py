"""
=========================================================
APEX Quant Research Framework

Module      : analytics/correlation_analysis.py
Version     : 1.0

Description : Feature Correlation & Redundancy Analysis module.
              Evaluates Pearson correlation, absolute correlation,
              detects highly correlated feature pairs (|r| >= 0.95),
              computes partner counts and feature redundancy metrics,
              and generates reduction recommendations (KEEP, MERGE, DROP).
=========================================================
"""

from pathlib import Path
import time
from typing import Dict, List, Optional, Set, Tuple, Union

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

# Label/Outcome columns to exclude from feature correlation matrix
LABEL_COLS = [
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


def _extract_numeric_features(df: pd.DataFrame) -> List[str]:
    """
    Extract numeric feature column names, excluding timestamp and label columns.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.

    Returns
    -------
    List[str]
        List of feature column names.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    feature_cols = []
    for col in numeric_cols:
        col_lower = col.lower()
        if not any(k in col_lower for k in EXCLUDE_KEYWORDS) and col not in LABEL_COLS:
            feature_cols.append(col)

    return feature_cols


def _find_high_correlation_pairs(
    corr_matrix: pd.DataFrame, threshold: float = 0.95
) -> pd.DataFrame:
    """
    Detect highly correlated feature pairs where |r| >= threshold.

    Parameters
    ----------
    corr_matrix : pd.DataFrame
        Pearson correlation matrix.
    threshold : float
        Absolute correlation threshold (default 0.95).

    Returns
    -------
    pd.DataFrame
        DataFrame of feature pairs with correlation metrics.
    """
    cols = corr_matrix.columns
    n = len(cols)
    records = []

    corr_values = corr_matrix.values

    for i in range(n):
        for j in range(i + 1, n):
            val = corr_values[i, j]
            if not np.isnan(val) and abs(val) >= threshold:
                records.append(
                    {
                        "feature_a": cols[i],
                        "feature_b": cols[j],
                        "correlation": round(float(val), 6),
                        "abs_correlation": round(abs(float(val)), 6),
                    }
                )

    pairs_df = pd.DataFrame(records)
    if not pairs_df.empty:
        pairs_df = pairs_df.sort_values(by="abs_correlation", ascending=False).reset_index(drop=True)
    return pairs_df


def _compute_feature_redundancy(
    corr_matrix: pd.DataFrame,
    df: pd.DataFrame,
    threshold: float = 0.95,
) -> pd.DataFrame:
    """
    Compute redundancy metrics, partner counts (|r| >= 0.95), uniqueness score, and reduction actions.

    Parameters
    ----------
    corr_matrix : pd.DataFrame
        Pearson correlation matrix.
    df : pd.DataFrame
        Master dataset DataFrame.
    threshold : float
        Correlation threshold for partner counting (default 0.95).

    Returns
    -------
    pd.DataFrame
        Feature redundancy DataFrame.
    """
    features = corr_matrix.columns.tolist()
    records = []

    abs_corr_matrix = corr_matrix.abs()

    for col in features:
        series = df[col].dropna()
        std_val = float(series.std()) if not series.empty else 0.0

        # Absolute correlations excluding self
        other_abs_corrs = abs_corr_matrix[col].drop(labels=[col]).dropna()

        mean_abs_corr = float(other_abs_corrs.mean()) if not other_abs_corrs.empty else 0.0
        max_abs_corr = float(other_abs_corrs.max()) if not other_abs_corrs.empty else 0.0

        # Highly correlated partners
        partners = other_abs_corrs[other_abs_corrs >= threshold].index.tolist()
        partner_count = len(partners)

        redundancy_score = round(mean_abs_corr * 100.0, 2)
        uniqueness_score = round(max(0.0, 100.0 - redundancy_score), 2)

        # Action logic
        if std_val < 1e-6 or np.isnan(std_val):
            action = "DROP"
            reason = "Zero or near-zero variance (constant feature)"
        elif partner_count > 0:
            # Check if this feature has lower uniqueness than any of its partners
            partner_means = [float(abs_corr_matrix[p].drop(labels=[p]).mean()) for p in partners]
            if partner_means and mean_abs_corr >= min(partner_means):
                action = "MERGE"
                reason = f"Highly correlated (|r| >= {threshold}) with {partner_count} partner(s): {', '.join(partners[:3])}"
            else:
                action = "KEEP"
                reason = "Primary representative of correlation group"
        else:
            action = "KEEP"
            reason = "Unique feature with low redundancy"

        records.append(
            {
                "feature": col,
                "std": round(std_val, 6),
                "mean_abs_correlation": round(mean_abs_corr, 4),
                "max_abs_correlation": round(max_abs_corr, 4),
                "high_corr_partners_count": partner_count,
                "high_corr_partners": ", ".join(partners) if partners else "None",
                "redundancy_score": redundancy_score,
                "uniqueness_score": uniqueness_score,
                "action": action,
                "reason": reason,
            }
        )

    redundancy_df = pd.DataFrame(records)
    if not redundancy_df.empty:
        redundancy_df = redundancy_df.sort_values(by="uniqueness_score", ascending=False).reset_index(drop=True)
    return redundancy_df


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Perform feature correlation and redundancy analysis on master dataset.

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
    out_path = Path(output_dir) / "correlation"
    ensure_dir(out_path)

    if df.empty:
        return AnalyticsResult(
            module="correlation",
            success=False,
            rows=0,
            columns=0,
            files=0,
            metrics={
                "total_numeric_features": 0,
                "high_corr_pairs": 0,
                "max_corr_partners_count": 0,
                "recommended_drop": 0,
                "recommended_merge": 0,
                "recommended_keep": 0,
            },
            elapsed_seconds=time.time() - start_time,
            message="Input DataFrame is empty.",
        )

    n_rows, n_cols = df.shape

    # 1. Extract numeric features
    feature_cols = _extract_numeric_features(df)
    total_numeric = len(feature_cols)

    if total_numeric < 2:
        return AnalyticsResult(
            module="correlation",
            success=False,
            rows=n_rows,
            columns=n_cols,
            files=0,
            metrics={
                "total_numeric_features": total_numeric,
                "high_corr_pairs": 0,
                "max_corr_partners_count": 0,
                "recommended_drop": 0,
                "recommended_merge": 0,
                "recommended_keep": total_numeric,
            },
            elapsed_seconds=time.time() - start_time,
            message=f"Insufficient numeric features for correlation analysis ({total_numeric} found).",
        )

    # 2. Compute Pearson & Absolute Correlation Matrix
    corr_matrix = df[feature_cols].corr(method="pearson").fillna(0.0)
    file_corr = write_csv(corr_matrix.reset_index(), out_path / "correlation_matrix.csv")

    # 3. Detect Highly Correlated Pairs (|r| >= 0.95)
    high_pairs_df = _find_high_correlation_pairs(corr_matrix, threshold=0.95)
    file_pairs = write_csv(high_pairs_df, out_path / "high_correlation_pairs.csv")

    # 4. Compute Feature Redundancy & Partner Counts
    redundancy_df = _compute_feature_redundancy(corr_matrix, df, threshold=0.95)
    file_redundancy = write_csv(redundancy_df, out_path / "feature_redundancy.csv")

    # Metrics
    count_keep = int((redundancy_df["action"] == "KEEP").sum())
    count_merge = int((redundancy_df["action"] == "MERGE").sum())
    count_drop = int((redundancy_df["action"] == "DROP").sum())

    max_partners = int(redundancy_df["high_corr_partners_count"].max()) if not redundancy_df.empty else 0
    top_unique_names = redundancy_df.head(5)["feature"].tolist()
    top_redundant_names = redundancy_df.tail(5)["feature"].tolist()[::-1]

    # 5. Generate correlation_report.md
    report_md = f"""# APEX Quant Research Framework - Feature Correlation & Redundancy Report

**Generated:** {get_timestamp()}  
**Dataset Shape:** {n_rows:,} rows x {n_cols:,} columns  
**Evaluated Numeric Features:** {total_numeric}  

---

## 1. Executive Summary

This module evaluates feature-to-feature Pearson correlation matrices, detects highly correlated feature pairs ($|r| \\ge 0.95$), counts high-correlation partners for each feature, and provides actionable feature reduction recommendations (`KEEP`, `MERGE`, `DROP`).

- **Total Numeric Features Evaluated:** {total_numeric}
- **Highly Correlated Pairs ($|r| \\ge 0.95$):** {len(high_pairs_df)}
- **Max High-Correlation Partners Count:** {max_partners}
- **Recommended KEEP:** {count_keep}
- **Recommended MERGE:** {count_merge}
- **Recommended DROP:** {count_drop}

---

## 2. Feature Reduction Summary

Recommendations based on uniqueness score, zero-variance checks, and correlation partner counts:

| Action | Count | Percentage | Description |
| :--- | :--- | :--- | :--- |
| **KEEP** | {count_keep} | {count_keep/total_numeric*100:.1f}% | High unique information content or primary cluster representative |
| **MERGE** | {count_merge} | {count_merge/total_numeric*100:.1f}% | Highly redundant feature with 1+ high-correlation partner(s) |
| **DROP** | {count_drop} | {count_drop/total_numeric*100:.1f}% | Constant or near-constant zero-variance feature |

---

## 3. Most Unique vs Most Redundant Features

### Top 5 Most Unique Features
{df_to_markdown(redundancy_df.head(5)[['feature', 'std', 'mean_abs_correlation', 'high_corr_partners_count', 'uniqueness_score', 'action']], max_rows=10)}

### Top 5 Most Redundant Features
{df_to_markdown(redundancy_df.tail(5)[['feature', 'std', 'mean_abs_correlation', 'high_corr_partners_count', 'uniqueness_score', 'action']], max_rows=10)}

---

## 4. Top Highly Correlated Pairs ($|r| \\ge 0.95$)

{df_to_markdown(high_pairs_df.head(25), max_rows=25) if not high_pairs_df.empty else "_No feature pairs found with absolute correlation >= 0.95._"}

---

## 5. Feature Redundancy & Partner Details

{df_to_markdown(redundancy_df.head(30)[['feature', 'high_corr_partners_count', 'mean_abs_correlation', 'max_abs_correlation', 'action', 'reason']], max_rows=30)}

"""
    file_report_md = write_markdown(report_md, out_path / "correlation_report.md")

    # 6. Generate summary.json
    elapsed = time.time() - start_time
    metrics_dict = {
        "total_numeric_features": total_numeric,
        "high_corr_pairs": len(high_pairs_df),
        "max_corr_partners_count": max_partners,
        "recommended_drop": count_drop,
        "recommended_merge": count_merge,
        "recommended_keep": count_keep,
        "top_unique_features": top_unique_names,
        "top_redundant_features": top_redundant_names,
    }

    summary_data = {
        "framework": "APEX Quant Research Framework",
        "module": "correlation",
        "timestamp": get_timestamp(),
        "dataset_rows": n_rows,
        "dataset_columns": n_cols,
        "files_generated": [
            "correlation_matrix.csv",
            "high_correlation_pairs.csv",
            "feature_redundancy.csv",
            "correlation_report.md",
            "summary.json",
        ],
        "metrics": metrics_dict,
        "elapsed_seconds": round(elapsed, 4),
        "message": f"Correlation analysis completed successfully. Found {len(high_pairs_df)} high correlation pairs across {total_numeric} features.",
    }

    file_summary_json = write_json(summary_data, out_path / "summary.json")

    if verbose:
        print(
            f"[analytics.correlation] Analyzed {total_numeric} features in {elapsed:.2f}s. "
            f"Found {len(high_pairs_df)} high-corr pairs (|r| >= 0.95). "
            f"Recommendations: {count_keep} KEEP, {count_merge} MERGE, {count_drop} DROP."
        )

    return AnalyticsResult(
        module="correlation",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=5,
        metrics=metrics_dict,
        elapsed_seconds=elapsed,
        message=f"Correlation analysis completed successfully. Found {len(high_pairs_df)} high correlation pairs across {total_numeric} features.",
    )
