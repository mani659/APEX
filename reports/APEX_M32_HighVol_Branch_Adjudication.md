# APEX M32: HIGH_VOL Branch Adjudication & Stopping Decision

## 1. Purpose
This document conducts a mandatory M31 saturation audit, reconstructs the complete HIGH_VOL evidence ledger, scores continuation options A/B/C, and delivers a stopping recommendation for the HIGH_VOL volatility-prediction branch of the APEX research programme.

## 2. M31 Saturation Audit (Mandatory)

### 2.1 What M31 Tested
- **Research Question**: Does the M17-R2 predicted persistence state condition the probability of breaching a predeclared direction-neutral spatial-risk boundary ($B_t = 1.0 \times RV20_{onset}$) over 12 hours?
- **Model**: Linear Probability Model (OLS), HAC maxlags=48, alpha=0.05 two-sided.
- **Sample**: 396 valid OOS episodes from M17-R2 walk-forward predictions.
- **Boundary**: $B_t = 1.0 \times RV20_{onset}$ (extracted from pre-trigger M15 data, strictly ex-ante).

### 2.2 M31 Results
- **Breach Rate**: 395/396 = 99.75% (near-universal).
- **Beta**: 0.054025 (positive, meaning higher risk score → slightly higher breach probability).
- **HAC Robust SE**: 0.045732.
- **t-statistic**: 1.1813.
- **p-value**: 0.2375.
- **95% CI**: [-0.035608, 0.143658].
- **Verdict**: FAIL TO REJECT null. BOUNDARY TRANSLATION NOT ESTABLISHED.

### 2.3 Saturation Diagnosis
The 99.75% base-rate breach rate constitutes **extreme base-rate saturation**. The boundary $1.0 \times RV20_{onset}$ is so narrow relative to the natural 12-hour price excursion during a structurally confirmed HIGH_VOL event that it is breached nearly universally. The APEX risk score cannot discriminate breach from non-breach because there is virtually no non-breach class remaining.

### 2.4 Relationship to M27
- **M27** (continuous MAE regression): $p = 7.5 \times 10^{-5}$, EXTREMUM TRANSLATION ESTABLISHED.
- **M31** (binary boundary): $p = 0.2375$, BOUNDARY TRANSLATION NOT ESTABLISHED.
- **Interpretation**: These results are perfectly consistent. The continuous relationship between the APEX score and the outer envelope of price excursion is real and strong (M27). However, the specific spatial threshold chosen ($1.0 \times RV20_{onset}$) lies far inside that envelope for nearly all events, so the binary breach indicator carries no discriminative information. The continuous structural expansion is real; the arbitrary static threshold is not.

### 2.5 Saturation vs. M27 Continuous Finding
The M31 saturation does **not** invalidate M27. It confirms that:
1. The APEX signal governs the continuous structural envelope of variance expansion.
2. The chosen static boundary is too narrow to act as a discriminative economic threshold.
3. A dynamic boundary (scaled as a function of the risk score) or a path-dependent execution simulation would be required to capture the continuous relationship economically.

## 3. Complete HIGH_VOL Evidence Ledger

| Milestone | Finding | Statistic | p-value | Verdict |
|-----------|---------|-----------|---------|---------|
| RC012 | HIGH_VOL distributional primitive exists | Cramér-von Mises D=0.1927 | <0.0001 | ESTABLISHED |
| RC012 S005 | Independent OOS validation of magnitude expansion | Out-of-sample replication | — | ESTABLISHED |
| RC012 S012 | Spot monetization attempts failed (all architectures) | Studies 007–011: truncation, whipsaw, tail risk | — | REJECTED (spot) |
| M13/M14 | HIGH_VOL persistence is non-memoryless, has structured lifecycle | D=0.1927, n=794 | <0.0001 | ESTABLISHED |
| M17-R2 | Conditional persistence prediction at onset | C-index=0.6656 (baseline=0.5000) | N/A (C-index) | ESTABLISHED |
| M21 | Predicted persistence → forward RV magnitude | beta=-0.014288 | 0.0032 | ESTABLISHED |
| M24 | Predicted persistence → directional drift | beta=-0.000367 | 0.6418 | NOT ESTABLISHED |
| M27 | Predicted persistence → max absolute excursion envelope | beta=-0.001153 | 7.5e-05 | ESTABLISHED |
| M31 | Predicted persistence → binary breach of 1.0×RV20 | beta=0.054025 | 0.2375 | NOT ESTABLISHED |

### 3.1 Evidence Summary
- **Established** (5 milestones): HIGH_VOL primitive (RC012), non-memoryless lifecycle (M13/M14), conditional predictability (M17-R2), RV translation (M21), extremum boundary translation (M27).
- **Not Established** (2 milestones): Directional drift (M24), binary boundary translation at 1.0×RV20 (M31).
- **Rejected** (1 milestone): Spot monetization architectures (RC012 Studies 007–011).

### 3.2 Evidence Chain Integrity
Every milestone in the chain was executed with frozen methodology, zero lookahead, HAC-corrected inference, and strict alpha=0.05. No methodological deviations were found in any milestone audit. The evidence chain is internally consistent and scientifically sound.

## 4. Continuation Option Scoring (A/B/C)

### 4.1 Option A: STOP — Declare HIGH_VOL Branch Stalled
**Description**: Accept that the HIGH_VOL volatility-prediction branch has reached its natural scientific conclusion. The physical relationship is fully mapped (M21, M24, M27), the first economic threshold test failed due to saturation (M31), and no further incremental experimentation within the current frozen methodology framework can yield novel information.

| Dimension | Score (0-10) | Rationale |
|-----------|-------------|-----------|
| Evidence Strength | 9 | Massive accumulated evidence; clear stopping signal from M31 |
| Novel Research Value | 2 | Most questions answered; M31 saturation provides clear endpoint |
| Cost to Execute | 10 | Zero cost — stopping is free |
| Time to Execute | 10 | Instant |
| Expected Economic Value | 3 | Edge exists theoretically but tested extraction methods failed |
| Risk of Curve-Fitting | 10 | No experiment = no curve-fitting risk |
| Reversibility | 10 | Completely reversible; can restart at any time |
| Cross-Instrument Portability | 5 | General findings apply; specific parameters are EURUSD-specific |
| Methodology Rigor | 10 | No methodology needed |
| Scientific Integrity | 8 | Stopping at the right time demonstrates programme discipline |
| **TOTAL** | **77** | |

### 4.2 Option B: CONTINUE — Dynamic Boundary / Path-Dependent Execution Simulation
**Description**: Address M31 saturation by replacing the static $1.0 \times RV20_{onset}$ boundary with a dynamic boundary scaled as a function of the APEX risk score. Alternatively, design a full path-dependent execution simulation that captures the continuous variance envelope rather than discretizing it.

| Dimension | Score (0-10) | Rationale |
|-----------|-------------|-----------|
| Evidence Strength | 8 | Strong M27 continuous result; M31 shows naive thresholds fail |
| Novel Research Value | 7 | Dynamic mapping is genuinely novel; addresses M31 saturation directly |
| Cost to Execute | 6 | Requires new simulation work; no external data cost |
| Time to Execute | 5 | Complex simulation design and validation required |
| Expected Economic Value | 7 | Could finally resolve the monetization question |
| Risk of Curve-Fitting | 4 | HIGH RISK — M27 coefficients are available for retroactive tuning |
| Reversibility | 8 | Can abandon at any point |
| Cross-Instrument Portability | 6 | Dynamic scaling is more portable than fixed thresholds |
| Methodology Rigor | 5 | Hard to freeze methodology when "dynamic" invites parameter choices |
| Scientific Integrity | 7 | Follows the natural next question from M31 |
| **TOTAL** | **63** | |

### 4.3 Option C: CONTINUE — Alternative Monetization (Options/Straddle Path)
**Description**: Pivot to M28's recommended monetization path: acquire option IV data, compute VRP (Variance Risk Premium), and test whether the APEX signal predicts IV-RV divergence. This would test the true monetization path identified in the post-RC012 strategy review.

| Dimension | Score (0-10) | Rationale |
|-----------|-------------|-----------|
| Evidence Strength | 6 | Need new data: option IV, spreads, funding rates |
| Novel Research Value | 6 | Different angle but same underlying signal |
| Cost to Execute | 3 | Requires new data acquisition (option IV, spreads, funding) |
| Time to Execute | 3 | Data acquisition + new methodology design |
| Expected Economic Value | 8 | M28 identified this as the true monetization path |
| Risk of Curve-Fitting | 5 | Moderate; new data reduces risk |
| Reversibility | 6 | Can abandon but data cost is sunk |
| Cross-Instrument Portability | 7 | Options pricing is more universal than spot mechanics |
| Methodology Rigor | 6 | New methodology design required from scratch |
| Scientific Integrity | 7 | Follows M28 recommendation and post-RC012 strategy review |
| **TOTAL** | **57** | |

## 5. Primary Recommendation

**PRIMARY: Option A — STOP the HIGH_VOL Branch.**

The HIGH_VOL volatility-prediction branch has reached its natural scientific conclusion. The physical relationship is comprehensively mapped (M21, M24, M27). The first economic threshold test (M31) failed due to near-perfect saturation (99.75% breach rate). The evidence chain is complete, internally consistent, and scientifically sound. No further incremental experimentation within the current frozen methodology framework can yield novel information.

**RUNNER-UP: Option B — CONTINUE with Dynamic Boundary Simulation.**

If the user wishes to push further before stopping, Option B is the most natural continuation: it directly addresses M31's saturation diagnosis and leverages the strong M27 continuous result. However, it carries significant curve-fitting risk (M27 coefficients are available for retroactive tuning) and requires careful methodology freezing to maintain scientific integrity.

## 6. Stopping Criteria Met
The mandatory M31 saturation audit confirms:
1. The APEX signal governs the continuous structural envelope of variance expansion (M27, $p = 7.5 \times 10^{-5}$).
2. The chosen static boundary ($1.0 \times RV20_{onset}$) is breached 99.75% of the time, providing no discriminative economic threshold (M31, $p = 0.2375$).
3. The continuous physical relationship is real; the arbitrary static economic threshold is not.
4. No further frozen-methodology experiments within the current framework can resolve the saturation problem.

**MANDATORY STOP: The HIGH_VOL branch is declared stalled. No further milestones should be authorized without explicit user override.**
