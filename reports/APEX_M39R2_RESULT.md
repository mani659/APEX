# APEX M39-R2-EXEC RESULT

**Milestone:** M39-R2-EXEC
**Date:** 2026-08-24
**Status:** COMPLETE

## Research Question

Does the validated RC013 LONDON_NY_OVERLAP session state produce a statistically distinct cumulative distribution function of 1-hour forward returns relative to non-overlap periods, under a correctly specified null?

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

## Observed Sample

- Transition (LNO): 2,757
- Control: 29,184
- Total: 31,941

## Observed Anderson-Darling Statistic

228.382562

## AD Implementation

`scipy.stats.anderson_ksamp` (two-sample)

## Null Construction

**Day-block permutation test with random label assignment**

- Blocks: 1331 day-boundary blocks (24 hourly obs/day)
- Resampling: Blocks resampled with replacement
- Label assignment: Random assignment of 2,757 LNO labels from pooled observations
- Group sizes: N_LNO = 2,757, N_CTRL = 29,184 (frozen per permutation)

## Permutation Configuration

- Replications: 10,000
- Seed: 42
- RNG: PCG-64

## Null Distribution Diagnostics

- Mean: -0.007660
- Median: -0.310692
- Std: 1.001076
- P5: -0.948507
- P95: 1.941382
- Max: 11.973414

## Primary Result

- Exceedance count: 0 / 10,000
- **Empirical p-value: 0.000100**
- Formula: (1 + 0) / (1 + 10,000)

## SciPy Diagnostic (SECONDARY ONLY)

- Significance level: 0.001000
- NOTE: This is a discretized lower bound, not a continuous p-value

## Primary Scientific Decision

**DISTRIBUTIONAL DIFFERENCE ESTABLISHED**

## Comparison with Invalid M39

| | M39 | M39-R2-EXEC |
|---|---|---|
| Null construction | Bootstrap (preserved labels) | Permutation (random labels) |
| p-value | 0.5445 | 0.000100 |
| Status | INVALID | VALID |

## Scientific Interpretation

The corrected day-block permutation test rejects the null hypothesis (p = 0.000100 < 0.05).

LONDON_NY_OVERLAP is associated with a statistically distinct 1-hour forward-return distribution relative to the frozen control population, under a correctly specified dependence-aware null.

This establishes only distributional difference — NOT direction, profitability, tradability, or causal mechanism. Do NOT reopen RC013's rejected raw-breakout monetization.
## What M39-R2-EXEC Establishes

- Whether LONDON_NY_OVERLAP produces a statistically distinct CDF of 1-hour forward returns under a correctly specified null
- A clean, pre-declared, non-parametric comparison

## What M39-R2-EXEC Does NOT Establish

- Direction, predictability, profitability, strategy edge, economic expectancy, causality, tradability

## Methodology Integrity

All checks: PASS

## Methodology Deviations

None.

## M40 Recommendation

Proceed to M40 if control session authorizes. M39-R2-EXEC result is now the authoritative distributional asymmetry finding.

---

## Summary Statistics

| Metric | Value |
|---|---|
| External API calls | 0 |
| New data acquired | 0 |
| Spend | $0.00 |

## Session State

**M39-R2-EXEC: COMPLETE**
**M40: PLANNED / NOT STARTED — REQUIRES AUTHORIZATION**
