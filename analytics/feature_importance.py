"""
=========================================================
APEX Quant Research Framework
Module      : analytics/feature_importance.py
Description : Stage-1 statistical feature ranking and informativeness analysis.
=========================================================
"""

from pathlib import Path
import time
from typing import List, Optional, Tuple, Union

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

# Optional scikit-learn import for Mutual Information
try:
    from sklearn.feature_selection import mutual_info_regression

    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


def _find_label_columns(df: pd.DataFrame) -> List[str]:
    """Find target or label columns in DataFrame."""
    candidates = []
    for col in df.columns:
        low = col.lower()
        if any(kw in low for kw in ["label", "target", "ret", "return", "pnl", "y_", "fwd_"]):
            if pd.api.types.is_numeric_dtype(df[col]):
                candidates.append(col)
    return candidates


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Perform Stage-1 statistical feature importance and relevance analysis.

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
    out_path = Path(output_dir) / "importance"
    ensure_dir(out_path)

    if df.empty:
        return AnalyticsResult(
            module="feature_importance",
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
    label_cols = _find_label_columns(df)

    # Features are numeric columns that are not labels themselves
    feature_cols = [c for c in numeric_cols if c not in label_cols]

    if not feature_cols:
        feature_cols = numeric_cols

    rows_data = []

    has_labels = len(label_cols) > 0

    # Sample data if dataset is extremely large for MI speed
    df_clean = df.replace([np.inf, -np.inf], np.nan).dropna(subset=feature_cols)
    if len(df_clean) > 10_000:
        sample_df = df_clean.sample(n=10_000, random_state=42)
    else:
        sample_df = df_clean

    for col in feature_cols:
        s = sample_df[col]
        var_val = float(s.var()) if len(s) > 1 else 0.0
        std_val = float(s.std()) if len(s) > 1 else 0.0
        snr_val = float(abs(s.mean()) / std_val) if std_val > 0 else 0.0

        max_pearson = 0.0
        max_spearman = 0.0
        top_target = None
        mi_score = 0.0

        if has_labels:
            for lbl in label_cols:
                lbl_series = sample_df[lbl]
                if lbl_series.std() > 0 and std_val > 0:
                    p_corr = float(s.corr(lbl_series, method="pearson"))
                    # Spearman rank correlation without scipy dependency
                    sp_corr = float(s.rank().corr(lbl_series.rank(), method="pearson"))

                    if abs(p_corr) >= abs(max_pearson):
                        max_pearson = p_corr
                        max_spearman = sp_corr
                        top_target = lbl

            # Mutual Information with top target if sklearn available
            if HAS_SKLEARN and top_target and len(sample_df) > 10:
                try:
                    X_vec = s.values.reshape(-1, 1)
                    y_vec = sample_df[top_target].values
                    mi_res = mutual_info_regression(X_vec, y_vec, random_state=42)
                    mi_score = float(mi_res[0])
                except Exception:
                    mi_score = 0.0

        # Composite score
        if has_labels:
            comp_score = 0.4 * abs(max_pearson) + 0.4 * abs(max_spearman) + 0.2 * mi_score
        else:
            comp_score = snr_val

        rows_data.append(
            {
                "feature": col,
                "variance": round(var_val, 6),
                "std": round(std_val, 6),
                "snr": round(snr_val, 4),
                "top_target": top_target if top_target else "N/A",
                "max_pearson_corr": round(max_pearson, 4),
                "max_spearman_corr": round(max_spearman, 4),
                "mutual_info": round(mi_score, 4),
                "composite_score": round(comp_score, 4),
            }
        )

    importance_df = pd.DataFrame(rows_data)

    if not importance_df.empty:
        importance_df = importance_df.sort_values(
            by="composite_score", ascending=False
        ).reset_index(drop=True)
        importance_df["rank"] = importance_df.index + 1
    else:
        importance_df["rank"] = []

    # 1. Write feature_importance.csv
    file_feat_imp = write_csv(importance_df, out_path / "feature_importance.csv")

    # 2. Write importance_rank.csv
    rank_cols = [
        "rank",
        "feature",
        "composite_score",
        "top_target",
        "max_pearson_corr",
        "max_spearman_corr",
        "variance",
    ]
    file_rank_csv = write_csv(
        importance_df[rank_cols], out_path / "importance_rank.csv"
    )

    # 3. Write importance_summary.md
    md_content = f"""# Feature Importance & Informativeness Report

**Generated:** {get_timestamp()}  
**Target:** `feature_importance`

---

## 1. Executive Summary

- **Total Features Analyzed:** {len(importance_df):,}
- **Target / Label Columns Found:** {len(label_cols)} ({", ".join(label_cols) if label_cols else "None"})
- **Mutual Information Method:** {"scikit-learn (active)" if HAS_SKLEARN else "fallback (variance/SNR)"}

---

## 2. Top Ranked Features

"""
    if not importance_df.empty:
        top_20 = importance_df[rank_cols].head(20)
        md_content += df_to_markdown(top_20) + "\n\n"
    else:
        md_content += "_No features were available for importance ranking._\n\n"

    file_summary_md = write_markdown(md_content, out_path / "importance_summary.md")

    # Metrics
    metrics_summary = {
        "features_analyzed": len(importance_df),
        "target_columns_detected": len(label_cols),
        "has_labels": has_labels,
        "top_feature": importance_df.iloc[0]["feature"]
        if not importance_df.empty
        else None,
        "top_composite_score": float(importance_df.iloc[0]["composite_score"])
        if not importance_df.empty
        else 0.0,
    }

    # 4. Write summary.json
    summary_data = {
        "module": "feature_importance",
        "timestamp": get_timestamp(),
        "metrics": metrics_summary,
        "files_generated": [
            file_feat_imp.name,
            file_rank_csv.name,
            file_summary_md.name,
            "summary.json",
        ],
    }
    file_summary_json = write_json(summary_data, out_path / "summary.json")

    elapsed = time.time() - start_time
    msg = (
        f"Feature importance ranking completed successfully for {len(importance_df)} features."
        if has_labels
        else f"Feature variance/SNR analysis completed ({len(importance_df)} features, no label columns detected)."
    )

    if verbose:
        print(f"[analytics.feature_importance] {msg} in {elapsed:.2f}s.")

    return AnalyticsResult(
        module="feature_importance",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=4,
        metrics=metrics_summary,
        elapsed_seconds=elapsed,
        message=msg,
    )
