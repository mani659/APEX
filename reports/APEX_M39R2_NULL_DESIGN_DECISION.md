# APEX M39-R2: Null Design Decision

**Milestone:** M39-R2 (Methodology/Control Review)
**Date:** 2026-08-24
**Status:** COMPLETE

---

## Decision

> **VALID NULL — REFREEZE REQUIRED**

A mathematically defensible null exists. It must be formally frozen before execution.

---

## Selected Null Construction

**Day-block permutation test with random label assignment.**

### Formal Name

Stratified block permutation test (strata = trading days)

### Procedure

1. **Pool** all eligible forward returns (LNO + control) into a single array
2. **Assign day labels** to each observation (trading day index)
3. **Partition** into day-boundary blocks: each trading day is one block
4. **For each permutation replicate** (b = 1 to 10,000):
   a. **Resample** D day-blocks with replacement (D = number of unique trading days)
   b. **Concatenate** resampled blocks into a single pool of observations
   c. **Randomly assign** exactly N_LNO = 2,757 labels as LNO from the pool
   d. **Assign** the remaining observations as CTRL
   e. **Compute** AD statistic: `D_null[b] = anderson_ksamp([lno_perm, ctrl_perm]).statistic`
5. **Compute** permutation p-value: `p = (1 + #{D_null ≥ D_obs}) / (1 + N_rep)`

### Why This Is Correct

Under H₀ (F_LNO = F_CTRL):
- All observations are exchangeable within day-blocks
- Random label assignment produces AD statistics from the null distribution
- Day-blocks preserve within-day serial correlation
- The AD statistic under random assignment has expectation near zero (no distributional difference)

The key distinction:

| Property | What It Means | How the Correct Null Handles It |
|---|---|---|
| **Preserving dependence** | Adjacent hourly returns remain correlated | Day-blocks keep observations in temporal positions; only labels change |
| **Preserving treatment effect** | LNO maintains association with 13:00–16:30 UTC | **DESTROYED** by random label assignment |

The incorrect M39 bootstrap preserved BOTH (correct for dependence, incorrect for treatment). The corrected test preserves dependence while destroying the treatment association.

---

## Frozen Parameters

| Parameter | Value | Source | Outcome-Dependent? |
|---|---|---|---|
| Null hypothesis | F_LNO(r) = F_CONTROL(r) for all r | M36 frozen | No |
| Exchangeability unit | Trading day (day-boundary block) | M39-R2 frozen | No |
| Block size | 24 hourly observations | M38 frozen | No |
| Block boundaries | Day (00:00 UTC) | M38 frozen | No |
| Resampling method | Block permutation (resample days with replacement) | M38/M39-R2 frozen | No |
| Label assignment | Random within pooled resampled observations | M39-R2 frozen | No |
| Group-size preservation | N_LNO = 2,757; N_CTRL = 29,184 | M39 frozen | No |
| Time-of-day conditioning | Unconditional (time-of-day IS the treatment) | M36 §14 frozen | No |
| AD statistic | `scipy.stats.anderson_ksamp` (two-sample) | M38 frozen | No |
| Replications | 10,000 | M38 frozen | No |
| Seed | 42 | M38 frozen | No |
| RNG | PCG-64 (`numpy.random.default_rng(42)`) | M38 frozen | No |
| Empirical p-value | (1 + #{D ≥ D_obs}) / (1 + N_rep) | M39-R2 frozen | No |
| Alpha | 0.05 two-sided | M36 frozen | No |
| SciPy significance_level role | Secondary diagnostic only | M39-R2 frozen | No |

---

## What Changed from M38/M39

| Component | M38/M39 | M39-R2 Corrected | Reason |
|---|---|---|---|
| Null construction | Bootstrap with preserved labels (INVALID) | Permutation with random labels (VALID) | Preserved labels did not simulate H₀ |
| Label assignment | "Split back using same session-state labels" | Randomly assign N_LNO labels from pooled observations | Must destroy treatment association under H₀ |
| Procedure name | "Block bootstrap" | "Day-block permutation test" | Mathematically accurate terminology |
| SciPy role | Primary decision criterion (ambiguous) | Secondary diagnostic only | Discretized bounded output; simulation-based null is primary |
| P-value formula | fraction ≥ observed | (1 + count) / (1 + N_rep) | Standard permutation test with see-included correction |

---

## What Did NOT Change

| Component | Value | Source |
|---|---|---|
| Research question | Session-transition CDF asymmetry | M36 frozen |
| Session definition | LONDON_NY_OVERLAP (RC013) | M36 frozen |
| Control population | Non-LNO, forward window non-overlapping | M36 frozen |
| Forward horizon | 60 minutes | M36 frozen |
| Forward return formula | (Close[T+60min] - Close[T]) / Close[T] | M36 frozen |
| Calendar exclusions | Sat/Sun, Dec 25–Jan 1, Good Friday, Thanksgiving, NFP | M36/M38 frozen |
| FOMC/ECB | Robustness-only (not primary) | M38 amended |
| AD test | `scipy.stats.anderson_ksamp` | M38 frozen |
| Overlap exclusion | Time-based interval; strict inequality | M38 frozen |
| Block length | 24 | M38 frozen |
| Block boundaries | Day (00:00 UTC) | M38 frozen |
| Replications | 10,000 | M38 frozen |
| Seed | 42 | M38 frozen |
| RNG | PCG-64 | M38 frozen |
| Alpha | 0.05 two-sided | M36 frozen |

---

## Inference Hierarchy (Frozen)

> **The permutation p-value is the primary decision criterion.**
> **SciPy significance_level is a secondary diagnostic.**
> **Reject H₀ if permutation p < 0.05.**

---

## M40 Status

> **M40 NOT AUTHORIZED**

M40 cannot proceed until:
1. The corrected permutation test is executed in a controlled milestone (M39-R2 empirical)
2. The result is validated by the control session

---

## Authorizations

| Action | Status |
|---|---|
| Execute permutation test | **NOT YET** — requires separate authorization |
| Begin M40 | **NOT AUTHORIZED** |
| Rerun M39 with old bootstrap | **NOT AUTHORIZED** |
| Acquire data | **NOT AUTHORIZED** |
| Call APIs | **NOT AUTHORIZED** |

---

## Mandatory Stop

This milestone is a methodology/control review. After this review:

- Do NOT execute the permutation test
- Do NOT calculate new p-values
- Do NOT begin M40
- Do NOT acquire data or call APIs

The next authorized action is a separate controlled milestone to execute the corrected permutation test.
