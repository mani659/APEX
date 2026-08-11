"""
=========================================================
APEX Quant Research Framework
Module      : analytics/tail_statistics.py
Description : Tail risk and extreme value analytics module.
=========================================================
"""

from pathlib import Path
import time
from typing import List, Union

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


def _is_label_column(col: str) -> bool:
    """Check if column name indicates a target, label, or return."""
    low = col.lower()
    return any(
        kw in low
        for kw in ["label", "target", "ret", "return", "pnl", "y_", "fwd_"]
    )


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Analyze tail risk, percentiles, and extreme behavior in numeric features and labels.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame (read-only).
    output_dir : Union[str, Path]
        Target base report directory (e.g. reports/analytics/latest).
    verbose : bool
        Whether to log progress.

    Returns
    -------
    AnalyticsResult
        Standardized analytics result object.
    """
    start_time = time.time()
    out_path = Path(output_dir) / "tails"
    ensure_dir(out_path)

    if df.empty:
        return AnalyticsResult(
            module="tail_statistics",
            success=False,
            rows=0,
            columns=0,
            files=0,
            metrics={},
            elapsed_seconds=time.time() - start_time,
            message="Input DataFrame is empty.",
        )

    n_rows, n_cols = df.shape
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        return AnalyticsResult(
            module="tail_statistics",
            success=True,
            rows=n_rows,
            columns=n_cols,
            files=0,
            metrics={"numeric_columns": 0},
            elapsed_seconds=time.time() - start_time,
            message="No numeric columns found for tail analysis.",
        )

    percentile_levels = [0.001, 0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999]
    percentile_names = [f"p{p*100:g}" for p in percentile_levels]

    tail_stats_rows = []
    percentile_rows = []

    label_columns_found = []

    for col in numeric_cols:
        s = df[col].replace([np.inf, -np.inf], np.nan).dropna()
        if s.empty:
            continue

        if _is_label_column(col):
            label_columns_found.append(col)

        cnt = len(s)
        mean_val = float(s.mean())
        std_val = float(s.std())
        min_val = float(s.min())
        max_val = float(s.max())

        # Quantiles
        q_vals = s.quantile(percentile_levels).values
        q_dict = {f"p{p*100:g}": float(v) for p, v in zip(percentile_levels, q_vals)}

        pct_row = {"column": col, "count": cnt}
        pct_row.update({k: round(v, 6) for k, v in q_dict.items()})
        percentile_rows.append(pct_row)

        p1_val = q_dict["p1"]
        p5_val = q_dict["p5"]
        p95_val = q_dict["p95"]
        p99_val = q_dict["p99"]

        # Expected Shortfall (CVaR style)
        left_es_1pct = float(s[s <= p1_val].mean()) if (s <= p1_val).any() else min_val
        left_es_5pct = float(s[s <= p5_val].mean()) if (s <= p5_val).any() else min_val
        right_es_95pct = float(s[s >= p95_val].mean()) if (s >= p95_val).any() else max_val
        right_es_99pct = float(s[s >= p99_val].mean()) if (s >= p99_val).any() else max_val

        # Extreme events (Z-score thresholds)
        if std_val > 0:
            z_scores = (s - mean_val) / std_val
            extreme_2std = int((z_scores.abs() > 2.0).sum())
            extreme_3std = int((z_scores.abs() > 3.0).sum())
            extreme_5std = int((z_scores.abs() > 5.0).sum())
        else:
            extreme_2std = 0
            extreme_3std = 0
            extreme_5std = 0

        # Downside vs Upside deviation
        downside_s = s[s < mean_val]
        upside_s = s[s > mean_val]
        downside_std = float(downside_s.std()) if len(downside_s) > 1 else 0.0
        upside_std = float(upside_s.std()) if len(upside_s) > 1 else 0.0
        asymmetry_ratio = (
            float(upside_std / downside_std)
            if downside_std > 0
            else (1.0 if upside_std == 0 else 999.0)
        )

        # Tail ratio (99th percentile vs abs(1st percentile))
        abs_p1 = abs(p1_val)
        tail_ratio = float(p99_val / abs_p1) if abs_p1 > 0 else np.nan

        tail_stats_rows.append(
            {
                "column": col,
                "is_label": _is_label_column(col),
                "count": cnt,
                "mean": round(mean_val, 6),
                "std": round(std_val, 6),
                "min": round(min_val, 6),
                "max": round(max_val, 6),
                "p1": round(p1_val, 6),
                "p5": round(p5_val, 6),
                "p50": round(q_dict["p50"], 6),
                "p95": round(p95_val, 6),
                "p99": round(p99_val, 6),
                "left_es_1pct": round(left_es_1pct, 6),
                "left_es_5pct": round(left_es_5pct, 6),
                "right_es_95pct": round(right_es_95pct, 6),
                "right_es_99pct": round(right_es_99pct, 6),
                "extreme_cnt_2std": extreme_2std,
                "extreme_cnt_3std": extreme_3std,
                "extreme_cnt_5std": extreme_5std,
                "downside_std": round(downside_std, 6),
                "upside_std": round(upside_std, 6),
                "asymmetry_ratio": round(asymmetry_ratio, 4)
                if not np.isnan(asymmetry_ratio)
                else None,
                "tail_ratio": round(tail_ratio, 4)
                if not np.isnan(tail_ratio)
                else None,
            }
        )

    tail_df = pd.DataFrame(tail_stats_rows)
    percentiles_df = pd.DataFrame(percentile_rows)

    # 1. Write tail_statistics.csv
    file_tail_stats = write_csv(tail_df, out_path / "tail_statistics.csv")

    # 2. Write tail_percentiles.csv
    file_percentiles = write_csv(percentiles_df, out_path / "tail_percentiles.csv")

    # 3. Write tail_summary.md
    md_content = f"""# Tail Statistics & Extreme Value Report

**Generated:** {get_timestamp()}  
**Target:** `tail_statistics`

---

## 1. Overview

- **Analyzed Numeric Columns:** {len(tail_df):,}
- **Label / Return Columns Detected:** {len(label_columns_found)} ({", ".join(label_columns_found) if label_columns_found else "None"})

---

## 2. Key Label / Return Tail Metrics

"""
    if label_columns_found:
        label_df = tail_df[tail_df["is_label"]][
            [
                "column",
                "min",
                "left_es_1pct",
                "p1",
                "p50",
                "p99",
                "right_es_99pct",
                "max",
                "extreme_cnt_3std",
                "asymmetry_ratio",
            ]
        ]
        md_content += df_to_markdown(label_df) + "\n\n"
    else:
        md_content += "_No explicit target or return label columns detected. Showing top numeric columns._\n\n"

    md_content += """## 3. Extreme Event Analysis (> 3 Std Devs)

Top columns with highest number of extreme outlier observations:

"""
    top_extremes = tail_df.sort_values(by="extreme_cnt_3std", ascending=False).head(15)[
        ["column", "count", "extreme_cnt_2std", "extreme_cnt_3std", "extreme_cnt_5std", "std", "min", "max"]
    ]
    md_content += df_to_markdown(top_extremes) + "\n\n"

    file_summary_md = write_markdown(md_content, out_path / "tail_summary.md")

    # Metrics
    metrics_summary = {
        "numeric_columns_analyzed": len(tail_df),
        "label_columns_detected": len(label_columns_found),
        "max_3std_extremes_single_col": int(tail_df["extreme_cnt_3std"].max())
        if not tail_df.empty
        else 0,
    }

    # 4. Write summary.json
    summary_data = {
        "module": "tail_statistics",
        "timestamp": get_timestamp(),
        "metrics": metrics_summary,
        "files_generated": [
            file_tail_stats.name,
            file_percentiles.name,
            file_summary_md.name,
            "summary.json",
        ],
    }
    file_summary_json = write_json(summary_data, out_path / "summary.json")

    elapsed = time.time() - start_time
    if verbose:
        print(
            f"[analytics.tail_statistics] Tail risk analysis completed on {len(tail_df)} numeric columns in {elapsed:.2f}s."
        )

    return AnalyticsResult(
        module="tail_statistics",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=4,
        metrics=metrics_summary,
        elapsed_seconds=elapsed,
        message=f"Tail statistics completed successfully. Wrote 4 artifacts to {out_path}.",
    )
