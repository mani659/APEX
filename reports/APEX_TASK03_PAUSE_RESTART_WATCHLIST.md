# APEX TASK 03 — PAUSE & RESTART WATCHLIST / DORMANT-STATE CONTROL

**Date**: 2026-08-30
**Task type**: GOVERNANCE / DOCUMENTATION ONLY
**Authoritative state (unchanged by this task)**: `APEX = PAUSED / DORMANT`; **M3 = 0, M4 = 0, M5 = 0**; no active research milestone; no authorized experiment / methodology / data acquisition / strategy modification; **no M51**.

---

## 1. Purpose

This task converts the existing APEX pause into a **formally documented DORMANT / WATCHLIST STATE** with:

1. An explicit inventory of **what may and may not change** while APEX is dormant.
2. A **restart gate (R1–R10)** that must be satisfied before any resumption of active research.
3. A **restart decision-state ladder (A–E)** governing how far any candidate may progress.
4. A **permanent watchlist** of mechanism items (W1, W2) and external triggers (T1–T5).
5. The **closed-path immutability** rule and the **prohibited restart paths** (all clearly labeled).
6. An explicit **future-session safety check** and **future Control Session procedure**.

This is a **governance contract**, not a research programme. It authorizes **no** research on its own.

---

## 2. Current Authoritative State (Recorded, Not Changed)

| Field | Value |
| --- | --- |
| Programme state | `APEX = PAUSED / DORMANT` |
| Economic hypothesis | `UNTESTED` |
| M3 (frozen falsifiable economic hypothesis) | **0** |
| M4 (validated base economic module) | **0** |
| M5 (deployment candidate) | **0** |
| Active research milestone | NONE |
| Custom-bot Week-6 document on disk | NOT FOUND (repository-audited NO) |
| External data authorized | NONE (0 acquired) |
| API calls / experiments / spend | 0 / 0 / $0 |

### Task history leading to dormancy
- **TASK 01** — Economic Knowledge & Closed-Path Map (2026-08-30): repository-only audit; M3=M4=M5=0 confirmed; closed paths C01–C14 documented.
- **TASK 01-R1** — RC012 Study-006 Adjudication (2026-08-30): NO M3/M4/M5 qualification; evidence-classification clarification only.
- **TASK 02** — Economic Mechanism Discovery (2026-08-30): 24 candidates surveyed (categories A–J); **21 rejected (Tier 0)**, **3 retained as Tier 1** (G1, G2, I2) forming **2 mechanism themes**, **0 Tier 2**, **0 Tier 3**; final verdict: **NO GENUINELY NEW ECONOMIC MECHANISM IDENTIFIED** as a current, accessible, independently-payoff M3/M4 candidate.
- **TASK 03** — This task: formalize dormancy + watchlist.

**Why paused:** No validated M4 base module exists; no repository-audited genuinely-new economic mechanism with an independent payoff is articulated; every leading candidate is an overlay/execution/portfolio layer on a nonexistent base.

---

## 3. Watchlist — Mechanism Items (W1, W2)

These are the ONLY two mechanism-level items surviving the Task 02 survey. They are retained for **watchlist-only** monitoring. **Neither is a current M3/M4 nominee.** Neither authorizes any action today.

### W1 — Commodity Convenience Yield / Inventory Term Structure
- **Source rows**: G1 / G2.
- **Mechanism**: Commodity futures-curve term structure embeds an inventory/convenience-yield economy (backwardation/contango), distinct from the **closed M49 funding/carry** path (perpetual-swap funding) and distinct from realized-volatility economics.
- **Why not merely a rename of a closed path**: different instrument class (commodity futures curve vs perp funding), different compensation object (inventory/convenience yield vs funding rate), different observable (term-structure slope/spread vs perp funding intervals).
- **Genuine**: Yes — a real mechanism + a real instrument class.
- **Independent payoff**: Plausible, and distinct from vol economics.
- **Coherent evidence chain**: Present in outline.
- **BLOCKER**: **No futures-curve dataset exists in APEX**, and no such data acquisition is authorized while dormant.
- **Classification**: **C — HYPOTHESIS / D — ARCHITECTURAL INFERENCE**. **NO A-class auditable evidence.**
- **Restart link**: External-development trigger — **T1** (with M45 Conditions A/D). See §6.

### W2 — New Liquid Venue / Instrument Carrying Existing Validated Vol Info with an Independent Economic Payoff
- **Source row**: I2 (prediction market / DeFi options / vol-linked structured product).
- **Mechanism**: APEX holds **validated non-directional volatility information** (HIGH_VOL, session-transition LNO, BTC transfer). That information is already **fully priced into existing options IV** (per IC7) and therefore offers no residual edge on *existing* listed/crypto options.
- **Genuine**: Yes (conceptually), but only if a **new** instrument/venue exists where the same vol information has a **separate, not-yet-arbitraged** economic payoff.
- **Independent payoff**: Would be independent of existing options IV.
- **BLOCKER**: **No such instrument/venue exists or is observable today** (IC8 §4D, RC015). The venue must arise externally.
- **Classification**: **C — HYPOTHESIS / D — ARCHITECTURAL INFERENCE**. **NO A-class auditable evidence.**
- **Restart link**: External-development trigger — **T2** (with M45 Conditions A/D). See §6.

> **Governance guarantee:** W1 and W2 are **WATCHLIST-ONLY**. Watching them is a passive monitoring posture. Their activation **only** moves the programme from STATE A to STATE B (watchlist review) — see §5 and §6. **They never self-authorize an experiment.**

---

## 4. Restart Gate R1–R10

Before **any** candidate (including W1, W2, or any future external-discovered mechanism) may be advanced beyond STATE B, the candidate must satisfy **ALL** of the following gates. A failure at any single gate is terminal for that candidate's progression at that time.

| Gate | Criterion | Current status (all candidates) |
| --- | --- | --- |
| R1 | Genuine economic novelty (not a rename/repackaging/rescue of a closed path) | BLOCKED — no candidate clears this today |
| R2 | Independent economic object (not an overlay of a nonexistent base) | BLOCKED — overlays all lack M4 base |
| R3 | Identifiable compensation (what is the economically-compensated risk) | BLOCKED for current candidate set |
| R4 | Accessible payoff (instrument + costs that let the compensation be monetized) | BLOCKED — W1 lacks futures data; W2 has no venue |
| R5 | Auditable evidence (repository-audited, or explicitly flagged-and-waived) | BLOCKED — no A-class evidence for W1/W2 |
| R6 | Validated M4 base where required (**overlays require existing M4 = 0 → cannot restart**) | HARD BLOCK — M4 = 0 |
| R7 | Frozen falsifiable M3 hypothesis (written, framed before execution) | NOT PRESENT for any candidate |
| R8 | No lookahead (leakage-free design) | NOT DESIGNED |
| R9 | Realistic costs (frozen execution/cost layer) | NOT DESIGNED |
| R10 | No research rescue (do not reverse-engineer a conclusion to justify a restart) | CONSTRAINT — must hold |

**M45 restart conditions (external-development triggers)** referenced by W1/W2: **Condition A** (a genuinely new economic object becomes accessible) and **Condition D** (new data/instrument availability that unlocks an independent payoff). These map to triggers **T1** and **T2** in §6.

---

## 5. Restart Decision States (Ladder A–E)

A candidate may move **only** to the next authorized state; each state requires an explicit Control Session decision to advance.

| State | Description | Authorizes |
| --- | --- | --- |
| **A** | Remain DORMANT (no candidate under active consideration) | NOTHING (default) |
| **B** | Watchlist REVIEW (a trigger fired; candidate reviewed against gate) | Reading + evaluation ONLY. NO experiment, data, or methodology. |
| **C** | Mechanism review AUTHORIZED | Articulation/refinement of the economic mechanism + evidence classification ONLY. NO experiment. |
| **D** | Methodology design AUTHORIZED (Control-only) | Writing a frozen methodology (M3 framing, gates, costs, no-lookahead). NO empirical execution. |
| **E** | Empirical execution AUTHORIZED | Running the frozen experiment — **only after freeze + pre-execution validation** (per R7/R8/R9). |

> **Immutability of progression:** A trigger moves the programme from **A → B only**. Moving **B → C → D → E** is a sequence of separate, explicit Control Session authorizations. **Nothing auto-advances beyond B.**

---

## 6. Watchlist External Triggers (T1–T5)

A trigger **activates REVIEW (A → B)**, not experimentation. Triggers are conditions to monitor while dormant; they do not, by themselves, authorize any research.

| Trigger | Description | What it activates |
| --- | --- | --- |
| **T1** | A new, accessible **futures-curve dataset** becomes available in the repository | REVIEW of **W1** (STATE B only) |
| **T2** | A new, liquid, tradable **instrument/venue** becomes available where validated vol info has an independent payoff | REVIEW of **W2** (STATE B only) |
| **T3** | **Repository discovery** of missing evidence (e.g., custom-bot Week-6 document found) | EVIDENCE REVIEW ONLY — re-classification, NOT research authorization |
| **T4** | An **independently documented economic mechanism** arises OUTSIDE the closed set | REVIEW as a new candidate (STATE B only) |
| **T5** | A **validated M4 module** is discovered in the repository | Overlay-Eligibility review only (enables future R6, does not itself authorize a restart) |

### Trigger semantics
- **T3 note:** Finding the missing custom-bot document would **NOT** auto-authorize research. It would trigger **evidence classification + repository audit only**; observations would remain `B — USER-SUPPLIED / OBSERVED` until properly classified and audited. It does **not** create an M4 module and does not unlock overlays.
- **T5 note:** Locating a previously-overlooked validated M4 module would relieve the R6 overlay blocker but **still** requires every other gate (R1–R5, R7–R10) and a positive M3 framing before any execution.

---

## 7. Closed-Path Immutability

The following economic paths are **CLOSED and must remain closed** absent a **materially different economic mechanism** (not a rename, repackaging, or rescue):

1. HIGH_VOL economics (M34)
2. Session raw breakout (RC013)
3. Session-transition STANDALONE / MODULAR economics (M42)
4. CME listed options (RC015)
5. Crypto-options / IV-RV / long straddle (IC7/IC8)
6. BOS + Order Block (SMC-R7)
7. CHOCH (SMC-R9-CR)
8. Cross-asset transmission (RC014)
9. Funding/carry (M49)
10. RC012 Study-006 synthetic-straddle proof-of-concept (non-deployable; not M4)
11. Execution-State overlay (requires M4 base)
12. Trade-Path / R-Velocity overlay (requires M4 base + audited B-class evidence)
13. Portfolio-Risk overlay (requires M4 modules)
14. Regime-specialist overlay (rejected, R11 regime-mining)
15. Cross-stream combination mining (rejected, M4 = 0)

> Reopening **any** closed path requires a genuinely new economic mechanism, full execution of the restart gate (R1–R10), and explicit Control Session authorization. **Renaming a closed path is prohibited** (see §8).

---

## 8. Prohibited Restart Paths (Explicitly Documented)

The following are **PROHIBITED as restart justifications**, even though they are superficially "new":
- Signal / model optimization
- Regime / filter optimization
- Exit optimization
- Risk / portfolio optimization
- Execution optimization
- Timeframe substitution
- Instrument substitution (where the economic mechanism is unchanged)
- **Terminology change (renaming)** — relabeling a closed or rejected path to present it as new

These are **not new economic mechanisms**; they are re-parameterisation or repackaging of existing, closed content.

---

## 9. Custom-Bot Evidence Limitation (verbatim, must remain visible)

> **EVIDENCE LIMITATION — REQUIRES FUTURE REPOSITORY AUDIT**

The original custom-bot **Week-6 analysis document was NOT found in the repository**. Its observations (R-Velocity, ATR, ADX, volume, session effects, stale cache, portfolio clustering, execution) remain **`B — USER-SUPPLIED / OBSERVED`**, **NOT validated APEX evidence**.

- They are **OBSERVED / HYPOTHESIS**, not repository-audited empirical proof.
- They are not elevated to validated APEX findings and cannot support an M3/M4 evidence requirement.
- Finding the document later would **NOT** auto-authorize research; it would require **evidence classification + repository audit** only (trigger T3), and would not unlock Execution-State/Trade-Path overlays without a validated M4 base module.

---

## 10. Dormant-State Operating Rule

While `APEX = PAUSED / DORMANT`, the default and only safe action is **STOP**.

**Permitted while dormant (governance/housekeeping only):**
- Reading repository files to confirm state.
- Maintaining this watchlist and recording external events (T1–T5 observations) in governance documents.
- Maintaining audit/security posture (e.g., `.gitignore` hygiene) — no research content.

**Forbidden while dormant:**
- Acquiring data (API = 0, data = 0).
- Running experiments or backtests (experiments = 0).
- Building/receiving methodology (except a Control-authorized STATE D design).
- Modifying the bot, strategy, signals, filters, risk, or portfolio logic.
- Reopening any closed path.
- Starting M51 or any milestone automatically.
- Treating user-supplied observations as validated evidence.

---

## 11. Future-Session Safety Check (mandatory, every session)

Every future session MUST, at the start:
1. Read `docs/APEX_SESSION_HANDOFF.md`.
2. Read `docs/APEX_SESSION_STATE.json`.
3. Determine: `current_state`, `current_authorization`, `closed_paths`, `restart_conditions`.
4. If `APEX = PAUSED` → **default action is STOP** and do not proceed without an explicit Control Session authorization for the specific action.

---

## 12. Future Control Session Procedure (for a genuine restart consideration)

If a Control Session wishes to consider a restart:
1. Confirm a trigger-fired REVIEW (STATE A → B) via this watchlist, OR a genuinely new external-development event documented to the Control Session.
2. Run the candidate against **all** gates R1–R10 (a signed record required).
3. If R-gates pass through R6/R7, move to STATE C (mechanism review) then STATE D (methodology design) — **each a separate explicit authorization**.
4. Freeze a falsifiable M3 hypothesis + realistic costs + no-lookahead controls.
5. Only then consider STATE E (empirical execution), with pre-execution validation.
6. Record the decision in `docs/APEX_SESSION_HANDOFF.md` and `docs/APEX_SESSION_STATE.json`.

A restart is a **control decision**, never an automatic consequence of trigger observation.

---

## 13. Contradiction Handling

If any future source contradicts the dormant state or this watchlist, do **NOT** silently resolve it. Record a **CONTRADICTION** entry with: (Source A, Source B, Nature, Materiality, Effect on dormant state, Control decision required). **Contradictions never authorize research.**

---

## 14. Compliance Statement

| Compliance item | Value |
| --- | --- |
| API calls | **0** |
| Data acquired | **0** |
| Experiments run | **0** |
| Spend | **$0** |
| New milestone invented | **NONE** (governance task only) |
| Files modified | New reports only (+ governance state files per §17) |
| M3 / M4 / M5 | **0 / 0 / 0** (unchanged) |
| Programme state | `APEX = PAUSED / DORMANT` (unchanged) |
