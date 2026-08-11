# APEX Quant Research Framework - Unified Research Report

**Generated:** 2026-07-27 14:53:31  
**Dataset Shape:** 2,000 rows x 116 columns  

---

## 1. Executive Summary

| Analytics Module | Status | Key Artifacts | Summary Message |
| :--- | :--- | :--- | :--- |
| **statistics** | ✅ Success | 4 files | Completed |
| **tail_statistics** | ✅ Success | 4 files | Completed |
| **regime_analysis** | ✅ Success | 4 files | Regime analysis completed successfully for 18 market regimes. |
| **correlation_analysis** | ✅ Success | 5 files | Correlation analysis completed successfully. Found 83 high correlation pairs across 103 features. |
| **stability_analysis** | ✅ Success | 6 files | Stability analysis completed across 1 monthly segments. Overall Score: 100.00/100. |
| **hypothesis_discovery** | ✅ Success | 4 files | Hypothesis discovery completed. Discovered and ranked 624 hypotheses. |
| **feature_importance** | ✅ Success | 4 files | Completed |
| **parameter_surface** | ✅ Success | 4 files | Completed |

---

# Dataset Statistical Overview

**Generated:** 2026-07-27 14:53:28  
**Target:** `statistics`

---

## 1. Executive Summary

- **Total Rows:** 2,000
- **Total Columns:** 116 (115 numeric)
- **Memory Footprint:** 1.30 MB
- **Duplicate Rows:** 0
- **Total Missing Cells:** 0
- **Total Infinite Cells:** 0

---

## 2. Column Diagnostics

- **Constant Columns (13):** volume, volume_ma20, volume_ratio, volume_zscore, volume_delta, volume_pct_change, volume_expanding, volume_contracting, high_volume, low_volume, vwap, vwap_distance, month
- **Near-Constant Columns (1):** bull_exhaustion
- **Zero-Variance Columns (13):** volume, volume_ma20, volume_ratio, volume_zscore, volume_delta, volume_pct_change, volume_expanding, volume_contracting, high_volume, low_volume, vwap, vwap_distance, month

---

## 3. Data Types Breakdown

| Data Type | Count |
| :--- | :--- |
| `float64` | 75 |
| `int8` | 35 |
| `int64` | 5 |
| `datetime64[us]` | 1 |

---

## 4. Top Feature Summary Preview

| column | dtype | missing | mean | std | median | iqr | is_constant |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| datetime | datetime64[us] | 0 |  |  |  |  | False |
| open | float64 | 0 | 1735 | 6.695 | 1733 | 12.48 | False |
| high | float64 | 0 | 1735 | 6.715 | 1733 | 12.61 | False |
| low | float64 | 0 | 1735 | 6.687 | 1733 | 12.33 | False |
| close | float64 | 0 | 1735 | 6.696 | 1733 | 12.47 | False |
| volume | int64 | 0 | 0 | 0 | 0 | 0 | True |
| price | float64 | 0 | 1735 | 6.696 | 1733 | 12.47 | False |
| hl2 | float64 | 0 | 1735 | 6.699 | 1733 | 12.49 | False |
| hlc3 | float64 | 0 | 1735 | 6.697 | 1733 | 12.45 | False |
| ohlc4 | float64 | 0 | 1735 | 6.696 | 1733 | 12.48 | False |
| body | float64 | 0 | 0.001461 | 0.3688 | -0.01 | 0.343 | False |
| body_abs | float64 | 0 | 0.2552 | 0.2662 | 0.17 | 0.2787 | False |
| upper_wick | float64 | 0 | 0.1113 | 0.1314 | 0.0735 | 0.127 | False |
| lower_wick | float64 | 0 | 0.1075 | 0.142 | 0.07 | 0.13 | False |
| range | float64 | 0 | 0.474 | 0.3331 | 0.3995 | 0.347 | False |
| body_pct | float64 | 0 | -0.01855 | 0.5747 | -0.02389 | 1.011 | False |
| volume_ma20 | float64 | 0 | 0 | 0 | 0 | 0 | True |
| volume_ratio | float64 | 0 | 0 | 0 | 0 | 0 | True |
| volume_zscore | float64 | 0 | 0 | 0 | 0 | 0 | True |
| volume_delta | float64 | 0 | 0 | 0 | 0 | 0 | True |
| volume_pct_change | float64 | 0 | 0 | 0 | 0 | 0 | True |
| volume_expanding | int8 | 0 | 0 | 0 | 0 | 0 | True |
| volume_contracting | int8 | 0 | 0 | 0 | 0 | 0 | True |
| high_volume | int8 | 0 | 0 | 0 | 0 | 0 | True |
| low_volume | int8 | 0 | 0 | 0 | 0 | 0 | True |



---

# Tail Statistics & Extreme Value Report

**Generated:** 2026-07-27 14:53:29  
**Target:** `tail_statistics`

---

## 1. Overview

- **Analyzed Numeric Columns:** 115
- **Label / Return Columns Detected:** 7 (body_abs, body_pct, volatility_expanding, liquidity_sweep_high, liquidity_sweep_low, return, future_return)

---

## 2. Key Label / Return Tail Metrics

| column | min | left_es_1pct | p1 | p50 | p99 | right_es_99pct | max | extreme_cnt_3std | asymmetry_ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| body_abs | 0 | 0 | 0 | 0.17 | 1.243 | 1.58 | 2.353 | 35 | 3.97 |
| body_pct | -1 | -1 | -1 | -0.02389 | 1 | 1 | 1 | 0 | 1.057 |
| volatility_expanding | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| liquidity_sweep_high | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| liquidity_sweep_low | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| return | -0.001229 | -0.000726 | -0.000542 | -6e-06 | 0.000624 | 0.000834 | 0.001339 | 30 | 1.143 |
| future_return | -0.007312 | -0.006731 | -0.006533 | 0 | 0.01162 | 0.01214 | 0.0128 | 21 | 1.776 |


## 3. Extreme Event Analysis (> 3 Std Devs)

Top columns with highest number of extreme outlier observations:

| column | count | extreme_cnt_2std | extreme_cnt_3std | extreme_cnt_5std | std | min | max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| trend_slope_100 | 2000 | 95 | 65 | 0 | 0.04626 | -0.0894 | 0.1657 |
| ema_dist_100 | 2000 | 118 | 52 | 0 | 0.001198 | -0.003309 | 0.005529 |
| ema_slope_100 | 2000 | 117 | 52 | 0 | 0.04198 | -0.1162 | 0.1942 |
| future_max_up | 2000 | 167 | 49 | 0 | 0.003421 | -4e-05 | 0.0141 |
| mfe | 2000 | 167 | 49 | 0 | 0.003421 | -4e-05 | 0.0141 |
| ema_slope_200 | 2000 | 109 | 48 | 0 | 0.03038 | -0.06973 | 0.1335 |
| ema_dist_200 | 2000 | 109 | 48 | 0 | 0.001743 | -0.003988 | 0.007659 |
| rolling_std20 | 2000 | 113 | 45 | 6 | 0.4187 | 0 | 3.17 |
| up_streak | 2000 | 100 | 44 | 6 | 1.296 | 0 | 10 |
| upper_wick | 2000 | 96 | 39 | 6 | 0.1314 | 0 | 1.6 |
| macd_hist_delta | 2000 | 108 | 39 | 4 | 0.03274 | -0.1698 | 0.1781 |
| roc_10 | 2000 | 119 | 38 | 3 | 0.07056 | -0.278 | 0.4229 |
| momentum_10 | 2000 | 119 | 38 | 3 | 1.225 | -4.83 | 7.33 |
| down_streak | 2000 | 125 | 37 | 1 | 1.401 | 0 | 9 |
| ema_slope_10 | 2000 | 106 | 37 | 3 | 0.1211 | -0.5205 | 0.7371 |




---

# APEX Quant Research Framework - Regime Analysis Report

**Generated:** 2026-07-27 14:53:29  
**Dataset Shape:** 2,000 rows x 116 columns  
**Detected Regimes Analyzed:** 18  

---

## 1. Executive Summary

This module evaluates how labels, returns, and execution outcomes behave across different market regimes (Trend vs Range, Bull vs Bear, Volatility States, Trading Sessions, and Execution Quality).

- **Total Regimes Evaluated:** 18
- **Best Performing Regime:** Good Execution (mean_future_return: 0.0042)
- **Worst Performing Regime:** Asian Session (mean_future_return: -0.0014)
- **Largest Market Regime:** Non-Overlap (1,640 rows, 82.0%)
- **Smallest Market Regime:** Session Overlap (360 rows, 18.0%)

---

## 2. Detected Regimes & Column Coverage

The following key regime columns were automatically detected in the master dataset:
- **Detected Columns (15):** `trend_strength, market_structure, volatility_expanding, ema_stack_bull, ema_stack_bear, asian, london, newyork, overlap, future_direction, future_return, good_execution, return, body_pct, body_abs`

⚠️ **Missing Optional Columns (2):** `session, bad_execution`  
*Analysis for missing columns degraded gracefully without failure.*

---

## 3. Performance by Regime (Full Summary)

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| All Data | 2000 | 100 | 1.153e-06 | -5.763e-06 | 0.0002142 | 47.65 | 50.8 | 0.0004735 | 0 | 0.002607 | -0.002284 |  | 29.95 | 70.05 | 0.4715 |
| Trend (High Trend Strength) | 757 | 37.85 | 5.715e-05 | 4.011e-05 | 0.0002127 | 59.58 | 39.1 | 0.0002323 | 0 | 0.002448 | -0.002482 |  | 22.46 | 77.54 | 0.4386 |
| Range (Low Trend Strength) | 1243 | 62.15 | -3.295e-05 | -2.693e-05 | 0.0002079 | 40.39 | 57.92 | 0.0006205 | 0 | 0.002704 | -0.002164 |  | 34.51 | 65.49 | 0.4916 |
| Bullish Structure | 734 | 36.7 | 0.0001227 | 8.372e-05 | 0.0001992 | 74.66 | 24.66 | 0.0004746 | 0 | 0.00255 | -0.00223 |  | 28.61 | 71.39 | 0.4605 |
| Bearish Structure | 814 | 40.7 | -0.0001167 | -8.65e-05 | 0.0001751 | 20.88 | 77.15 | 0.0005106 | 0 | 0.002617 | -0.002285 |  | 30.22 | 69.78 | 0.4767 |
| Ranging Structure | 452 | 22.6 | 1.587e-05 | 5.756e-06 | 0.000185 | 51.99 | 45.8 | 0.0004051 | 0 | 0.002683 | -0.002372 |  | 31.64 | 68.36 | 0.4801 |
| EMA Bull Stack | 488 | 24.4 | 2.283e-05 | 5.763e-06 | 0.0002555 | 51.23 | 47.95 | 0.0001914 | 0 | 0.002753 | -0.002726 |  | 28.07 | 71.93 | 0.4734 |
| EMA Bear Stack | 478 | 23.9 | -1.611e-05 | -1.158e-05 | 0.0002238 | 44.98 | 53.56 | 0.0009359 | 0.0001715 | 0.003194 | -0.001991 |  | 42.47 | 57.53 | 0.569 |
| High Volatility (Expanding) | 981 | 49.05 | 1.454e-05 | 1.734e-06 | 0.0002709 | 50.25 | 49.24 | 0.0005809 | 0 | 0.002749 | -0.002264 |  | 31.19 | 68.81 | 0.4801 |
| Low Volatility (Contracting) | 1019 | 50.95 | -1.173e-05 | -5.78e-06 | 0.0001381 | 45.14 | 52.31 | 0.0003702 | 0 | 0.002471 | -0.002304 |  | 28.75 | 71.25 | 0.4632 |
| Asian Session | 480 | 24 | -5.199e-06 | -5.788e-06 | 0.0001809 | 46.88 | 51.25 | -0.001364 | -0.0005695 | 0.001767 | -0.003005 |  | 32.29 | 67.71 | 0.3625 |
| London Session | 779 | 38.95 | 5.646e-06 | -7.531e-06 | 0.0002791 | 47.24 | 51.6 | 0.001839 | 0.001142 | 0.004669 | -0.002699 |  | 46.85 | 53.15 | 0.5777 |
| New York Session | 960 | 48 | 1.453e-06 | 0 | 0.0002279 | 49.06 | 49.79 | -9.124e-05 | 0 | 0.001201 | -0.001667 |  | 18.23 | 81.77 | 0.3844 |
| Session Overlap | 360 | 18 | 1.028e-06 | -1.436e-05 | 0.0003178 | 47.5 | 51.94 | -0.0004222 | -0.0006553 | 0.001788 | -0.002499 |  | 26.67 | 73.33 | 0.4194 |
| Non-Overlap | 1640 | 82 | 1.181e-06 | -5.73e-06 | 0.0001839 | 47.68 | 50.55 | 0.0006702 | 0 | 0.002787 | -0.002237 |  | 30.67 | 69.33 | 0.4829 |
| Good Execution | 599 | 29.95 | 3.143e-06 | -5.796e-06 | 0.0002506 | 46.74 | 51.42 | 0.004198 | 0.002578 | 0.006397 | -0.001001 |  | 100 | 0 | 0.9065 |
| Bad Execution | 1401 | 70.05 | 3.027e-07 | -5.731e-06 | 0.0001966 | 48.04 | 50.54 | -0.001119 | -0.0001788 | 0.000987 | -0.002833 |  | 0 | 100 | 0.2855 |
| Large Candle Body | 1000 | 50 | 3.186e-06 | -4.615e-05 | 0.0002904 | 47.9 | 52 | 0.0004626 | 0 | 0.002543 | -0.002239 |  | 29.2 | 70.8 | 0.459 |
| Small Candle Body | 1000 | 50 | -8.796e-07 | 0 | 8.625e-05 | 47.4 | 49.6 | 0.0004845 | 0 | 0.002671 | -0.00233 |  | 30.7 | 69.3 | 0.484 |


---

## 4. Conditional Pairwise Analyses

### Trend vs Range Analysis

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Trend (High Trend Strength) | 757 | 37.85 | 5.715e-05 | 4.011e-05 | 0.0002127 | 59.58 | 39.1 | 0.0002323 | 0 | 0.002448 | -0.002482 |  | 22.46 | 77.54 | 0.4386 |
| Range (Low Trend Strength) | 1243 | 62.15 | -3.295e-05 | -2.693e-05 | 0.0002079 | 40.39 | 57.92 | 0.0006205 | 0 | 0.002704 | -0.002164 |  | 34.51 | 65.49 | 0.4916 |
| Bullish Structure | 734 | 36.7 | 0.0001227 | 8.372e-05 | 0.0001992 | 74.66 | 24.66 | 0.0004746 | 0 | 0.00255 | -0.00223 |  | 28.61 | 71.39 | 0.4605 |
| Bearish Structure | 814 | 40.7 | -0.0001167 | -8.65e-05 | 0.0001751 | 20.88 | 77.15 | 0.0005106 | 0 | 0.002617 | -0.002285 |  | 30.22 | 69.78 | 0.4767 |
| Ranging Structure | 452 | 22.6 | 1.587e-05 | 5.756e-06 | 0.000185 | 51.99 | 45.8 | 0.0004051 | 0 | 0.002683 | -0.002372 |  | 31.64 | 68.36 | 0.4801 |


### Bull vs Bear Analysis

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| EMA Bull Stack | 488 | 24.4 | 2.283e-05 | 5.763e-06 | 0.0002555 | 51.23 | 47.95 | 0.0001914 | 0 | 0.002753 | -0.002726 |  | 28.07 | 71.93 | 0.4734 |
| EMA Bear Stack | 478 | 23.9 | -1.611e-05 | -1.158e-05 | 0.0002238 | 44.98 | 53.56 | 0.0009359 | 0.0001715 | 0.003194 | -0.001991 |  | 42.47 | 57.53 | 0.569 |


### High Volatility vs Low Volatility Analysis

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| High Volatility (Expanding) | 981 | 49.05 | 1.454e-05 | 1.734e-06 | 0.0002709 | 50.25 | 49.24 | 0.0005809 | 0 | 0.002749 | -0.002264 |  | 31.19 | 68.81 | 0.4801 |
| Low Volatility (Contracting) | 1019 | 50.95 | -1.173e-05 | -5.78e-06 | 0.0001381 | 45.14 | 52.31 | 0.0003702 | 0 | 0.002471 | -0.002304 |  | 28.75 | 71.25 | 0.4632 |


### London vs Asia Analysis

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| London Session | 779 | 38.95 | 5.646e-06 | -7.531e-06 | 0.0002791 | 47.24 | 51.6 | 0.001839 | 0.001142 | 0.004669 | -0.002699 |  | 46.85 | 53.15 | 0.5777 |
| Asian Session | 480 | 24 | -5.199e-06 | -5.788e-06 | 0.0001809 | 46.88 | 51.25 | -0.001364 | -0.0005695 | 0.001767 | -0.003005 |  | 32.29 | 67.71 | 0.3625 |


### London vs NY Analysis

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| London Session | 779 | 38.95 | 5.646e-06 | -7.531e-06 | 0.0002791 | 47.24 | 51.6 | 0.001839 | 0.001142 | 0.004669 | -0.002699 |  | 46.85 | 53.15 | 0.5777 |
| New York Session | 960 | 48 | 1.453e-06 | 0 | 0.0002279 | 49.06 | 49.79 | -9.124e-05 | 0 | 0.001201 | -0.001667 |  | 18.23 | 81.77 | 0.3844 |


### Session Overlap Analysis

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Session Overlap | 360 | 18 | 1.028e-06 | -1.436e-05 | 0.0003178 | 47.5 | 51.94 | -0.0004222 | -0.0006553 | 0.001788 | -0.002499 |  | 26.67 | 73.33 | 0.4194 |
| Non-Overlap | 1640 | 82 | 1.181e-06 | -5.73e-06 | 0.0001839 | 47.68 | 50.55 | 0.0006702 | 0 | 0.002787 | -0.002237 |  | 30.67 | 69.33 | 0.4829 |


### Execution Quality Analysis

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Good Execution | 599 | 29.95 | 3.143e-06 | -5.796e-06 | 0.0002506 | 46.74 | 51.42 | 0.004198 | 0.002578 | 0.006397 | -0.001001 |  | 100 | 0 | 0.9065 |
| Bad Execution | 1401 | 70.05 | 3.027e-07 | -5.731e-06 | 0.0001966 | 48.04 | 50.54 | -0.001119 | -0.0001788 | 0.000987 | -0.002833 |  | 0 | 100 | 0.2855 |


---

## 5. Interesting Findings

- Session disparity detected: Highest return session is `London Session` (mean: 0.000006), lowest is `Asian Session` (mean: -0.000005).
- Volatility impact evaluated: `High Volatility (Expanding)` shows return std of 0.000271 vs `Low Volatility (Contracting)` std of 0.000138.
- Execution quality impact: `Good Execution` yields mean future return of 0.004198.

---

## 6. Warnings & Missing Columns

- **Missing Columns Warning:** The dataset lacks `session, bad_execution`. Ensure feature and label pipelines populate these for deeper regime attribution.


---

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




---

# APEX Quant Research Framework - Feature & Label Stability Report

**Generated:** 2026-07-27 14:53:29  
**Dataset Shape:** 2,000 rows x 116 columns  
**Overall Stability Score:** **100.00 / 100**  
**Time Periods Evaluated:** 1 Year(s), 1 Quarter(s), 1 Month(s)  

---

## 1. Executive Summary

This module evaluates whether feature and label distributions remain stable across time segments (yearly, quarterly, monthly) rather than optimizing trading strategies.

- **Overall Stability Score:** **100.00 / 100**
- **Evaluated Time History:** 1 Year(s) | 1 Quarter(s) | 1 Month(s)
- **Top Stable Features:** `open, high, low, close, volume`
- **Least Stable Features:** `reward_risk, survived, grid_expansion, future_max_down, future_max_up`
- **Unstable Labels Flagged:** `None (All Labels Stable)`

---

## 2. Feature Stability Highlights

### Most Stable Features (Top 5)
| column | global_mean | global_std | cv_period_means | drift_first_last | stability_score | instability_flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| open | 1735 | 6.695 | 0 | 0 | 100 | FALSE |
| high | 1735 | 6.715 | 0 | 0 | 100 | FALSE |
| low | 1735 | 6.687 | 0 | 0 | 100 | FALSE |
| close | 1735 | 6.696 | 0 | 0 | 100 | FALSE |
| volume | 0 | 0 | 0 | 0 | 100 | FALSE |


### Least Stable Features (Top 5)
| column | global_mean | global_std | cv_period_means | drift_first_last | stability_score | instability_flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| future_max_up | 0.002607 | 0.003421 | 0 | 0 | 100 | FALSE |
| future_max_down | -0.002284 | 0.001938 | 0 | 0 | 100 | FALSE |
| grid_expansion | 0.004892 | 0.003383 | 0 | 0 | 100 | FALSE |
| survived | 0.88 | 0.325 | 0 | 0 | 100 | FALSE |
| reward_risk | 4.938 | 80.29 | 0 | 0 | 100 | FALSE |


---

## 3. Largest Distribution Drift (First vs Last Period)

Top columns experiencing highest relative drift between initial and final time segments:

| column | is_label | global_mean | global_std | drift_first_last | max_dev_global | stability_score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| open | False | 1735 | 6.695 | 0 | 0 | 100 |
| high | False | 1735 | 6.715 | 0 | 0 | 100 |
| low | False | 1735 | 6.687 | 0 | 0 | 100 |
| close | False | 1735 | 6.696 | 0 | 0 | 100 |
| volume | False | 0 | 0 | 0 | 0 | 100 |
| price | False | 1735 | 6.696 | 0 | 0 | 100 |
| hl2 | False | 1735 | 6.699 | 0 | 0 | 100 |
| hlc3 | False | 1735 | 6.697 | 0 | 0 | 100 |
| ohlc4 | False | 1735 | 6.696 | 0 | 0 | 100 |
| body | False | 0.001461 | 0.3688 | 0 | 0 | 100 |


---

## 4. Label Stability Breakdown

Evaluation of target outcome labels across time periods:

| column | global_mean | global_std | cv_period_means | drift_first_last | max_dev_global | stability_score | instability_flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| return | 1e-06 | 0.000214 | 0 | 0 | 0 | 100 | FALSE |
| future_return | 0.000474 | 0.003711 | 0 | 0 | 0 | 100 | FALSE |
| future_direction | 0.4715 | 0.4993 | 0 | 0 | 0 | 100 | FALSE |
| mae | -0.002284 | 0.001938 | 0 | 0 | 0 | 100 | FALSE |
| mfe | 0.002607 | 0.003421 | 0 | 0 | 0 | 100 | FALSE |
| good_execution | 0.2995 | 0.4582 | 0 | 0 | 0 | 100 | FALSE |


---

## 5. Time Segment Coverage Overview

- **Yearly Periods:** 1
- **Quarterly Periods:** 1
- **Monthly Periods:** 1


---

# APEX Quant Research Framework - Hypothesis Discovery Report

**Generated:** 2026-07-27 14:53:31  
**Dataset Shape:** 2,000 rows x 116 columns  
**Total Hypotheses Discovered:** 624  

---

## 1. Executive Summary

This module automatically discovers statistically supported research hypotheses across numeric features, boolean indicators, market regimes, and trading sessions against label outcomes.

- **Total Hypotheses Discovered:** 624
- **Strongest Supported Hypothesis:** Regime good_execution (1 vs 0) -> future_return (confidence: 100.0)
- **Average Absolute Effect Size (Cohen's d):** 320513.2581
- **Inconclusive Findings:** 327 hypotheses
- **Top Predictor Features for Validation:** `good_execution, future_max_up, price_velocity, london, market_structure`

---

## 2. Strongest Supported Hypotheses (Top 10)

Hypotheses ranked by statistical confidence score (0.40 * correlation + 0.30 * effect_size + 0.30 * t_stat_scale):

| hypothesis | category | predictor | target | cohen_d | pct_improvement | sample_size | confidence_score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Regime good_execution (1 vs 0) -> future_return | Regime -> Label | good_execution | future_return | 1.689 | 475.2 | 2000 | 100 |
| Regime good_execution (1 vs 0) -> future_direction | Regime -> Label | good_execution | future_direction | 1.634 | 217.5 | 2000 | 100 |
| Regime good_execution (1 vs 0) -> mfe | Regime -> Label | good_execution | mfe | 1.836 | 548.1 | 2000 | 100 |
| Regime good_execution (1 vs 0) -> mae | Regime -> Label | good_execution | mae | 1.206 | 64.65 | 2000 | 100 |
| Regime good_execution (1 vs 0) -> good_execution | Regime -> Label | good_execution | good_execution | 1e+08 | 1e+10 | 2000 | 100 |
| High vs Low price_velocity -> return | Numeric Feature -> Label | price_velocity | return | 3.153 |  | 1014 | 100 |
| High vs Low future_max_up -> mfe | Numeric Feature -> Label | future_max_up | mfe | 2.57 |  | 1000 | 100 |
| Session london (1 vs 0) -> mfe | Session -> Label | london | mfe | 1.011 | 261.4 | 2000 | 100 |
| Regime market_structure (2 vs -2) -> return | Regime -> Label | market_structure | return | 1.325 | 204.1 | 1432 | 100 |
| High vs Low future_max_down -> mae | Numeric Feature -> Label | future_max_down | mae | 5.104 |  | 1000 | 100 |


---

## 3. Weakest Supported Hypotheses (Bottom 10)

| hypothesis | category | predictor | target | cohen_d | pct_improvement | sample_size | confidence_score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| swing_high (True vs False) -> future_direction | Boolean Feature -> Label | swing_high | future_direction | 0.0044 | 0.47 | 2000 | 0.68 |
| liquidity_sweep_low (True vs False) -> mfe | Boolean Feature -> Label | liquidity_sweep_low | mfe | 0.0042 | 0.55 | 2000 | 0.64 |
| newyork (True vs False) -> return | Boolean Feature -> Label | newyork | return | 0.0027 | 64.85 | 2000 | 0.49 |
| lower_high (True vs False) -> mfe | Boolean Feature -> Label | lower_high | mfe | -0.0023 | -0.3 | 2000 | 0.43 |
| High vs Low price_acceleration -> mae | Numeric Feature -> Label | price_acceleration | mae | 0.0007 |  | 1002 | 0.36 |
| future_down (True vs False) -> return | Boolean Feature -> Label | future_down | return | 0.0018 | 36.7 | 2000 | 0.28 |
| High vs Low rsi_acceleration -> good_execution | Numeric Feature -> Label | rsi_acceleration | good_execution | 0 |  | 1000 | 0.18 |
| lower_high (True vs False) -> good_execution | Boolean Feature -> Label | lower_high | good_execution | -0.0008 | -0.12 | 2000 | 0.14 |
| Session overlap (0 vs 1) -> return | Session -> Label | overlap | return | 0.0006 | 14.76 | 2000 | 0.12 |
| overlap (True vs False) -> return | Boolean Feature -> Label | overlap | return | -0.0006 | -12.86 | 2000 | 0.08 |


---

## 4. Inconclusive Findings

Hypotheses showing weak effect sizes (|d| < 0.05) or low statistical confidence (< 20.0):

| hypothesis | category | predictor | target | cohen_d | confidence_score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| High vs Low hour -> future_direction | Numeric Feature -> Label | hour | future_direction | -0.1454 | 19.87 |
| Session overlap (0 vs 1) -> good_execution | Session -> Label | overlap | good_execution | 0.0886 | 19.85 |
| ema_stack_bull (True vs False) -> return | Boolean Feature -> Label | ema_stack_bull | return | 0.1253 | 19.66 |
| High vs Low upper_wick -> future_return | Numeric Feature -> Label | upper_wick | future_return | 0.1362 | 19.41 |
| swing_high (True vs False) -> return | Boolean Feature -> Label | swing_high | return | 0.1244 | 19.32 |
| bear_fvg (True vs False) -> future_return | Boolean Feature -> Label | bear_fvg | future_return | 0.145 | 19.19 |
| overlap (True vs False) -> future_direction | Boolean Feature -> Label | overlap | future_direction | -0.1277 | 19 |
| High vs Low rsi_21 -> future_direction | Numeric Feature -> Label | rsi_21 | future_direction | -0.1327 | 18.86 |
| High vs Low range_pct -> future_return | Numeric Feature -> Label | range_pct | future_return | 0.1297 | 18.51 |
| High vs Low roc_10 -> mae | Numeric Feature -> Label | roc_10 | mae | -0.1313 | 18.07 |


---

## 5. Features Requiring Further Validation

The following predictor features appear most frequently among the highest-confidence hypotheses:
- `good_execution, future_max_up, price_velocity, london, market_structure`

---

## 6. Recommended Next Experiments

1. **Conduct Feature Importance & SHAP Ranking:** Target top predictor features (`good_execution, future_max_up, price_velocity`) in the Feature Importance module to evaluate non-linear predictive contribution.
2. **Analyze Parameter Surfaces:** Evaluate parameter stability across surface slices for high-effect hypotheses.
3. **Prune Redundant Predictors:** Cross-reference weak or inconclusive features with Correlation Analysis to streamline feature sets.


---

# Feature Importance & Informativeness Report

**Generated:** 2026-07-27 14:53:31  
**Target:** `feature_importance`

---

## 1. Executive Summary

- **Total Features Analyzed:** 108
- **Target / Label Columns Found:** 7 (body_abs, body_pct, volatility_expanding, liquidity_sweep_high, liquidity_sweep_low, return, future_return)
- **Mutual Information Method:** fallback (variance/SNR)

---

## 2. Top Ranked Features

| rank | feature | composite_score | top_target | max_pearson_corr | max_spearman_corr | variance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | price_velocity | 0.8 | return | 1 | 1 | 0.1382 |
| 2 | body | 0.795 | return | 0.9954 | 0.9921 | 0.136 |
| 3 | rsi_velocity | 0.7358 | return | 0.874 | 0.9655 | 22.01 |
| 4 | mfe | 0.6176 | future_return | 0.8665 | 0.6774 | 1.2e-05 |
| 5 | future_max_up | 0.6176 | future_return | 0.8665 | 0.6774 | 1.2e-05 |
| 6 | future_direction | 0.6085 | future_return | 0.656 | 0.8654 | 0.2493 |
| 7 | tr | 0.5971 | body_abs | 0.7881 | 0.7046 | 0.111 |
| 8 | range | 0.5966 | body_abs | 0.7878 | 0.7037 | 0.1109 |
| 9 | range_pct | 0.5964 | body_abs | 0.7875 | 0.7036 | 0 |
| 10 | future_up | 0.5817 | future_return | 0.7775 | 0.6766 | 0.1524 |
| 11 | up_streak | 0.5697 | body_pct | 0.6188 | 0.8054 | 1.681 |
| 12 | down_streak | 0.564 | body_pct | -0.6106 | -0.7993 | 1.962 |
| 13 | macd_hist_delta | 0.5625 | return | 0.7349 | 0.6714 | 0.001072 |
| 14 | price_acceleration | 0.5474 | return | 0.7048 | 0.6638 | 0.2747 |
| 15 | good_execution | 0.5234 | future_return | 0.6565 | 0.652 | 0.2099 |
| 16 | future_down | 0.5184 | future_return | -0.6099 | -0.6862 | 0.1567 |
| 17 | rsi_acceleration | 0.4917 | body_pct | 0.6079 | 0.6215 | 46.09 |
| 18 | bull_displacement | 0.4848 | body_pct | 0.6101 | 0.6019 | 0.1208 |
| 19 | bear_displacement | 0.4841 | body_pct | -0.6004 | -0.6099 | 0.124 |
| 20 | mae | 0.4814 | future_return | 0.6109 | 0.5926 | 4e-06 |




---

# Parameter Surface & Stability Analysis

**Generated:** 2026-07-27 14:53:31  
**Target:** `parameter_surface`

---

## 1. Status

- **Parameter Inputs Available:** Yes
- **Message:** Analyzed parameter surface for 'grid_expansion' against 'volume_zscore'.

---

## 2. Parameter Surface Summary

| parameter | mean_performance | std_stability | best_performance | median_performance | worst_performance | count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | 0 | 0 | 0 | 0 | 0 | 240 |
| 0.00203 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00203 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00203 | 0 |  | 0 | 0 | 0 | 1 |
| 0.002036 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00207 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.00208 | 0 |  | 0 | 0 | 0 | 1 |
| 0.002081 | 0 |  | 0 | 0 | 0 | 1 |
| 0.002081 | 0 | 0 | 0 | 0 | 0 | 2 |
| 0.002081 | 0 |  | 0 | 0 | 0 | 1 |
| 0.002081 | 0 |  | 0 | 0 | 0 | 1 |
| 0.002081 | 0 |  | 0 | 0 | 0 | 1 |
| 0.002081 | 0 |  | 0 | 0 | 0 | 1 |
| 0.002082 | 0 |  | 0 | 0 | 0 | 1 |
| 0.002104 | 0 |  | 0 | 0 | 0 | 1 |




---

