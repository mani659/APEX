# APEX AR1 — Module Qualification & Multi-Module Research Architecture Reset

**Date**: 2026-08-27
**Milestone**: AR1
**Status**: COMPLETE
**Classification**: Architecture / Governance design — no empirical work

---

## 1. Executive Summary

AR1 establishes the formal governance and research architecture for APEX's eventual bot construction. It defines what qualifies as a module, how modules mature through a lifecycle, how combination is governed, and what evidence level is required before a component enters the final bot.

**Decision: FRAMEWORK COMPLETE — PAUSED PENDING NEW SCIENTIFIC QUESTION**

The framework is ready. No current APEX artifact has reached M3 (Economic Candidate) or beyond. The programme remains paused pending a new instrument class, new predictive model, independently validated edge, or new market.

---

## 2. Current Programme State

```
Scientific discoveries    = STRONG (10 validated findings)
Predictive findings       = MULTIPLE (C-index 0.6656, 0.6224; p=0.000011, 0.0001)
Validated economic edge   = NONE
Standalone strategy       = NOT ESTABLISHED
Crypto-options path       = CLOSED (IC7/IC8)
Economic development      = PAUSED (M43)
Module candidates at M3+  = 0
```

---

## 3. The Six States of a Research Artifact

AR1 formally distinguishes these states:

| State | Name | Description | Example |
|-------|------|-------------|---------|
| 1 | Scientific Phenomenon | Interesting observation | "LNO dispersion differs" |
| 2 | Predictive Primitive | OOS predictive ability validated | "HIGH_VOL onset predicts persistence" |
| 3 | Economic Candidate | Concrete payoff mechanism exists | "Long straddle when predicted RV > IV" |
| 4 | Validated Economic Module | Positive expectancy / validated role established | (none currently) |
| 5 | Production Candidate | Execution and operational validation completed | (none currently) |
| 6 | Bot Component | Integrated into final architecture | (none currently) |

**Critical rule:** Only State 4 or later may contribute to the final bot candidate architecture.

---

## 4. Module Lifecycle (Maturity Scale)

### M0 — Phenomenon

An observation exists but has not survived formal testing.

**Evidence:** Anecdotal, exploratory, or preliminary.

### M1 — Validated Scientific Primitive

The phenomenon survives formal testing under a frozen methodology.

**Evidence:** Statistical significance under appropriate null; independence-aware inference; reproducible.

**APEX examples:** HIGH_VOL primitive (RC012), BTC transferability (IC3), LNO scale (M41).

### M2 — Predictive Primitive

The information has OOS predictive ability for a specific economic variable.

**Evidence:** Walk-forward or chronological OOS validation; predictive metric exceeds baseline.

**APEX examples:** HIGH_VOL persistence predictability (C-index 0.6656), BTC forward RV translation (p=0.000011).

### M3 — Economic Candidate

A concrete payoff mechanism exists and can be frozen ex ante.

**Evidence:** Frozen methodology; instrument identified; economic hypothesis stated; falsification criteria defined.

**APEX examples:** Long ATM straddle (IC5) — reached M3 but failed at M4.

### M4 — Validated Economic Module

The module demonstrates positive expectancy under strict OOS validation with realistic costs.

**Evidence:** Frozen methodology; positive expected value; appropriate statistical test; costs included; no post-hoc parameterization.

**APEX examples:** None currently.

### M5 — Production Candidate

The module additionally survives execution validation and operational testing.

**Evidence:** Forward/demo observation; execution verification; operational robustness.

**APEX examples:** None currently.

---

## 5. Module Qualification Checklist

A research artifact must satisfy ALL of the following to qualify as an M4 module:

### Scientific Foundation
- [ ] Underlying phenomenon is independently validated (M1+)
- [ ] Predictive value is established where applicable (M2+)

### Economic Role
- [ ] Module has a specific risk/payoff job (not "interesting indicator")
- [ ] Module role is defined within a larger architecture
- [ ] Economic compensation mechanism is articulated

### Frozen Definition
- [ ] Module activation rules are frozen ex ante
- [ ] Module role cannot be changed after seeing outcomes
- [ ] Entry/exit/payoff rules are frozen (if trade generator)

### Positive Expectancy
- [ ] If trade generator: standalone positive expectancy established
- [ ] If modifier: conditioning hypothesis independently validated
- [ ] Costs are included
- [ ] OOS chronological validation passed

### Evidence Sufficiency
- [ ] Enough independent evidence to distinguish signal from noise
- [ ] Effect is stable across the validation period
- [ ] No post-hoc parameterization used

### Independence
- [ ] Scientifically independent from other modules (evidence established separately)
- [ ] Economically independent (distinct risk/payoff mechanism)

---

## 6. Module Roles (Controlled Taxonomy)

| Role | Definition | Qualification Requirement |
|------|-----------|--------------------------|
| **A. Signal Generator** | Produces a tradeable event | Must demonstrate positive standalone expectancy |
| **B. Regime Router** | Determines which specialist module operates | Regime definition must be independently validated |
| **C. Risk Modifier** | Changes exposure/risk based on validated information | Conditioning hypothesis must be independently validated |
| **D. Timing Module** | Determines when an validated setup becomes active | Timing signal must be independently validated |
| **E. Exit/Management Module** | Controls an independently justified payoff | Must have its own frozen validation |
| **F. Information Filter** | Filters signals based on validated information | Must demonstrate independent economic value; NOT selected via combined PnL |

**Forbidden role:** "Decorative confirmation" — a filter added because it "feels right" or improves combined backtest.

---

## 7. Rare-Event Module Principles

### Event Frequency ≠ Evidence Sufficiency

A rare event is NOT automatically weak. A module producing 10 high-quality events/year may be valuable if:
- Expectancy is genuinely positive
- Evidence is sufficient to distinguish signal from noise
- Effect is stable
- Forward observation is possible

### Rare-Event Validation Protocol

```
Frozen event definition
    ↓
Historical OOS validation
    ↓
Positive expectancy evidence
    ↓
Confidence interval assessment
    ↓
Independent forward/demo observation
    ↓
Execution verification
    ↓
Module qualification (M4)
```

### Evidence Sufficiency Criteria for Rare Events

| Criterion | Requirement |
|-----------|-------------|
| Independent events | Sufficient to construct meaningful confidence intervals |
| Calendar exposure | Forward observation period long enough for expected event frequency |
| Effect stability | Consistent direction/magnitude across subperiods |
| Sequential observation | New events observed out-of-sample after methodology freeze |
| Execution realism | Forward observation tests execution, not retroactively proving expectancy |

### Forbidden

- "Wait until enough wins appear" — the observation protocol must be frozen
- Retroactive redefinition of event after seeing outcomes
- Using forward observation to rescue a failed historical test

---

## 8. Standalone vs Module Qualification

### Path A — Standalone Strategy

A research artifact becomes a standalone strategy only if:
- Event definition frozen
- Entry/exit/payoff frozen
- Economic mechanism explicit
- Expected value positive under strict OOS validation
- Realistic costs included
- No post-hoc parameterization
- Sufficient independent evidence
- Reaches M4+ status

### Path B — Specialist Module

A module qualifies even if NOT a complete standalone strategy, but only if:
1. Independently validated economic role
2. Defined function inside a larger architecture
3. Role can be frozen before combined testing
4. Economic reason another validated module should interact with it
5. Own falsifiable validation criteria
6. NOT selected solely because it improved combined backtest PnL

### Key Distinction

> A module is not "a useful indicator."
> A module is "an independently justified economic component with a defined job."

---

## 9. Module Independence Requirements

A module does NOT need zero statistical correlation with another. Instead, it needs:

| Dimension | Requirement |
|-----------|-------------|
| **Scientific independence** | Evidence established independently from other modules |
| **Economic independence** | Distinct risk/payoff mechanism |
| **Informational independence** | Adds information beyond the other module |

Portfolio independence (different return behavior) is desirable but not required for qualification.

---

## 10. Module Interaction Rules

### Permitted

```
Module A (M4, independently validated)
    +
Module B (M4, independently validated)
    +
Ex-ante interaction rationale
    +
Frozen interaction rule
    +
Combined OOS validation
    =
Potential bot component
```

### Forbidden

```
Module A (M1 or M2, not economically validated)
    +
Module B (M1 or M2, not economically validated)
    +
combined backtest is profitable
    =
keep A+B
```

This is **combination mining** and must remain prohibited.

### The Anti-Combinatorial Rule

A combined architecture may contain Module A + Module B ONLY if:
1. A has independent economic justification (M4)
2. B has independent economic justification (M4)
3. Interaction has ex-ante rationale
4. Interaction rule frozen before combined testing
5. Combined testing is a new falsifiable hypothesis

---

## 11. Negative Standalone Result Rule

> A module that fails as a standalone strategy is NOT automatically deleted.

```
Standalone failure
    ↓
Does it have an independently validated economic role?
    ↓
YES → possible module (subject to M4 qualification)
NO  → archive (preserve in knowledge base)
```

**Critical safeguard:** The module cannot be "rescued" solely because a combination backtest improves. The module must independently qualify at M4.

---

## 12. Regime-Specialist Principle

A specialist module does NOT need to perform well outside its scientifically validated environment.

```
Range Module → active only in RANGE
Trend Module → active only in TREND
```

Acceptable:
- Range module silent during trend
- Trend module silent during range

**Required:** The regime routing rule itself must be independently justified.

**Forbidden:**
```
Try every regime definition
    → find one that improves portfolio backtest
```

---

## 13. Bot Architecture Options

### Architecture A — Single Killer Strategy

```
ONE M4/M5 STRATEGY
    ↓
BOT
```

Requires: one research artifact reaches M5 with sufficient standalone economic value.

### Architecture B — Validated Module Set

```
REGIME / ROUTER (M4)
    ↓
┌───┼───┐
↓   ↓   ↓
M4  M4  M4
A   B   C
```

Each module must independently qualify at M4. The router must independently qualify at M4.

Minimum viable Architecture B:
- 1 regime router (M4)
- 2-3 specialist modules (M4 each)
- Predeclared interaction rules

### Anti-Proliferation Rule

> A module should exist only if its independent economic contribution is sufficiently valuable to justify its complexity.

Prefer:
- Small number of strong modules
Over:
- Large number of weak modules

---

## 14. Research Pipeline (Standard)

```
DISCOVERY (phenomenon identification)
    ↓
SCIENTIFIC VALIDATION (M0 → M1)
    ↓
PREDICTIVE VALIDATION (M1 → M2)
    ↓
ECONOMIC HYPOTHESIS (M2 → M3)
    ↓
STANDALONE MODULE VALIDATION (M3 → M4)
    ↓
MODULE QUALIFICATION (M4)
    ↓
OPTIONAL: COMBINATION HYPOTHESIS
    ↓
COMBINED OOS VALIDATION
    ↓
EXECUTION VALIDATION (M4 → M5)
    ↓
BOT INTEGRATION
```

No step may be skipped merely because combination results look attractive.

---

## 15. Research Budget Principle

Each new candidate gets a bounded research budget:

```
Discovery → Methodology → Validation → Economic Test → Adjudication
```

If it fails its frozen economic hypothesis: **stop.**

A new path requires a genuinely new hypothesis, not endless parameterization.

---

## 16. Existing APEX Artifact Classification

| Artifact | Current Level | Status | Notes |
|----------|:---:|--------|-------|
| HIGH_VOL primitive | **M1** | Validated scientific primitive | No economic payoff identified |
| HIGH_VOL persistence | **M2** | Validated predictive primitive | C-index 0.6656, no economic module |
| BTC volatility transfer | **M2** | Validated predictive primitive | C-index 0.6224, options path closed |
| BTC forward RV translation | **M2** | Validated predictive primitive | p=0.000011, no economic module |
| LNO scale dispersion | **M1** | Validated scientific primitive | p=0.0001, deterministic, no economic payoff |
| Session-transition CDF | **M1** | Validated scientific primitive | p=0.0001, scale component identified |
| BTC options VRP | **M1** | Validated scientific finding | IV > RV, long straddle rejected |
| Long ATM straddle | **CLOSED** | Rejected economic mechanism | IC7: p=0.953, mean PnL = -$130 |
| Crypto-options alternatives | **CLOSED** | No distinct mechanism | IC8: all candidates failed |
| RC013 raw breakout | **CLOSED** | Rejected monetization | Studies 007-011 |
| RC014 cross-asset | **CLOSED** | Transmission rejected | Not reopenable |
| HIGH_VOL standalone | **CLOSED** | Economic layer not defensible | M34 closure |

**Current M4+ count: 0**
**Current M3 count: 0** (long straddle reached M3 but failed)
**Current M2 count: 3** (HIGH_VOL persistence, BTC transfer, BTC RV translation)
**Current M1 count: 4** (HIGH_VOL primitive, LNO scale, session CDF, BTC VRP)

---

## 17. What AR1 Establishes

1. The six-state lifecycle for research artifacts (Phenomenon → M1 → M2 → M3 → M4 → M5)
2. Module qualification checklist (8 categories, ~20 criteria)
3. Module role taxonomy (6 roles with qualification requirements)
4. Rare-event validation principles
5. Standalone vs module distinction
6. Module independence requirements
7. Anti-combination-mining rules
8. Negative standalone result rule
9. Regime-specialist principle
10. Bot architecture options (A and B)
11. Research pipeline standard
12. Existing artifact maturity matrix

---

## 18. What AR1 Does NOT Establish

1. Which module should be developed next (requires new scientific question)
2. Whether Architecture A or B is superior (depends on what reaches M4)
3. Any specific economic mechanism
4. Any strategy or PnL
5. Any parameter values

---

## 19. External API calls: 0 | New data acquired: 0 | Spend: $0.00

---

*AR1 is an architecture/governance milestone. No experiments were run. No data was acquired. No PnL was calculated.*
