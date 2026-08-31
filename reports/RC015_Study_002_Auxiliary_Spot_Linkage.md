# RC015 Study 002 — EURUSD Tick Coverage and Spot Linkage

## 1. File Discovery
- File Size: 8.74 MB
- Row Count: 205088
- First TS: 2026-08-09 21:00:17
- Last TS: 2026-08-14 20:59:59

## 2. Date Coverage
- Target 2026-08-12 ticks: 45491

## 3. Inspect Tick Feed
- Duplicates: 22702
- Chronological: True

## 7. Spot <-> Futures Synchronization
- Inferred Timezone Shift (Hours to UTC): 0
- Exact Overlap Count (Minutes): 1267
- First Common: 2026-08-12 00:00:00+00:00
- Last Common: 2026-08-12 23:56:00+00:00

## 9. Spot/Futures Basis (Futures Mid - Spot Mid)
- Mean: 0.005514
- Median: 0.005520
- StdDev: 0.000118
- Min/Max: 0.004855 / 0.006825
- P1 / P5: 0.005230 / 0.005350
- P95 / P99: 0.005650 / 0.005738

## 12. Real-Data Consistency
- Sync Futures Obs: 9602
- Sync Options Obs: 9602
- Successful IVs: 9602
- Convergence %: 100.00%
- Median Abs Residual: 0.0000000008
- Failed Inversions: 0

## 13. RC012 / RC013 Technical Synchronization
M15 aligned timestamps available: 86

## 15. Final Classification
### LINKED
EURUSD auxiliary spot, 6EZ6 futures, and EUR/USD options can be synchronized and the Black-76 IV pipeline works.
