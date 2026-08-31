# APEX M46: SMC-Derived Research Integration & Programme Re-Entry

**Milestone**: APEX-M46
**Date**: 2026-08-29
**Status**: COMPLETE
**Purpose**: Formally embed SMC-derived research workstream into APEX governance; reconcile history; establish current combined state

---

## A — Why SMC Entered APEX

After APEX M45 closed the current research cycle (PAUSED), a separate SMC strategy/knowledge base was introduced as a NEW SOURCE OF RESEARCH HYPOTHESES. The SMC stream was executed using APEX research/control principles and subsequently physically preserved inside the APEX repository at `research/SMC_RESEARCH/`.

The SMC work was NOT an independent master programme. It was a research workstream performed AFTER APEX M45 using SMC knowledge as the hypothesis-generation source.

---

## B — Exact Research Lineage from M45 Onward

```
APEX M45 (2026-08-27): Research-Cycle Closure, Evidence Ledger & Restart Conditions
    DECISION: A — CURRENT CYCLE CLOSED / PAUSED
    ↓
Post-M45: SMC knowledge introduced as new hypothesis source
    ↓
SMC-R1 (2026-08-27): Formalization / Structural Model Specifications
    DECISION: FRAMEWORK COMPLETE
    ↓
SMC-R2 (2026-08-27): Extraction Validation
    DECISION: EXTRACTION VALID
    ↓
SMC-R3 (2026-08-27): BOS+OB Economic Methodology
    DECISION: METHODOLOGY FROZEN (with CR, CR2 amendments)
    ↓
SMC-R4 (2026-08-27): BOS+OB Experiment
    DECISION: POSITIVE EXPECTANCY (+1.01 bps gross, 123,386 events)
    ↓
SMC-R5 (2026-08-27): BOS+OB M4 Qualification Methodology
    DECISION: M4 METHODOLOGY FROZEN
    ↓
SMC-R6 (2026-08-27): BOS+OB M4 Qualification Experiment
    DECISION: M4 FAILED
    ↓
SMC-R7 (2026-08-27): BOS+OB Programme Adjudication
    DECISION: BOS+OB CLOSED
    ↓
SMC-R8 (2026-08-27): CHOCH Methodology
    DECISION: CHOCH METHODOLOGY FROZEN (with CR amendments)
    ↓
SMC-R9 (2026-08-27): CHOCH Experiment
    DECISION: M3 FAILED (+0.89 bps gross, -17.03 bps net, 7,483 events)
    ↓
SMC-R9-CR (2026-08-27): Programme Closure
    DECISION: SMC M1 CYCLE CLOSED
    ↓
SMC-R10 (2026-08-27): Economic Qualification Framework
    DECISION: QUALIFICATION FRAMEWORK ESTABLISHED
    ↓
SMC-R11 (2026-08-27): Rare-Event Module Framework + Bot Architecture Governance
    DECISION: FRAMEWORK COMPLETE
    ↓
APEX-M46 (2026-08-29): SMC Research Integration & Re-Entry Audit
    THIS MILESTONE
```

**Namespace distinction preserved:**
- APEX milestones: `APEX-Mxx` (M00 through M45, AR1, IC1-IC9)
- SMC milestones: `SMC-Rxx` (R1 through R11)

No renaming of historical SMC milestones. Clear namespace separation within integrated governance.

---

## C — SMC-R1 to R11 Milestone Summary

| Milestone | Purpose | Decision | Key Evidence |
|-----------|---------|----------|--------------|
| SMC-R1 | Formalize SMC structural primitives | FRAMEWORK COMPLETE | BOS, OB, FVG, CHOCH, sweeps, swings, freshness |
| SMC-R2 | Validate deterministic extraction | EXTRACTION VALID | 123k BOS, 23M FVG, 8M OBs, 7.5M swings on XAUUSD M1 |
| SMC-R3 | BOS+OB economic methodology | METHODOLOGY FROZEN | Long/Short rules, TP/SL, 12h max hold |
| SMC-R4 | BOS+OB gross experiment | POSITIVE EXPECTANCY | +1.01 bps gross, 123,386 events |
| SMC-R5 | BOS+OB M4 qualification design | M4 METHODOLOGY FROZEN | Daily-level validation, dependence-aware |
| SMC-R6 | BOS+OB M4 qualification exec | M4 FAILED | Net < 0 after costs |
| SMC-R7 | BOS+OB adjudication | CLOSED | Economic path closed; info preserved |
| SMC-R8 | CHOCH methodology | METHODOLOGY FROZEN | Reversal rules, 4h max hold |
| SMC-R9 | CHOCH experiment | M3 FAILED | +0.89 bps gross, -17.03 bps net, 7,483 events |
| SMC-R9-CR | SMC M1 cycle closure | CYCLE CLOSED | No automatic restart |
| SMC-R10 | Economic qualification framework | FRAMEWORK ESTABLISHED | 4-level hierarchy, E[R_net] > 0 threshold |
| SMC-R11 | Rare-event + module governance | FRAMEWORK COMPLETE | Rare ≠ weak, module rules, Architecture A/B |

---

## D — Scientific Findings Preserved

**Validated Structural Primitives (Level 1 — Scientific Effect):**
- BOS (Break of Structure): deterministic, reproducible
- OB (Order Block): deterministic, reproducible
- FVG (Fair Value Gap): deterministic, reproducible
- CHOCH (Change of Character): deterministic, reproducible
- Liquidity Sweep: deterministic, reproducible
- Swing detection (N=5): deterministic, reproducible
- Freshness state machine: deterministic, reproducible

**Gross Effect Findings (Level 1):**
- BOS+OB: gross +1.01 bps/event (123,386 unique events)
- CHOCH: gross +0.89 bps/event (7,483 events)

Both effects are positive and statistically detectable. Both are below transaction-cost requirements on M1 XAUUSD under the tested architecture.

---

## E — Economic Findings Preserved

**BOS+OB:**
- Gross edge: +1.01 bps/event
- Net under tested M1 cost architecture: NEGATIVE
- M4 qualification: FAILED
- Economic path: CLOSED (SMC-R7)

**CHOCH:**
- Gross edge: +0.89 bps/event
- Net under tested M1 cost architecture: NEGATIVE (-17.03 bps net)
- M3 qualification: FAILED
- Economic path: CLOSED (SMC-R9-CR)

**Critical Distinction**: Scientific validity ≠ economic viability. The gross effects are real; the tested cost architectures make them economically non-viable on M1 XAUUSD.

---

## F — Closed Economic Paths

| Path | Status | Closure Milestone |
|------|--------|-------------------|
| BOS+OB standalone | CLOSED | SMC-R7 |
| BOS+OB M4 qualification | CLOSED | SMC-R6 |
| CHOCH standalone | CLOSED | SMC-R9-CR |
| SMC M1 cycle | CLOSED | SMC-R9-CR |
| Crypto-options path (APEX IC) | CLOSED | APEX IC8 |
| HIGH_VOL branch (APEX) | CLOSED | APEX M34 |

---

## G — R10/R11 Governance Principles Adopted into APEX-Wide Architecture

### 1. Four-Level Qualification Hierarchy (R10)
```
Level 1: Scientific Effect — "Does the event contain predictive information?"
Level 2: Economic Candidate (M3) — E[R_net] > 0 after realistic frozen costs
Level 3: Validated Economic Module (M4) — Survives stronger validation
Level 4: Deployment Candidate (M5) — Suitable for bot inclusion
```

### 2. Minimum Economic Threshold (R10)
$$E[R_{net}] > 0$$ after realistic, frozen transaction costs. **No universal minimum bps, dollars, annual return, or trade count.**

### 3. Evidence Sufficiency ≠ Event Frequency (R10)
Separate dimensions: frequency, evidence sufficiency, economic magnitude, aggregate contribution, scalability.

### 4. Rare-Event Framework (R11)
- `rare ≠ weak`, `frequent ≠ good`
- Evidence classifications: INSUFFICIENT / POSITIVE CANDIDATE / NEGATIVE / INCONCLUSIVE
- No universal N thresholds; Control Session decides per phenomenon
- `INCONCLUSIVE — EVIDENCE INSUFFICIENT` prevents both false rejection and false acceptance

### 5. Module Rules (R11)
- Each module must qualify independently (M4)
- Combination = new hypothesis with separate OOS
- Anti-combination-mining rule enforced
- Failed artifacts may inform but not rescue

### 6. Module Economic Roles (R11)
- Trade Generator (A)
- Regime Specialist (B)
- Risk/Exposure Modifier (C) — requires independent hypothesis
- Trade Suppressor (D) — requires independent hypothesis

### 7. Bot Architecture Principles (R11)
**Architecture A**: One independently validated killer strategy
**Architecture B**: Small number of validated specialist modules with market-state router
Both valid. Neither forced. Router itself must not be invented solely to make weak modules profitable.

### 8. Failed Artifact Reuse (R10/R11)
Failed standalone artifacts:
- Preserve as background knowledge for new hypotheses
- Do NOT automatically become filters, confirmations, regime labels, suppressors
- Reuse requires: new hypothesis + new methodology + independent validation + Control Session authorization

---

## H — Current M4/M5 State (Integrated)

| Category | Count | Details |
|----------|-------|---------|
| **M4 Modules** | 0 | None in APEX or SMC |
| **M5 Deployment Candidates** | 0 | None in APEX or SMC |
| **M3 Candidates** | 0 | BOS+OB (Level 2 FAIL), CHOCH (Level 2 FAIL), APEX candidates (all FAIL) |
| **M2 Predictive Primitives** | 3 (APEX) + 2 (SMC) | APEX: HIGH_VOL persistence, Session-transition scale, BTC C-index. SMC: BOS+OB gross, CHOCH gross |
| **M1 Scientific Primitives** | 4 (APEX) + 5+ (SMC) | APEX: HIGH_VOL, Session-transition, BTC risk score. SMC: BOS, OB, FVG, CHOCH, Sweeps, Swings |

---

## I — Future Bot Architecture (Integrated)

The integrated APEX programme preserves both final architectures:

**Architecture A — Single Dominant Strategy**
- One independently validated strategy (M4/M5)
- Sufficient on its own
- No need to manufacture modules

**Architecture B — Specialist Module Combination**
- Market-state router (M4) + 2-3 specialist modules (M4 each)
- Every component independently validates (M4+)
- Predeclared interaction mechanism
- Combined OOS validation required
- Anti-combination-mining: forbidden to test all combinations and pick best PnL

**Current Status**: Neither architecture has any M4+ components.
**Bot Readiness**: NOT READY

---

## J — What Remains Scientifically/Economically Unresolved

**Scientific Questions:**
1. Are there other SMC structural primitives with stronger gross effects on different instruments/timeframes?
2. Can session-transition scale effect (LNO 1.65× dispersion) be characterized further?
3. Does the BTC HIGH_VOL transferability (C-index = 0.6224) generalize to other crypto?
4. Are there rare SMC events with meaningful positive net expectancy?

**Economic Questions:**
1. What instrument class naturally captures non-directional volatility predictions?
2. Can any rare SMC event achieve E[R_net] > 0 on a different cost architecture?
3. Is there a genuinely new economic mechanism distinct from M1 continuation/CHOCH reversal?
4. Can multiple independently validated modules be discovered that genuinely complement?

**Governance Questions:**
1. How to evaluate "evidence sufficiency" for rare events without universal N thresholds?
2. What constitutes a "new hypothesis" vs "rescue of failed path"?

---

## K — Conditions for Future SMC-Derived Research (APEX Gate)

Per R10/R11 and APEX M45, a new SMC-derived research cycle may begin **only if at least ONE** exists:

- **A**: Genuinely new scientific primitive (observable, deterministic, falsifiable)
- **B**: Genuinely new economic mechanism (materially different from M1 continuation, M1 CHOCH reversal, failed cost-rescue paths)
- **C**: New instrument whose payoff structure matches a validated SMC information type
- **D**: New market regime hypothesis (not a filter added to existing failed strategy)
- **E**: Rare-event discovery with defensible payoff geometry
- **F**: New external evidence creating materially different research opportunity

**Forbidden triggers**: "Try another timeframe", "Try another stop", "Try another filter", "Try combination", "Pick best historical config", rescue without new hypothesis.

**Gate Questions (per R10):**
1. What new scientific/economic question is being asked?
2. Why is it distinct from closed paths?
3. What economic mechanism is hypothesized?
4. What is the minimum evidence needed?
5. What constitutes positive economics?
6. What constitutes deployment readiness?

---

## L — Current Authorization State

| Authorization | Status |
|---------------|--------|
| SMC-R12 (any new SMC experiment) | NOT AUTHORIZED |
| APEX-M47 (any new APEX experiment) | NOT AUTHORIZED |
| SMC-R1 through R11 historical work | PRESERVED / INTEGRATED |
| APEX M00-M45 historical work | PRESERVED |
| R10/R11 governance principles | ADOPTED into APEX-wide economic architecture |
| Next step | CONTROL SESSION REVIEW |

**Current integrated programme state**: PAUSED — awaiting Control Session decision on whether a genuinely new hypothesis exists.

---

## Summary

The SMC-derived research workstream (SMC-R1 through SMC-R11) is now formally embedded inside APEX as a **hypothesis-generation source / research branch**, not a competing master programme. The authoritative hierarchy is:

```
APEX (Master Research / Control Architecture)
│
├── Core RC Research (RC012-RC015 — all CLOSED)
│
├── APEX M-Series Research/Control (M00-M45 — cycle CLOSED)
│
└── SMC-Derived Research Branch
      ├── SMC-R1 through SMC-R11 (COMPLETE, HISTORICAL)
      ├── R10/R11 Governance Principles (ADOPTED APEX-WIDE)
      └── Current Authorization: NONE
```

All scientific findings, economic results, and governance frameworks are preserved without modification. The combined programme stands at a Control Session review point.