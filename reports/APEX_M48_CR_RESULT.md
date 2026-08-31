# APEX M48-CR RESULT

**Milestone**: APEX-M48-CR
**Date**: 2026-08-29
**Status**: COMPLETE

---

## Mission

Control / Methodology Integrity Review of M48 Funding-Rate Economic Methodology

---

## M48 Decision Being Reviewed

**M48 Decision**: METHODOLOGY FROZEN — READY FOR CONTROL SESSION REVIEW

**Selected Configuration**:
- Funding Variable: Next-period funding rate (bps) on Binance BTCUSDT
- Information Source: APEX HIGH_VOL state on BTC M1 (binary)
- Instrument: Binance BTCUSDT USDT-margined linear perpetual
- Mechanism: Directional carry — SHORT when HIGH_VOL=1
- Payoff: `NetPayoff = -F×N + (P_entry-P_exit)×N - Costs`
- M3 Hypothesis: `E[NetPayoff | HIGH_VOL=1] > 0`
- Architecture: A — Directional Carry (46/50)

---

## Control Review Decision

**C — M48 BLOCKED — ECONOMIC MECHANISM NOT ESTABLISHED**

---

## Primary Blocking Issues

### 1. Fundamental Sign Error (Blocking)
M48 freezes SHORT position but mechanism chain argues for positive funding premium (SHORT would **pay** funding, not receive it).

### 2. Circularity (Blocking)
Methodology freezes SHORT position assuming negative funding, but mechanism chain argues for positive funding premium. Assumes the funding direction it claims to test.

### 3. Funding Cash Flow Formula Error (Blocking)
`FundingCashFlow = -F × Notional` — missing `× Mark_Price` multiplier. Dimensionally incorrect for Binance linear perpetuals.

### 4. Circular Position Direction (Blocking)
SHORT position frozen assuming negative funding, but mechanism chain argues for positive funding premium. No validated evidence for funding direction.

### 5. Incomplete Frozen Methodology (Blocking)
Critical parameters unresolved: event unit, OOS split, test statistic, dependence treatment, alpha, evidence rule.

### 5. Event Identity Unresolved (Blocking)
Multiple M1 signals per HIGH_VOL episode → same funding interval → duplicate economic exposure. Not resolved.

### 6. Unvalidated Predictor for New Target
HIGH_VOL validated for RV prediction, not funding. Resolution changed M15→M1. Threshold validated for RV, not funding.

---

## Audit Summary

| Audit | Result | Blocking |
|-------|--------|----------|
| A: HIGH_VOL → Funding Logic | FAIL | YES |
| B: Info-to-Payoff Chain | PARTIAL FAIL | YES |
| C: Predictor vs Condition | PARTIAL FAIL | Contributing |
| D: HIGH_VOL Definition | PARTIAL FAIL | Contributing |
| E: Funding Variable | PARTIAL FAIL | Contributing |
| F: Funding Direction | FAIL | YES |
| G: Position Direction | FAIL | YES |
| H: Price Risk | PASS | No |
| I: Unit Consistency | PASS | No |
| J: Funding Cash Flow Formula | FAIL | YES |
| K: Position Timing | PARTIAL FAIL | Contributing |
| L: Future Funding Lookahead | PASS | No |
| M: Execution Cost | PASS | No |
| N: Funding vs Exec Frequency | FAIL | YES |
| O: Event Identity | FAIL | YES |
| P: Repeated Signals | FAIL | YES |
| Q: Economic Independence | FAIL | YES |
| R: M3 Hypothesis | PARTIAL FAIL | Contributing |
| S: Prediction vs Economic | PASS | No |
| T: Market Edge Rationale | FAIL | Contributing |
| U: Distinctness | PASS | No |
| V: Hedged vs Directional | PASS | No |
| W: Instrument/Venue | PARTIAL FAIL | Contributing |
| X: Parameter Classification | PARTIAL FAIL | YES |
| 27: OOS/Statistical Design | FAIL | YES |
| 28: Rare-Event Governance | PARTIAL FAIL | Contributing |
| 29: M3 Definition | PASS | No |
| 30: Future Milestones | PASS | No |

**Total Blocking Issues**: 11

---

## Decision

**C — M48 BLOCKED — ECONOMIC MECHANISM NOT ESTABLISHED**

The methodology has fundamental errors that cannot be fixed by controlled amendment. The issues are fundamental to the economic mechanism design.

---

## Required Actions Before Restart

If funding/carry direction is pursued:
1. Do not freeze position direction — let experiment discover funding sign
2. Fix funding cash flow formula (add mark price)
3. Define event unit (funding interval, not signal)
5. Validate HIGH_VOL as funding predictor first
6. Freeze ALL statistical design parameters
7. Define economic observation unit (funding interval)

These are fundamental redesigns, not controlled amendments.

---

## Authorization Status

| Milestone | Status |
|-----------|--------|
| M49 (Control Review) | NOT AUTHORIZED |
| M50 (Data Feasibility) | NOT AUTHORIZED |
| M51 (Economic Experiment) | NOT AUTHORIZED |
| M52 (Economic Adjudication) | NOT AUTHORIZED |

**Programme Status**: PAUSED. Awaiting Control Session decision.

---

## External API Calls: 0 | New Data Acquired: 0 | Spend: $0.00