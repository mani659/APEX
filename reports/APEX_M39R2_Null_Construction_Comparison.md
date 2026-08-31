# APEX M39-R2: Statistical Null Construction Comparison

**Milestone:** M39-R2 (Methodology/Control Review)
**Date:** 2026-08-24
**Status:** COMPLETE
**Classification:** METHODOLOGY REVIEW ONLY — No empirical execution

---

## 1. Fundamental Null Question

The test is:

> H₀: F_LNO(r) = F_CONTROL(r) for all r

The control session must determine:

> **What quantity is invariant under H₀, what dependence structure must remain intact, and what operation removes only the session-transition membership association?**

### What Is Invariant Under H₀

- The pooled return distribution: all forward returns (LNO + control) are drawn from the same distribution
- Within-day dependence structure: adjacent hourly returns are serially correlated
- Day-of-week effects: if any, they apply equally to all observations on that day
- Calendar structure: excluded dates remain excluded
- Time ordering: observations maintain their chronological positions
- Group sizes: N_LNO = 2,757; N_CTRL = 29,184

### What Must Be Destroyed

- The association between session-transition membership (LNO) and the return distribution

Nothing else should be intentionally changed unless mathematically necessary.

---

## 2. Dependency Structure Analysis

The following dependence structures exist in the data:

| Dependence | Structure | Strength | Implication for Null |
|---|---|---|---|
| Hourly serial correlation | Adjacent hours within a day are correlated | Moderate (typical for FX hourly returns) | Must be preserved in null |
| Within-day clustering | All hourly returns within a day share common daily effects | Strong | Day-level blocks preserve this |
| Day-of-week | Monday vs Friday may differ | Weak-moderate | Day-block permutation preserves this |
| DST regime | Summer vs winter session timing | Structural | Day-block permutation preserves this |
| Session clustering | LNO observations cluster at 13:00–16:30 UTC | Deterministic | Treatment definition, not a confounder |

### Smallest Exchangeability Unit

The smallest unit that can be treated as exchangeable under H₀ is **a trading day**.

Within a day, the forward returns share:
- Common daily market conditions
- Common macro environment
- Serial correlation structure
- Day-of-week effects

Across days, these effects are approximately independent (the frozen block length of 24 was chosen for this reason).

**Therefore: day-boundary blocks are the correct exchangeability unit.**

---

## 3. Candidate A — Label / Permutation Null

### Concept

Pool all observations. Randomly assign N_LNO labels to N_LNO observations and N_CTRL labels to N_CTRL observations. Compute the AD statistic from the labeled groups. Repeat many times to build the null distribution.

### Evaluation

| Criterion | Assessment |
|---|---|
| Exchangeability assumption | **FAILS.** Observations are not independent (serial correlation within days). Unrestricted permutation ignores this. |
| Session membership permutable? | **PARTIALLY.** Under H₀, labels are exchangeable. But unrestricted permutation assigns LNO labels to observations at times when LNO cannot occur (e.g., 03:00 UTC). |
| Time-of-day structure | **DESTROYED.** Unrestricted permutation creates physically meaningless LNO assignments at arbitrary times. |
| Dependence preservation | **FAILS.** Individual-level permutation breaks within-day serial correlation. |
| H₀ validity | **MARGINALLY VALID.** Under strict H₀ (independent observations), this is valid. But the data violate independence. |
| Main risk | **Time-of-day confounding.** The test statistic is contaminated by the destruction of temporal structure. |

### Verdict: **REJECTED** for primary use.

Unrestricted label permutation is invalid when observations have temporal dependence and the treatment is defined by time-of-day. The dependence structure is destroyed, and the test conflates session effects with time-of-day effects.

---

## 4. Candidate B — Pooled-Block Resampling + Random Group Assignment

### Concept

1. Pool all eligible forward returns by day
2. Resample day-boundary blocks with replacement
3. Within each resampled day-block, randomly assign LNO/control labels
4. Preserve original group sizes (N_LNO = 2,757; N_CTRL = 29,184)
5. Compute the AD statistic from the labeled bootstrap sample

### Evaluation

| Criterion | Assessment |
|---|---|
| Exchangeability assumption | **VALID.** Under H₀, labels within a day-block are exchangeable. Random assignment correctly simulates this. |
| Session membership permutable? | **YES.** Under H₀, it doesn't matter which observations within a day are labeled LNO. |
| Time-of-day structure | **PRESERVED within blocks.** Day-blocks maintain the temporal ordering of observations. LNO assignments are random but the time-positions are fixed. |
| Dependence preservation | **YES.** Within-day serial correlation is preserved because the block structure is intact. |
| H₀ validity | **VALID.** Random label assignment within day-blocks correctly simulates H₀ while preserving dependence. |
| Main risk | **Minor.** Random LNO assignments may place labels at implausible times (e.g., 03:00 UTC). This adds noise but does not bias the test under H₀. |

### Why This Is Mathematically Correct

Under H₀:
- All observations are drawn from the same distribution
- The AD statistic depends only on the values and their group assignments
- Random label assignment within day-blocks produces AD statistics from the null distribution
- Day-block resampling preserves within-day dependence
- The empirical distribution of AD statistics approximates the null distribution

The key insight: **we are not permuting observations, only labels.** The observations remain at their fixed time positions. The correlation structure is preserved because the observations themselves don't move—only their group assignments change.

### Verdict: **SELECTED** as the primary null construction.

---

## 5. Candidate C — Group-Wise Bootstrap

### Concept

Independently resample from the LNO group and from the control group. Compute the AD statistic from the two resampled groups.

### Evaluation

| Criterion | Assessment |
|---|---|
| Exchangeability assumption | **NOT TESTED.** This resamples within groups, not across groups. |
| Session membership permutable? | **NO.** Group labels are preserved by construction. |
| Time-of-day structure | Partially preserved (within each group). |
| Dependence preservation | **YES** (within each group, via block resampling). |
| H₀ validity | **INVALID.** This does NOT simulate H₀. It preserves the very distributional difference being tested. |
| Main risk | **Fundamentally wrong.** The bootstrap null distribution is centered around the observed AD statistic, not around zero. Produces p-values that test sampling variability, not distributional equivalence. |

### Why This Fails

Group-wise resampling answers: *"How much does the AD statistic vary due to sampling?"*

It does NOT answer: *"Is the observed AD statistic larger than expected under H₀?"*

The two questions are fundamentally different. Group-wise bootstrap tests the wrong hypothesis.

Under H₀ with group-wise bootstrap:
- The bootstrap LNO distribution ≈ the true LNO distribution
- The bootstrap control distribution ≈ the true control distribution
- Under H₀, these are the same distribution
- But the bootstrap doesn't know this—it uses the observed (potentially different) distributions

The bootstrap null distribution is centered at the observed AD statistic (≈ 228), not at the AD statistic under H₀ (near 0).

### Verdict: **REJECTED.** Mathematically invalid for H₀ testing.

---

## 6. Candidate D — Restricted / Stratified Block Permutation

### Concept

Permute labels only within scientifically comparable strata (e.g., same day-of-week, same DST regime, same calendar eligibility state).

### Evaluation of Strata Options

| Stratum | Can labels be permuted within? | Assessment |
|---|---|---|
| Same day | YES — this is Candidate B | Selected |
| Same day-of-week | YES — but strata are too large; includes cross-day mixing | Unnecessary restriction |
| Same hour-of-day | NO — LNO and non-LNO occupy different hours; nothing to permute | Infeasible |
| Same DST regime | YES — but too coarse; doesn't address within-day dependence | Unnecessary restriction |
| Same calendar eligibility | YES — but all eligible observations share this; no restriction | No additional value |

### Is Restricted Permutation Required?

**No.** Day-level block permutation (Candidate B) already provides sufficient structure:

- Within-day dependence is preserved by the block structure
- Day-of-week effects are preserved because blocks are entire days
- DST effects are preserved because blocks are entire days
- Calendar eligibility is preserved because only eligible observations are included

Additional stratification would:
1. Reduce the permutation space unnecessarily
2. Create smaller strata with fewer observations
3. Potentially reduce the power of the test
4. Introduce additional researcher degrees of freedom (choice of strata)

### Is Restricted Permutation an Additional Researcher Degree of Freedom?

**Yes, if additional strata are introduced beyond day-blocks.** The choice of strata (day-of-week? hour-of-day? DST regime?) is a researcher degree of freedom that should not be introduced without mathematical necessity.

Day-block permutation is the **minimum sufficient restriction** that preserves all relevant dependence while allowing label exchange under H₀.

### Verdict: **ABSORBED into Candidate B.** Day-block permutation is a special case of restricted block permutation where the stratum is the trading day.

---

## 7. Formal Comparison Table

| Null construction | What it preserves | What it destroys | Exchangeability assumption | Dependence preservation | Session structure preserved? | H₀ validity | Main risk |
|---|---|---|---|---|---|---|---|
| **A: Label permutation** | Pooled return values; group sizes | Session membership; time-of-day structure; within-day dependence | FAILS (serial correlation) | FAILS (individual-level permutation) | NO (LNO assigned to arbitrary times) | MARGINALLY (requires independence) | Time-of-day confounding; dependence destruction |
| **B: Pooled-block + random labels** (SELECTED) | Pooled return values; group sizes; within-day dependence; temporal ordering; day structure | Session membership association only | VALID (labels exchangeable within day-blocks under H₀) | YES (day-blocks preserve within-day correlation) | YES (blocks are entire days) | VALID | Minor: random LNO assignments at implausible times (noise, not bias) |
| **C: Group-wise bootstrap** | Within-group distributions; group labels; dependence within groups | Sampling variability only | NOT TESTED (doesn't test H₀) | YES (within each group) | YES (within each group) | **INVALID** | **Fundamentally wrong null construction** |
| **D: Restricted/block permutation** | Same as B with additional strata restrictions | Session membership within strata | VALID (more restrictive) | YES | YES | VALID | Additional researcher degree of freedom; reduced permutation space |

---

## 8. Session-Structure Problem: Detailed Analysis

### The Problem

LONDON_NY_OVERLAP membership is determined by timestamp. Therefore:

> Can observations be freely relabeled without destroying the exact time-of-day structure that defines the treatment?

### Answer

**Under H₀, yes — but only within day-blocks.**

The treatment IS the time-of-day effect (M36 §14 explicitly states: "Time of day — This IS the research question"). Therefore:

- We do NOT need to preserve time-of-day structure within the null (it would defeat the purpose)
- We DO need to preserve within-day dependence (serial correlation)
- Day-block permutation preserves dependence while allowing label exchange

### Why Unrestricted Permutation Is Problematic

If we assign LNO labels to observations at 03:00 UTC, we create a physically meaningless assignment. However:

1. Under H₀, the AD statistic doesn't care about physical meaning — it only cares about the values
2. The values at 03:00 UTC are drawn from the same distribution as values at 14:00 UTC (under H₀)
3. Therefore, the AD statistic under random assignment is a valid draw from the null distribution

The physical implausibility adds noise but not bias. The test is still valid.

### Why Day-Block Permutation Is Preferred

Day-block permutation is preferred not because unrestricted permutation is invalid under H₀, but because:

1. It preserves within-day dependence (which affects the variance of the AD statistic)
2. It produces tighter null distributions (less noise)
3. It has more power to detect real effects
4. It is the minimum sufficient restriction that respects the data structure

---

## 9. Null Invariance Statement

### What Remains Invariant

| Quantity | Invariant? | Reason |
|---|---|---|
| Pooled return distribution | YES | Under H₀, all returns are from the same distribution |
| Within-day dependence | YES | Day-blocks preserve serial correlation |
| Time ordering | YES | Observations remain at their fixed time positions |
| Group sizes | YES | N_LNO = 2,757; N_CTRL = 29,184 are frozen |
| Calendar structure | YES | Excluded dates remain excluded |
| Day-of-week effects | YES | Day-blocks are entire days |
| DST regime | YES | Day-blocks span full days |

### What Is Destroyed

| Quantity | Destroyed? | Reason |
|---|---|---|
| Association between LNO membership and return distribution | YES | Random label assignment within day-blocks |
| Specific time-of-day → group mapping | YES | LNO labels are randomly assigned within each day |

---

## 10. Group-Size Preservation

### Decision: PRESERVE ORIGINAL GROUP SIZES

| Parameter | Value | Rationale |
|---|---|---|
| N_LNO | 2,757 | Preserved in every permutation replicate |
| N_CTRL | 29,184 | Preserved in every permutation replicate |

### Why Preserve Group Sizes?

1. **Direct test of H₀.** Preserving group sizes ensures that the AD statistic is computed from the same sample sizes as the observed statistic.
2. **Valid comparison.** The observed AD statistic is computed from groups of size 2,757 and 29,184. The null distribution should also use these sizes.
3. **Maximum power.** Preserving the original group sizes maximizes the power of the test to detect distributional differences.

### Implementation

Within each resampled day-block:
1. Count eligible observations (eligible_LNO + eligible_CTRL)
2. Randomly assign exactly N_LNO_original labels as LNO
3. Assign the remaining as CTRL
4. If the block doesn't have enough eligible observations, pool across blocks

Alternatively (simpler and equally valid):
1. Pool all eligible observations across all resampled day-blocks
2. Randomly assign exactly N_LNO_original labels as LNO from the pooled observations
3. Assign the remaining as CTRL

---

## 11. Time-of-Day Conditioning

### Question

Should H₀ compare unconditional distributions or distributions conditional on time-of-day?

### Analysis

M36 §14 states:

> "Time of day — LONDON_NY_OVERLAP occurs at a specific time of day; any time-of-day effect could confound. **This IS the research question — time-of-day effects are the structural property being tested.**"

Therefore:

- The test is NOT conditioning on time-of-day
- The test IS comparing distributions across time-of-day periods (LNO vs non-LNO)
- The null assumes these distributions are identical
- Day-block permutation correctly tests this by randomizing which time-period observations get which labels

### Why Conditioning Would Be Wrong

If we conditioned on time-of-day (e.g., only comparing LNO observations at 13:30 to non-LNO observations at 13:30), we would:

1. Destroy the treatment effect (time-of-day IS the treatment)
2. Test a different hypothesis (within-hour variation, not across-hour variation)
3. Lose the ability to detect the session-transition effect

---

## 12. Anderson-Darling Statistic

### Keep: Two-Sample Anderson-Darling Test

| Component | Value | Source |
|---|---|---|
| Statistic | Two-sample AD | `scipy.stats.anderson_ksamp` |
| Implementation | `scipy.stats.anderson_ksamp([group1, group2])` | M38 frozen |
| Treatment of ties | Handled internally by SciPy | Tied values treated as single ordered value |
| Role in null simulation | Computed for each permutation replicate | Used to build null distribution |

### Do NOT Use SciPy's `significance_level` as Primary P-Value

SciPy's `significance_level` is a discretized, bounded output (floor = 0.001, cap = 0.25). It is NOT a continuous p-value. The corrected procedure uses a simulation-based null, which produces a proper empirical p-value.

The SciPy output should be reported as a **secondary diagnostic** only.

---

## 13. SciPy Significance Output: Classification

| Classification | Status | Rationale |
|---|---|---|
| Primary inference | **NO** | Discretized, bounded, does not account for serial correlation |
| Secondary diagnostic | **YES** | Useful for comparing against simulation-based result |
| Not used | **NO** | Still informative as a sanity check |

---

## 14. Correct Empirical P-Value Definition

The corrected procedure uses a **permutation test** (not a bootstrap). The p-value is:

```
p = (1 + #{D_null ≥ D_obs}) / (1 + N_rep)
```

Where:
- D_obs = observed AD statistic (228.382562)
- D_null = AD statistics from permutation replicates
- N_rep = 10,000
- The "+1" in numerator and denominator is the standard correction for permutation tests (includes the observed statistic itself in the null distribution)

### Frozen Parameters

| Parameter | Value | Source |
|---|---|---|
| Statistic | Two-sample AD (`anderson_ksamp`) | M36 frozen |
| Null generator | Day-block permutation with random label assignment | M39-R2 frozen |
| Number of replications | 10,000 | M38 frozen |
| Seed | 42 | M38 frozen |
| RNG | PCG-64 (`numpy.random.default_rng(42)`) | M38 frozen |
| Comparison rule | D_null ≥ D_obs | Standard one-sided permutation test |
| Alpha | 0.05 | M36 frozen |
| Group sizes | N_LNO = 2,757; N_CTRL = 29,184 | M39 frozen |

---

## 15. Bootstrap vs Permutation Classification

### Terminology Decision

The corrected procedure is a **permutation test** (also called a randomization test or exact test), NOT a bootstrap.

| Term | Definition | Applicable? |
|---|---|---|
| **Permutation test** | Randomly permute labels to build null distribution | **YES — SELECTED** |
| Block permutation | Permutation with block structure | **YES — this is the specific variant** |
| Randomization test | Synonym for permutation test | YES (synonym) |
| Null bootstrap | Bootstrap under H₀ (resample from pooled null distribution) | Close, but not exactly |
| Block bootstrap | Resample blocks with replacement | Partially (resamples blocks but assigns labels) |
| Restricted permutation | Permute within strata | YES (day-blocks are the strata) |

### Formal Name

> **Stratified block permutation test** with day-level strata and random label assignment

Or more concisely:

> **Day-block permutation test**

---

## 16. Methodology Degrees-of-Freedom Audit

| Decision | Candidate | Final Rule | Why | Outcome-Dependent? |
|---|---|---|---|---|
| Null hypothesis | F_LNO = F_CTRL | F_LNO(r) = F_CONTROL(r) for all r | M36/M38 frozen | No |
| Exchangeability unit | Day-boundary block | Trading day (00:00–00:00 UTC) | Preserves within-day dependence; minimum sufficient | No |
| Resampling method | Block permutation | Resample D day-blocks with replacement from eligible pool | M38 frozen (block bootstrap = permutation with labels) | No |
| Block size | 24 | 24 hourly observations per block | M38 frozen | No |
| Block boundaries | Day (00:00 UTC) | Day boundary (00:00 UTC) | M38 frozen | No |
| Label assignment | Random within pooled resampled observations | Randomly assign N_LNO labels to resampled observations | M39-R2 frozen | No |
| Group-size preservation | Preserve N_LNO=2757, N_CTRL=29184 | Preserve original group sizes | Direct test of H₀; maximum power | No |
| Time-of-day conditioning | Unconditional | Unconditional (time-of-day IS the treatment) | M36 §14 frozen | No |
| DST handling | pytz automatic | pytz automatic (as in M39) | M37 validated | No |
| AD statistic | `scipy.stats.anderson_ksamp` | Two-sample AD via `anderson_ksamp` | M38 frozen | No |
| Replications | 10,000 | 10,000 | M38 frozen | No |
| Seed | 42 | 42 | M38 frozen | No |
| RNG | PCG-64 | PCG-64 (`numpy.random.default_rng(42)`) | M38 frozen | No |
| Empirical p-value | (1 + #{D ≥ D_obs}) / (1 + N_rep) | Standard permutation p-value | Mathematically correct | No |
| Alpha | 0.05 | 0.05 two-sided | M36 frozen | No |

**All items resolved. No material unresolved items.**

> **M39-R2 IS FREEZABLE.**

---

## 17. Key Distinction: Preserving Dependence vs. Preserving Treatment Effect

This is the central conceptual point:

| Property | What It Means | How the Correct Null Handles It |
|---|---|---|
| **Preserving dependence** | Adjacent hourly returns within a day remain correlated | Day-blocks keep observations in their temporal positions; only labels change |
| **Preserving treatment effect** | LNO observations maintain their specific association with 13:00–16:30 UTC returns | **This is what must be DESTROYED** under H₀ |

The incorrect M39 bootstrap did **both**: it preserved dependence (correct) AND preserved the treatment effect (incorrect). The corrected permutation test preserves dependence (via day-blocks) while destroying the treatment effect (via random label assignment).

**This is the precise distinction the user identified: "preserving dependence" vs. "preserving the observed treatment effect."**

---

## 18. Expected Behavior of Corrected Test

Under the corrected permutation test:

1. The null distribution of AD statistics will be centered near zero (reflecting H₀ of identical distributions)
2. The observed AD statistic of 228.38 will be far in the right tail
3. The permutation p-value will be very small (likely 0 or near 0 out of 10,000)
4. The SciPy significance output and permutation result will be **consistent** (both rejecting H₀)

This is because the AD statistic of 228.38 is so extreme (35× the 0.1% critical value) that even with dependence-corrected null distribution, the result will be highly significant.

---

## 19. Required Outputs

| File | Status |
|---|---|
| `reports/APEX_M39R2_Null_Construction_Comparison.md` | ✅ Created (this file) |
| `reports/APEX_M39R2_NULL_DESIGN_DECISION.md` | ✅ Created |
| `reports/APEX_M39R2_RESULT.md` | ✅ Created |

No empirical result files. No new data. No p-values computed.
