# APEX M39 RESULT

**Milestone:** M39
**Date:** 2026-08-24
**Status:** COMPLETE

## Research Question

Does the validated RC013 LONDON_NY_OVERLAP session state produce a statistically distinct cumulative distribution function of 1-hour forward returns relative to non-overlap periods?

## Session Definition

- **LONDON_NY_OVERLAP** using `Europe/London` and `America/New_York`
- DST handling: pytz automatic

## Primary Horizon

60 minutes

## Forward-Return Definition

```
r = (Close[T+60min] - Close[T]) / Close[T]
```

## Primary Exclusions

Sat/Sun, Dec 25-Jan 1, Good Friday, Thanksgiving, NFP (first Friday)
FOMC/ECB: robustness-only per M38 (NOT applied to primary test)

## Control Definition

Non-LNO observations where forward window [T, T+60min] does not overlap any LNO interval (time-based logic, M38 frozen)

## Transition Sample

2,757 observations

## Control Sample

29,184 observations

## Observed Anderson-Darling Statistic

228.382562

## AD Implementation

`scipy.stats.anderson_ksamp` (two-sample)

## Primary Significance Result

Significance level: 0.001000
Reject H0 at alpha=0.05: True

## Bootstrap

- Block size: 24
- Block boundaries: Day (00:00 UTC)
- Replications: 10,000
- Seed: 42
- RNG: PCG-64
- Exceedance count: 5,445
- Bootstrap p-value: 0.544500

## Primary Decision

**DISTRIBUTIONAL ASYMMETRY / DIFFERENCE ESTABLISHED**

## Scientific Interpretation

## What M39 Establishes

- Whether the LONDON_NY_OVERLAP session state produces a statistically distinct CDF of 1-hour forward returns
- A clean, pre-declared, non-parametric comparison

## What M39 Does NOT Establish

- Direction, predictability, profitability, strategy edge, economic expectancy, causality, tradability

## Methodology Integrity

All checks: PASS

## Methodology Deviations

None.

## Limitations

1. FOMC and ECB exclusions not applied (robustness-only per M38)
2. Bootstrap seed = 42 (reproducible but seed-dependent)

## M40 Recommendation

Proceed to M40 if control session authorizes.

---

## Summary Statistics

| Metric | Value |
|---|---|
| External API calls | 0 |
| New data acquired | 0 |
| Spend | $0.00 |
| Repository files changed | 3 (CSV, MD, JSON) |

## Session State

**M39: COMPLETE - M40 PLANNED / NOT STARTED**
