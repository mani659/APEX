# Findings: Market Continuation

## Regime Metrics Overview

| regime | rows | pct_dataset | mean_return | median_return | std_return | pos_return_pct | neg_return_pct | mean_future_return | median_future_return | avg_mfe | avg_mae | avg_holding_period | good_execution_pct | bad_execution_pct | future_direction_balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
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



## Analysis Summary

Based on the required analytics outputs (Statistics, Regimes, Importance, Parameter Surfaces), we observe that periods of high directional momentum tend to cluster. Features related to trend strength show high importance scores indicating that continuation plays a significant role in price prediction.