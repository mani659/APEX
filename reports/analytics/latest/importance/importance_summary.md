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


