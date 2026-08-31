# APEX AR1 — Bot Architecture Principles

**Date**: 2026-08-27
**Milestone**: AR1 (supplementary document)

---

## 1. Two Valid Final Architectures

### Architecture A — Single Killer Strategy

```
ONE M4/M5 STRATEGY
    ↓
BOT
```

**Requirements:**
- One research artifact reaches M4+ with sufficient standalone economic value
- The strategy is independently validated under strict OOS with realistic costs
- The strategy is frozen ex ante

**When to prefer:** When one clearly dominant edge exists that justifies the entire bot.

### Architecture B — Validated Module Set

```
REGIME / ROUTER (M4)
    ↓
┌───┼───┐
↓   ↓   ↓
M4  M4  M4
A   B   C
```

**Requirements:**
- 1 regime router (M4)
- 2-3 specialist modules (M4 each)
- Each module independently validated
- Predeclared interaction rules
- Combined OOS validation

**When to prefer:** When multiple independent edges exist in different market regimes, and no single edge dominates.

---

## 2. Module Qualification Standard

Every module must earn its place independently. The minimum evidence for entering the final bot:

| Criterion | Requirement |
|-----------|-------------|
| Maturity level | M4+ (Validated Economic Module or Production Candidate) |
| Scientific independence | Evidence established separately from other modules |
| Economic independence | Distinct risk/payoff mechanism |
| Frozen role | Activation and function defined ex ante |
| Positive expectancy | Standalone positive expectation (trade generator) or validated conditioning hypothesis (modifier) |
| Costs included | Realistic transaction/execution costs |
| OOS validated | Strict chronological out-of-sample validation |
| Evidence sufficient | Enough independent evidence to distinguish signal from noise |

---

## 3. Anti-Combination-Mining Rule

**Forbidden:**
```
Test A + B + C + D + E
    → choose best PnL combination
```

This is curve-fitting and must remain prohibited.

**Permitted:**
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
```

**The combined test is a new falsifiable hypothesis, not an optimization.**

---

## 4. Module Roles (Standardized)

| Role | Job | Standalone Requirement |
|------|-----|----------------------|
| Signal Generator | Produces tradeable events | Must show positive standalone expectancy (M4) |
| Regime Router | Routes to specialist modules | Regime definition independently validated (M4) |
| Risk Modifier | Adjusts exposure/risk | Conditioning hypothesis independently validated (M4) |
| Timing Module | Activates validated setups | Timing signal independently validated (M4) |
| Exit/Management | Controls justified payoff | Own frozen validation (M4) |
| Information Filter | Filters based on validated info | Independent economic value demonstrated; NOT via combined PnL |

---

## 5. Anti-Proliferation Principle

> A module should exist only if its independent economic contribution is sufficiently valuable to justify its complexity.

**Prefer:**
- 2-3 strong M4 modules
- Each with clear, distinct economic roles

**Avoid:**
- 5+ weak modules
- Redundant filters
- Overlapping volatility indicators
- Duplicate regime detectors
- Decorative confirmation signals

---

## 6. Rare-Event Module Governance

A rare event is NOT automatically weak. A module with 10 events/year can qualify if:

1. Expectancy is genuinely positive under OOS validation
2. Confidence intervals are meaningful
3. Effect is stable across subperiods
4. Forward observation protocol is frozen
5. Execution verification is possible

**Forbidden:**
- "Wait until enough wins appear"
- Retroactive event redefinition
- Using forward observation to rescue failed historical tests

---

## 7. Negative Standalone Result

> A module that fails standalone is NOT automatically deleted.

```
Standalone failure
    ↓
Does it have an independently validated economic role?
    ↓
YES → possible module (must still reach M4)
NO  → archive in knowledge base
```

**Never rescued by:** "Combined backtest looks good."

---

## 8. Regime-Specialist Principle

A specialist module does NOT need to perform outside its validated environment.

- Range module: silent during trend ✓
- Trend module: silent during range ✓

**Required:** The regime routing rule itself must be independently validated (M4).

**Forbidden:** Try every regime definition → pick the one that improves portfolio backtest.

---

## 9. Research Pipeline Standard

```
DISCOVERY → M1 → M2 → M3 → M4 → M5 → BOT
```

No step may be skipped because combination results look attractive.

Each candidate gets a bounded research budget. If frozen hypothesis fails: stop.

---

## 10. Current Bot Readiness

| Component | Maturity | Bot-Ready |
|-----------|:---:|:---:|
| HIGH_VOL primitive | M1 | NO |
| HIGH_VOL predictability | M2 | NO |
| BTC volatility transfer | M2 | NO |
| BTC forward RV translation | M2 | NO |
| LNO scale dispersion | M1 | NO |
| Session-transition CDF | M1 | NO |
| BTC options VRP | M1 | NO |
| **M4+ modules** | **0** | **NOT READY** |

**Bot status: NOT READY.** No module has reached M4. The programme requires new scientific discovery before bot construction can begin.
