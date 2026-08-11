"""
=========================================================
APEX Quant Research Framework
Module      : analytics/statistics.py
Description : Master dataset descriptive analytics module.
=========================================================
"""

from pathlib import Path
import time
from typing import Union

import numpy as np
import pandas as pd

from analytics.utils import (
    AnalyticsResult,
    compute_mad,
    df_to_markdown,
    ensure_dir,
    format_bytes,
    get_timestamp,
    write_csv,
    write_json,
    write_markdown,
)


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Perform descriptive statistical analysis on the master dataset.

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
    out_path = Path(output_dir) / "statistics"
    ensure_dir(out_path)

    if df.empty:
        result = AnalyticsResult(
            module="statistics",
            success=False,
            rows=0,
            columns=0,
            files=0,
            metrics={},
            elapsed_seconds=time.time() - start_time,
            message="Input DataFrame is empty.",
        )
        return result

    n_rows, n_cols = df.shape
    mem_usage = int(df.memory_usage(deep=True).sum())
    dup_rows = int(df.duplicated().sum())

    # Dtype counts
    dtype_counts = df.dtypes.value_counts().to_dict()
    dtype_str_counts = {str(k): int(v) for k, v in dtype_counts.items()}

    # Columns analysis
    feature_stats_list = []

    constant_cols = []
    near_constant_cols = []
    zero_var_cols = []
    total_missing_cells = 0
    total_inf_cells = 0

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in df.columns:
        series = df[col]
        dtype_str = str(series.dtype)
        n_count = int(series.count())
        missing_cnt = int(series.isna().sum())
        missing_pct = float(missing_cnt / n_rows) if n_rows > 0 else 0.0
        total_missing_cells += missing_cnt

        # Check infinite values for numeric columns
        inf_cnt = 0
        if pd.api.types.is_numeric_dtype(series):
            inf_cnt = int(np.isinf(series.dropna()).sum())
            total_inf_cells += inf_cnt

        n_unique = int(series.nunique(dropna=True))

        # Check constant / near constant
        is_const = n_unique <= 1
        if is_const:
            constant_cols.append(col)

        # Near constant: top value occupies >= 99% of non-null observations
        is_near_const = False
        if not is_const and n_count > 0:
            top_freq = series.value_counts(normalize=True, dropna=True).iloc[0]
            if top_freq >= 0.99:
                is_near_const = True
                near_constant_cols.append(col)

        # Numeric stats
        mean_val = np.nan
        std_val = np.nan
        min_val = np.nan
        q1_val = np.nan
        med_val = np.nan
        q3_val = np.nan
        max_val = np.nan
        var_val = np.nan
        skew_val = np.nan
        kurt_val = np.nan
        iqr_val = np.nan
        mad_val = np.nan
        is_zero_var = False

        if pd.api.types.is_numeric_dtype(series) and n_count > 0:
            clean_s = series.replace([np.inf, -np.inf], np.nan).dropna()
            if not clean_s.empty:
                mean_val = float(clean_s.mean())
                std_val = float(clean_s.std())
                min_val = float(clean_s.min())
                q1_val = float(clean_s.quantile(0.25))
                med_val = float(clean_s.median())
                q3_val = float(clean_s.quantile(0.75))
                max_val = float(clean_s.max())
                var_val = float(clean_s.var())
                iqr_val = float(q3_val - q1_val)
                mad_val = float(compute_mad(clean_s))

                if len(clean_s) > 2:
                    skew_val = float(clean_s.skew())
                    kurt_val = float(clean_s.kurtosis())

                if var_val == 0.0 or (np.isnan(var_val) and is_const):
                    is_zero_var = True
                    zero_var_cols.append(col)

        feature_stats_list.append(
            {
                "column": col,
                "dtype": dtype_str,
                "count": n_count,
                "missing": missing_cnt,
                "missing_pct": round(missing_pct, 4),
                "inf_count": inf_cnt,
                "unique_values": n_unique,
                "mean": round(mean_val, 6) if not np.isnan(mean_val) else None,
                "std": round(std_val, 6) if not np.isnan(std_val) else None,
                "min": round(min_val, 6) if not np.isnan(min_val) else None,
                "q1": round(q1_val, 6) if not np.isnan(q1_val) else None,
                "median": round(med_val, 6) if not np.isnan(med_val) else None,
                "q3": round(q3_val, 6) if not np.isnan(q3_val) else None,
                "max": round(max_val, 6) if not np.isnan(max_val) else None,
                "variance": round(var_val, 6) if not np.isnan(var_val) else None,
                "skew": round(skew_val, 6) if not np.isnan(skew_val) else None,
                "kurtosis": round(kurt_val, 6) if not np.isnan(kurt_val) else None,
                "iqr": round(iqr_val, 6) if not np.isnan(iqr_val) else None,
                "mad": round(mad_val, 6) if not np.isnan(mad_val) else None,
                "is_constant": is_const,
                "is_near_constant": is_near_const,
                "is_zero_variance": is_zero_var,
            }
        )

    feature_stats_df = pd.DataFrame(feature_stats_list)

    # Global summary df
    global_stats = [
        {"metric": "row_count", "value": n_rows},
        {"metric": "column_count", "value": n_cols},
        {"metric": "numeric_column_count", "value": len(numeric_cols)},
        {"metric": "memory_usage_bytes", "value": mem_usage},
        {"metric": "memory_usage_formatted", "value": format_bytes(mem_usage)},
        {"metric": "duplicate_rows", "value": dup_rows},
        {"metric": "total_missing_cells", "value": total_missing_cells},
        {"metric": "total_inf_cells", "value": total_inf_cells},
        {"metric": "constant_column_count", "value": len(constant_cols)},
        {"metric": "near_constant_column_count", "value": len(near_constant_cols)},
        {"metric": "zero_variance_column_count", "value": len(zero_var_cols)},
    ]
    global_stats_df = pd.DataFrame(global_stats)

    # 1. Write dataset_statistics.csv
    file_ds_stats = write_csv(global_stats_df, out_path / "dataset_statistics.csv")

    # 2. Write feature_statistics.csv
    file_feat_stats = write_csv(
        feature_stats_df, out_path / "feature_statistics.csv"
    )

    # 3. Write dataset_summary.md
    md_content = f"""# Dataset Statistical Overview

**Generated:** {get_timestamp()}  
**Target:** `statistics`

---

## 1. Executive Summary

- **Total Rows:** {n_rows:,}
- **Total Columns:** {n_cols:,} ({len(numeric_cols)} numeric)
- **Memory Footprint:** {format_bytes(mem_usage)}
- **Duplicate Rows:** {dup_rows:,}
- **Total Missing Cells:** {total_missing_cells:,}
- **Total Infinite Cells:** {total_inf_cells:,}

---

## 2. Column Diagnostics

- **Constant Columns ({len(constant_cols)}):** {", ".join(constant_cols) if constant_cols else "None"}
- **Near-Constant Columns ({len(near_constant_cols)}):** {", ".join(near_constant_cols) if near_constant_cols else "None"}
- **Zero-Variance Columns ({len(zero_var_cols)}):** {", ".join(zero_var_cols) if zero_var_cols else "None"}

---

## 3. Data Types Breakdown

| Data Type | Count |
| :--- | :--- |
"""
    for dt_name, dt_count in dtype_str_counts.items():
        md_content += f"| `{dt_name}` | {dt_count} |\n"

    md_content += """
---

## 4. Top Feature Summary Preview

"""
    preview_cols = [
        "column",
        "dtype",
        "missing",
        "mean",
        "std",
        "median",
        "iqr",
        "is_constant",
    ]
    preview_df = feature_stats_df[preview_cols].head(25)
    md_content += df_to_markdown(preview_df) + "\n"

    file_summary_md = write_markdown(md_content, out_path / "dataset_summary.md")

    # Metrics dict for output result
    metrics_summary = {
        "rows": n_rows,
        "columns": n_cols,
        "numeric_columns": len(numeric_cols),
        "memory_bytes": mem_usage,
        "duplicate_rows": dup_rows,
        "constant_columns": len(constant_cols),
        "near_constant_columns": len(near_constant_cols),
        "zero_variance_columns": len(zero_var_cols),
        "missing_cells": total_missing_cells,
        "inf_cells": total_inf_cells,
    }

    # 4. Write summary.json
    summary_data = {
        "module": "statistics",
        "timestamp": get_timestamp(),
        "metrics": metrics_summary,
        "files_generated": [
            file_ds_stats.name,
            file_feat_stats.name,
            file_summary_md.name,
            "summary.json",
        ],
    }
    file_summary_json = write_json(summary_data, out_path / "summary.json")

    elapsed = time.time() - start_time
    if verbose:
        print(
            f"[analytics.statistics] Completed analysis on {n_rows:,} rows x {n_cols} cols in {elapsed:.2f}s."
        )

    return AnalyticsResult(
        module="statistics",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=4,
        metrics=metrics_summary,
        elapsed_seconds=elapsed,
        message=f"Statistics completed successfully. Wrote 4 artifacts to {out_path}.",
    )
