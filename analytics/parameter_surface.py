"""
=========================================================
APEX Quant Research Framework
Module      : analytics/parameter_surface.py
Description : Parameter surface robustness and sensitivity analytics module.
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


def _find_parameter_columns(df: pd.DataFrame) -> List[str]:
    """Find parameter candidate columns in DataFrame."""
    params = []
    for col in df.columns:
        low = col.lower()
        if any(
            kw in low
            for kw in [
                "param_",
                "parameter",
                "grid_",
                "window",
                "step",
                "threshold",
                "spacing",
            ]
        ):
            params.append(col)
    return params


def _find_metric_columns(df: pd.DataFrame) -> List[str]:
    """Find metric candidate columns in DataFrame."""
    metrics = []
    for col in df.columns:
        low = col.lower()
        if any(
            kw in low
            for kw in [
                "metric",
                "sharpe",
                "pnl",
                "return",
                "drawdown",
                "win_rate",
                "score",
                "profit_factor",
            ]
        ):
            metrics.append(col)
    return metrics


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Measure parameter robustness, sensitivity, and surface topology.

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
    out_path = Path(output_dir) / "surfaces"
    ensure_dir(out_path)

    n_rows, n_cols = df.shape
    param_cols = _find_parameter_columns(df)
    metric_cols = _find_metric_columns(df)

    has_param_inputs = len(param_cols) > 0 and len(metric_cols) > 0

    if has_param_inputs:
        primary_param = param_cols[0]
        primary_metric = metric_cols[0]

        grouped = df.groupby(primary_param)[primary_metric]

        surface_df = (
            grouped.agg(
                mean_performance="mean",
                std_stability="std",
                best_performance="max",
                median_performance="median",
                worst_performance="min",
                count="count",
            )
            .reset_index()
            .rename(columns={primary_param: "parameter"})
        )

        metrics_summary_df = pd.DataFrame(
            [
                {"metric": "parameter_column", "value": primary_param},
                {"metric": "metric_column", "value": primary_metric},
                {"metric": "unique_parameter_values", "value": len(surface_df)},
                {
                    "metric": "best_overall_performance",
                    "value": float(surface_df["best_performance"].max()),
                },
                {
                    "metric": "worst_overall_performance",
                    "value": float(surface_df["worst_performance"].min()),
                },
                {
                    "metric": "avg_parameter_stability_std",
                    "value": float(surface_df["std_stability"].mean())
                    if not surface_df["std_stability"].isna().all()
                    else 0.0,
                },
            ]
        )

        status_msg = f"Analyzed parameter surface for '{primary_param}' against '{primary_metric}'."
    else:
        # Placeholder surface structure for dataset without explicit parameter sweep columns
        surface_df = pd.DataFrame(
            columns=[
                "parameter",
                "mean_performance",
                "std_stability",
                "best_performance",
                "median_performance",
                "worst_performance",
                "count",
            ]
        )
        metrics_summary_df = pd.DataFrame(
            [
                {"metric": "status", "value": "missing_parameter_inputs"},
                {
                    "metric": "note",
                    "value": "Dataset does not contain parameterized experiment grid inputs (param_* / metric columns).",
                },
            ]
        )
        status_msg = "No parameter or experiment metric columns detected in current dataset. Generating safe placeholder surface artifact."

    # 1. Write surface.csv
    file_surface = write_csv(surface_df, out_path / "surface.csv")

    # 2. Write surface_metrics.csv
    file_surface_metrics = write_csv(
        metrics_summary_df, out_path / "surface_metrics.csv"
    )

    # 3. Write surface_summary.md
    md_content = f"""# Parameter Surface & Stability Analysis

**Generated:** {get_timestamp()}  
**Target:** `parameter_surface`

---

## 1. Status

- **Parameter Inputs Available:** {"Yes" if has_param_inputs else "No"}
- **Message:** {status_msg}

---

## 2. Parameter Surface Summary

"""
    if has_param_inputs and not surface_df.empty:
        md_content += df_to_markdown(surface_df) + "\n\n"
    else:
        md_content += (
            "_No explicit parameter sweep data was present in the dataset. "
            "When parameter grid optimization runs are ingested into the dataset, "
            "this section will visualize parameter robustness and degradation surfaces._\n\n"
        )

    file_summary_md = write_markdown(md_content, out_path / "surface_summary.md")

    # Metrics
    metrics_data = {
        "has_parameter_inputs": has_param_inputs,
        "parameter_columns": param_cols,
        "metric_columns": metric_cols,
        "surface_rows": len(surface_df),
    }

    # 4. Write summary.json
    summary_json_data = {
        "module": "parameter_surface",
        "timestamp": get_timestamp(),
        "metrics": metrics_data,
        "files_generated": [
            file_surface.name,
            file_surface_metrics.name,
            file_summary_md.name,
            "summary.json",
        ],
    }
    file_summary_json = write_json(summary_json_data, out_path / "summary.json")

    elapsed = time.time() - start_time
    if verbose:
        print(f"[analytics.parameter_surface] {status_msg} ({elapsed:.2f}s).")

    return AnalyticsResult(
        module="parameter_surface",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=4,
        metrics=metrics_data,
        elapsed_seconds=elapsed,
        message=status_msg,
    )
