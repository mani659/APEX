# APEX M33: FINAL Control Adjudication — HIGH_VOL Branch

## Section A — Current APEX State

| Item | Value |
|---|---|
| Branch | `main` |
| HEAD | `98abd02` (M31+M32 commit) |
| Remote | Untouched |
| HIGH_VOL branch status | STALLED (M32) |
| M32 mandatory stop | Imposed |
| Current authorization | NONE — no milestone authorized |

---

## Section B — HIGH_VOL Evidence Ledger

| Milestone | Finding | Statistic | p-value | Verdict |
|---|---|---|---|---|
| RC012 | HIGH_VOL distributional primitive exists | Cramér-von Mises D=0.1927 | <0.0001 | ESTABLISHED |
| RC012 S005 | Independent OOS validation | Out-of-sample replication | — | ESTABLISHED |
| RC012 S012 | Spot monetization failed (all architectures) | Studies 007–011 | — | REJECTED (spot) |
| M13/M14 | Non-memoryless persistence, structured lifecycle | D=0.1927, n=794 | <0.0001 | ESTABLISHED |
| M17-R2 | Conditional persistence prediction at onset | C-index=0.6656 (Δ=+0.1656) | N/A | ESTABLISHED |
| M21 | Predicted persistence → forward RV magnitude | β=−0.014288 | 0.0032 | ESTABLISHED |
| M24 | Predicted persistence → directional drift | β=−0.000367 | 0.6418 | NOT ESTABLISHED |
| M27 | Predicted persistence → max absolute excursion | β=−0.001153 | 7.5×10⁻⁵ | ESTABLISHED |
| M31 | Binary breach of 1.0×RV20_onset | β=0.054025 | 0.2375 | NOT ESTABLISHED |

**Established** (5): RC012, M13/M14, M17-R2, M21, M27.
**Not Established** (2): M24 (directional), M31 (binary boundary).
**Rejected** (1): RC012 Studies 007–011 (spot monetization).

Every milestone executed with frozen methodology, zero lookahead, HAC-corrected inference, strict α=0.05. No methodological deviations found.

---

## Section C — What Is Established

1. **HIGH_VOL is a structural distributional primitive** (RC012). It is not a statistical artifact.
2. **HIGH_VOL persistence is non-memoryless** (M13/M14). The state possesses a structured lifecycle with structural memory.
3. **Onset Intensity + Momentum predict future persistence** (M17-R2). C-index=0.6656, a meaningful improvement over baseline.
4. **Predicted persistence scales forward RV magnitude** (M21). A one-unit increase in risk score reduces annualized forward RV by ~1.43%.
5. **Predicted persistence does NOT predict directional drift** (M24). The signal is a pure volatility oracle, not a directional oracle.
6. **Predicted persistence scales the outer spatial envelope of price excursion** (M27). Higher risk score → smaller MAE_abs envelope.
7. **The expansion is near-symmetric** (M27 secondary): upside/downside ratio = 0.92.

---

## Section D — What Is Unproven

### Scientific Questions (Unresolved)
- Causal mechanism linking onset features to future persistence.
- Cross-instrument generalization (tested only on EURUSD).
- Temporal out-of-sample robustness across different market regimes.

### Implementation/Strategy Questions (Unresolved)
- Profitability of any HIGH_VOL-based strategy.
- Capital efficiency and margin requirements.
- Transaction-cost robustness.
- Execution edge in live markets.
- Strategy expectancy.
- Optimal grid/barrier parameterization.
- Path-dependent drawdown characteristics.

### Already Closed Questions
- Whether HIGH_VOL is a real phenomenon: YES (RC012, M13/M14).
- Whether it is predictable at onset: YES (M17-R2).
- Whether it scales RV magnitude: YES (M21).
- Whether it predicts direction: NO (M24).
- Whether it scales the excursion envelope: YES (M27).
- Whether a static 1.0×RV20 boundary discriminates: NO (M31, saturation).

---

## Section E — M31 Saturation Interpretation

### M31 DOES Establish
- The chosen binary threshold ($1.0 \times RV20_{onset}$) has almost no remaining outcome variance (99.75% breach rate).
- The threshold cannot discriminate persistence-risk states effectively on a binary basis.
- The specific ex-ante boundary chosen is too narrow to act as a discriminative economic threshold.

### M31 DOES NOT Establish
- M27 is false. The continuous regression relationship remains valid ($p = 7.5 \times 10^{-5}$).
- Continuous excursion prediction is false. The APEX signal genuinely conditions the outer spatial envelope.
- All possible economic translations fail. Only this specific binary threshold failed.
- Dynamic boundaries must succeed. This is a separate question requiring separate methodology.
- Grid trading is viable. M31 does not simulate path-dependent capital requirements or drawdown.

### Correct Interpretation
The M31 saturation is a limitation of the chosen binary representation, not a refutation of the underlying continuous relationship. M27 and M31 are perfectly consistent: the continuous expansion is real; the arbitrary static threshold is not.

---

## Section F — Dynamic Translation Feasibility

### The Question
> Can the continuous M27 excursion relationship be converted into one predeclared dynamic economic boundary using previously validated information, without outcome-derived calibration?

### A. Ex-Ante Derivability
The M27 regression gives: $MAE_{abs} = \alpha + \beta \times RiskScore + \varepsilon$.
A dynamic boundary would require: $B_t = f(RiskScore_t)$ where $f$ is defined ex-ante.
**Problem**: The functional form $f$ and its parameters ($\alpha$, $\beta$, or any transformation thereof) were estimated FROM M27 outcomes. Writing $f$ before viewing M27 results would require a purely rank-based approach (e.g., quartile boundaries), but even quartile boundaries are calibrated to the M27 outcome distribution.

### B. Valid Inputs
- `conditional_risk_score` is available at onset (validated by M17-R2).
- `RV20_onset` is available at onset (validated by M29).
- The mapping $f$ between RiskScore and boundary width requires M27 coefficients.

### C. New Constants
Any dynamic boundary requires at minimum:
- A multiplier or scaling factor.
- A functional form (linear, quantile-based, etc.).
- Potentially a threshold or percentile.
Each is a researcher degree of freedom.

### D. Outcome Calibration
The mapping MUST be estimated from M27 MAE data. This is outcome-derived calibration. Even if frozen before execution, the calibration data is the same data used to validate M27. This creates a circularity: the boundary is tuned to the same distribution it is tested against.

### E. Scientific Novelty
M27 already established the continuous association between RiskScore and MAE_abs. A dynamic boundary would merely re-parameterize the same association into a binary threshold. It would NOT answer a genuinely different question.

### F. Falsifiability
A dynamic boundary experiment could produce a clean negative result. However, because the boundary is calibrated to M27, falsification would mean the calibration failed — not that the underlying relationship is absent. This reduces the scientific value of the falsification.

### G. Economic Meaning
The result would tell us how to choose a grid/barrier width after seeing the M27 data. It would NOT establish new economic information beyond what M27 already told us. The economic content is already fully captured by the continuous M27 regression.

### Classification: `METHODOLOGICALLY WEAK`

Dynamic translation is technically possible but:
- Introduces arbitrary constants (multiplier, scaling factor, functional form).
- Depends on calibration to M27 outcomes (circularity).
- Adds little scientific novelty (same question, different parameterization).
- Risks becoming hidden parameter search.
- The economic information content is already fully captured by M27.

---

## Section G — Options A/B/C Scoring

| Dimension | Option A (Close) | Option B (Dynamic Design) | Option C (Broader Discovery) |
|---|---|---|---|
| Scientific novelty | 1 | 2 | 3 |
| Continuity | 5 | 4 | 3 |
| Falsifiability | 5 | 3 | 4 |
| Ex-ante defensibility | 5 | 2 | 4 |
| Information value | 4 | 2 | 3 |
| Data feasibility | 5 | 4 | 4 |
| Economic relevance | 3 | 3 | 4 |
| Independence | 5 | 2 | 5 |
| Overfitting risk | 5 | 2 | 4 |
| Stopping value | 5 | 2 | 3 |
| **TOTAL** | **43** | **28** | **37** |

Scoring rules: 1–5 scale; higher = better; overfitting risk scored as 5 = lowest risk.

---

## Section H — Primary Decision

**FORMALLY CLOSE HIGH_VOL BRANCH (Option A, score=43/50).**

The HIGH_VOL branch is scientifically mature. The physical relationship is fully mapped (M21, M24, M27). The first economic threshold test (M31) failed due to saturation. The dynamic-translation continuation candidate (Option B) is methodologically weak: it introduces arbitrary constants, depends on outcome-derived calibration, adds little scientific novelty, and risks becoming hidden parameter search. The APEX stopping principle applies: continue only when the next research question is materially different from previous experiments and can be frozen without expanding outcome-dependent researcher freedom.

---

## Section I — Runner-Up

**RETURN TO BROADER APEX RESEARCH-DIRECTION DISCOVERY (Option C, score=37/50).**

If the user does not wish to formally close the HIGH_VOL branch, the next best action is to return to the wider RC-series research tree and discover new research directions. This avoids the methodological weaknesses of Option B while preserving the option to revisit HIGH_VOL in the future if new data or methods become available.

---

## Section J — Exact Next Authorized Milestone

If Option A is accepted:
> **M34 — HIGH_VOL Final Scientific Closure**
> Status: `PLANNED — NOT STARTED`
> Purpose: Document complete evidence chain, validated findings, failed representations, unresolved questions, and why further continuation is not justified.

If Option C is accepted:
> **M34 — APEX Next-Research Direction Discovery**
> Status: `PLANNED — NOT STARTED`
> Purpose: Discover and score next research directions for the broader APEX programme.

---

## Section K — Stopping / Continuation Rationale

### Why Option A Is Scientifically Superior

1. **The major scientific questions are answered.** HIGH_VOL is real (RC012), has a structured lifecycle (M13/M14), is predictable at onset (M17-R2), scales RV magnitude (M21), does not predict direction (M24), and scales the excursion envelope (M27). This is a complete physical characterization.

2. **Remaining work is mainly parameterization.** The only continuation candidate (Option B) is essentially boundary optimization — choosing how to convert a continuous relationship into a binary threshold. This is an implementation question, not a scientific question.

3. **New experiments would primarily optimize economic implementation.** Option B would not discover new physical relationships. It would attempt to engineer an economic extraction method from an already-characterized relationship.

4. **Scientific novelty is small relative to methodology flexibility.** Option B introduces arbitrary constants, depends on calibration, and risks becoming hidden parameter search. The APEX stopping principle applies.

5. **A stopping decision is a valid scientific outcome.** The branch is scientifically informative but currently lacks a sufficiently defensible next experiment. This is not a failure — it is a mature conclusion.

### Why Option B Is Scientifically Inferior

- Introduces arbitrary constants (multiplier, scaling factor, functional form).
- Depends on calibration to M27 outcomes (circularity).
- Adds little scientific novelty (same question re-parameterized).
- Risks becoming hidden parameter search (grid optimization, stop/target tuning).
- The economic information content is already fully captured by M27.

### Why Option C Is Scientifically Acceptable but Inferior to Option A

- Opens new research branches (good).
- Does not duplicate HIGH_VOL work (good).
- But: the HIGH_VOL branch has a clear, defensible closure point. Returning to broader discovery before formally closing it leaves the branch in an ambiguous state.

---

**MANDATORY STOP. No M34 or later milestone may begin during M33.**
