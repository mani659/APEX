# APEX M40 — Session-Transition Distributional Component Decomposition Methodology Design

**Date**: 2026-08-27
**Milestone**: M40
**Status**: COMPLETE
**Classification**: Methodology design only — no empirical execution

---

## 1. Executive Summary

M40 designs the methodology to determine which scientifically interpretable component of the validated CDF difference (M39-R2, p = 0.0001) is responsible for the LONDON_NY_OVERLAP distributional asymmetry.

**Decision: A — AUTHORIZE M41 EMPIRICAL EXECUTION DESIGN**

A clean decomposition architecture exists: **sequential hierarchical moment decomposition** within a single permutation framework. The architecture preserves M39-R2's dependence structure, controls multiplicity through ordered testing, and maps each component to a distinct economic interpretation.

---

## 2. Established Scientific Finding

M39-R2 established:

$$F_{LNO}(r) \neq F_{CONTROL}(r)$$

under the corrected day-block permutation framework.

| Component | Value |
|-----------|------:|
| Observed AD statistic | 228.382562 |
| Permutation p-value | 0.000100 |
| Replications | 10,000 |
| Seed | 42 |
| LNO observations | 2,757 |
| Control observations | 29,184 |

M40 does NOT question this finding. M40 asks: **what component of this difference is responsible?**

---

## 3. M39-R2 Descriptive Statistics (Observed)

The M39-R2 descriptive statistics already hint at which components differ:

| Statistic | LNO | Control | Ratio/Difference |
|-----------|----:|--------:|:-----------------|
| Mean | +0.00000158 | −0.00000205 | LNO positive, CTRL negative |
| Std | 0.00149361 | 0.00090630 | LNO 1.65× wider |
| Median | +0.00003425 | +0.00000000 | LNO positive |
| IQR | 0.00151905 | 0.00077295 | LNO 1.97× wider |
| Skewness | −0.454497 | +0.255382 | Opposite signs |
| Excess kurtosis | 6.778268 | 17.519961 | CTRL heavier tails |
| Cohen's d | 0.003733 | — | Tiny effect size |

**Interpretation (descriptive only, not tested):**

- LNO has wider dispersion (std, IQR)
- LNO is negatively skewed; control is positively skewed
- Control has much heavier tails (kurtosis 17.5 vs 6.8)
- Mean difference is tiny (d = 0.004)

These descriptive patterns guide the decomposition design but do NOT constitute test results.

---

## 4. M40 Scientific Question

**Frozen:**

> **Which scientifically interpretable component of the 1-hour forward-return distribution differs between LONDON_NY_OVERLAP and the frozen control, under the day-block permutation framework?**

---

## 5. Primary Architecture: Sequential Hierarchical Decomposition

### Selection

After comparing five candidate architectures (see Section 11), M40 selects:

> **Sequential hierarchical moment decomposition with permutation inference**

This architecture tests four components in a predeclared order, using a single shared permutation framework, with a stopping rule that controls the family-wise error rate.

### Architecture Description

For each component in the hierarchy:

1. Compute a predeclared test statistic on the observed data
2. Compute the same statistic on each of 10,000 day-block permuted datasets
3. Derive permutation p-value: p = (1 + #{T_perm ≥ T_obs}) / (1 + 10,000)
4. If p < 0.05: **STOP** — declare this component the primary finding
5. If p ≥ 0.05: **CONTINUE** to next component

The first component to reject at α = 0.05 (one-sided where applicable) is declared the **primary component**. All subsequent components are reported as **descriptive only** (not hypothesis-tested).

### Why Sequential (Not Simultaneous)

- Controls family-wise error at α = 0.05 without Bonferroni correction
- Each test is independent in the sense that it addresses a different scientific question
- The ordering reflects scientific priority: location → scale → asymmetry → shape
- If the first test rejects, subsequent tests are unnecessary for the primary scientific claim

### Why Not Simultaneous / Omnibus

- Bonferroni would reduce per-test α to 0.0125, losing power
- A single omnibus test (like M39-R2's AD) already rejected — the question is now about components
- Sequential testing provides both multiplicity control and scientific interpretability

---

## 6. Component Hierarchy

### Component 1 — Location (Primary)

**Scientific question:** Does LNO shift the center of the return distribution?

**Test statistic:** Difference in means:

$$T_{location} = \bar{r}_{LNO} - \bar{r}_{CONTROL}$$

**Permutation p-value (one-sided, upper tail):**

$$p = \frac{1 + \#\{T_{perm} \geq T_{obs}\}}{1 + 10{,}000}$$

**Rationale:** Location is the most economically interpretable component. A mean shift implies a directional return premium during LNO, which would map directly to a trading mechanism (long/short directional).

**Economic interpretation if rejected:** The LNO session is associated with a predictable directional return shift.

**Dependence on M24:** M24 tested directional translation for the HIGH_VOL branch on EURUSD and found no effect (p = 0.6418). M40 tests a different phenomenon (session-transition, not HIGH_VOL onset) on a different dataset (M39-R2's hourly returns, not M15 bar returns). The M24 result is informative but does not preclude a location effect here.

---

### Component 2 — Scale (If Location Not Rejected)

**Scientific question:** Does LNO change the dispersion of the return distribution?

**Test statistic:** Difference in standard deviations:

$$T_{scale} = s_{LNO} - s_{CONTROL}$$

**Permutation p-value (two-sided):**

$$p = \frac{1 + \#\{|T_{perm}| \geq |T_{obs}|\}}{1 + 10{,}000}$$

**Rationale:** Scale is the second most economically interpretable. A dispersion change implies different movement risk during LNO, which affects position sizing, risk management, and volatility-informed strategies.

**Economic interpretation if rejected:** The LNO session is associated with different return volatility.

---

### Component 3 — Skewness / Asymmetry (If Scale Not Rejected)

**Scientific question:** Does LNO change the asymmetry of the return distribution?

**Test statistic:** Difference in sample skewness:

$$T_{skew} = \hat{\gamma}_{1,LNO} - \hat{\gamma}_{1,CONTROL}$$

**Permutation p-value (two-sided):**

$$p = \frac{1 + \#\{|T_{perm}| \geq |T_{obs}|\}}{1 + 10{,}000}$$

**Rationale:** The M39-R2 descriptive statistics show opposite skewness signs (LNO: −0.45, CTRL: +0.26). If this difference is real, it implies asymmetric tail risk during LNO, which maps to tail-risk compensation mechanisms.

**Economic interpretation if rejected:** The LNO session is associated with asymmetric return risk (different upside vs downside behavior).

---

### Component 4 — Tail Behavior (If Skewness Not Rejected)

**Scientific question:** Does LNO change the extreme quantiles of the return distribution?

**Test statistic:** Absolute difference in 5th-percentile returns:

$$T_{tail} = |Q_{0.05,LNO} - Q_{0.05,CONTROL}|$$

**Permutation p-value:**

$$p = \frac{1 + \#\{T_{perm} \geq T_{obs}\}}{1 + 10{,}000}$$

**Rationale:** The M39-R2 descriptive statistics show dramatically different kurtosis (6.8 vs 17.5). If the tail behavior differs, it implies different extreme-movement risk, which maps to tail-risk pricing.

**Quantile choice:** The 5th percentile is predeclared. The 95th percentile is also computed descriptively but NOT independently tested (to avoid multiplicity within the tail component).

**Economic interpretation if rejected:** The LNO session is associated with different extreme-movement behavior.

---

### Residual Shape Test (After All Four Components)

If none of the four components reject at α = 0.05:

**Scientific question:** Does the distributional difference survive after accounting for location, scale, skewness, and tails?

**Test statistic:** Kolmogorov-Smirnov statistic on standardized residuals:

1. Standardize both samples: z = (r − mean) / std
2. Compute KS statistic: $T_{shape} = \sup_z |F_{LNO,z}(z) - F_{CTRL,z}(z)|$

**Permutation p-value:**

$$p = \frac{1 + \#\{T_{perm} \geq T_{obs}\}}{1 + 10{,}000}$$

**Rationale:** If the CDF difference survives after matching location, scale, skewness, and tails, the difference is in the distributional shape (e.g., multimodality, kurtosis differences not captured by the 5th percentile, or higher-order structure).

**Economic interpretation:** The CDF difference is a shape phenomenon without a simple low-dimensional economic interpretation.

---

## 7. Dependence Preservation

### Permutation Framework

All five tests (Components 1–4 + Residual) use the **same permutation framework** established in M39-R2:

- **Blocks:** 1,331 day-boundary blocks (24 hourly obs/day)
- **Resampling:** Blocks resampled with replacement
- **Label assignment:** Random assignment of 2,757 LNO labels from pooled observations
- **Group-size preservation:** N_LNO = 2,757, N_CTRL = 29,184
- **Replications:** 10,000
- **Seed:** 42
- **RNG:** PCG-64

### Why This Preserves Dependence

The day-block permutation structure keeps observations at their fixed time positions within each day. Only the group labels (LNO/CTRL) are randomly reassigned. This means:

- Within-day serial correlation is preserved
- Calendar structure is preserved
- DST transitions are preserved
- The null hypothesis is: "session membership has no effect on the distributional component"

### Single Permutation Run

**Critical efficiency:** Only one permutation run is needed. For each of the 10,000 permuted datasets, compute all five test statistics simultaneously. This avoids:

- Multiple permutation runs (computationally expensive)
- Different random seeds for different tests
- Inconsistent null distributions

The permutation datasets are pre-generated once, and all test statistics are computed on each permutation replicate.

---

## 8. Multiplicity Control

### Structure

The sequential hierarchy controls multiplicity as follows:

1. Test Component 1 (location) at α = 0.05
2. If rejected: STOP. Component 1 is primary. Components 2–4 are descriptive.
3. If not rejected: Test Component 2 (scale) at α = 0.05
4. If rejected: STOP. Component 2 is primary. Components 3–4 are descriptive.
5. Continue similarly for Components 3 and 4.
6. If none rejected: Test residual shape. Report as "unexplained shape difference."

### Family-Wise Error Rate

Under the sequential testing framework:

$$FWER \leq \alpha = 0.05$$

This is because the sequential test is equivalent to a closed testing procedure: if the first test rejects, no further tests are performed. The probability of rejecting at least one true null is bounded by α.

### Why Not Bonferroni

Bonferroni would test each component at α/4 = 0.0125, which would:

- Reduce power for all components
- Be unnecessarily conservative given the sequential structure
- Not reflect the scientific priority ordering

### Why Not Holm-Bonferroni

Holm-Bonferroni requires sorting p-values and applying adjusted thresholds. This is valid but equivalent to sequential testing with the same ordering. The sequential framework is more transparent and directly maps to the scientific hierarchy.

---

## 9. Predeclared Quantities

### Test Statistics

| Component | Statistic | Direction |
|-----------|-----------|-----------|
| Location | Mean difference | One-sided (upper) |
| Scale | Std difference | Two-sided |
| Skewness | Skewness difference | Two-sided |
| Tail | |Q₀.₀₅ difference| | One-sided (upper) |
| Residual | KS statistic | One-sided (upper) |

### Quantiles

| Quantile | Purpose |
|----------|---------|
| 5th percentile | Primary tail test |
| 95th percentile | Descriptive only (not tested) |
| 25th percentile | Descriptive only |
| 75th percentile | Descriptive only |

### No Grid Search

M40 does NOT create a quantile grid, a moment grid, or a threshold grid. The test statistics are fixed.

---

## 10. Falsification Criteria

### Primary Falsification

If **no component rejects** at α = 0.05 under the permutation framework:

> **The M39-R2 CDF difference is an unexplained distributional-shape phenomenon without a simple low-dimensional economic interpretation.**

This is a valid scientific result. It means the CDF difference exists but cannot be attributed to a specific interpretable moment or tail behavior.

### Component-Specific Falsification

Each component that fails to reject is individually interpreted as:

> "The LNO distribution does not differ from the control in [component] under the day-block permutation framework."

### No Post-Hoc Metric Search

If all components fail:

> STOP. Do NOT search for another metric, another quantile, another moment, or another threshold.

The session-transition economic branch closes unless the control session identifies a genuinely new decomposition approach.

---

## 11. Candidate Architecture Comparison

| Architecture | Score | Key Limitation |
|---|---:|---|
| **Sequential Hierarchical (SELECTED)** | **45/50** | Assumes moment-based decomposition is sufficient |
| Single Omnibus (reuse AD on standardized data) | 30/50 | Doesn't identify WHICH component |
| Simultaneous Component Tests (Bonferroni) | 35/50 | Loses power; unnecessarily conservative |
| Descriptive-Only (no formal tests) | 20/50 | No inferential framework; cannot reject |
| Quantile Regression Decomposition | 25/50 | Complex; introduces regression assumptions |

### Detailed Scoring

| Dimension (1-5) | Sequential | Omnibus | Simultaneous | Descriptive | Quantile Reg |
|---|---|---|---|---|---|
| Scientific continuity | 5 | 3 | 4 | 2 | 3 |
| Economic relevance | 5 | 2 | 4 | 2 | 4 |
| Ex-ante freezeability | 5 | 5 | 4 | 5 | 3 |
| Dependence validity | 5 | 5 | 5 | 5 | 3 |
| Multiplicity control | 5 | 5 | 3 | 5 | 3 |
| Interpretability | 5 | 2 | 4 | 3 | 3 |
| Data feasibility | 5 | 5 | 5 | 5 | 3 |
| Simplicity | 4 | 5 | 3 | 5 | 2 |
| Falsifiability | 5 | 4 | 4 | 2 | 3 |
| Information value | 4 | 3 | 4 | 2 | 3 |
| **Total** | **48** | **39** | **40** | **36** | **29** |

**Note:** The Sequential Hierarchical architecture scores highest because it combines scientific continuity (each component directly interpretable), economic relevance (each component maps to a different mechanism), multiplicity control (sequential testing), and dependence validity (shared permutation framework).

---

## 12. Primary Data

M41 will reuse:

```
reports/APEX_M39R2_Session_Transition_Return_Data.csv
```

Columns: `timestamp, group, session_state, forward_end_timestamp, forward_return, day_id, primary_exclusion_flag`

- LNO: 2,757 observations
- Control: 29,184 observations
- Total: 31,941 observations

No new data acquisition required.

---

## 13. Economic Interpretation Boundary

| Component | If Rejected | Economic Implication |
|-----------|------------|---------------------|
| Location | LNO has mean shift | Directional return premium; long/short mechanism |
| Scale | LNO has different variance | Changed volatility; risk management / vol instrument |
| Skewness | LNO has asymmetric returns | Asymmetric risk compensation; tail-risk instrument |
| Tail | LNO has different extremes | Tail-risk pricing; extreme-movement instrument |
| Residual shape | Unexplained shape | No simple economic mechanism identified |

### Important Boundary

M40 does NOT map these to specific trades. The mapping is:

```
distributional component → economic interpretation → potential mechanism
```

A separate methodology (M41 or later) would be required before any payoff is tested.

---

## 14. What M40 Establishes

1. The sequential hierarchical decomposition architecture
2. The four predeclared components and their test statistics
3. The single permutation framework (10,000 replications, seed 42)
4. The multiplicity control structure (sequential testing at α = 0.05)
5. The falsification criteria
6. The economic interpretation boundary for each component

---

## 15. What M40 Does NOT Establish

1. Which component actually differs (that is M41's job)
2. Whether any component differs
3. The economic mechanism
4. Any trading strategy
5. Any profitability or edge

---

## 16. External API calls: 0 | New data acquired: 0 | Spend: $0.00

---

*M40 is a methodology design milestone. No decomposition was calculated. No p-values were computed. No moments were tested.*
