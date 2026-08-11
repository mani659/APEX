"""
=========================================================
APEX Quant Research Framework

Module      : analytics/stability_analysis.py
Version     : 1.0

Description : Stability Analysis module (Analytics V2).
              Evaluates feature and label stability across time segments
              (yearly, quarterly, monthly), calculating drift, period CV,
              max global deviation, stability scores, and instability flags.
=========================================================
"""

from pathlib import Path
import time
from typing import Dict, List, Optional, Tuple, Union

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

# Known label columns to evaluate for instability
LABEL_COLS = [
    "future_return",
    "future_direction",
    "good_execution",
    "bad_execution",
    "pnl",
    "mfe",
    "mae",
    "return",
]

EXCLUDE_KEYWORDS = ["datetime", "date", "time", "row_id", "timestamp"]


def _detect_datetime_series(df: pd.DataFrame) -> Optional[pd.Series]:
    """
    Automatically detect a datetime column or DatetimeIndex in DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.

    Returns
    -------
    Optional[pd.Series]
        Parsed pandas datetime Series if available, else None.
    """
    if "datetime" in df.columns:
        return pd.to_datetime(df["datetime"], errors="coerce")

    if isinstance(df.index, pd.DatetimeIndex):
        return pd.Series(df.index, index=df.index)

    # Search datetime64 or string date columns
    for col in df.columns:
        col_lower = str(col).lower()
        if any(k in col_lower for k in ["datetime", "date", "timestamp"]):
            try:
                dt_series = pd.to_datetime(df[col], errors="coerce")
                if dt_series.notna().sum() > 0:
                    return dt_series
            except Exception:
                continue

    return None


def _compute_period_statistics(
    df: pd.DataFrame,
    dt_series: pd.Series,
    freq: str,
    target_cols: List[str],
) -> Tuple[pd.DataFrame, int]:
    """
    Compute distribution statistics (mean, median, std, var, skew, kurt, missing %, CV) per time period.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.
    dt_series : pd.Series
        Datetime Series.
    freq : str
        Period frequency: 'Y' (yearly), 'Q' (quarterly), 'M' (monthly).
    target_cols : List[str]
        List of numeric column names to evaluate.

    Returns
    -------
    Tuple[pd.DataFrame, int]
        - DataFrame of period statistics.
        - Number of distinct periods evaluated.
    """
    if dt_series is None or dt_series.dropna().empty:
        return pd.DataFrame(), 0

    valid_mask = dt_series.notna()
    if not valid_mask.any():
        return pd.DataFrame(), 0

    valid_df = df.loc[valid_mask]
    valid_dt = dt_series.loc[valid_mask]

    if freq == "Y":
        period_group = valid_dt.dt.year.astype(str)
    elif freq == "Q":
        period_group = valid_dt.dt.to_period("Q").astype(str)
    elif freq == "M":
        period_group = valid_dt.dt.to_period("M").astype(str)
    else:
        period_group = valid_dt.dt.year.astype(str)

    unique_periods = sorted(period_group.unique())
    if len(unique_periods) == 0:
        return pd.DataFrame(), 0

    records = []
    for p_name, group_indices in valid_df.groupby(period_group).groups.items():
        sub_df = valid_df.loc[group_indices]
        p_rows = len(sub_df)

        for col in target_cols:
            series = sub_df[col].dropna()
            total_cnt = len(sub_df[col])
            missing_cnt = total_cnt - len(series)
            missing_pct = float(missing_cnt / total_cnt * 100) if total_cnt > 0 else 0.0

            if series.empty:
                records.append(
                    {
                        "period": str(p_name),
                        "column": col,
                        "rows": p_rows,
                        "mean": np.nan,
                        "median": np.nan,
                        "std": np.nan,
                        "variance": np.nan,
                        "skew": np.nan,
                        "kurtosis": np.nan,
                        "missing_pct": round(missing_pct, 2),
                        "cv": np.nan,
                    }
                )
                continue

            mean_val = float(series.mean())
            median_val = float(series.median())
            std_val = float(series.std()) if len(series) > 1 else 0.0
            var_val = float(series.var()) if len(series) > 1 else 0.0
            skew_val = float(series.skew()) if len(series) > 2 else 0.0
            kurt_val = float(series.kurtosis()) if len(series) > 3 else 0.0
            cv_val = std_val / (abs(mean_val) + 1e-8)

            records.append(
                {
                    "period": str(p_name),
                    "column": col,
                    "rows": p_rows,
                    "mean": round(mean_val, 6),
                    "median": round(median_val, 6),
                    "std": round(std_val, 6),
                    "variance": round(var_val, 6),
                    "skew": round(skew_val, 4),
                    "kurtosis": round(kurt_val, 4),
                    "missing_pct": round(missing_pct, 2),
                    "cv": round(cv_val, 4),
                }
            )

    res_df = pd.DataFrame(records)
    return res_df, len(unique_periods)


def _compute_stability_metrics(
    df: pd.DataFrame,
    period_stats_df: pd.DataFrame,
    target_cols: List[str],
) -> pd.DataFrame:
    """
    Compute stability metrics across time periods for all evaluated features and labels.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.
    period_stats_df : pd.DataFrame
        Period-by-period statistics DataFrame.
    target_cols : List[str]
        List of numeric column names.

    Returns
    -------
    pd.DataFrame
        Overall feature & label stability metrics DataFrame.
    """
    records = []

    if period_stats_df.empty:
        # Fallback if no time periods present
        for col in target_cols:
            series = df[col].dropna()
            g_mean = float(series.mean()) if not series.empty else 0.0
            g_std = float(series.std()) if not series.empty else 0.0
            records.append(
                {
                    "column": col,
                    "is_label": col in LABEL_COLS,
                    "global_mean": round(g_mean, 6),
                    "global_std": round(g_std, 6),
                    "cv_period_means": 0.0,
                    "drift_first_last": 0.0,
                    "max_dev_global": 0.0,
                    "stability_score": 100.0,
                    "instability_flag": "FALSE",
                }
            )
        return pd.DataFrame(records)

    indexed = period_stats_df.set_index(["column", "period"])

    for col in target_cols:
        series = df[col].dropna()
        g_mean = float(series.mean()) if not series.empty else 0.0
        g_std = float(series.std()) if not series.empty else 0.0

        if col in indexed.index.get_level_values(0):
            sub_p = period_stats_df[period_stats_df["column"] == col]
            p_means = sub_p["mean"].dropna().values

            if len(p_means) > 0:
                mean_p_means = float(np.mean(p_means))
                std_p_means = float(np.std(p_means))
                cv_period_means = std_p_means / (abs(mean_p_means) + 1e-8)

                p_first = p_means[0]
                p_last = p_means[-1]
                drift_first_last = (p_last - p_first) / (g_std + 1e-8)
                max_dev_global = float(np.max(np.abs(p_means - g_mean)))

                stability_score = max(0.0, min(100.0, 100.0 / (1.0 + cv_period_means)))
                is_instable = (cv_period_means > 0.5) or (stability_score < 50.0)
            else:
                cv_period_means = 0.0
                drift_first_last = 0.0
                max_dev_global = 0.0
                stability_score = 100.0
                is_instable = False
        else:
            cv_period_means = 0.0
            drift_first_last = 0.0
            max_dev_global = 0.0
            stability_score = 100.0
            is_instable = False

        records.append(
            {
                "column": col,
                "is_label": col in LABEL_COLS,
                "global_mean": round(g_mean, 6),
                "global_std": round(g_std, 6),
                "cv_period_means": round(cv_period_means, 4),
                "drift_first_last": round(drift_first_last, 4),
                "max_dev_global": round(max_dev_global, 6),
                "stability_score": round(stability_score, 2),
                "instability_flag": "TRUE" if is_instable else "FALSE",
            }
        )

    res_df = pd.DataFrame(records)
    if not res_df.empty:
        res_df = res_df.sort_values(by="stability_score", ascending=False).reset_index(drop=True)
    return res_df


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
    config: Optional[dict] = None,
) -> AnalyticsResult:
    """
    Perform stability analysis across time segments on master dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame (read-only).
    output_dir : Union[str, Path]
        Target base report directory (e.g. reports/analytics/latest).
    verbose : bool
        Whether to log progress to stdout.
    config : Optional[dict]
        Optional configuration parameters.

    Returns
    -------
    AnalyticsResult
        Standardized analytics result object.
    """
    start_time = time.time()
    out_path = Path(output_dir) / "stability"
    ensure_dir(out_path)

    if df.empty:
        return AnalyticsResult(
            module="stability",
            success=False,
            rows=0,
            columns=0,
            files=0,
            metrics={
                "overall_score": 0.0,
                "yearly_periods_count": 0,
                "quarterly_periods_count": 0,
                "monthly_periods_count": 0,
                "stable_features": [],
                "unstable_features": [],
                "unstable_labels": [],
            },
            elapsed_seconds=time.time() - start_time,
            message="Input DataFrame is empty.",
        )

    n_rows, n_cols = df.shape

    # 1. Select numeric features and present labels
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    target_cols = [
        c
        for c in numeric_cols
        if not any(k in c.lower() for k in EXCLUDE_KEYWORDS)
    ]

    # 2. Time Segmentation
    dt_series = _detect_datetime_series(df)

    yearly_df, n_years = _compute_period_statistics(df, dt_series, "Y", target_cols)
    quarterly_df, n_quarters = _compute_period_statistics(df, dt_series, "Q", target_cols)
    monthly_df, n_months = _compute_period_statistics(df, dt_series, "M", target_cols)

    file_yearly = write_csv(yearly_df, out_path / "yearly_statistics.csv")
    file_quarterly = write_csv(quarterly_df, out_path / "quarterly_statistics.csv")
    file_monthly = write_csv(monthly_df, out_path / "monthly_statistics.csv")

    # Primary period stats used for stability scoring (monthly if available else quarterly/yearly)
    primary_period_df = (
        monthly_df if not monthly_df.empty else (quarterly_df if not quarterly_df.empty else yearly_df)
    )

    # 3. Compute Stability Metrics
    stab_df = _compute_stability_metrics(df, primary_period_df, target_cols)
    file_stab = write_csv(stab_df, out_path / "feature_stability.csv")

    # Features vs Labels split
    feature_stab_df = stab_df[~stab_df["is_label"]].copy()
    label_stab_df = stab_df[stab_df["is_label"]].copy()

    top_stable_features = feature_stab_df.head(5)["column"].tolist() if not feature_stab_df.empty else []
    top_unstable_features = (
        feature_stab_df.tail(5)["column"].tolist()[::-1] if not feature_stab_df.empty else []
    )

    largest_drift_df = (
        stab_df.reindex(stab_df["drift_first_last"].abs().sort_values(ascending=False).index)
        if not stab_df.empty
        else pd.DataFrame()
    )

    unstable_labels = (
        label_stab_df[label_stab_df["instability_flag"] == "TRUE"]["column"].tolist()
        if not label_stab_df.empty
        else []
    )

    overall_score = float(stab_df["stability_score"].mean()) if not stab_df.empty else 100.0

    # 4. Generate stability_summary.md
    report_md = f"""# APEX Quant Research Framework - Feature & Label Stability Report

**Generated:** {get_timestamp()}  
**Dataset Shape:** {n_rows:,} rows x {n_cols:,} columns  
**Overall Stability Score:** **{overall_score:.2f} / 100**  
**Time Periods Evaluated:** {n_years} Year(s), {n_quarters} Quarter(s), {n_months} Month(s)  

---

## 1. Executive Summary

This module evaluates whether feature and label distributions remain stable across time segments (yearly, quarterly, monthly) rather than optimizing trading strategies.

- **Overall Stability Score:** **{overall_score:.2f} / 100**
- **Evaluated Time History:** {n_years} Year(s) | {n_quarters} Quarter(s) | {n_months} Month(s)
- **Top Stable Features:** `{", ".join(top_stable_features) if top_stable_features else "None"}`
- **Least Stable Features:** `{", ".join(top_unstable_features) if top_unstable_features else "None"}`
- **Unstable Labels Flagged:** `{", ".join(unstable_labels) if unstable_labels else "None (All Labels Stable)"}`

---

## 2. Feature Stability Highlights

### Most Stable Features (Top 5)
{df_to_markdown(feature_stab_df.head(5)[['column', 'global_mean', 'global_std', 'cv_period_means', 'drift_first_last', 'stability_score', 'instability_flag']], max_rows=10) if not feature_stab_df.empty else "_No feature metrics available._"}

### Least Stable Features (Top 5)
{df_to_markdown(feature_stab_df.tail(5)[['column', 'global_mean', 'global_std', 'cv_period_means', 'drift_first_last', 'stability_score', 'instability_flag']], max_rows=10) if not feature_stab_df.empty else "_No feature metrics available._"}

---

## 3. Largest Distribution Drift (First vs Last Period)

Top columns experiencing highest relative drift between initial and final time segments:

{df_to_markdown(largest_drift_df.head(10)[['column', 'is_label', 'global_mean', 'global_std', 'drift_first_last', 'max_dev_global', 'stability_score']], max_rows=15) if not largest_drift_df.empty else "_No drift metrics available._"}

---

## 4. Label Stability Breakdown

Evaluation of target outcome labels across time periods:

{df_to_markdown(label_stab_df[['column', 'global_mean', 'global_std', 'cv_period_means', 'drift_first_last', 'max_dev_global', 'stability_score', 'instability_flag']], max_rows=15) if not label_stab_df.empty else "_No label columns present in dataset._"}

---

## 5. Time Segment Coverage Overview

- **Yearly Periods:** {n_years}
- **Quarterly Periods:** {n_quarters}
- **Monthly Periods:** {n_months}
"""

    file_report_md = write_markdown(report_md, out_path / "stability_summary.md")

    # 5. Generate summary.json
    elapsed = time.time() - start_time
    metrics_dict = {
        "overall_score": round(overall_score, 2),
        "yearly_periods_count": n_years,
        "quarterly_periods_count": n_quarters,
        "monthly_periods_count": n_months,
        "stable_features": top_stable_features,
        "unstable_features": top_unstable_features,
        "unstable_labels": unstable_labels,
    }

    summary_data = {
        "framework": "APEX Quant Research Framework",
        "module": "stability",
        "timestamp": get_timestamp(),
        "dataset_rows": n_rows,
        "dataset_columns": n_cols,
        "files_generated": [
            "yearly_statistics.csv",
            "quarterly_statistics.csv",
            "monthly_statistics.csv",
            "feature_stability.csv",
            "stability_summary.md",
            "summary.json",
        ],
        "metrics": metrics_dict,
        "elapsed_seconds": round(elapsed, 4),
        "message": f"Stability analysis completed across {n_months} monthly segments. Overall Score: {overall_score:.2f}/100.",
    }

    file_summary_json = write_json(summary_data, out_path / "summary.json")

    if verbose:
        print(
            f"[analytics.stability_analysis] Completed analysis in {elapsed:.2f}s across {n_months} monthly segments. "
            f"Overall Stability Score: {overall_score:.2f}/100."
        )

    return AnalyticsResult(
        module="stability",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=6,
        metrics=metrics_dict,
        elapsed_seconds=elapsed,
        message=f"Stability analysis completed across {n_months} monthly segments. Overall Score: {overall_score:.2f}/100.",
    )
