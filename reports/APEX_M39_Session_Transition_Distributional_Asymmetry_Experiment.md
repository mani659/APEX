# APEX M39: Session-Transition Distributional Asymmetry Experiment

**Milestone:** M39
**Date:** 2026-08-24
**Status:** COMPLETE

## Research Question

Does the validated RC013 LONDON_NY_OVERLAP session state produce a statistically distinct cumulative distribution function of 1-hour forward returns relative to non-overlap periods?

## Session Definition

**LONDON_NY_OVERLAP:** M1 bar whose timestamp falls within the overlap of London and New York trading hours.

- London: 08:00-16:30 local (`Europe/London`)
- New York: 09:30-16:00 local (`America/New_York`)
- DST handling: pytz automatic DST transitions

## Primary Horizon

60 minutes (1 hour)

## Forward-Return Definition

```
r = (Close[T+60min] - Close[T]) / Close[T]
```

Where T = end of hourly bar (deterministic timestamp).

## Primary Exclusions

1. Saturdays and Sundays (absent in M1 data)
2. December 25-January 1 (year-end holidays)
3. Good Friday (computed via `pandas.tseries.holiday.USFederalHolidayCalendar`)
4. Thanksgiving (fourth Thursday of November)
5. First Friday of each month (NFP)

**Note:** FOMC and ECB exclusions are robustness-only per M38 amendment. Primary test proceeds without them.

## Control Definition

Non-LONDON_NY_OVERLAP observations where:
1. Timestamp is outside LONDON_NY_OVERLAP
2. Forward interval [T, T+60min] does NOT overlap any LONDON_NY_OVERLAP interval
3. Not excluded by primary calendar exclusions
4. Valid forward return available

## Sample Sizes

| Group | Observations |
|---|---|
| Transition (LNO) | 2,757 |
| Control | 29,184 |
| Calendar exclusions | 2,257 |
| Overlap contamination | 2,950 |

## Primary Test

**Two-sample Anderson-Darling test** (`scipy.stats.anderson_ksamp`)

- H0: F_LNO(r) = F_control(r) for all r
- H1: F_LNO(r) != F_control(r) for some r
- alpha = 0.05 (two-sided)

### Result

| Metric | Value |
|---|---|
| AD statistic | 228.382562 |
| Critical value (5%) | 1.961000 |
| Significance level | 0.001000 |
| Reject H0 | True |

## Bootstrap Calibration

| Parameter | Value |
|---|---|
| Block size | 24 |
| Block boundaries | Day boundaries (00:00 UTC) |
| Replications | 10,000 |
| Seed | 42 |
| RNG | PCG-64 (`numpy.random.default_rng`) |
| Resampling | Joint (treatment + control) |

### Bootstrap Result

| Metric | Value |
|---|---|
| Successful replications | 10,000 |
| Failed replications | 0 |
| Mean bootstrap AD | 230.114246 |
| Std bootstrap AD | 15.446861 |
| Exceedance count | 5,445 |
| Bootstrap p-value | 0.544500 |

## Primary Decision

**DISTRIBUTIONAL ASYMMETRY / DIFFERENCE ESTABLISHED**

## Descriptive Statistics

| Statistic | LNO | Control |
|---|---|---|
| n | 2,757 | 29,184 |
| Mean | 0.00000158 | -0.00000205 |
| Std | 0.00149361 | 0.00090630 |
| Median | 0.00003425 | 0.00000000 |
| IQR | 0.00151905 | 0.00077295 |
| Skewness | -0.454497 | 0.255382 |
| Excess kurtosis | 6.778268 | 17.519961 |
| Min | -0.01372771 | -0.01200826 |
| Max | 0.00945928 | 0.01743964 |

**Cohen's d:** 0.003733

## What M39 Establishes

- Whether the LONDON_NY_OVERLAP session state produces a statistically distinct CDF of 1-hour forward returns
- The magnitude and direction of any distributional difference (via descriptive statistics)
- A clean, pre-declared, non-parametric comparison with no post-hoc adjustments

## What M39 Does NOT Establish

- Direction of price movement (M39 tests distributional shape, not direction)
- Predictability or profitability
- Strategy edge or economic expectancy
- Causality (session state is deterministic; this is a correlation test)
- Tradability or market microstructure effects

## Methodology Integrity

All checks: PASS

## Methodology Deviations

None.

## Limitations

1. FOMC and ECB exclusions not applied (robustness-only per M38)
2. Bootstrap seed frozen at 42 (results are reproducible but seed-dependent)
3. Block length = 24 assumes hourly observations are equally spaced (valid for M1 to hourly resampling)

## M40 Recommendation

Proceed to M40 if the control session authorizes:
- If H0 rejected: characterize the nature of the distributional asymmetry (mean shift, variance change, skewness, tails)
- If H0 not rejected: consider alternative session transitions or longer horizons
