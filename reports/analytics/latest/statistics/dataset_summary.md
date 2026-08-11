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

