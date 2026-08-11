# APEX Quant Research Framework - Stability & Robustness Analysis Report

**Generated:** 2026-07-27 14:38:09  
**Dataset Shape:** 2,000 rows x 116 columns  
**Overall Robustness Score:** 66.20 / 100  

---

## 1. Executive Summary

This module measures whether the statistical edge and feature distributions remain stable across 10 chronological rolling windows and between dataset halves.

- **Overall Robustness Score:** **66.20 / 100**
- **Dataset Target Stability:** 62.94 / 100
- **Feature Stability Score:** 76.53 / 100
- **Regime Stability Score:** 57.94 / 100
- **Best Performing Window:** Window 7 (future_return mean: 0.007696)
- **Worst Performing Window:** Window 1 (future_return mean: -0.003989)
- **Most Stable Regime:** New York Session (score: 77.54)
- **Least Stable Regime:** London Session (score: 47.27)

---

## 2. Summary Scores & Mathematical Formulas

The scores are evaluated on a 0–100 scale using the following standardized formulas:

1. **Feature Stability Score**:
   $$\text{drift\_score} = \frac{\sigma(\mu_{w_1}, \dots, \mu_{w_{10}})}{\sigma_{\text{global}} + 1e-8}, \quad \text{stability} = \frac{100}{1 + \text{drift\_score}}$$
2. **Dataset Target Stability Score**: Mean stability score across outcome target metrics.
3. **Regime Stability Score**: Mean consistency score of market regimes across 10 chronological windows.
4. **Overall Robustness Score**:
   $$\text{Overall} = 0.35 \times \text{Dataset} + 0.35 \times \text{Feature} + 0.30 \times \text{Regime}$$

| Metric Name | Score (0-100) | Weight |
| :--- | :--- | :--- |
| **Dataset Stability Score** | 62.94 | 35% |
| **Feature Stability Score** | 76.53 | 35% |
| **Regime Stability Score** | 57.94 | 30% |
| **Overall Robustness Score** | **66.20** | **100%** |

---

## 3. Feature Stability Highlights

### Most Stable Features (Top 5)
| feature | global_mean | global_std | cv | drift_score | stability_score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| volume | 0 | 0 | 0 | 0 | 100 |
| volume_zscore | 0 | 0 | 0 | 0 | 100 |
| volume_delta | 0 | 0 | 0 | 0 | 100 |
| volume_ma20 | 0 | 0 | 0 | 0 | 100 |
| low_volume | 0 | 0 | 0 | 0 | 100 |


### Least Stable Features (Top 5 Unstable)
| feature | global_mean | global_std | cv | drift_score | stability_score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ema_50 | 1735 | 6.472 | 0.0037 | 0.9254 | 51.94 |
| asian | 0.24 | 0.4272 | 1.78 | 0.9317 | 51.77 |
| ema_100 | 1735 | 6.212 | 0.0036 | 0.9406 | 51.53 |
| weekday | 0.64 | 0.4801 | 0.7502 | 0.9462 | 51.38 |
| ema_200 | 1735 | 5.665 | 0.0033 | 0.9574 | 51.09 |


---

## 4. Rolling Window Target Performance

Summary of target outcomes across 10 chronological windows:

| window | row_start | row_end | rows | target | mean | median | std | win_rate | pos_return_pct | neg_return_pct |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 0 | 199 | 200 | return | -1.617e-05 | -1.928e-05 | 0.0002803 | 45 | 45 | 54 |
| 1 | 0 | 199 | 200 | future_return | -0.003989 | -0.004195 | 0.001827 | 1 | 1 | 99 |
| 1 | 0 | 199 | 200 | future_direction | 0.01 | 0 | 0.09975 | 1 | 1 | 0 |
| 1 | 0 | 199 | 200 | mfe | 0.0008967 | 0.0008095 | 0.0006855 | 97.5 | 97.5 | 1 |
| 1 | 0 | 199 | 200 | mae | -0.005292 | -0.005879 | 0.001932 | 0 | 0 | 100 |
| 1 | 0 | 199 | 200 | good_execution | 0.005 | 0 | 0.07071 | 0.5 | 0.5 | 0 |
| 2 | 200 | 399 | 200 | return | -7.527e-06 | -5.771e-06 | 0.0002024 | 46 | 46 | 52 |
| 2 | 200 | 399 | 200 | future_return | -0.0008684 | -0.0002912 | 0.0012 | 32 | 32 | 67.5 |
| 2 | 200 | 399 | 200 | future_direction | 0.32 | 0 | 0.4676 | 32 | 32 | 0 |
| 2 | 200 | 399 | 200 | mfe | 0.0009325 | 0.0008047 | 0.0006208 | 98.5 | 98.5 | 0.5 |
| 2 | 200 | 399 | 200 | mae | -0.003166 | -0.00309 | 0.0006501 | 0 | 0 | 100 |
| 2 | 200 | 399 | 200 | good_execution | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 400 | 599 | 200 | return | 6.726e-08 | 2.888e-06 | 0.0001385 | 50 | 50 | 49 |
| 3 | 400 | 599 | 200 | future_return | 2.132e-05 | -4.708e-05 | 0.001252 | 47 | 47 | 53 |
| 3 | 400 | 599 | 200 | future_direction | 0.47 | 0 | 0.5004 | 47 | 47 | 0 |
| 3 | 400 | 599 | 200 | mfe | 0.001348 | 0.00113 | 0.0007412 | 100 | 100 | 0 |
| 3 | 400 | 599 | 200 | mae | -0.001618 | -0.001903 | 0.0009618 | 0.5 | 0.5 | 98.5 |
| 3 | 400 | 599 | 200 | good_execution | 0.26 | 0 | 0.4397 | 26 | 26 | 0 |
| 4 | 600 | 799 | 200 | return | -1.1e-05 | -1.068e-05 | 0.0001358 | 44 | 44 | 53.5 |
| 4 | 600 | 799 | 200 | future_return | 0.0005569 | 0.000524 | 0.0007474 | 74.5 | 74.5 | 25.5 |


---

## 5. Distribution Shift (First Half vs Second Half)

Top 10 features by mean shift between dataset halves:

| column | mean_h1 | mean_h2 | mean_shift | variance_shift | median_shift | iqr_shift |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| reward_risk | 0.7575 | 9.119 | 8.362 | 1.233e+04 | 1.333 | 4.273 |
| rsi_14 | 46.96 | 51.23 | 4.276 | -23.09 | 2.873 | -2.919 |
| rsi_21 | 47.05 | 51.29 | 4.241 | -24.05 | 2.223 | -3.076 |
| rsi_7 | 46.91 | 50.85 | 3.936 | -5.668 | 3.837 | -2.554 |
| high | 1734 | 1737 | 2.694 | 59.14 | 7.551 | 13.92 |
| hl2 | 1734 | 1736 | 2.647 | 59.37 | 7.208 | 14.1 |
| hlc3 | 1734 | 1736 | 2.647 | 59.33 | 7.2 | 14.09 |
| price | 1734 | 1736 | 2.647 | 59.27 | 7.295 | 14.17 |
| close | 1734 | 1736 | 2.647 | 59.27 | 7.295 | 14.17 |
| ohlc4 | 1734 | 1736 | 2.64 | 59.32 | 7.152 | 14.11 |

---

## 6. Regime Stability Analysis

| regime | mean_performance | window_std | cv | regime_stability_score |
| :--- | :--- | :--- | :--- | :--- |
| New York Session | -0.000196 | 0.001075 | 5.484 | 77.54 |
| Session Overlap | -0.000429 | 0.001579 | 3.679 | 70.15 |
| Asian Session | -0.001075 | 0.001832 | 1.704 | 66.95 |
| Bad Execution | -0.000556 | 0.001902 | 3.423 | 66.12 |
| Good Execution | 0.002236 | 0.00293 | 1.31 | 55.88 |
| Trend (High Trend Strength) | -9.9e-05 | 0.003101 | 31.23 | 54.47 |
| Low Volatility (Contracting) | 0.000399 | 0.003162 | 7.933 | 53.99 |
| High Volatility (Expanding) | 0.000551 | 0.003268 | 5.928 | 53.18 |
| Range (Low Trend Strength) | 0.000873 | 0.003406 | 3.902 | 52.14 |
| EMA Bear Stack | 0.001249 | 0.003884 | 3.11 | 48.86 |
| EMA Bull Stack | 0.000148 | 0.003896 | 26.27 | 48.78 |
| London Session | 0.001389 | 0.004139 | 2.981 | 47.27 |
