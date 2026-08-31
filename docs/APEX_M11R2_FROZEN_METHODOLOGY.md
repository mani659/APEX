# APEX M11-R2 FROZEN METHODOLOGY

This document serves as the absolute, ex-ante frozen methodological basis for the APEX M13 Economic Experiment, superseding the original M11.

## 1. Scientific Objective
Determine whether the duration (persistence) of endogenous variance expansion (`HIGH_VOL`) is structurally conditioned by the `ASIA_TO_LONDON` institutional liquidity transition.

## 2. Metrics & Thresholds
- **Base Metric**: RV20 (20-period standard deviation of log returns on EURUSD M15).
- **HIGH_VOL Threshold**: The rolling 80th percentile of RV20, calculated over the trailing 252 trading days ending at `t-1`.
- **Baseline Reset Threshold**: The rolling 50th percentile (median) of RV20, similarly calculated.

## 3. Episode Construction (Regime Reset Rule)
- **Onset**: Bar `t` where RV20 crosses above the 80th percentile threshold, provided the regime is currently "Reset."
- **Termination**: Bar where RV20 crosses back below the 80th percentile.
- **Reset**: The system is blocked from triggering a new episode until RV20 crosses below the 50th percentile threshold.

## 4. Cohort Classification
- **Exposure Cohort**: Episodes whose onset bar falls exactly within `07:00-09:00 UTC` (`ASIA_TO_LONDON`).
- **Control Cohort**: Episodes whose onset bar falls exactly within `20:00-06:00 UTC` (Off-peak).

## 5. Statistical Framework
- **Primary Endpoint**: Persistence (Duration in contiguous M15 bars).
- **Test**: Kaplan-Meier survival analysis with a Log-rank test.
- **Falsification Criteria**: The hypothesis is supported ONLY IF the Log-rank test yields `p < 0.05` AND the 95% Confidence Interval for the difference in median survival time excludes zero. No arbitrary bar thresholds apply.

## 6. Known Limitations
- Fixed UTC session boundaries will drift slightly during mismatched DST weeks.
- The 252-day trailing calculation requires dropping the first year of canonical data as a warm-up period.
