# APEX M34: HIGH_VOL Branch Final Scientific Closure

## 1. Branch Identity

**Branch Name**: HIGH_VOL Lifecycle / Predictability / Translation

**Milestones**: RC012 → M13/M14 → M17-R2 → M21 → M24 → M27 → M31 → M32/M33 → M34

**Final Status**: `CLOSED — SCIENTIFICALLY INFORMATIVE, ECONOMIC IMPLEMENTATION UNRESOLVED`

---

## 2. Starting Hypothesis

RC012 established that the `HIGH_VOL` state — defined as `RV20 > 80th percentile` on EURUSD M15 — is a distinct distributional primitive. The subsequent research question was whether this primitive could be predicted, characterized, and economically translated into actionable information.

---

## 3. Complete Evidence Chain

### RC012 — HIGH_VOL Primitive Discovery

| Item | Value |
|---|---|
| Research Question | Does a distinct volatility distributional primitive exist? |
| Methodology | Distributional analysis of EURUSD M15 volatility states |
| Result | HIGH_VOL validated as structural distributional primitive |
| What It Did NOT Establish | Predictability, lifecycle, economic utility |

### M13/M14 — Structural Lifecycle Validation

| Item | Value |
|---|---|
| Research Question | Is HIGH_VOL persistence memoryless? |
| Methodology | Monte Carlo comparison against predeclared geometric null |
| Sample | 794 episodes |
| Observed CDF distance | D = 0.19270 |
| Monte Carlo simulations | 10,000 |
| Null exceedances | 0 |
| p-value | < 0.0001 |
| Result | `VALIDATED STRUCTURAL PHENOMENON` — memoryless geometric model rejected |
| Interpretation | HIGH_VOL persistence is strongly inconsistent with the predeclared memoryless geometric model |
| What It Did NOT Establish | Predictability prior to onset, causal mechanism, tradability, economic value |

### M17-R2 — Conditional Persistence Predictability

| Item | Value |
|---|---|
| Research Question | Is HIGH_VOL persistence predictable from onset information? |
| Methodology | Walk-forward Cox Proportional Hazards (statsmodels.PHReg) |
| Sample | 794 episodes (397 training / 397 OOS) |
| Predictors | Breakout Intensity, Variance Momentum (at onset close only) |
| C-index | 0.6656 |
| Baseline C-index | 0.5000 |
| Delta C-index | +0.1656 |
| Result | `PREDICTIVE SIGNAL ESTABLISHED` |
| Interpretation | Onset-state information provides substantial out-of-sample rank information about subsequent HIGH_VOL persistence |
| What It Did NOT Establish | Causality, tradability, profitability, execution edge |

### M21 — Realized Volatility Translation

| Item | Value |
|---|---|
| Research Question | Does predicted persistence condition forward RV magnitude? |
| Methodology | OLS with HAC (maxlags=48), alpha=0.05 two-sided |
| Beta | -0.014288 |
| HAC SE | 0.004847 |
| p-value | 0.0032 |
| 95% CI | [-0.023788, -0.004788] |
| Result | `TRANSLATION ESTABLISHED` |
| Interpretation | Predicted persistence is associated with subsequent 12-hour realized-volatility magnitude |
| What It Did NOT Establish | Profitability, directional prediction, causality |

### M24 — Directional Translation

| Item | Value |
|---|---|
| Research Question | Does predicted persistence condition directional drift? |
| Methodology | OLS with HAC (maxlags=48), alpha=0.05 two-sided |
| Beta | -0.000367 |
| p-value | 0.6418 |
| 95% CI | [-0.001915, 0.001181] |
| Result | `NO DIRECTIONAL TRANSLATION` |
| Interpretation | The frozen test did not detect a linear directional-return relationship over the tested 12-hour horizon |
| What It Did NOT Establish | Universal directional neutrality (only linear drift over tested horizon) |

### M27 — Continuous Excursion Translation

| Item | Value |
|---|---|
| Research Question | Does predicted persistence condition maximum absolute excursion? |
| Methodology | OLS with HAC (maxlags=48), alpha=0.05 two-sided |
| Beta | -0.001153 |
| HAC SE | 0.000291 |
| p-value | 7.5147e-05 |
| 95% CI | [-0.001723, -0.000582] |
| Upside/Downside Ratio | 0.9218 (near-symmetric) |
| Result | `EXTREMUM TRANSLATION ESTABLISHED` |
| Interpretation | Predicted persistence conditions future maximum absolute excursion magnitude |
| What It Did NOT Establish | Profitability, path dependency, optimal stop/target distances |

### M31 — Static Economic Boundary

| Item | Value |
|---|---|
| Research Question | Does predicted persistence condition binary breach of 1.0×RV20_onset? |
| Methodology | Linear Probability Model (OLS), HAC maxlags=48 |
| Breach Rate | 395/396 = 99.75% |
| Beta | 0.054025 |
| p-value | 0.2375 |
| Result | `BOUNDARY TRANSLATION NOT ESTABLISHED` |
| Interpretation | The specific 1.0×RV20_onset binary boundary is saturated and non-discriminative |
| What It Did NOT Establish | Invalidation of M27, failure of all economic translations |

### M32/M33 — Continuation Adjudication

| Item | Value |
|---|---|
| Research Question | Should the HIGH_VOL branch continue? |
| Methodology | Evidence-based control adjudication |
| Option A (Close) | 43/50 — PRIMARY |
| Option B (Dynamic Design) | 28/50 — REJECTED |
| Option C (Broader Discovery) | 37/50 — RUNNER-UP |
| Dynamic Translation Classification | `METHODOLOGICALLY WEAK` |
| Result | `FORMALLY CLOSE HIGH_VOL BRANCH` |

---

## 4. Validated Findings

1. **HIGH_VOL is a structural distributional primitive** (RC012). It is not a statistical artifact.

2. **HIGH_VOL persistence is non-memoryless** (M13/M14). The state possesses a structured lifecycle with structural memory. The memoryless geometric model is rejected with p < 0.0001.

3. **Onset Intensity + Momentum predict future persistence** (M17-R2). C-index = 0.6656 (Δ = +0.1656 over baseline). This is a meaningful out-of-sample improvement.

4. **Predicted persistence scales forward RV magnitude** (M21). Higher risk score (shorter predicted duration) → lower forward RV. p = 0.0032.

5. **Predicted persistence does NOT predict directional drift** (M24). The signal is a pure volatility oracle, not a directional oracle. p = 0.6418.

6. **Predicted persistence scales the outer spatial envelope of price excursion** (M27). Higher risk score → smaller MAE_abs envelope. p = 7.5×10⁻⁵.

7. **The expansion is near-symmetric** (M27 secondary). Upside/downside ratio = 0.9218.

---

## 5. Negative Findings

1. **Session-transition branch infeasibility**: The HIGH_VOL × ASIA_TO_LONDON branch became statistically infeasible after causal independence rules reduced exposure events to n = 8.

2. **No linear directional translation**: M24 failed to detect a linear directional-return relationship (p = 0.6418). This does not disprove all directional effects — only the frozen linear test over the tested horizon.

3. **Static boundary saturation**: M31's 1.0×RV20_onset boundary was breached 99.75% of the time (p = 0.2375). The specific binary threshold is saturated and non-discriminative. It does not invalidate M27.

4. **Spot monetization failure**: RC012 Studies 007–011 demonstrated that all tested spot execution architectures (fixed-direction holding, OCO breakout, bounded inventory) failed due to path truncation, whipsaw, and tail risk.

---

## 6. M31 Saturation Lesson

**Lesson**: A continuous predictive relationship can become useless when compressed into an overly loose binary threshold.

M27 established that the APEX signal genuinely conditions the continuous structural envelope of price excursion. M31 showed that the specific static boundary $1.0 \times RV20_{onset}$ is so narrow relative to the natural expansion during HIGH_VOL events that it is breached nearly universally. The continuous relationship is real; the arbitrary static threshold is not.

This is a general methodological lesson: continuous associations do not automatically translate into useful binary economic thresholds.

---

## 7. Why Dynamic Continuation Was Rejected

M33 classified dynamic translation as `METHODOLOGICALLY WEAK` because:

1. **Arbitrary constants**: Any dynamic boundary requires a multiplier, scaling factor, or functional form — each a researcher degree of freedom.

2. **Outcome-derived calibration**: The mapping between RiskScore and boundary width MUST be estimated from M27 MAE data. This creates circularity: the boundary is tuned to the same distribution it is tested against.

3. **Low scientific novelty**: M27 already established the continuous association. A dynamic boundary merely re-parameterizes the same association into a binary threshold. It does not answer a genuinely different question.

4. **Hidden parameter search risk**: The boundary design process would likely devolve into grid optimization, stop/target tuning, or payoff engineering — all implementation questions, not scientific questions.

5. **Economic information already captured**: The economic content is fully captured by the continuous M27 regression. A dynamic boundary adds no new information.

---

## 8. What Remains Unproven

### Scientific Questions
- Causal mechanism linking onset features to future persistence.
- Cross-instrument generalization (tested only on EURUSD).
- Temporal out-of-sample robustness across different market regimes.

### Implementation/Strategy Questions
- Profitability of any HIGH_VOL-based strategy.
- Positive expectancy.
- Trading strategy design.
- Execution edge in live markets.
- Capital efficiency.
- Transaction-cost robustness.
- Financing robustness.
- Optimal grid spacing, stop distance, barrier width.
- Path-dependent drawdown characteristics.

---

## 9. Reusable Knowledge

The following knowledge is preserved for future APEX research:

1. **HIGH_VOL_STATE** as a validated market-state primitive with:
   - Structural persistence (non-memoryless lifecycle)
   - Onset predictability (C-index = 0.6656)
   - Volatility translation (scales forward RV magnitude)
   - Excursion translation (scales outer spatial envelope)
   - No detected linear directional translation over tested horizon

2. **Canonical HIGH_VOL episode ledger** (794 episodes, EURUSD M15).

3. **M17-R2 prediction methodology** (walk-forward Cox PH with statsmodels).

4. **M21/M24/M27 translation results** (frozen methodology, zero lookahead).

---

## 10. Methodological Lessons

These lessons should become reusable APEX governance principles:

1. **Do not relax scientifically justified event definitions to inflate sample size.** (Session-transition branch lesson: n=8 after independence rules.)

2. **Methodology must be repaired before economic testing.** (M11 original methodology contained lookahead, confounding, arbitrary thresholds.)

3. **Statistical calibration must match the data structure.** (Discrete K-S issue: continuous K-S inference inappropriate for discrete durations.)

4. **Feature count is not scientific value.** (Predictor redundancy: Breakout Intensity and Regime Depth were nearly redundant.)

5. **Continuous relationships do not automatically translate into useful binary thresholds.** (M31 saturation lesson.)

6. **The APEX stopping principle**: Continue only when the next research question is materially different from previous experiments and can be frozen without expanding outcome-dependent researcher freedom.

---

## 11. Final Status

> **CLOSED — SCIENTIFICALLY INFORMATIVE, ECONOMIC IMPLEMENTATION UNRESOLVED**

The HIGH_VOL branch produced substantial validated scientific information. The remaining path from continuous excursion prediction to economically actionable implementation requires additional parameterization that cannot currently be specified with sufficient ex-ante defensibility.

The branch is closed for now, not because the phenomenon failed, but because the next economic research layer is not currently sufficiently defensible.

---

## 12. Next APEX Milestone

> **M35 — APEX Next-Research Direction Discovery**
> Status: `PLANNED — NOT STARTED`

After M34, the HIGH_VOL branch is formally CLOSED. The next research direction should be selected through a new broader APEX direction-discovery/control milestone.
