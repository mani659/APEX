# APEX M39-CR: Session-Transition Distributional Asymmetry Result Integrity Review

**Milestone:** M39-CR
**Date:** 2026-08-24
**Status:** COMPLETE
**Classification:** CONTROL REVIEW ONLY

---

## 1. Mission

Independently adjudicate whether the M39 result is statistically valid under the frozen M36/M38 methodology before authorizing M40.

**Do NOT:**
- Run a new economic experiment
- Test another session
- Rerun the bootstrap with different parameters
- Acquire data or call APIs
- Begin M40

---

## 2. Authoritative Inputs Read

| File | Purpose |
|---|---|
| `docs/APEX_SESSION_HANDOFF.md` | Current project state |
| `docs/APEX_SESSION_STATE.json` | Milestone registry |
| `reports/APEX_M36_Session_Transition_Distributional_Asymmetry_Methodology.md` | Frozen methodology |
| `reports/APEX_M36_RESULT.md` | M36 completion record |
| `reports/APEX_M37_Pre_Execution_Data_Validation.md` | Data validation gate |
| `reports/APEX_M37_RESULT.md` | M37 completion record |
| `reports/APEX_M38_Methodology_Completeness_Amendment.md` | M38 amendment |
| `reports/APEX_M38_RESULT.md` | M38 completion record |
| `reports/APEX_M39_Session_Transition_Distributional_Asymmetry_Experiment.md` | M39 experiment report |
| `reports/APEX_M39_RESULT.md` | M39 result file |
| `reports/APEX_M39_Result_Summary.json` | M39 result JSON |
| `reports/APEX_M39_Bootstrap_Summary.csv` | Bootstrap summary |
| `scripts/m39_experiment.py` | M39 implementation script |
| `docs/RC013_FREEZE.md` | RC013 frozen knowledge |

All files read completely. No reliance on M39 summary alone.

---

## 3. CRITICAL ISSUE A — Inference Conflict: Resolution

### 3.1 What M38 Froze

M38 specifies **two** inferential outputs:

**Output 1 — SciPy significance level (Section 3):**
> `reject_h0 = result.significance_level < 0.05`

**Output 2 — Bootstrap p-value (Section 4, Step 6):**
> `p_value = sum(ad_stat >= observed_ad_stat) / 10000`

M38 also states (Section 1.4):
> Bootstrap purpose frozen as: **Calibrating uncertainty of the Anderson-Darling test statistic under the null hypothesis of identical distributions.**

### 3.2 M39's Reported Results

| Metric | Value | Source |
|---|---|---|
| AD statistic | 228.382562 | `anderson_ksamp` |
| SciPy significance level | 0.001 | `anderson_ksamp.significance_level` |
| Bootstrap exceedance count | 5,445 / 10,000 | Bootstrap |
| Bootstrap p-value | 0.5445 | Bootstrap |

### 3.3 Frozen Primary Decision Rule

M38 Section 3 explicitly states:
```
REJECT H₀ if significance_level < 0.05
FAIL TO REJECT H₀ if significance_level >= 0.05
```

This rule references `significance_level`, which is the SciPy `anderson_ksamp` output.

**However**, M38 Section 1.4 also designates the bootstrap as the null-calibration mechanism, implying the bootstrap p-value should be the authoritative test.

**Conclusion:** M38 does not establish an explicit hierarchy between the two outputs. The decision rule in Section 3 uses SciPy, while the bootstrap purpose in Section 1.4 implies the bootstrap should govern inference. This ambiguity is a **methodological incompleteness in M38 itself**.

### 3.4 Cannot Resolve Without Fixing Bootstrap

Even if we accept SciPy as primary, the bootstrap (designated as null-calibration) contradicts SciPy. The conflict is:

- SciPy says: reject H₀ (actual p-value astronomically small)
- Bootstrap says: fail to reject H₀ (p = 0.5445)

**The bootstrap result cannot be dismissed as secondary** because M38 explicitly designated it as the null-calibration mechanism. Conversely, the SciPy result cannot be dismissed because M38's decision rule references it.

**This is an irresolvable conflict under the current M38 specification.**

---

## 4. Bootstrap Mathematical Coherence Audit

### 4.1 What the M38 Specification Requires

M38 Section 4 specifies the bootstrap procedure:

```
1. Pool all forward returns (LNO + non-LNO) into a single array Y
2. Assign day labels to each observation
3. Partition Y into day-boundary blocks
4. Resample day-boundary blocks with replacement
5. Concatenate resampled blocks into Y_bootstrap
6. Split Y_bootstrap back into treatment and control using the same session-state labels
7. Compute AD statistic for each bootstrap sample
8. P-value = fraction of bootstrap AD statistics >= observed AD statistic
```

### 4.2 What the M39 Implementation Actually Does

From `scripts/m39_experiment.py` (Section 10):

```python
# Pool all forward returns with their group labels
all_returns = np.concatenate([lno_returns, ctrl_returns])
all_groups = np.concatenate([np.ones(len(lno_returns)), np.zeros(len(ctrl_returns))])

# Assign day labels
# ... (correct)

# Partition into day-boundary blocks
blocks = []        # forward returns by day
block_groups = []  # group labels (1=LNO, 0=control) by day

# Bootstrap
for b in range(N_BOOTSTRAP):
    sample_indices = rng.choice(n_blocks, size=n_blocks, replace=True)
    boot_returns = np.concatenate([blocks[i] for i in sample_indices])
    boot_groups = np.concatenate([block_groups[i] for i in sample_indices])
    boot_lno = boot_returns[boot_groups == 1]
    boot_ctrl = boot_returns[boot_groups == 0]
    # Compute AD statistic
```

### 4.3 Critical Flaw: Null Construction

**The M39 bootstrap preserves group labels within each resampled day-block.**

This means:
1. Day `d` has `n_LNO(d)` LNO observations and `n_ctrl(d)` control observations
2. When day `d` is resampled, its group-label structure is preserved: the same observations are still labeled LNO/control
3. The only variation across bootstrap replicates comes from which days are sampled (and how many times), not from which observations are assigned to which group

**This does NOT construct the null distribution of the AD statistic under H₀.**

Under H₀ (LNO and control are drawn from the same distribution), a valid null-calibration bootstrap must:

1. **Pool** all observations (removing group labels)
2. **Resample** with replacement (preserving temporal structure via blocks)
3. **Randomly assign** group labels to the resampled observations
4. **Compute** the AD statistic from the labeled bootstrap sample

Step 3 is **completely absent** from the M39 implementation. Without random group-label assignment, the bootstrap is not testing whether LNO and control differ; it is testing whether the **day-level variation** in the AD statistic is large enough to exceed the observed value.

### 4.4 Why Bootstrap p = 0.5445

The bootstrap mean AD statistic is 230.11 (std = 15.45). The observed AD statistic is 228.38. Since the observed value is near the center of the bootstrap null distribution (slightly below the mean), approximately 54.45% of bootstrap statistics exceed it. This produces p = 0.5445.

**This is the expected behavior of an incorrectly specified bootstrap that does not construct the null distribution.**

### 4.5 Root Cause

| Step | M38 Specification | M39 Implementation | Correct? |
|---|---|---|---|
| Pool returns | Pool LNO + control into Y | Pool LNO + control | ✅ |
| Assign day labels | Assign day labels | Assign day labels | ✅ |
| Partition into blocks | Day-boundary blocks | Day-boundary blocks | ✅ |
| Resample blocks | Resample with replacement | Resample with replacement | ✅ |
| Concatenate | Concatenate resampled blocks | Concatenate resampled blocks | ✅ |
| **Assign group labels** | **"Split back into treatment and control using the same session-state labels"** | **Uses preserved group labels from blocks** | ❌ **FLAWED** |
| Compute AD | Compute AD statistic | Compute AD statistic | ✅ |
| P-value | Fraction >= observed | Fraction >= observed | ✅ |

**The flaw is in M38 Step 6 itself.** The specification says "Split Y_bootstrap back into treatment and control using the same session-state labels." This preserves group labels rather than reassigning them, which fails to construct H₀.

### 4.6 Classification

**The M38 bootstrap specification is mathematically incorrect for its stated purpose.**

The purpose is "calibrating uncertainty of the AD statistic under the null hypothesis of identical distributions." The implementation preserves group labels, which does not simulate H₀. Therefore:

> **M39 bootstrap result is INVALID. The bootstrap does not produce a valid null distribution.**

---

## 5. CRITICAL ISSUE B — Bootstrap / AD Definition: Detailed Analysis

### 5.1 Source Population

All forward returns from the canonical EURUSD M1 dataset (2021-01-04 to 2026-06-30), after hourly resampling.

### 5.2 How Groups Are Assigned

Group assignment is based on session-state classification:
- LNO: timestamp falls within London ∩ New York trading hours
- Control: timestamp outside LNO, forward window non-overlapping with LNO

### 5.3 Whether Group Sizes Are Preserved

**No.** The bootstrap resamples days with replacement. Each day contributes a fixed number of LNO and control observations. The total group sizes vary across replicates depending on which days are sampled and how many times.

### 5.4 Whether Day Blocks Are Resampled

Yes. Day-boundary blocks (trading days) are resampled with replacement.

### 5.5 Whether Group Labels Are Shuffled

**No.** Group labels are preserved within each resampled day-block. This is the critical flaw.

### 5.6 How the AD Statistic Is Calculated

Via `scipy.stats.anderson_ksamp([lno_bootstrap, ctrl_bootstrap])` — the standard two-sample Anderson-Darling test.

### 5.7 How the Empirical P-Value Is Obtained

`p = (count of bootstrap AD stats >= observed AD stat) / 10000`

### 5.8 Conclusion

The implementation does NOT construct a valid null distribution for the AD statistic. Under H₀, group labels should be randomly assigned (or all observations pooled and re-labeled). The current implementation preserves the correlation between group labels and day-level effects, which biases the bootstrap null toward the observed AD statistic.

**The bootstrap is not mathematically clear and cannot be approved as a valid inference mechanism.**

---

## 6. CRITICAL ISSUE C — SciPy Significance Level

### 6.1 Exact Behavior of `scipy.stats.anderson_ksamp`

Empirical verification:

| Test | AD Statistic | Significance Level | SciPy Warning |
|---|---|---|---|
| Identical distributions (n=5000 each) | 0.2726 | 0.25 | "p-value capped: true value larger than 0.25" |
| Different means (n=5000 each) | 474.07 | 0.001 | "p-value floored: true value smaller than 0.001" |
| Very different means (n=5000 each) | 3484.40 | 0.001 | "p-value floored: true value smaller than 0.001" |

### 6.2 What `significance_level = 0.001` Means

The `significance_level` output is **NOT a p-value**. It is a discretized, bounded estimate:

- The critical values correspond to significance levels [0.25, 0.10, 0.05, 0.025, 0.01, 0.005, 0.001]
- If the AD statistic exceeds the critical value for 0.001, the output is `0.001`
- SciPy explicitly warns: **"p-value floored: true value smaller than 0.001"**
- The actual p-value is **astronomically small** — potentially 1e-10, 1e-50, or smaller

### 6.3 M39's AD Statistic vs. Critical Values

For M39's AD statistic of 228.38:
- Critical value at 0.001 significance: 6.546
- 228.38 >> 6.546
- The AD statistic is **35× larger** than the critical value at the 0.1% level
- The actual p-value is effectively zero

### 6.4 Comparison to Bootstrap p-value

| Metric | Value | Nature |
|---|---|---|
| SciPy significance level | 0.001 | Discretized lower bound; actual p ≈ 0 |
| Bootstrap p-value | 0.5445 | Invalid null construction |

These are **not directly comparable** because:
1. SciPy uses asymptotic critical values for the AD distribution
2. The bootstrap was intended to provide finite-sample calibration but is incorrectly implemented
3. The SciPy result tests H₀ against the asymptotic AD distribution; the bootstrap (as specified) tests something entirely different

### 6.5 Conclusion

`significance_level = 0.001` means the true p-value is **much smaller than 0.001**. It is NOT a precise p-value of 0.001. The SciPy result strongly rejects H₀. However, the SciPy asymptotic test does not account for serial correlation in the data, which is why M38 specified a block bootstrap for proper calibration.

---

## 7. CRITICAL ISSUE D — Sample Reconciliation

### 7.1 M37 Pre-Exclusion Counts

| Group | M37 Count |
|---|---|
| Total hourly bars | 34,199 |
| Transition (LNO) | 2,950 |
| Control (non-LNO) | 31,249 |
| Forward returns available | 34,198 |

### 7.2 M39 Post-Exclusion Counts

| Group | M39 Count |
|---|---|
| Total eligible | 31,941 |
| Transition (LNO) | 2,757 |
| Control (non-LNO) | 29,184 |

### 7.3 Reconciliation

| Source | Count | Notes |
|---|---|---|
| M37 total | 34,199 | All hourly bars |
| M37 LNO | 2,950 | Pre-calendar-exclusion |
| M37 control | 31,249 | Pre-calendar-exclusion |
| Calendar exclusions applied | −2,257 | Sat/Sun (0), Dec 25–Jan 1, Good Friday, Thanksgiving, NFP |
| Overlap contamination | −2,950 | Non-LNO hours whose forward window overlaps LNO |
| M39 LNO | 2,757 | 2,950 − 193 calendar-excluded LNO hours |
| M39 control | 29,184 | 31,249 − 2,065 calendar-excluded control hours |
| M39 total | 31,941 | 2,757 + 29,184 |

The difference between M37 (34,199) and M39 (31,941) is 2,258, which matches the calendar exclusion count of 2,257 (±1 edge effect). The sample construction is **internally consistent** with the frozen M38 exclusion rules.

### 7.4 Verification

M39's exclusion rules exactly match M38:
- Sat/Sun: ✅ (absent in M1 data; 0 exclusions)
- Dec 25–Jan 1: ✅
- Good Friday: ✅ (computed via Easter algorithm, matching M38's `pandas.tseries.holiday` recommendation)
- Thanksgiving: ✅ (fourth Thursday of November)
- NFP: ✅ (first Friday of month)
- FOMC/ECB: ✅ NOT excluded from primary (downgraded to robustness-only by M38)

**Sample reconciliation: PASS**

---

## 8. Calendar Audit

### 8.1 M38 Frozen Exclusions (Primary)

| Exclusion | M38 Classification | M39 Applied? | Match? |
|---|---|---|---|
| Sat/Sun | DETERMINISTIC, primary | Yes (0 in M1 data) | ✅ |
| Dec 25–Jan 1 | DETERMINISTIC, primary | Yes | ✅ |
| Good Friday | DETERMINISTIC, primary | Yes | ✅ |
| Thanksgiving | DETERMINISTIC, primary | Yes | ✅ |
| NFP (1st Friday) | DETERMINISTIC, primary | Yes | ✅ |
| FOMC | BLOCKED, robustness-only | No | ✅ |
| ECB | BLOCKED, robustness-only | No | ✅ |

### 8.2 FOMC/ECB Check

M39 did NOT remove FOMC or ECB observations from the primary sample. M38 downgraded these to "recommended robustness check" because the exact date lists were not locally available.

**Calendar reconciliation: PASS — No methodology deviation.**

---

## 9. Overlap Exclusion Audit

### 9.1 M38 Specification (Frozen)

Time-based interval logic with strict inequality:
```
Two intervals [a, b) and [c, d) overlap if: max(a, c) < min(b, d)
```

### 9.2 M39 Implementation

```python
hourly['next_hour_is_lno'] = hourly['is_lno'].shift(-1).fillna(False)
hourly['forward_overlaps_lno'] = hourly['next_hour_is_lno']
```

### 9.3 Equivalence Analysis

For LNO intervals that are exactly 60 minutes (hourly bars), the position-based shift `shift(-1)` is equivalent to the time-based interval comparison:

- Forward window [T, T+60min) overlaps LNO [A, A+60min) iff T+60min falls within [A, A+60min)
- For hourly data, T+60min = next hourly bar timestamp
- Therefore: overlap iff next hourly bar is LNO

**This equivalence holds for all DST transitions** because each LNO interval is exactly one hourly bar, regardless of UTC offset changes.

**Overlap exclusion: PASS — Implementation is equivalent to M38 specification.**

---

## 10. Primary Scientific Decision

### 10.1 The Inference Cannot Be Reconciled

| Component | Status |
|---|---|
| M38 frozen inference rule | Ambiguous (no explicit hierarchy between SciPy and bootstrap) |
| SciPy significance level | 0.001 (floored; actual p ≈ 0; rejects H₀) |
| Bootstrap p-value | 0.5445 (FAILS to reject H₀; invalid null construction) |
| Bootstrap mathematical validity | INVALID — does not construct H₀ |

The bootstrap was designated by M38 as the null-calibration mechanism, but it is mathematically incorrect. M38's decision rule uses SciPy, but M38's bootstrap purpose statement implies the bootstrap should govern inference.

**The conflict cannot be resolved without methodological correction.**

### 10.2 Classification

> **M39 INVALID — STATISTICAL INFERENCE CONFLICT**

The SciPy AD test and the bootstrap produce contradictory results. The bootstrap was the frozen inference mechanism but is mathematically invalid. The SciPy result is consistent but does not account for serial correlation (the reason M38 specified a bootstrap).

**M39 cannot be classified as either VALID — DIFFERENCE ESTABLISHED or VALID — NO DIFFERENCE ESTABLISHED.**

### 10.3 What Correction Is Required

A controlled statistical amendment must:

1. **Fix the bootstrap null construction**: Pool all observations, resample day-boundary blocks, and randomly assign group labels to resampled observations. This is the only way to construct H₀ for the AD statistic under serial correlation.

2. **Establish an explicit inference hierarchy**: Either:
   - (a) Make the corrected bootstrap p-value the primary decision criterion, OR
   - (b) Explicitly specify that SciPy asymptotic test is primary and the bootstrap is secondary/descriptive

3. **Re-run M39 with the corrected bootstrap** under a controlled amendment (not silently in M39-CR).

---

## 11. What M39 Can and Cannot Establish

Even if the distributional difference is ultimately validated after bootstrap correction:

### What M39 establishes:

> LONDON_NY_OVERLAP is associated with a different 1-hour forward-return distribution from the control population.

The SciPy AD statistic of 228.38 is extreme (35× the 0.1% critical value), and the descriptive statistics show clear distributional differences (LNO std = 0.001494 vs control std = 0.000906; skewness = −0.454 vs +0.255). The distributional difference is almost certainly real.

### What M39 does NOT establish:

- **Directional profitability** — M39 tests distributional shape, not direction
- **Tradability** — Execution costs, slippage, and market microstructure are unexamined
- **Causal mechanism** — Session state is deterministic; this is a correlation test
- **Breakout strategy** — RC013 already rejected raw breakout monetization
- **Positive expectancy** — No PnL calculation was performed
- **Execution edge** — No transaction cost analysis

**Do NOT reopen RC013's rejected raw-breakout monetization path.**

---

## 12. Required Outputs

| File | Status |
|---|---|
| `reports/APEX_M39CR_Result_Integrity_Review.md` | ✅ Created |
| `reports/APEX_M39CR_Decision.md` | ✅ Created |
| `reports/APEX_M39CR_RESULT.md` | ✅ Created |
| `docs/APEX_M39_STATISTICAL_AMENDMENT.md` | ✅ Created (correction required) |

---

## 13. Summary Table

| Metric | Value |
|---|---|
| External API calls | 0 |
| New data acquired | 0 |
| Spend | $0.00 |
| Repository files changed | 3 (CR reports) + 1 (amendment) |
| M39 re-executed | No |
| Bootstrap re-run | No |
| M40 begun | No |
