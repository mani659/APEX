"""
========================================================
APEX Quant Research Framework
Module      : analytics/regime_analysis.py
Description : Market regime analysis analytics module (Analytics V2).
========================================================
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

# Expected columns for regime detection & outcome evaluation
EXPECTED_REGIME_COLS = [
    "trend_strength",
    "market_structure",
    "volatility_expanding",
    "ema_stack_bull",
    "ema_stack_bear",
    "session",
    "asian",
    "london",
    "newyork",
    "overlap",
    "future_direction",
    "future_return",
    "good_execution",
    "bad_execution",
    "return",
    "body_pct",
    "body_abs",
]


def _compute_regime_stats(
    df: pd.DataFrame, mask: pd.Series, regime_name: str
) -> Dict[str, Union[str, int, float]]:
    """
    Compute vectorized summary statistics for a given regime mask.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.
    mask : pd.Series
        Boolean series defining the regime subset.
    regime_name : str
        Human-readable name of the regime.

    Returns
    -------
    Dict[str, Union[str, int, float]]
        Dictionary of calculated metrics for the regime.
    """
    total_rows = len(df)
    sub = df.loc[mask]
    n_rows = len(sub)
    pct_dataset = float(n_rows / total_rows * 100) if total_rows > 0 else 0.0

    stats: Dict[str, Union[str, int, float]] = {
        "regime": regime_name,
        "rows": n_rows,
        "pct_dataset": round(pct_dataset, 2),
    }

    if n_rows == 0:
        stats.update(
            {
                "mean_return": np.nan,
                "median_return": np.nan,
                "std_return": np.nan,
                "pos_return_pct": np.nan,
                "neg_return_pct": np.nan,
                "mean_future_return": np.nan,
                "median_future_return": np.nan,
                "avg_mfe": np.nan,
                "avg_mae": np.nan,
                "avg_holding_period": np.nan,
                "good_execution_pct": np.nan,
                "bad_execution_pct": np.nan,
                "future_direction_balance": np.nan,
            }
        )
        return stats

    # 1. Return statistics
    if "return" in df.columns:
        ret_series = sub["return"].dropna()
        if not ret_series.empty:
            stats["mean_return"] = float(ret_series.mean())
            stats["median_return"] = float(ret_series.median())
            stats["std_return"] = float(ret_series.std())
            stats["pos_return_pct"] = float((ret_series > 0).mean() * 100)
            stats["neg_return_pct"] = float((ret_series < 0).mean() * 100)
        else:
            stats["mean_return"] = np.nan
            stats["median_return"] = np.nan
            stats["std_return"] = np.nan
            stats["pos_return_pct"] = np.nan
            stats["neg_return_pct"] = np.nan
    else:
        stats["mean_return"] = np.nan
        stats["median_return"] = np.nan
        stats["std_return"] = np.nan
        stats["pos_return_pct"] = np.nan
        stats["neg_return_pct"] = np.nan

    # 2. Future return statistics
    if "future_return" in df.columns:
        f_ret_series = sub["future_return"].dropna()
        if not f_ret_series.empty:
            stats["mean_future_return"] = float(f_ret_series.mean())
            stats["median_future_return"] = float(f_ret_series.median())
        else:
            stats["mean_future_return"] = np.nan
            stats["median_future_return"] = np.nan
    else:
        stats["mean_future_return"] = np.nan
        stats["median_future_return"] = np.nan

    # 3. MFE (Maximum Favorable Excursion)
    mfe_col = "mfe" if "mfe" in df.columns else ("future_max_up" if "future_max_up" in df.columns else None)
    if mfe_col:
        mfe_s = sub[mfe_col].dropna()
        stats["avg_mfe"] = float(mfe_s.mean()) if not mfe_s.empty else np.nan
    else:
        stats["avg_mfe"] = np.nan

    # 4. MAE (Maximum Adverse Excursion)
    mae_col = "mae" if "mae" in df.columns else ("future_max_down" if "future_max_down" in df.columns else None)
    if mae_col:
        mae_s = sub[mae_col].dropna()
        stats["avg_mae"] = float(mae_s.mean()) if not mae_s.empty else np.nan
    else:
        stats["avg_mae"] = np.nan

    # 5. Holding period
    hold_col = (
        "holding_period"
        if "holding_period" in df.columns
        else ("holding_bars" if "holding_bars" in df.columns else None)
    )
    if hold_col:
        h_s = sub[hold_col].dropna()
        stats["avg_holding_period"] = float(h_s.mean()) if not h_s.empty else np.nan
    else:
        stats["avg_holding_period"] = np.nan

    # 6. Good & Bad Execution %
    if "good_execution" in df.columns:
        ge_s = sub["good_execution"].dropna()
        stats["good_execution_pct"] = float(ge_s.mean() * 100) if not ge_s.empty else np.nan
    else:
        stats["good_execution_pct"] = np.nan

    if "bad_execution" in df.columns:
        be_s = sub["bad_execution"].dropna()
        stats["bad_execution_pct"] = float(be_s.mean() * 100) if not be_s.empty else np.nan
    elif "good_execution" in df.columns:
        ge_s = sub["good_execution"].dropna()
        stats["bad_execution_pct"] = float((1 - ge_s).mean() * 100) if not ge_s.empty else np.nan
    else:
        stats["bad_execution_pct"] = np.nan

    # 7. Future direction balance
    if "future_direction" in df.columns:
        fd_s = sub["future_direction"].dropna()
        stats["future_direction_balance"] = float(fd_s.mean()) if not fd_s.empty else np.nan
    else:
        stats["future_direction_balance"] = np.nan

    return stats


def _build_regimes_dict(df: pd.DataFrame) -> Dict[str, pd.Series]:
    """
    Dynamically define regime masks based on present columns.

    Returns
    -------
    Dict[str, pd.Series]
        Mapping of regime name to boolean Series.
    """
    regimes: Dict[str, pd.Series] = {}
    cols = set(df.columns)

    # 0. Baseline (All Data)
    regimes["All Data"] = pd.Series(True, index=df.index)

    # 1. Trend vs Range
    if "trend_strength" in cols:
        median_ts = df["trend_strength"].median()
        regimes["Trend (High Trend Strength)"] = df["trend_strength"] > median_ts
        regimes["Range (Low Trend Strength)"] = df["trend_strength"] <= median_ts

    if "market_structure" in cols:
        # Check if numeric
        if pd.api.types.is_numeric_dtype(df["market_structure"]):
            regimes["Bullish Structure"] = df["market_structure"] > 0
            regimes["Bearish Structure"] = df["market_structure"] < 0
            regimes["Ranging Structure"] = df["market_structure"] == 0
        else:
            for val in df["market_structure"].dropna().unique():
                regimes[f"Structure: {val}"] = df["market_structure"] == val

    # 2. Bull vs Bear
    if "ema_stack_bull" in cols:
        regimes["EMA Bull Stack"] = df["ema_stack_bull"] == 1
    if "ema_stack_bear" in cols:
        regimes["EMA Bear Stack"] = df["ema_stack_bear"] == 1

    # 3. High Volatility vs Low Volatility
    if "volatility_expanding" in cols:
        regimes["High Volatility (Expanding)"] = df["volatility_expanding"] == 1
        regimes["Low Volatility (Contracting)"] = df["volatility_expanding"] == 0
    elif "high_volatility" in cols:
        regimes["High Volatility"] = df["high_volatility"] == 1
        regimes["Low Volatility"] = df["high_volatility"] == 0

    # 4. Session Regimes
    if "session" in cols:
        for sess_val in df["session"].dropna().unique():
            regimes[f"Session: {sess_val}"] = df["session"] == sess_val

    if "asian" in cols:
        regimes["Asian Session"] = df["asian"] == 1
    if "london" in cols:
        regimes["London Session"] = df["london"] == 1
    if "newyork" in cols:
        regimes["New York Session"] = df["newyork"] == 1
    if "overlap" in cols:
        regimes["Session Overlap"] = df["overlap"] == 1
        regimes["Non-Overlap"] = df["overlap"] == 0

    # 5. Execution Quality Regimes
    if "good_execution" in cols:
        regimes["Good Execution"] = df["good_execution"] == 1
    if "bad_execution" in cols:
        regimes["Bad Execution"] = df["bad_execution"] == 1
    elif "good_execution" in cols:
        regimes["Bad Execution"] = df["good_execution"] == 0

    # 6. Body Regimes (Candle dynamics)
    if "body_pct" in cols:
        med_bp = df["body_pct"].abs().median()
        regimes["Large Candle Body"] = df["body_pct"].abs() >= med_bp
        regimes["Small Candle Body"] = df["body_pct"].abs() < med_bp

    return regimes


def _build_conditional_tables(
    summary_df: pd.DataFrame, cols_present: set
) -> List[Tuple[str, pd.DataFrame]]:
    """
    Build comparative conditional analysis tables for regime pairs.

    Returns
    -------
    List[Tuple[str, pd.DataFrame]]
        List of (analysis_title, comparative_df) tuples.
    """
    tables: List[Tuple[str, pd.DataFrame]] = []
    if summary_df.empty:
        return tables

    summary_indexed = summary_df.set_index("regime")

    def get_sub_table(regime_names: List[str]) -> Optional[pd.DataFrame]:
        valid = [r for r in regime_names if r in summary_indexed.index]
        if valid:
            return summary_indexed.loc[valid].reset_index()
        return None

    # 1. Trend vs Range
    trend_range_names = [
        "Trend (High Trend Strength)",
        "Range (Low Trend Strength)",
        "Bullish Structure",
        "Bearish Structure",
        "Ranging Structure",
    ]
    tbl = get_sub_table(trend_range_names)
    if tbl is not None and not tbl.empty:
        tables.append(("Trend vs Range Analysis", tbl))

    # 2. Bull vs Bear
    bull_bear_names = ["EMA Bull Stack", "EMA Bear Stack"]
    tbl = get_sub_table(bull_bear_names)
    if tbl is not None and not tbl.empty:
        tables.append(("Bull vs Bear Analysis", tbl))

    # 3. High Volatility vs Low Volatility
    vol_names = [
        "High Volatility (Expanding)",
        "Low Volatility (Contracting)",
        "High Volatility",
        "Low Volatility",
    ]
    tbl = get_sub_table(vol_names)
    if tbl is not None and not tbl.empty:
        tables.append(("High Volatility vs Low Volatility Analysis", tbl))

    # 4. London vs Asia
    session_la = ["London Session", "Asian Session"]
    tbl = get_sub_table(session_la)
    if tbl is not None and not tbl.empty:
        tables.append(("London vs Asia Analysis", tbl))

    # 5. London vs NY
    session_lny = ["London Session", "New York Session"]
    tbl = get_sub_table(session_lny)
    if tbl is not None and not tbl.empty:
        tables.append(("London vs NY Analysis", tbl))

    # 6. Session Overlap
    session_ov = ["Session Overlap", "Non-Overlap"]
    tbl = get_sub_table(session_ov)
    if tbl is not None and not tbl.empty:
        tables.append(("Session Overlap Analysis", tbl))

    # 7. Execution Quality
    exec_names = ["Good Execution", "Bad Execution"]
    tbl = get_sub_table(exec_names)
    if tbl is not None and not tbl.empty:
        tables.append(("Execution Quality Analysis", tbl))

    return tables


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Perform market regime analysis on master dataset.

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
    out_path = Path(output_dir) / "regimes"
    ensure_dir(out_path)

    if df.empty:
        return AnalyticsResult(
            module="regime_analysis",
            success=False,
            rows=0,
            columns=0,
            files=0,
            metrics={
                "number_of_regimes": 0,
                "best_regime": "N/A",
                "worst_regime": "N/A",
                "largest_regime": "N/A",
                "smallest_regime": "N/A",
            },
            elapsed_seconds=time.time() - start_time,
            message="Input DataFrame is empty.",
        )

    n_rows, n_cols = df.shape
    cols_set = set(df.columns)

    # 1. Discover columns & missing columns
    detected_cols = [c for c in EXPECTED_REGIME_COLS if c in cols_set]
    missing_cols = [c for c in EXPECTED_REGIME_COLS if c not in cols_set]

    # 2. Build regime masks
    regimes_dict = _build_regimes_dict(df)

    # 3. Compute stats for each regime
    stats_list = []
    for r_name, mask in regimes_dict.items():
        stats = _compute_regime_stats(df, mask, r_name)
        stats_list.append(stats)

    summary_df = pd.DataFrame(stats_list)

    # 4. Save regime_summary.csv
    file_regime_summary = write_csv(summary_df, out_path / "regime_summary.csv")

    # 5. Build comparative / conditional tables & save regime_metrics.csv
    conditional_tables = _build_conditional_tables(summary_df, cols_set)

    # Create metrics DataFrame with focus on non-baseline regimes
    non_baseline_df = summary_df[summary_df["regime"] != "All Data"].copy()

    # Save metrics csv
    file_regime_metrics = write_csv(non_baseline_df, out_path / "regime_metrics.csv")

    # 6. Determine metrics (best, worst, largest, smallest)
    number_of_regimes = len(non_baseline_df)

    best_regime = "N/A"
    worst_regime = "N/A"
    largest_regime = "N/A"
    smallest_regime = "N/A"

    if not non_baseline_df.empty:
        # Determine primary ranking metric (mean_future_return if available else mean_return)
        rank_col = (
            "mean_future_return"
            if "mean_future_return" in non_baseline_df.columns
            and non_baseline_df["mean_future_return"].notna().any()
            else ("mean_return" if "mean_return" in non_baseline_df.columns else None)
        )

        if rank_col and non_baseline_df[rank_col].notna().any():
            clean_rank_df = non_baseline_df.dropna(subset=[rank_col])
            if not clean_rank_df.empty:
                best_row = clean_rank_df.loc[clean_rank_df[rank_col].idxmax()]
                worst_row = clean_rank_df.loc[clean_rank_df[rank_col].idxmin()]
                best_regime = f"{best_row['regime']} ({rank_col}: {best_row[rank_col]:.4f})"
                worst_regime = f"{worst_row['regime']} ({rank_col}: {worst_row[rank_col]:.4f})"

        # Largest and smallest by rows
        if "rows" in non_baseline_df.columns and (non_baseline_df["rows"] > 0).any():
            valid_rows_df = non_baseline_df[non_baseline_df["rows"] > 0]
            largest_row = valid_rows_df.loc[valid_rows_df["rows"].idxmax()]
            smallest_row = valid_rows_df.loc[valid_rows_df["rows"].idxmin()]
            largest_regime = f"{largest_row['regime']} ({largest_row['rows']:,} rows, {largest_row['pct_dataset']}%)"
            smallest_regime = f"{smallest_row['regime']} ({smallest_row['rows']:,} rows, {smallest_row['pct_dataset']}%)"

    detected_cols_str = ", ".join(detected_cols) if detected_cols else "None"
    missing_cols_str = ", ".join(missing_cols) if missing_cols else "None"

    # 7. Generate regime_report.md
    report_md = f"""# APEX Quant Research Framework - Regime Analysis Report

**Generated:** {get_timestamp()}  
**Dataset Shape:** {n_rows:,} rows x {n_cols:,} columns  
**Detected Regimes Analyzed:** {number_of_regimes}  

---

## 1. Executive Summary

This module evaluates how labels, returns, and execution outcomes behave across different market regimes (Trend vs Range, Bull vs Bear, Volatility States, Trading Sessions, and Execution Quality).

- **Total Regimes Evaluated:** {number_of_regimes}
- **Best Performing Regime:** {best_regime}
- **Worst Performing Regime:** {worst_regime}
- **Largest Market Regime:** {largest_regime}
- **Smallest Market Regime:** {smallest_regime}

---

## 2. Detected Regimes & Column Coverage

The following key regime columns were automatically detected in the master dataset:
- **Detected Columns ({len(detected_cols)}):** `{detected_cols_str}`

"""

    if missing_cols:
        report_md += f"⚠️ **Missing Optional Columns ({len(missing_cols)}):** `{missing_cols_str}`  \n*Analysis for missing columns degraded gracefully without failure.*\n\n"

    report_md += "---\n\n## 3. Performance by Regime (Full Summary)\n\n"
    report_md += df_to_markdown(summary_df, max_rows=50) + "\n\n---\n\n"

    # Add Conditional Analysis Sections
    report_md += "## 4. Conditional Pairwise Analyses\n\n"
    if conditional_tables:
        for title, c_df in conditional_tables:
            report_md += f"### {title}\n\n"
            report_md += df_to_markdown(c_df, max_rows=20) + "\n\n"
    else:
        report_md += "_No pairwise conditional analyses available for current dataset columns._\n\n"

    report_md += "---\n\n## 5. Interesting Findings\n\n"
    findings = []

    if not non_baseline_df.empty:
        # Check sessions comparison
        session_rows = non_baseline_df[non_baseline_df["regime"].str.contains("Session", na=False)]
        if len(session_rows) > 1 and "mean_return" in session_rows.columns:
            session_clean = session_rows.dropna(subset=["mean_return"])
            if not session_clean.empty:
                max_s = session_clean.loc[session_clean["mean_return"].idxmax()]
                min_s = session_clean.loc[session_clean["mean_return"].idxmin()]
                findings.append(
                    f"Session disparity detected: Highest return session is `{max_s['regime']}` (mean: {max_s['mean_return']:.6f}), lowest is `{min_s['regime']}` (mean: {min_s['mean_return']:.6f})."
                )

        # Check volatility comparison
        vol_rows = non_baseline_df[non_baseline_df["regime"].str.contains("Volatility", na=False)]
        if len(vol_rows) >= 2 and "std_return" in vol_rows.columns:
            vol_clean = vol_rows.dropna(subset=["std_return"])
            if not vol_clean.empty:
                findings.append(
                    f"Volatility impact evaluated: `{vol_clean.iloc[0]['regime']}` shows return std of {vol_clean.iloc[0]['std_return']:.6f} vs `{vol_clean.iloc[-1]['regime']}` std of {vol_clean.iloc[-1]['std_return']:.6f}."
                )

        # Check execution quality
        exec_rows = non_baseline_df[non_baseline_df["regime"].str.contains("Execution", na=False)]
        if len(exec_rows) >= 1 and "mean_future_return" in exec_rows.columns:
            exec_clean = exec_rows.dropna(subset=["mean_future_return"])
            if not exec_clean.empty:
                findings.append(
                    f"Execution quality impact: `{exec_clean.iloc[0]['regime']}` yields mean future return of {exec_clean.iloc[0]['mean_future_return']:.6f}."
                )

    if not findings:
        findings.append("No anomalous performance skew detected across evaluated market regimes.")

    for f in findings:
        report_md += f"- {f}\n"

    report_md += "\n---\n\n## 6. Warnings & Missing Columns\n\n"
    if missing_cols:
        report_md += f"- **Missing Columns Warning:** The dataset lacks `{missing_cols_str}`. Ensure feature and label pipelines populate these for deeper regime attribution.\n"
    else:
        report_md += "- **Column Coverage Complete:** All expected regime columns were present in the master dataset.\n"

    file_regime_report = write_markdown(report_md, out_path / "regime_report.md")

    # 8. Generate summary.json
    elapsed = time.time() - start_time
    metrics_dict = {
        "number_of_regimes": number_of_regimes,
        "best_regime": best_regime,
        "worst_regime": worst_regime,
        "largest_regime": largest_regime,
        "smallest_regime": smallest_regime,
        "detected_columns": detected_cols,
        "missing_columns": missing_cols,
    }

    summary_data = {
        "framework": "APEX Quant Research Framework",
        "module": "regime_analysis",
        "timestamp": get_timestamp(),
        "dataset_rows": n_rows,
        "dataset_columns": n_cols,
        "files_generated": [
            "regime_summary.csv",
            "regime_metrics.csv",
            "regime_report.md",
            "summary.json",
        ],
        "metrics": metrics_dict,
        "elapsed_seconds": round(elapsed, 4),
        "message": f"Regime analysis completed successfully for {number_of_regimes} market regimes.",
    }

    file_summary_json = write_json(summary_data, out_path / "summary.json")

    if verbose:
        print(f"[analytics.regime_analysis] Analyzed {number_of_regimes} regimes in {elapsed:.2f}s.")

    return AnalyticsResult(
        module="regime_analysis",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=4,
        metrics=metrics_dict,
        elapsed_seconds=elapsed,
        message=f"Regime analysis completed successfully for {number_of_regimes} market regimes.",
    )
