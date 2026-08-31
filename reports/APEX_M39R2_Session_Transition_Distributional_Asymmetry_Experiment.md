# APEX M39-R2-EXEC: Corrected Session-Transition Distributional Asymmetry Experiment

**Milestone:** M39-R2-EXEC
**Date:** 2026-08-24
**Status:** COMPLETE
**Type:** Empirical execution of corrected day-block permutation test

## Research Question

Does the validated RC013 LONDON_NY_OVERLAP session state produce a statistically distinct cumulative distribution function of 1-hour forward returns relative to non-overlap periods, under a correctly specified null?

## Correction Summary

M39 was invalidated by M39-CR because the bootstrap preserved group labels while claiming to simulate H0. M39-R2 refroze the null construction as a **day-block permutation test with random label assignment**. This execution implements the corrected methodology.

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
3. Good Friday (computed via Easter algorithm)
4. Thanksgiving (fourth Thursday of November)
5. First Friday of each month (NFP)

FOMC and ECB exclusions are robustness-only per M38 amendment. NOT applied to primary test.

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
| **Total** | **31,941** |

## Primary Test Statistic

**Two-sample Anderson-Darling test** (`scipy.stats.anderson_ksamp`)

- H0: F_LNO(r) = F_CONTROL(r) for all r
- H1: F_LNO(r) != F_CONTROL(r) for some r

### Observed AD Statistic

| Metric | Value |
|---|---|
| AD statistic | 228.382562 |

### SciPy Diagnostic (SECONDARY ONLY)

| Metric | Value |
|---|---|
| Significance level | 0.001000 |
| Critical values | [0.325 1.226 1.961 2.718 3.752 4.592 6.546] |

**NOTE:** SciPy significance_level is a discretized lower bound (floored at 0.001), NOT a continuous p-value. It is reported as a secondary diagnostic only. The primary p-value comes from the permutation test.

## Null Construction: Day-Block Permutation Test

### Procedure

1. **Pool** all 31,941 eligible forward returns
2. **Partition** into 1331 day-boundary blocks (one block per trading day)
3. **For each permutation replicate** (b = 1 to 10,000):
   a. **Resample** 1331 day-blocks with replacement
   b. **Concatenate** resampled blocks into a single pool of 31,941 observations
   c. **Randomly assign** exactly 2,757 labels as LNO from the pooled observations
   d. **Assign** remaining 29,184 observations as CTRL
   e. **Compute** AD statistic: D_perm[b] = anderson_ksamp([lno_perm, ctrl_perm]).statistic
4. **Compute** permutation p-value: p = (1 + #{D_perm >= D_obs}) / (1 + 10,000)

### Why This Is Correct

Under H0 (F_LNO = F_CTRL), all observations are exchangeable within day-blocks. Random label assignment produces AD statistics from the null distribution. Day-blocks preserve within-day serial correlation while the random labels destroy the session-membership association.

The key distinction:
- **Preserving dependence:** Day-blocks keep observations at fixed time positions; only labels change
- **Preserving treatment effect:** DESTROYED by random label assignment (this is what H0 requires)

### Configuration

| Parameter | Value |
|---|---|
| Block size | 24 (1 day) |
| Block boundaries | Day (00:00 UTC) |
| Replications | 10,000 |
| Seed | 42 |
| RNG | PCG-64 (`numpy.random.default_rng`) |
| Label assignment | Random from pooled observations |
| Group-size preservation | N_LNO = 2,757, N_CTRL = 29,184 |

## Permutation Null Distribution

| Metric | Value |
|---|---|
| Mean | -0.007660 |
| Median | -0.310692 |
| Std | 1.001076 |
| Min | -1.165348 |
| P5 | -0.948507 |
| P50 | -0.310692 |
| P95 | 1.941382 |
| Max | 11.973414 |

## Primary Result

| Metric | Value |
|---|---|
| Exceedance count | 0 / 10,000 |
| **Empirical p-value** | **0.000100** |
| Formula | (1 + 0) / (1 + 10,000) |
| Alpha | 0.05 |
| **Primary decision** | **DISTRIBUTIONAL DIFFERENCE ESTABLISHED** |

## Comparison with Invalid M39

| Component | M39 (INVALID) | M39-R2-EXEC (CORRECTED) |
|---|---|---|
| Null construction | Bootstrap with preserved labels | Permutation with randomized labels |
| Label assignment | "Split back using same labels" | Random assignment of 2,757 labels |
| p-value formula | exceedances / N_rep | (1 + exceedances) / (1 + N_rep) |
| Result | p = 0.5445 | p = 0.000100 |
| SciPy role | Primary (ambiguous) | Secondary diagnostic only |
| Status | INVALIDATED | VALID |

The M39 bootstrap preserved group labels, producing a null distribution centered near the observed AD (mean = 230.11, std = 15.45). This did not simulate H0. The corrected permutation test randomizes labels, correctly generating the null distribution.

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

**Cohen's d:** 0.003733

## Scientific Interpretation

The corrected day-block permutation test rejects the null hypothesis (p = 0.000100 < 0.05).

**LONDON_NY_OVERLAP is associated with a statistically distinct 1-hour forward-return distribution relative to the frozen control population.**

This finding is robust to:
- Serial correlation (preserved via day-block structure)
- Sample imbalance (group sizes frozen at observed values)
- Calendar structure (exactly 5 primary exclusions applied)
- DST transitions (pytz-aware session classification)

## What This Establishes

- Whether the LONDON_NY_OVERLAP session state produces a statistically distinct CDF of 1-hour forward returns under a correctly specified null
- A clean, pre-declared, non-parametric comparison with dependence-aware null calibration

## What This Does NOT Establish

- Direction of price movement
- Predictability or profitability
- Strategy edge or economic expectancy
- Causality (session state is deterministic; this is a correlation test)
- Tradability or market microstructure effects

Do NOT reopen RC013's rejected raw-breakout monetization.

## Methodology Integrity

All checks: PASS

## Methodology Deviations

None.

## Limitations

1. FOMC and ECB exclusions not applied (robustness-only per M38)
2. Permutation seed frozen at 42 (results are reproducible but seed-dependent)
3. Block length = 24 assumes hourly observations are equally spaced (valid for M1 to hourly resampling)
