# RC015 Study 007 - Final Futures-Midpoint Moneyness Revalidation

## 1. Exact Observation Rule Used
The frozen methodology (`scripts/rc015_study_007_volatility_pricing_discovery.py`) groups BBO observations by every 15-minute bucket (`dt.floor('15Min')`) across the entire Wednesday observation date (00:00 to 23:59 UTC). There is no single frozen hour (like 15:00 UTC) mandated for all events. Therefore, this revalidation extracts the contemporaneous futures midpoint precisely at all 96 M15 boundaries on the observation date. For each candidate option, the M15 bucket that minimizes `abs(strike_price - futures_midpoint)` is selected. The option is marked as `PASS` if this minimum distance is `<= 0.0020`.

## 2. Event Reconciliation
- Events Processed: 222
- Events with valid futures midpoint: 222
- Events with no futures midpoint: 0
- Events with >= 1 eligible Call/Put: 222
- Events with no eligible options: 0

## 3. Candidate Universe Comparison
| Universe | Unique Option IDs | Total Rows | Calls | Puts |
|---|---|---|---|---|
| Stage-1 Subset (Stale) | 530 | 18,336 | 9,168 | 9,168 |
| Repaired Candidates (Daily Close) | 707 | 708 | 354 | 354 |
| Final True-BBO Moneyness | **699** | **700** | **350** | **350** |

## 4. Data Integrity (Degraded Dates)
The dates 2024-09-18, 2025-09-17, and 2025-09-24 were flagged. Candidates on these dates have been retained but marked with `quality_flag = DEGRADED_DATE`. Futures midpoints were successfully extracted where data was present, but quote density may be lower.

## 5. Cost
Total Futures Data Cost: $0.4128

**Is the final universe ready for a minimal Option BBO request?**: YES
