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
