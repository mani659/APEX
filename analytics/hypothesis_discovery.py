"""
=========================================================
APEX Quant Research Framework

Module      : analytics/hypothesis_discovery.py
Version     : 2.0

Description : Hypothesis Discovery module (Analytics V2).
              Exploratory statistical analysis automatically generating research
              hypotheses for numeric features, boolean indicators, regimes,
              and sessions against label outcomes.
              Computes Pearson & Spearman correlations, top vs bottom quartile
              differences, True vs False mean/median percentage improvements,
              effect sizes, and transparent confidence scores.
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

# Known label outcome columns to evaluate
LABEL_COLS = [
    "future_return",
    "future_direction",
    "mfe",
    "mae",
    "pnl",
    "good_execution",
    "bad_execution",
    "return",
]

EXCLUDE_KEYWORDS = ["datetime", "date", "time", "row_id", "timestamp"]


def _discover_numeric_feature_hypotheses(
    df: pd.DataFrame, feature_cols: List[str], label_cols: List[str]
) -> List[Dict[str, Any]]:
    """
    Evaluate Numeric Feature -> Label hypotheses using Pearson, Spearman, and Q4 vs Q1 quartile differences.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.
    feature_cols : List[str]
        Numeric feature column names.
    label_cols : List[str]
        Label outcome column names.

    Returns
    -------
    List[Dict[str, Any]]
        List of hypothesis record dictionaries.
    """
    records = []

    for f in feature_cols:
        series_f = df[f].dropna()
        if series_f.empty or series_f.nunique() <= 1:
            continue

        q25 = float(series_f.quantile(0.25))
        q75 = float(series_f.quantile(0.75))

        top_mask = df[f] >= q75
        bot_mask = df[f] <= q25

        for y in label_cols:
            series_y = df[y].dropna()
            if series_y.empty:
                continue

            # Vectorized correlations
            valid_sub = df[[f, y]].dropna()
            if len(valid_sub) < 3 or valid_sub[f].std() == 0 or valid_sub[y].std() == 0:
                continue

            r_pearson = float(valid_sub[f].corr(valid_sub[y], method="pearson"))
            # Spearman correlation computed via rank correlation (avoids scipy dependency)
            r_spearman = float(valid_sub[f].rank().corr(valid_sub[y].rank()))

            top_y = df.loc[top_mask, y].dropna()
            bot_y = df.loc[bot_mask, y].dropna()

            if top_y.empty or bot_y.empty:
                continue

            mean_top = float(top_y.mean())
            mean_bot = float(bot_y.mean())
            diff_q4_q1 = mean_top - mean_bot

            std_top = float(top_y.std()) if len(top_y) > 1 else 0.0
            std_bot = float(bot_y.std()) if len(bot_y) > 1 else 0.0
            sample_size = len(top_y) + len(bot_y)

            # Cohen's d effect size
            pooled_std = np.sqrt((std_top**2 + std_bot**2) / 2.0)
            cohen_d = diff_q4_q1 / (pooled_std + 1e-8)

            # Welch's t-statistic
            se_diff = np.sqrt((std_top**2 / max(1, len(top_y))) + (std_bot**2 / max(1, len(bot_y))))
            t_stat = abs(diff_q4_q1) / (se_diff + 1e-8)

            # Transparent Confidence Score (0-100 scale)
            max_corr = max(abs(r_pearson), abs(r_spearman))
            confidence_score = max(
                0.0,
                min(
                    100.0,
                    0.40 * (max_corr * 100.0)
                    + 0.30 * min(100.0, abs(cohen_d) * 100.0)
                    + 0.30 * min(100.0, t_stat * 20.0),
                ),
            )

            records.append(
                {
                    "hypothesis": f"High vs Low {f} -> {y}",
                    "category": "Numeric Feature -> Label",
                    "predictor": f,
                    "target": y,
                    "pearson_corr": round(r_pearson, 4),
                    "spearman_corr": round(r_spearman, 4),
                    "mean_q4": round(mean_top, 6),
                    "mean_q1": round(mean_bot, 6),
                    "diff_q4_q1": round(diff_q4_q1, 6),
                    "pct_improvement": np.nan,
                    "cohen_d": round(cohen_d, 4),
                    "sample_size": sample_size,
                    "confidence_score": round(confidence_score, 2),
                }
            )

    return records


def _discover_boolean_feature_hypotheses(
    df: pd.DataFrame, bool_cols: List[str], label_cols: List[str]
) -> List[Dict[str, Any]]:
    """
    Evaluate Boolean Feature -> Label hypotheses comparing True vs False means/medians.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame.
    bool_cols : List[str]
        Boolean/binary column names.
    label_cols : List[str]
        Label outcome column names.

    Returns
    -------
    List[Dict[str, Any]]
        List of hypothesis record dictionaries.
    """
    records = []

    for b in bool_cols:
        mask_true = df[b] == 1
        mask_false = df[b] == 0

        for y in label_cols:
            true_y = df.loc[mask_true, y].dropna()
            false_y = df.loc[mask_false, y].dropna()

            if true_y.empty or false_y.empty:
                continue

            mean_true = float(true_y.mean())
            mean_false = float(false_y.mean())
            median_true = float(true_y.median())
            median_false = float(false_y.median())

            diff_mean = mean_true - mean_false
            pct_improvement = (diff_mean / (abs(mean_false) + 1e-8)) * 100.0

            std_true = float(true_y.std()) if len(true_y) > 1 else 0.0
            std_false = float(false_y.std()) if len(false_y) > 1 else 0.0
            sample_size = len(true_y) + len(false_y)

            pooled_std = np.sqrt((std_true**2 + std_false**2) / 2.0)
            cohen_d = diff_mean / (pooled_std + 1e-8)

            # Point-biserial correlation
            valid_sub = df[[b, y]].dropna()
            r_pearson = float(valid_sub[b].corr(valid_sub[y])) if len(valid_sub) > 2 else 0.0
            r_spearman = r_pearson

            se_diff = np.sqrt((std_true**2 / max(1, len(true_y))) + (std_false**2 / max(1, len(false_y))))
            t_stat = abs(diff_mean) / (se_diff + 1e-8)

            confidence_score = max(
                0.0,
                min(
                    100.0,
                    0.40 * (abs(r_pearson) * 100.0)
                    + 0.30 * min(100.0, abs(cohen_d) * 100.0)
                    + 0.30 * min(100.0, t_stat * 20.0),
                ),
            )

            records.append(
                {
                    "hypothesis": f"{b} (True vs False) -> {y}",
                    "category": "Boolean Feature -> Label",
                    "predictor": b,
                    "target": y,
                    "pearson_corr": round(r_pearson, 4),
                    "spearman_corr": round(r_spearman, 4),
                    "mean_true": round(mean_true, 6),
                    "mean_false": round(mean_false, 6),
                    "median_true": round(median_true, 6),
                    "median_false": round(median_false, 6),
                    "diff_mean": round(diff_mean, 6),
                    "pct_improvement": round(pct_improvement, 2),
                    "cohen_d": round(cohen_d, 4),
                    "sample_size": sample_size,
                    "confidence_score": round(confidence_score, 2),
                }
            )

    return records


def _discover_regime_session_hypotheses(
    df: pd.DataFrame, cat_cols: List[str], label_cols: List[str]
) -> List[Dict[str, Any]]:
    """
    Evaluate Regime / Session -> Label hypotheses comparing state outcomes.

    Returns
    -------
    List[Dict[str, Any]]
        List of hypothesis record dictionaries.
    """
    records = []

    for c in cat_cols:
        series_c = df[c].dropna()
        if series_c.empty or series_c.nunique() <= 1:
            continue

        category_type = "Session" if c in ["asian", "london", "newyork", "overlap"] else "Regime"

        for y in label_cols:
            groups = df.groupby(c)[y].mean()
            if len(groups) < 2:
                continue

            max_group = groups.idxmax()
            min_group = groups.idxmin()
            mean_max = float(groups[max_group])
            mean_min = float(groups[min_group])
            diff_mean = mean_max - mean_min
            pct_improvement = (diff_mean / (abs(mean_min) + 1e-8)) * 100.0

            sub_max = df.loc[df[c] == max_group, y].dropna()
            sub_min = df.loc[df[c] == min_group, y].dropna()
            std_max = float(sub_max.std()) if len(sub_max) > 1 else 0.0
            std_min = float(sub_min.std()) if len(sub_min) > 1 else 0.0
            sample_size = len(sub_max) + len(sub_min)

            pooled_std = np.sqrt((std_max**2 + std_min**2) / 2.0)
            cohen_d = diff_mean / (pooled_std + 1e-8)

            se_diff = np.sqrt((std_max**2 / max(1, len(sub_max))) + (std_min**2 / max(1, len(sub_min))))
            t_stat = abs(diff_mean) / (se_diff + 1e-8)

            confidence_score = max(
                0.0,
                min(
                    100.0,
                    0.50 * min(100.0, abs(cohen_d) * 100.0) + 0.50 * min(100.0, t_stat * 20.0),
                ),
            )

            records.append(
                {
                    "hypothesis": f"{category_type} {c} ({max_group} vs {min_group}) -> {y}",
                    "category": f"{category_type} -> Label",
                    "predictor": c,
                    "target": y,
                    "pearson_corr": np.nan,
                    "spearman_corr": np.nan,
                    "mean_max_state": round(mean_max, 6),
                    "mean_min_state": round(mean_min, 6),
                    "diff_mean": round(diff_mean, 6),
                    "pct_improvement": round(pct_improvement, 2),
                    "cohen_d": round(cohen_d, 4),
                    "sample_size": sample_size,
                    "confidence_score": round(confidence_score, 2),
                }
            )

    return records


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    config: Optional[dict] = None,
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Perform Hypothesis Discovery analysis on master dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame (read-only).
    output_dir : Union[str, Path]
        Target base report directory (e.g. reports/analytics/latest).
    config : Optional[dict]
        Optional configuration parameters.
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
            module="hypothesis_discovery",
            success=False,
            rows=0,
            columns=0,
            files=0,
            metrics={
                "total_hypotheses_discovered": 0,
                "strongest_hypothesis": "N/A",
                "average_effect_size": 0.0,
                "inconclusive_count": 0,
            },
            elapsed_seconds=time.time() - start_time,
            message="Input DataFrame is empty.",
        )

    n_rows, n_cols = df.shape

    # 1. Dataset Auto-Discovery of Columns
    present_labels = [c for c in LABEL_COLS if c in df.columns]
    if not present_labels:
        return AnalyticsResult(
            module="hypothesis_discovery",
            success=False,
            rows=n_rows,
            columns=n_cols,
            files=0,
            metrics={
                "total_hypotheses_discovered": 0,
                "strongest_hypothesis": "N/A",
                "average_effect_size": 0.0,
                "inconclusive_count": 0,
            },
            elapsed_seconds=time.time() - start_time,
            message="No label outcome columns found in master dataset.",
        )

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    candidate_features = [
        c
        for c in numeric_cols
        if not any(k in c.lower() for k in EXCLUDE_KEYWORDS) and c not in LABEL_COLS
    ]

    bool_features = [c for c in candidate_features if df[c].nunique() <= 2]
    num_features = [c for c in candidate_features if df[c].nunique() > 2]
    cat_regime_session_cols = [
        c
        for c in [
            "trend_strength",
            "market_structure",
            "volatility_expanding",
            "asian",
            "london",
            "newyork",
            "overlap",
            "good_execution",
            "bad_execution",
        ]
        if c in df.columns
    ]

    # 2. Run Subroutines (Vectorized, No row loops)
    num_records = _discover_numeric_feature_hypotheses(df, num_features, present_labels)
    bool_records = _discover_boolean_feature_hypotheses(df, bool_features, present_labels)
    cat_records = _discover_regime_session_hypotheses(df, cat_regime_session_cols, present_labels)

    all_records = num_records + bool_records + cat_records
    discovered_df = pd.DataFrame(all_records)

    total_hypotheses = len(discovered_df)
    if discovered_df.empty:
        return AnalyticsResult(
            module="hypothesis_discovery",
            success=False,
            rows=n_rows,
            columns=n_cols,
            files=0,
            metrics={
                "total_hypotheses_discovered": 0,
                "strongest_hypothesis": "N/A",
                "average_effect_size": 0.0,
                "inconclusive_count": 0,
            },
            elapsed_seconds=time.time() - start_time,
            message="No valid hypotheses could be generated from available dataset features and outcomes.",
        )

    # 3. Output Files Generation
    file_discovered = write_csv(discovered_df, out_path / "discovered_hypotheses.csv")

    # Ranked by Confidence Score descending
    ranked_df = discovered_df.sort_values(by="confidence_score", ascending=False).reset_index(drop=True)
    file_ranked = write_csv(ranked_df, out_path / "ranked_hypotheses.csv")

    # Inconclusive findings (confidence_score < 20.0 or abs(cohen_d) < 0.05)
    inconclusive_df = ranked_df[
        (ranked_df["confidence_score"] < 20.0) | (ranked_df["cohen_d"].abs() < 0.05)
    ].reset_index(drop=True)

    strongest_hyp_str = (
        f"{ranked_df.iloc[0]['hypothesis']} (confidence: {ranked_df.iloc[0]['confidence_score']})"
        if not ranked_df.empty
        else "N/A"
    )
    avg_effect_size = float(ranked_df["cohen_d"].abs().mean()) if not ranked_df.empty else 0.0

    # Top features requiring further validation
    top_hyp_features = (
        ranked_df.head(20)["predictor"].value_counts().head(5).index.tolist()
        if not ranked_df.empty
        else []
    )

    # Pre-format list strings for clean f-string interpolation
    top_features_str = ", ".join(top_hyp_features) if top_hyp_features else "None"
    top_features_3_str = ", ".join(top_hyp_features[:3]) if top_hyp_features else "N/A"

    # 4. Generate hypothesis_report.md
    report_md = f"""# APEX Quant Research Framework - Hypothesis Discovery Report

**Generated:** {get_timestamp()}  
**Dataset Shape:** {n_rows:,} rows x {n_cols:,} columns  
**Total Hypotheses Discovered:** {total_hypotheses:,}  

---

## 1. Executive Summary

This module automatically discovers statistically supported research hypotheses across numeric features, boolean indicators, market regimes, and trading sessions against label outcomes.

- **Total Hypotheses Discovered:** {total_hypotheses:,}
- **Strongest Supported Hypothesis:** {strongest_hyp_str}
- **Average Absolute Effect Size (Cohen's d):** {avg_effect_size:.4f}
- **Inconclusive Findings:** {len(inconclusive_df):,} hypotheses
- **Top Predictor Features for Validation:** `{top_features_str}`

---

## 2. Strongest Supported Hypotheses (Top 10)

Hypotheses ranked by statistical confidence score (0.40 * correlation + 0.30 * effect_size + 0.30 * t_stat_scale):

{df_to_markdown(ranked_df.head(10)[['hypothesis', 'category', 'predictor', 'target', 'cohen_d', 'pct_improvement', 'sample_size', 'confidence_score']], max_rows=15)}

---

## 3. Weakest Supported Hypotheses (Bottom 10)

{df_to_markdown(ranked_df.tail(10)[['hypothesis', 'category', 'predictor', 'target', 'cohen_d', 'pct_improvement', 'sample_size', 'confidence_score']], max_rows=15)}

---

## 4. Inconclusive Findings

Hypotheses showing weak effect sizes (|d| < 0.05) or low statistical confidence (< 20.0):

{df_to_markdown(inconclusive_df.head(10)[['hypothesis', 'category', 'predictor', 'target', 'cohen_d', 'confidence_score']], max_rows=15) if not inconclusive_df.empty else "_No inconclusive findings detected; all evaluated hypotheses met confidence thresholds._"}

---

## 5. Features Requiring Further Validation

The following predictor features appear most frequently among the highest-confidence hypotheses:
- `{top_features_str}`

---

## 6. Recommended Next Experiments

1. **Conduct Feature Importance & SHAP Ranking:** Target top predictor features (`{top_features_3_str}`) in the Feature Importance module to evaluate non-linear predictive contribution.
2. **Analyze Parameter Surfaces:** Evaluate parameter stability across surface slices for high-effect hypotheses.
3. **Prune Redundant Predictors:** Cross-reference weak or inconclusive features with Correlation Analysis to streamline feature sets.
"""

    file_report_md = write_markdown(report_md, out_path / "hypothesis_report.md")

    # 5. Generate summary.json
    elapsed = time.time() - start_time
    metrics_dict = {
        "total_hypotheses_discovered": total_hypotheses,
        "strongest_hypothesis": strongest_hyp_str,
        "average_effect_size": round(avg_effect_size, 4),
        "inconclusive_count": len(inconclusive_df),
        "top_features_for_validation": top_hyp_features,
    }

    summary_data = {
        "framework": "APEX Quant Research Framework",
        "module": "hypothesis_discovery",
        "timestamp": get_timestamp(),
        "dataset_rows": n_rows,
        "dataset_columns": n_cols,
        "files_generated": [
            "discovered_hypotheses.csv",
            "ranked_hypotheses.csv",
            "hypothesis_report.md",
            "summary.json",
        ],
        "metrics": metrics_dict,
        "elapsed_seconds": round(elapsed, 4),
        "message": f"Hypothesis discovery completed. Discovered and ranked {total_hypotheses} hypotheses.",
    }

    file_summary_json = write_json(summary_data, out_path / "summary.json")

    if verbose:
        print(
            f"[analytics.hypothesis_discovery] Discovered and ranked {total_hypotheses} hypotheses in {elapsed:.2f}s. "
            f"Strongest hypothesis: {strongest_hyp_str}."
        )

    return AnalyticsResult(
        module="hypothesis_discovery",
        success=True,
        rows=n_rows,
        columns=n_cols,
        files=4,
        metrics=metrics_dict,
        elapsed_seconds=elapsed,
        message=f"Hypothesis discovery completed. Discovered and ranked {total_hypotheses} hypotheses.",
    )
