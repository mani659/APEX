# APEX POST-M50 CONTROL — RESEARCH RESTART ADJUDICATION

**Milestone**: POST-M50 CONTROL (Control Session)
**Date**: 2026-08-30
**Status**: COMPLETE
**Type**: Control Decision Only (no experiment, no methodology, no data acquisition)

---

## 1. Purpose

Adjudicate whether any genuinely new economic hypothesis earned the right to restart APEX, or whether APEX should remain paused — in light of M50's integrated discovery and the critical evidence limitation (the custom-bot analysis document was not found on the filesystem).

This is a **CONTROL DECISION ONLY**. No experiment, data acquisition, methodology build, strategy modification, or automatic M51 was performed.

---

## 2. First Control Question — Did M50 Really Need to Pause?

**Yes.** M50 correctly rejected all immediate candidates.

For each of the three leading candidates (Execution-State, Trade-Path, Portfolio-Risk) the full 8-point restart gate was re-applied in this control session (see §4-§6). Every candidate fails at least one necessary condition:

| Candidate | New object | Mechanism | Payoff | Pos-net hyp | Causal observ | Ex-ante freeze | Evidence path | Falsification |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Execution-State | △ | △ | ✗ | ✗ | ✗ | △ | ✗ | ✗ |
| Trade-Path | ✓ | △ | ✗ | ✗ | ✗ | △ | ✗ | ✗ |
| Portfolio-Risk | △ | △ | ✗ | ✗ | ✗ | △ | ✗ | ✗ |
| Regime-Specialist | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Transition-Aware | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Cross-Stream | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

✓ = satisfies; △ = partial/debatable; ✗ = fails.

No candidate passes the complete gate. M50's pause was therefore correct.

---

## 3. Critical Evidence Limitation

**Confirmed and kept visible throughout.**

> The original custom-bot analysis document was not found on the filesystem.

Therefore:
- Custom-bot observations (R-Velocity, ATR, ADX, volume, session effects, cache freshness, portfolio clustering) = **USER-SUPPLIED OBSERVATIONS**.
- They are **NOT repository-audited empirical evidence.**
- They remain **OBSERVED / HYPOTHESIS**, and were not silently elevated to validated APEX findings in M50.

This limitation is material: the two highest-scoring candidates (Execution-State, Trade-Path) each depend on a user-supplied operational observation (execution/regime conditions; R-Velocity) whose primary source document is missing from the repository.

**Classification**: `EVIDENCE LIMITATION — REQUIRES FUTURE REPOSITORY AUDIT`.

The program does NOT search external data during this control session. The limitation is recorded so the Control Session can initiate a bounded repository audit of the custom-bot analysis only if/when separately authorized.

---

## 4. Execution-State Economics

**M50 score**: 34/60. **M50 classification**: genuine layer, hypothesis only.

**Control question (§6)**: Is this a genuinely NEW economic mechanism, or merely a cost/filter layer that should already be included in any future economic experiment?

**Adjudication**:
- The concept "a statistically valid signal becomes economically invalid when execution friction consumes the edge" is real and directly explains the SMC M1 failure pattern (BOS+OB gross +1.01 bp, CHOCH +0.89 bp vs ~18 bp cost).
- **However**, the R10/R11 governance already REQUIRES realistic frozen costs in every M3 experiment. Execution friction (spread, slippage, liquidity, commission, rollover, stale information) is the **cost layer that is supposed to be part of any future economic experiment**, not a separate compensated-risk payoff.
- The one concrete observed trigger (stale cache → poor entry) is a **system/engineering defect**, not a market/execution state that systematically predicts positive vs negative expectancy.
- A genuine execution-state module would require the stronger claim (a measurable, ex-ante market/execution state that predicts whether otherwise-valid exposure turns net-positive or net-negative) — but establishing this requires an M4 base module (none exists) and repository-audited data.

**Verdict**: Primarily **ordinary execution/cost modeling** rather than a standalone new APEX economic mechanism. Not eligible for restart now. Hypotenuse preserved only as background note that cost realism remains mandatory in future experiments.

---

## 5. Trade-Path Economics

**M50 score**: 30/60. **M50 classification**: genuine layer, hypothesis only.

**Control question (§7)**: A genuinely different economic object from entry-signal prediction, or merely a discretionary exit/filter mechanism?

**Adjudication**:
- **Genuinely-new-object claim is the strongest conceptually**: "path state predicts conditional future payoff" is a different layer from APEX's historical predictive-entry focus.
- **However**: A legitimate new mechanism requires "path state → predictable change in future payoff distribution," NOT merely "losing trades tend to keep losing." The custom-bot evidence (R-Velocity early deterioration) is B-class user-supplied and its source document is missing.
- Trade-path management is fundamentally a **decision / exit / risk-modifier** (R11 role C or D). It has no independent tradeable payoff disconnected from the entry module it manages — and **M4 = 0**, so there is no base module whose path is being managed.
- The compensation chain is weak: early-loss avoidance preserves capital rather than capturing a distinct externally-compensated risk.

**Verdict**: Conceptually the most novel, but it is closer to **exit/decision optimization** than a distinct compensated-risk mechanism, it has no validated base module to act on, and its observational support is not repository-audited. Not eligible for restart now.

---

## 6. Portfolio-Risk Economics

**M50 score**: 29/60. **M50 classification**: architectural inference.

**Control question (§8)**: Risk-mgmt engineering only, or a potentially independent economic module?

**Adjudication**:
- A legitimate portfolio/exposure module would need a measurable economic role: "aggregate exposure state predicts nonlinear portfolio loss / execution risk, managed with positive economic value."
- This is a genuine future architectural layer (R11 role C overlay; Architecture B signal→risk→allocation).
- **However**: with M4 = 0 there is no portfolio of independently validated modules to manage. The module has NO independent E[R_net]>0 testable payoff disconnected from the modules it overlays. Drawdown-concentration observations (B-class) are not evidence of an M4 module.

**Verdict**: **Risk-management engineering only (A)** at present. A potentially valuable architectural layer, but not an independent economic module and not currently authorizable. Not eligible for restart now.

---

## 7. Regime-Specialist Economics

**M50 score**: 27/60. **M50 classification**: not sufficiently mature / filter-mining risk.

**Adjudication (§9)**: The proper question — "does a pre-existing, independently justified market state define a genuinely different economic opportunity?" — is NOT answered by the observations. The observed dimensions (ADX, ATR, volume, session) are outcome-leaning and, absent an independent economic regime definition, violate the R11 regime-mining prohibition. No M4 base exists to specialize. **Rejected.**

---

## 8. Session-Transition Research

**M50 score**: 20/60. **M50 classification**: weak / conflicts with existing closure.

**Adjudication (§10)**: APEX established LNO → different return distribution → scale/dispersion component, but M42 rejected the standalone and modular economic mechanism (deterministic, no location asymmetry, no base). No new economic mechanism or payoff is identified that was not already rejected. **Session-transition = PRESERVED BACKGROUND.** Cannot restart a session-distribution decomposition. **Rejected.**

---

## 9. Cross-Stream APEX + SMC

**M50 score**: 17/60. **Rejected.**

**Adjudication (§11)**: M4 = 0 on both sides, so no combined APEX/SMC module research is authorized. A future interaction requires independently validated components first. **Rejected (combination-mining).**

---

## 10. Rare-Event Governance

**Adjudication (§12)**: R11 is preserved: rare ≠ weak, rare ≠ automatically valid. A future rare event may qualify only with objective definition + economic mechanism + positive-net hypothesis + sufficient evidence + realistic costs + falsification. No arbitrary minimum frequency; no lowering the evidentiary standard because an event is rare. **No current rare event satisfies these conditions** (BOS+OB and CHOCH both closed).

---

## 11. M3 / M4 / M5 Governance

**Preserved unchanged (§13)**: M3 = positive net expectancy + appropriate evidence + realistic frozen costs + clear economic role + predeclared falsification. M4 = M3 + independent validation + OOS validation + execution realism + known risk characteristics. M5 = M4 + production execution validation + capital/risk/capacity suitability. **No levels collapsed.**

---

## 12. Failed Artifact Reuse

**BOS+OB and CHOCH remain CLOSED at their tested economic scopes (§14).** They cannot automatically become filters, confirmations, risk modifiers, regime labels, or path-management modules. Any reuse requires a new economic hypothesis. **Preserved.**

---

## 13. Scientific Novelty Audit (§15)

| Candidate | Classification |
|-----------|----------------|
| Execution-State | Potentially new economic object (edge-vs-friction); here judged largely cost/execution modeling |
| Trade-Path | Potentially genuinely new (path state → conditional future payoff) |
| Portfolio-Risk | New architectural layer, not a current economic object |
| Regime-Specialist | Rescue/filter engineering risk |
| Transition-Aware | NEW REPRESENTATION OF OLD KNOWLEDGE (reopens M42 session-transition) |
| Cross-Stream | Repackaging / combination-mining |

No candidate is a currently-validated genuinely-new economic object with a payoff.

---

## 14. Vertical-Progress Test (§16)

No candidate advances `validated information → economic mechanism → positive net expectancy → M4 → M5`. Every leading candidate either:
- Requires an M4 base module that does not exist (Execution-State, Trade-Path, Portfolio-Risk), or
- Re-expresses validated/library knowledge without a new economic translation (Regime, Transition, Cross-Stream), or
- Depends on non-audited user-supplied evidence (Execution-State, Trade-Path).

None escapes M0/M1/M2 descriptive/lateral status; none reaches the M2→M3 economic translation that the Independent Audit identified as the programme's bottleneck.

---

## 15. Candidate Scorecard

| Candidate | M50 score | New economic object | Independent payoff | Repository-audited evidence | Restart gate | Control verdict |
|-----------|:---:|:---:|:---:|:---:|:---:|---|
| Execution-State | 34 | △ (mostly cost modeling) | ✗ | ✗ | FAIL | Reject — cost/execution layer, no base |
| Trade-Path | 30 | △ (strongest conceptually) | ✗ | ✗ | FAIL | Reject — exit optimization, no base, missing doc |
| Portfolio-Risk | 29 | △ (architectural) | ✗ | ✗ | FAIL | Reject — risk-mgmt engineering, no portfolio |
| Regime-Specialist | 27 | ✗ | ✗ | ✗ | FAIL | Reject — regime-mining risk |
| Transition-Aware | 20 | ✗ | ✗ | ✗ | FAIL | Reject — reopens M42 closure |
| Cross-Stream | 17 | ✗ | ✗ | ✗ | FAIL | Reject — combination-mining |

No candidate passes the complete restart gate. **Scores are discovery aids only, not evidence of economic value.**

---

## 16. Top Candidate

**NONE.** No candidate earns the right to become M51.

---

## 17. Decision

**A — KEEP APEX PAUSED**

**No candidate has enough economic substance to deserve a new methodology cycle.**

### Rationale
1. **M4 = 0**: Every leading candidate (Execution-State, Trade-Path, Portfolio-Risk) is an overlay/risk/execution layer that requires an independently validated base module that does not exist. None has an independent tradeable payoff.
2. **Execution-State is largely cost/execution modeling** — the frozen-cost layer already mandatory in all future experiments — not a standalone new economic mechanism.
3. **Trade-Path is conceptually novel but reads as exit/decision optimization** on a nonexistent base, and depends on the missing, non-audited R-Velocity observation.
4. **Portfolio-Risk is risk-management engineering only** without a validated module portfolio.
5. **Regime / Transition / Cross-Stream** are rejected on regime-mining, closed-path (M42), and combination-mining grounds.
6. **Material evidence limitation**: the custom-bot document is missing from the repository; none of the user-supplied operational observations is independently auditable, so none can support an M3/M4 evidence requirement.
7. The directive explicitly permits "NO CURRENT CANDIDATE EARNS RESTART" and warns against manufacturing a candidate from scores.

**Option C (narrow discovery audit) was considered and not selected**: the genuine domains (execution, trade-path) are not currently independent economic mechanisms, and a discovery audit could not proceed without either the missing document or a validated base module — neither exists. A C-audit would risk becoming an unauthorized search.

---

## 18. What Must Change Before Any Restart

None of the following alone authorizes restart, but any future genuine candidate must:
1. Identify a **genuinely new economic object** with an **identifiable, independent payoff** (not an overlay of a nonexistent base).
2. Ground its evidence in **repository-audited data** OR explicitly flag `EVIDENCE LIMITATION — REQUIRES FUTURE REPOSITORY AUDIT` (as here).
3. Have an **M4 base module** if it is an execution / trade-path / portfolio / regime-specialist overlay.
4. Complete the R10/R11 economic-mechanism chain and state a **frozen, falsifiable M3 hypothesis** with realistic costs.

The prerequisite for the three leading candidates is therefore: **a validated M4 base module (or a repository-audited new mechanism with its own payoff) must first exist.** No such module exists. No such mechanism is currently articulated.

---

## 19. Answers to Final Control Questions

1. **Did M50 preserve the validated-vs-observational distinction?** Yes. Custom-bot observations were classified B/OBSERVED, C/HYPOTHESIS, D/ARCHITECTURAL and were not elevated to validated APEX evidence.
2. **Is the missing custom-bot document a material evidence limitation?** Yes. It is `EVIDENCE LIMITATION — REQUIRES FUTURE REPOSITORY AUDIT`, and it blocks the two highest-scoring candidates from being elevated.
3. **Is Execution-State a genuinely new mechanism or execution filtering?** Predominantly execution/cost modeling (the mandatory frozen-cost layer), not a standalone new mechanism. Rejected.
4. **Is Trade-Path a genuinely new object or exit optimization?** Conceptually the most novel, but functionally exit/decision optimization on a nonexistent base with non-audited evidence. Rejected now.
5. **Can Portfolio-Risk become an independent economic module?** Only as a future architectural layer once M4 modules exist; not independent today. Rejected now.
6. **Does regime specialization represent a new mechanism or filter mining?** Filter/regime mining risk (R11). Rejected.
7. **Does session-transition support a new mechanism?** No; M42 closure stands. Session-transition = preserved background.
8. **Any cross-APEX/SMC independent economic rationale?** No; M4=0. Rejected.
9. **Can a rare positive-net module qualify under R10/R11?** Yes in principle; none currently satisfies the conditions.
10. **Does any candidate satisfy the complete restart gate?** No.
11. **Should APEX remain paused?** Yes.

---

## 20. Required Outputs

- This adjudication report
- `reports/APEX_POST_M50_CONTROL_SCORECARD.csv`
- `reports/APEX_POST_M50_CONTROL_RESULT.md`
- Updated `docs/APEX_SESSION_HANDOFF.md`
- Updated `docs/APEX_SESSION_STATE.json`

**No methodology created (Decision A). No experiment scripts created.**

**External API calls: 0 | New data acquired: 0 | Spend: $0.00**
