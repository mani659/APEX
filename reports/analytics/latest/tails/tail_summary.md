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


