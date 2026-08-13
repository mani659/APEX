# RC007 Study 007: Corrected Entry Isolation Report

## Decision Funnel

| Stage | Count |
|---|---:|
| Total M1 bars | 2041613 |
| Behavioral Events | 5235 |
| LOW_PARTICIPATION | 482 |
| HIGH_PARTICIPATION | 4753 |
| WAIT | 482 |
| REJECT_HIGH_ENTROPY | 4753 |
| REJECT_TIMEOUT | 0 |
| REJECT_PERMISSION | 72 |
| EXECUTE | 410 |
| EXIT / OBSERVATION COMPLETE | 410 |

## Entry Frequency
- Total behavioural events: 5235
- Qualified events (passed participation): 482
- Executed entries: 410
- Execution conversion rate: 7.83%

## MAE
- Mean: 0.00132
- Median: 0.00109
- Standard deviation: 0.00108
- 90th percentile: 0.00240
- 95th percentile: 0.00305
- Maximum: 0.01080

## MFE
- Mean: 0.00059
- Median: 0.00028
- Standard deviation: 0.00089
- 90th percentile: 0.00143
- 95th percentile: 0.00203
- Maximum: 0.01014

## Timing
- Mean bars to MAE: 120.0
- Median bars to MAE: 120.0
- Mean bars to MFE: 120.0
- Median bars to MFE: 120.0
- Mean holding duration: 240.0

## Outcome Distribution
- Total observations: 410
- Mean PnL: -0.00048
- Median PnL: -0.00043
- Win Rate (positive PnL at 240 bars): 35.1%

## Comparison Against Invalidated Study 004
### Study 004
Study 004 was invalidated because of engineering defects, specifically hardcoded volume data which led to a mechanical 100% rejection rate at the entropy layer. It yielded 0 executions.

### Study 007
The corrected engineering foundation restores real volume data and fixes the candle body stabilization calculations. As a result, the engine processed actual volume percentiles and successfully yielded 410 executions. This represents the true baseline.

## Scientific Interpretation
1. **How many behavioural events actually survive the frozen Participation and Stabilization rules?**
Out of 5235 events, 410 survived all frozen rules.

2. **Does the corrected engine now produce executable entries?**
Yes, the corrected engineering framework successfully yields executions (410 total).

3. **What is the raw MAE/MFE fingerprint of those entries?**
The raw fingerprint shows a mean MFE of 0.00059 against a mean MAE of 0.00132.

4. **Is there measurable standalone behavioural asymmetry?**
No, MFE and MAE are relatively symmetric or adverse-skewed.

5. **Does the evidence support or reject intrinsic entry alpha?**
**NOT SUPPORTED**

# Final Verdict

**NOT SUPPORTED**
