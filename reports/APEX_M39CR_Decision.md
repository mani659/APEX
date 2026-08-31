# APEX M39-CR Decision

**Milestone:** M39-CR
**Date:** 2026-08-24
**Status:** COMPLETE

---

## Decision

> **M39 INVALID — STATISTICAL INFERENCE CONFLICT**

M39's distributional-difference conclusion is **NOT supported** by the frozen M38 inference procedure.

---

## Rationale

### The Conflict

M38 established two inference outputs without an explicit hierarchy:
1. **SciPy significance level** (Section 3 decision rule): 0.001 → reject H₀
2. **Bootstrap p-value** (Section 1.4 purpose): 0.5445 → fail to reject H₀

### Root Cause

The M38 bootstrap specification is mathematically incorrect for its stated purpose.

M38 says: *"Bootstrap purpose = calibrating uncertainty of the AD statistic under the null hypothesis of identical distributions."*

The M38 bootstrap procedure (Section 4, Step 6) says: *"Split Y_bootstrap back into treatment and control using the same session-state labels."*

This preserves group labels within resampled day-blocks. It does NOT simulate H₀. A valid null-calibration bootstrap must randomly assign group labels after resampling. Without this step, the bootstrap tests day-level variation, not group-level distributional differences.

### Consequence

The bootstrap p-value of 0.5445 is the result of an incorrectly specified null construction. It cannot be used as an inference criterion. The SciPy significance level of 0.001 (which is a lower bound — the actual p-value is astronomically small) is consistent with rejecting H₀, but it does not account for serial correlation (the reason M38 specified a bootstrap in the first place).

### Classification

The inference cannot be reconciled under the frozen M38 methodology. The M39 result is **INVALID** pending a controlled statistical amendment.

---

## Required Correction

A controlled statistical amendment must:

1. **Fix the bootstrap null construction**: After resampling day-boundary blocks, randomly assign group labels to the pooled resampled observations before computing the AD statistic. This correctly simulates H₀.

2. **Establish an explicit inference hierarchy**: Specify whether the corrected bootstrap p-value or the SciPy asymptotic test is the primary decision criterion.

3. **Re-execute M39** under the corrected methodology in a controlled amendment (not silently).

---

## M40 Status

> **M40 NOT AUTHORIZED**

M40 cannot proceed until the bootstrap is corrected and M39 is re-executed under the amendment.

---

## Calendar / Sample Reconciliation

| Check | Result |
|---|---|
| Sample sizes | PASS — internally consistent with M38 exclusion rules |
| Calendar exclusions | PASS — 5/7 categories applied; FOMC/ECB correctly omitted |
| Overlap exclusion | PASS — equivalent to M38 time-based specification |
| FOMC/ECB in primary sample | NO — correctly excluded from primary (robustness-only) |
| Methodology deviations | None detected |
