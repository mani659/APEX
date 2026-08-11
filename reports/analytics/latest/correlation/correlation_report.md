# APEX Quant Research Framework - Feature Correlation & Redundancy Report

**Generated:** 2026-07-27 14:53:29  
**Dataset Shape:** 2,000 rows x 116 columns  
**Evaluated Numeric Features:** 103  

---

## 1. Executive Summary

This module evaluates feature-to-feature Pearson correlation matrices, detects highly correlated feature pairs ($|r| \ge 0.95$), counts high-correlation partners for each feature, and provides actionable feature reduction recommendations (`KEEP`, `MERGE`, `DROP`).

- **Total Numeric Features Evaluated:** 103
- **Highly Correlated Pairs ($|r| \ge 0.95$):** 83
- **Max High-Correlation Partners Count:** 11
- **Recommended KEEP:** 63
- **Recommended MERGE:** 27
- **Recommended DROP:** 13

---

## 2. Feature Reduction Summary

Recommendations based on uniqueness score, zero-variance checks, and correlation partner counts:

| Action | Count | Percentage | Description |
| :--- | :--- | :--- | :--- |
| **KEEP** | 63 | 61.2% | High unique information content or primary cluster representative |
| **MERGE** | 27 | 26.2% | Highly redundant feature with 1+ high-correlation partner(s) |
| **DROP** | 13 | 12.6% | Constant or near-constant zero-variance feature |

---

## 3. Most Unique vs Most Redundant Features

### Top 5 Most Unique Features
| feature | std | mean_abs_correlation | high_corr_partners_count | uniqueness_score | action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| volume | 0 | 0 | 0 | 100 | DROP |
| volume_zscore | 0 | 0 | 0 | 100 | DROP |
| volume_delta | 0 | 0 | 0 | 100 | DROP |
| volume_pct_change | 0 | 0 | 0 | 100 | DROP |
| volume_expanding | 0 | 0 | 0 | 100 | DROP |


### Top 5 Most Redundant Features
| feature | std | mean_abs_correlation | high_corr_partners_count | uniqueness_score | action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| rsi_14 | 12.65 | 0.3285 | 1 | 67.15 | MERGE |
| ema_slope_20 | 0.08665 | 0.3427 | 1 | 65.73 | KEEP |
| ema_dist_20 | 0.000474 | 0.3428 | 1 | 65.72 | MERGE |
| ema_slope_50 | 0.05703 | 0.3439 | 1 | 65.61 | KEEP |
| ema_dist_50 | 0.000805 | 0.344 | 1 | 65.6 | MERGE |


---

## 4. Top Highly Correlated Pairs ($|r| \ge 0.95$)

| feature_a | feature_b | correlation | abs_correlation |
| :--- | :--- | :--- | :--- |
| close | price | 1 | 1 |
| ema_dist_200 | ema_slope_200 | 1 | 1 |
| ema_dist_100 | ema_slope_100 | 1 | 1 |
| ema_dist_50 | ema_slope_50 | 1 | 1 |
| roc_5 | momentum_5 | 1 | 1 |
| roc_10 | momentum_10 | 1 | 1 |
| ema_dist_20 | ema_slope_20 | 1 | 1 |
| ema_dist_10 | ema_slope_10 | 1 | 1 |
| roc_20 | momentum_20 | 1 | 1 |
| range | range_pct | 1 | 1 |
| hl2 | ohlc4 | 1 | 1 |
| atr | atr_pct | 1 | 1 |
| hlc3 | ohlc4 | 1 | 1 |
| hl2 | hlc3 | 1 | 1 |
| price | hlc3 | 0.9998 | 0.9998 |
| close | hlc3 | 0.9998 | 0.9998 |
| high | hl2 | 0.9997 | 0.9997 |
| low | hl2 | 0.9997 | 0.9997 |
| high | ohlc4 | 0.9997 | 0.9997 |
| high | hlc3 | 0.9997 | 0.9997 |
| low | ohlc4 | 0.9997 | 0.9997 |
| low | hlc3 | 0.9996 | 0.9996 |
| close | ohlc4 | 0.9996 | 0.9996 |
| price | ohlc4 | 0.9996 | 0.9996 |
| open | ohlc4 | 0.9996 | 0.9996 |


---

## 5. Feature Redundancy & Partner Details

| feature | high_corr_partners_count | mean_abs_correlation | max_abs_correlation | action | reason |
| :--- | :--- | :--- | :--- | :--- | :--- |
| volume | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| volume_zscore | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| volume_delta | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| volume_pct_change | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| volume_expanding | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| volume_contracting | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| high_volume | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| low_volume | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| volume_ma20 | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| volume_ratio | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| vwap_distance | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| vwap | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| month | 0 | 0 | 0 | DROP | Zero or near-zero variance (constant feature) |
| volatility_expanding | 0 | 0.045 | 0.361 | KEEP | Unique feature with low redundancy |
| liquidity_sweep_low | 0 | 0.0664 | 0.5494 | KEEP | Unique feature with low redundancy |
| bull_exhaustion | 0 | 0.0665 | 0.2318 | KEEP | Unique feature with low redundancy |
| liquidity_sweep_high | 0 | 0.0677 | 0.5614 | KEEP | Unique feature with low redundancy |
| rsi_acceleration | 0 | 0.0683 | 0.8904 | KEEP | Unique feature with low redundancy |
| price_acceleration | 0 | 0.0707 | 0.8904 | KEEP | Unique feature with low redundancy |
| lower_wick | 0 | 0.0714 | 0.4734 | KEEP | Unique feature with low redundancy |
| swing_high | 0 | 0.0725 | 0.5499 | KEEP | Unique feature with low redundancy |
| swing_low | 0 | 0.0729 | 0.5494 | KEEP | Unique feature with low redundancy |
| bear_exhaustion | 0 | 0.076 | 0.2756 | KEEP | Unique feature with low redundancy |
| weekday | 0 | 0.077 | 0.4961 | KEEP | Unique feature with low redundancy |
| high_volatility | 0 | 0.0928 | 0.4765 | KEEP | Unique feature with low redundancy |
| london | 0 | 0.0995 | 0.5957 | KEEP | Unique feature with low redundancy |
| body_abs | 0 | 0.1065 | 0.7881 | KEEP | Unique feature with low redundancy |
| overlap | 0 | 0.1087 | 0.5935 | KEEP | Unique feature with low redundancy |
| bull_displacement | 0 | 0.1179 | 0.6101 | KEEP | Unique feature with low redundancy |
| newyork | 0 | 0.1185 | 0.6099 | KEEP | Unique feature with low redundancy |


