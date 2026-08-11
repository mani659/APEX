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
