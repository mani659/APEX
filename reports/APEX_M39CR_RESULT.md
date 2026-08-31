# APEX M39-CR RESULT

**Milestone:** M39-CR
**Status:** COMPLETE

---

## Primary M39 Result

| Metric | Value |
|---|---|
| Transition sample | 2,757 |
| Control sample | 29,184 |
| Total | 31,941 |

## M39 Statistical Test Results

| Metric | Value |
|---|---|
| AD statistic | 228.382562 |
| SciPy significance level | 0.001 (floored; actual p < 0.001) |
| Critical value (5%) | 1.961 |

## M39 Bootstrap Results

| Metric | Value |
|---|---|
| Replications | 10,000 |
| Exceedance count | 5,445 |
| Bootstrap p-value | 0.5445 |
| Mean bootstrap AD | 230.114246 |
| Std bootstrap AD | 15.446861 |

## Frozen Inference Rule

M38 specifies two outputs without explicit hierarchy:
1. SciPy significance level decision rule (Section 3): reject if < 0.05
2. Bootstrap p-value as null-calibration mechanism (Section 1.4)

## Inference Conflict

**YES — Conflict exists.**
- SciPy rejects H₀ (significance_level = 0.001; actual p ≈ 0)
- Bootstrap fails to reject H₀ (p = 0.5445)
- The bootstrap is the frozen inference mechanism but is mathematically invalid

## Root Cause

The M38 bootstrap specification preserves group labels within resampled day-blocks (Step 6: "Split Y_bootstrap back into treatment and control using the same session-state labels"). This does NOT construct the null distribution of the AD statistic under H₀. A valid null-calibration bootstrap must randomly assign group labels after resampling.

## Sample Reconciliation

**PASS** — M39 counts (2,757 + 29,184 = 31,941) are consistent with M37 counts after applying M38 calendar exclusions (2,257 observations removed).

## Calendar Reconciliation

**PASS** — M39 applies all 5 primary exclusions (Sat/Sun, Dec 25–Jan 1, Good Friday, Thanksgiving, NFP). FOMC/ECB correctly omitted from primary (robustness-only per M38). No methodology deviation.

## M39 Classification

> **M39 INVALID — STATISTICAL INFERENCE CONFLICT**

The distributional-difference conclusion is not supported by the frozen M38 inference procedure. The bootstrap is mathematically invalid and the inference hierarchy is unspecified.

## Required Correction

1. Fix bootstrap null construction: randomly assign group labels after resampling day-blocks
2. Establish explicit inference hierarchy
3. Re-execute M39 under controlled amendment

## M40 Status

> **NOT AUTHORIZED**

M40 cannot proceed until the bootstrap is corrected and M39 is re-executed.

## External API Calls

0

## New Data Acquired

0

## Spend

$0.00

## Repository Files Changed

| File | Action |
|---|---|
| `reports/APEX_M39CR_Result_Integrity_Review.md` | CREATED |
| `reports/APEX_M39CR_Decision.md` | CREATED |
| `reports/APEX_M39CR_RESULT.md` | CREATED |
| `docs/APEX_M39_STATISTICAL_AMENDMENT.md` | CREATED |
| `docs/APEX_SESSION_HANDOFF.md` | MODIFIED |
| `docs/APEX_SESSION_STATE.json` | MODIFIED |
