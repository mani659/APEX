# APEX CONTROL SESSION — RESEARCH RESTART REVIEW

**Session type**: Control / Adjudication (no experiment, no methodology, no data acquisition, no strategy/bot modification)
**Date**: 2026-08-30
**Status**: COMPLETE

---

## A. CURRENT STATE (one-page reconstruction)

Authoritative state confirmed by direct reading of `docs/APEX_SESSION_HANDOFF.md`, `docs/APEX_SESSION_STATE.json`, and the milestone result files:

```
APEX = PAUSED / AWAITING NEW ECONOMIC HYPOTHESIS
M4 validated economic modules = 0
M5 deployment candidates = 0
M3 economic candidates = 0
M1/M2 validated scientific/information primitives = 10+
No M51 authorized.
POST-M50 CONTROL = A — KEEP APEX PAUSED
```

**Core economic bottleneck (confirmed unchanged):**
> No validated M4 base module exists, and no repository-audited genuinely-new economic mechanism with an independent payoff has yet been articulated.

**Governance in force**: R10 four-level qualification hierarchy (Scientific Effect → Economic Candidate [E[R_net]>0 after realistic frozen costs] → Validated Module → Deployment Candidate); R11 rare-event/module framework; R11 bot-architecture governance (anti-combination-mining, anti-regime-mining, anti-filter-rescue). Frozen methodology documents M15/M36 unchanged.

---

## B. EVIDENCE LEDGER

Each finding below was **re-verified against the actual repository result files** (not from the handoff summary alone).

### Validated surviving primitives (A-class, scientific/information only)

| Primitive | What was validated | Target | Econ. interp. | Independent payoff | M4? | Economic status |
|---|---|---|---|---|---|---|
| HIGH_VOL (RC012→M13) | Distributional primitive D=0.1927 | RV state | Vol regime exists | NO | NO (M1) | Closed economics |
| HIGH_VOL persistence (M13/M14) | Non-memoryless, p<0.0001, n=794 | RV persistence | Duration structure | NO | NO | Background |
| HIGH_VOL predictability (M17-R2) | C-index 0.6656 OOS | Episode duration | Predictive info | NO | NO (M2) | Background |
| HIGH_VOL→fwd RV (M21) | β=-0.0143, p=0.0032 | 12h RV | Scales forward RV | NO | NO (M2) | Background |
| HIGH_VOL→direction (M24) | **REJECTED**, p=0.6418 | 12h return | No direction | NO | NO | Closed |
| HIGH_VOL→excursion (M27) | p=7.5e-05, ratio 0.92 | MAE envelope | Near-symmetric boundary | NO | NO (M2) | Background |
| HIGH_VOL→boundary (M31) | **REJECTED**, 99.75% sat. | Boundary breach | No edge | NO | NO | Closed |
| Session-transition LNO (M39-R2) | AD=228.38, p=0.0001, d=0.0037 | 1h fwd returns | Vol regime (scale) | NO | NO (M1) | Economy closed (M42) |
| LNO scale (M41) | 1.65× dispersed, p=0.0001 | Dispersion | Vol magnitude | NO | NO | Economy closed (M42) |
| BTC transfer (IC3) | C-index 0.6224, fwd RV p=0.000011 | BTC RV | Cross-market predictive | NO | NO (M2) | Economic translation closed |

**Every validated finding is M1/M2 (scientific/predictive/distributional). None claims positive net-after-cost expectancy (E[R_net]>0). Each experimental report explicitly disclaims profitability/tradability/economic expectancy.**

### SMC-derived (Level 1 / M1)
- 7 deterministic structural primitives (BOS, OB, FVG, CHOCH, sweep, swing N=5, freshness): M1 deterministic, reproducible — but NOT economic.
- BOS+OB: gross +1.01 bp, net **-1,347 bp/day** (18× cost overwhelm) — M4 FAIL, CLOSED (SMC-R7).
- CHOCH: gross +0.89 bp, net **-17.03 bp**, OOS -9.64 bp — M3 FAIL, CLOSED (SMC-R9-CR).
- KMEANS/GMM/HDBSCAN trend-regime ML: **negative/rejected** (no predictive information over deterministic baseline).

### Custom-bot evidence (B/C/D — NOT repository-audited)
User-supplied operational observations: R-Velocity early-deterioration association; ATR/ADX/volume/session outcome differences; stale-cache→poor-entry; correlated drawdown concentration; regime UNKNOWN; missing spread/execution measurement. **NONE is A-class. NONE is validated.**

### No repository-audited new economic mechanism with an independent payoff exists.
No finding in the ledger qualifies as an M4 base module or an independent tradeable payoff.

---

## C. CLOSED-PATH CHECK

Verified all 13 documented closed paths remain closed and were NOT accidentally reopened by any candidate:

1. HIGH_VOL spot monetization (RC012 S007-011) — CLOSED
2. HIGH_VOL static boundary (M31) — CLOSED
3. HIGH_VOL dynamic translation (M33) — CLOSED
4. HIGH_VOL branch (M34) — CLOSED
5. Session raw breakout (RC013) — CLOSED
6. Session-transition LNO standalone/modular (M42) — CLOSED
7. Listed CME options (RC015) — CLOSED
8. Crypto long straddle (IC7) — CLOSED
9. Crypto alternatives (IC8) — CLOSED
10. BOS+OB M1 XAUUSD (SMC-R7) — CLOSED
11. CHOCH M1 XAUUSD (SMC-R9-CR) — CLOSED
12. Cross-asset structural transmission (RC014) — CLOSED
13. Funding / carry (M47→M48→M48-CR→M49) — CLOSED

**No candidate reopens any of these.** (Regime candidate = filter-mining risk, not a reopening; Transition candidate = rejected precisely because it would revisit the M42-closed session-transition knowledge with no new mechanism.)

---

## D. RESTART-GATE SCORECARD (R1–R10)

**Candidate discovery was NOT warranted by brainstorming.** First, the repository was searched for an overlooked validated M4 module / independent payoff / genuinely new unexplored mechanism. **None was found** (see §B: all validated findings are M1/M2; all economic tests negative/closed; KMEANS regime negative; no standalone custom-bot document). 

The only survivors from M50's formal survey (Execution-State, Trade-Path, Portfolio-Risk) were re-adjudicated against the mission's R1–R10 gate. All other M50 candidates (Regime, Transition, Cross-Stream) were already hard-rejected and are re-rejected without scoring (mining/closed-path/combination).

| Candidate | Economic object | Independent payoff (R2) | Evidence class (R3) | M4 status (R4) | Complete chain (R5) | Causal validity (R6) | Accessibility (R7) | Falsifiability (R8) | No rescue (R9) | Auditability (R10) | Gate result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Execution-State** (34/60) | Edge vs execution friction | **NO** — no base to protect; no independent payoff | B/D (engineered defect) | NO (overlay; M4=0) | NO | partial | NO (no base inst.) | not frozen | — | NO (missing doc) | **FAIL** |
| **Trade-Path** (30/60) | Path state→cond. payoff | **NO** — loss-avoidance, no distinct compensation stream | B (R-Velocity, missing doc) | NO (overlay/exit; M4=0) | NO (weak chain) | partial | NO (non-APEX data) | not frozen | — | NO (missing doc) | **FAIL** |
| **Portfolio-Risk** (29/60) | Correlated exposure mgmt | **NO** — no indep. E[R_net]>0; no portfolio | D (architectural) | NO (overlay; M4=0) | NO | partial | NO (no modules) | not frozen | — | NO | **FAIL** |
| Regime-Specialist | — | NO | B (outcome-leaning) | NO | NO | NO | NO | NO | **rescue/mining** | NO | **FAIL** |
| Transition-Aware | — | NO | B | NO | NO | NO | NO | NO | **reopens M42** | NO | **FAIL** |
| Cross-Stream | — | NO | — | NO (M4=0) | NO | NO | NO | NO | **combination-mining** | NO | **FAIL** |

**None passes the restart gate.** Each leading candidate is an overlay/execution/risk layer requiring a validated M4 base module that does not exist, and none has an independent payoff. The two top-scoring (Execution-State, Trade-Path) additionally depend on the missing, non-audited custom-bot document.

---

## E. MISSING EVIDENCE (what prevents restart)

1. **No validated M4 base module** (M4 = 0). Every leading candidate is an overlay with no base to condition.
2. **No repository-audited genuinely-new economic mechanism with an independent payoff.** All validated findings are M1/M2 scientific; every economic test (SMC-R7, SMC-R9, IC7, IC8, M42, M49, RC012, RC013, RC015) is negative and closed.
3. **The custom-bot Week-6 analysis document is missing from the repository.** Searched (filename AND content) across the entire apex tree and the broader `grid research` tree for `r-velocity / ghost / sniper / cab / unified runner / week-6`. The only matches are APEX's own governance/report files that *refer to* the analysis and unrelated telemetry logs. **No standalone source document exists on disk.** Its observations therefore remain `OBSERVED / HYPOTHESIS`, cannot be independently audited, and cannot support an M3/M4 evidence requirement.
4. **No frozen M3 hypothesis and no falsification condition** exist for any candidate.
5. **No overlooked new instrument class / new primitive / new predictive model / new mechanism** is present in the repository.

---

## F. CUSTOM-BOT EVIDENCE AUDIT DECISION

**Question**: Is a bounded repository audit justified?

**Finding from this Control Session's own search**: The custom-bot Week-6 analysis document does not exist on disk. I performed a comprehensive filename AND content search across the apex repository and the broader `grid research` tree; no such document exists (only internal references to it in APEX governance files).

**Adjudication under §16 decision-B criterion** — "Use this only if locating/auditing existing project evidence could **materially change the restart decision**":
- Even if the document were found, its observations would remain **B-class operational evidence**, requiring a full new M0→M1→M2 controlled validation programme on the bot's own (non-APEX, non-authorized) data to become validated.
- Critically, the Execution-State and Trade-Path candidates still **require a validated M4 base module** (none exists). Finding the document does NOT create that base and does NOT by itself satisfy the restart gate.
- Therefore locating the document would **not materially change the restart decision** — it would convert a documented evidence limitation into auditable hypothesis-generation material, not into a validated economic module.

**Decision**: A bounded repository audit is **NOT currently justified** under the mission's strict criterion. The audit is recorded as a **future optional action** the Control Session may authorize separately, but it is **not authorized now** and would not unblock restart on its own. The evidence limitation is preserved as `EVIDENCE LIMITATION — REQUIRES FUTURE REPOSITORY AUDIT`.

---

## G. FINAL CONTROL DECISION

# A — KEEP APEX PAUSED

**No candidate satisfies the restart gate. No repository-audited genuinely-new economic mechanism with an independent payoff exists. No validated M4 base module exists.**

This is the **scientifically correct outcome**, not a failure. The burden of proof on any restart is not met.

Rationale (all verified against the repository):
1. M4 = 0 — the single decisive bottleneck. Every leading candidate is an overlay/execution/risk layer with no validated base and no independent tradeable payoff.
2. Execution-State is largely the mandatory frozen-cost layer (already required by R10 in every future experiment), not a standalone new mechanism; its strongest observed trigger (stale cache) is an engineering defect.
3. Trade-Path is conceptually the most novel but reads as exit/decision optimization on a nonexistent base, with only missing, non-audited B-class support.
4. Portfolio-Risk is risk-management engineering without a validated module portfolio.
5. Regime / Transition / Cross-Stream are rejected on regime-mining, closed-path (M42), and combination-mining grounds.
6. The custom-bot document is absent from the repository; no user-supplied observation is independently auditable and none can support an M3/M4 evidence requirement.
7. No overlooked validated M4 module or independent payoff was found anywhere in the evidence base.

---

## H. AUTHORIZATION BOUNDARY

The next session IS **authorized** to:
- Read the authoritative state and governance files.
- Maintain/preserve the evidence ledger and closed-path registry.
- Record control outcomes and update session handoff/state (governance bookkeeping only).

The next session is **NOT authorized** to:
- Start M51 or any milestone.
- Run any experiment, backtest, PnL, or parameter/filter/threshold/timeframe/combination test.
- Acquire or download any data (internal or external).
- Design or build any methodology, filter, regime classifier, or EA.
- Modify any trading bot or the trading system.
- Reopen any closed path (HIGH_VOL economics, session breakout, session-transition economy, listed/crypto options, BOS+OB, CHOCH, cross-asset, funding/carry).
- Re-run the custom-bot evidence as validated.

---

## I. RESTART PREREQUISITES (if paused)

A genuine restart candidate must satisfy ALL of:
1. A **genuinely new economic object** with an identifiable, **independent payoff** (new source of compensation / payoff mechanism / accessible risk premium / microstructure mechanism / state-dependent payoff) — NOT a filter, regime, exit, execution, cost, portfolio-sizing, signal-combination, or parameter layer.
2. **Genuinely new = NOT a rebranding** of a closed path (same mechanism, changed target variable, changed instrument, added filter, combined weak signal, regime/parameter mining, portfolio aggregation without independent payoff, execution engineering spun as discovery).
3. **Repository-audited evidence** traceable to a file/dataset/methodology/experiment/result — OR explicitly flagged `EVIDENCE LIMITATION — REQUIRES FUTURE REPOSITORY AUDIT` (never treated as proof).
4. A **validated M4 base module** if the candidate is an execution / trade-path / portfolio / regime-specialist overlay (an overlay without an independent payoff must fail).
5. A **complete R10/R11 economic chain**: Information → Economic State → Compensated Risk/Mechanism → Accessible Payoff → Net Expectancy → Falsifiable Hypothesis, with a **frozen, falsifiable M3 hypothesis (E[R_net]>0)** and **realistic frozen costs**.
6. **No lookahead** (causal/temporal validity) and **falsification defined ex-ante** — no repeated redefinition after observing results.

No candidate currently satisfies these. APEX remains PAUSED.

---

## J. IF AUDIT AUTHORIZED (scope and stopping condition) — NOT CURRENTLY AUTHORIZED

Because Decision is A, no audit is authorized. If the Control Session later authorizes it, the bounded scope would be:
- Search repository/project directories for the original Week-6 analysis by filename and content.
- Inspect logs/reports/data already present for any bot-operational evidence.
- **Stop immediately** when the document is either (a) located (record path/provenance/reproducibility, evaluate whether it can support a future M3/M4 hypothesis, reconcile against this report) or (b) confirmed absent (preserve `EVIDENCE LIMITATION — REQUIRES FUTURE REPOSITORY AUDIT` and return to Control Session).
- **Must NOT** acquire external data, run experiments, create strategies, optimize the bot, or convert observations into validated findings.

This report's own search already indicates outcome (b) is the expected result.

---

## K. IF METHODOLOGY AUTHORIZED (design scope) — NOT CURRENTLY AUTHORIZED

Because Decision is A, no methodology-design cycle is authorized. No methodology scope is defined. This remains prohibited until a candidate passes the restart gate.

---

## Required Outputs
- This report: `reports/APEX_CONTROL_SESSION_RESTART_REVIEW.md`
- Scorecard: `reports/APEX_CONTROL_SESSION_RESTART_SCORECARD.csv`
- Result: `reports/APEX_CONTROL_SESSION_RESTART_RESULT.md`
- Session handoff/state update (governance bookkeeping)

**External API calls: 0 | New data acquired: 0 | Spend: $0.00**
**No experiment, methodology, data acquisition, or bot modification performed.**

---

## Answers to the Control Session's closing questions
- **Does the repository contain enough evidence to justify another research cycle on a genuinely independent economic mechanism?** NO.
- **Is this a successful control decision?** YES — preserving the programme in PAUSED is the correct scientific outcome; a pause is preferable to another sequence of statistically interesting but economically disconnected experiments.
