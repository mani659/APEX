# APEX M49 RESULT

**Milestone**: APEX-M49
**Date**: 2026-08-29
**Status**: COMPLETE

---

## Mission

Funding/Carry Mechanism Re-Discovery — determine whether a coherent funding/carry economic mechanism exists that APEX can justify before observing funding outcomes.

---

## M48 Outcome Being Addressed

**M48 Decision**: C — M48 BLOCKED — ECONOMIC MECHANISM NOT ESTABLISHED

**Primary M48 Failures**:
1. Fundamental sign error: SHORT position but mechanism argued for positive funding (SHORT pays)
2. Circularity: Position direction assumed funding direction
3. Funding cash flow formula error: Missing mark price multiplier
5. Unresolved observation unit
6. Incomplete statistical design
6. HIGH_VOL validated for RV, not funding

---

## H1 — PREDICTION HYPOTHESIS

> **Can an existing validated APEX information state predict a future funding variable?**

### Assessment

| Predictor | Validation | Predicts | Funding Prediction |
|-----------|------------|----------|-------------------|
| HIGH_VOL (BTC) | M2 (RV persistence, C=0.6224) | Future RV, excursion | **UNVALIDATED** |
| LNO scale (EURUSD) | M1 (p=0.0001) | RV dispersion | **UNVALIDATED** |
| BOS+OB (XAUUSD) | M1 (gross +1.01 bps) | Direction/continuation | **UNVALIDATED** |
| CHOCH (XAUUSD) | M1 (gross +0.89 bps) | Reversal | **UNVALIDATED** |
| BTC HIGH_VOL | M2 (C=0.6224) | Forward RV (p=0.000011) | **UNVALIDATED** |

**Conclusion**: **NO VALIDATED PREDICTOR EXISTS** for funding rates among current APEX primitives.

---

## H2 — ECONOMIC RELATIONSHIP HYPOTHESIS

> **Does a predicted funding state imply a tradeable compensation relationship?**

### Funding Economics (Binance BTCUSDT)

- Funding every 8h: `F > 0` → longs pay shorts; `F < 0` → shorts pay longs
- Funding = Position_Size × Mark_Price × Funding_Rate
- For SHORT 1 BTC: Cash_Flow = -1 × Mark_Price × F (USDT)

### Economic Mechanism

| Market State | Funding | Compensation For |
|--------------|---------|------------------|
| Long bias / leveraged longs | `F > 0` (longs pay shorts) | Inventory risk of short side |
| Short bias / leveraged shorts | `F < 0` (shorts pay longs) | Inventory risk of long side |

**Theoretically Plausible**: Funding compensates inventory risk of counter-party liquidity providers.

**But**: No validated predictor for the funding state itself.

---

## H3 — TRADING HYPOTHESIS

> **Can a concrete position monetize after all costs?**

### Complete Payoff (SHORT 1 BTC, 8h funding interval)

```
NetPayoff = -1 × Mark_Price × F + (P_entry - P_exit) × 1 - (Spread + Commission + Slippage)
```

### Cost Reality (Binance BTCUSDT)

| Component | Typical |
|-----------|---------|
| Spread | 1-5 bps |
| Commission | 2 bps (0.02% per leg) |
| Slippage | 0.5-5 bps |
| **Total/round-trip** | **5-12 bps** |

### Funding Reality

| Metric | Typical |
|--------|---------|
| Median funding/8h | ~1 bp |
| 90th percentile | ~3 bp |
| Cap | ±3.75 bp |

**Critical Reality**: **Funding per interval (1-3 bp) < Execution costs (5-12 bp)**

---

## FUNDING SIGN CONVENTION (Explicit)

| Funding Rate | Meaning | Payer | Receiver |
|--------------|---------|-------|----------|
| `F > 0` | Longs pay shorts | Longs | **Shorts** |
| `F < 0` | Shorts pay longs | Shorts | **Longs** |

**M48 Error**: "SHORT receives positive funding" = **mathematically false**. SHORT receives when `F < 0`.

---

## POSITION DIRECTION PRINCIPLE

**Direction must follow mechanism, not precede it.**

| Predicted Funding | Correct Position | Reason |
|-------------------|------------------|--------|
| `F > 0` (longs pay shorts) | **SHORT** | Receive from longs |
| `F < 0` (shorts pay longs) | **LONG** | Receive from shorts |

**M48 Error**: Froze SHORT assuming it receives funding, but mechanism argued for positive funding (which SHORT pays).

---

## H1/H2/H3 INTEGRATION

| Hypothesis | Status | Evidence |
|------------|--------|----------|
| **H1: Prediction** | **FAILS** | No validated predictor for funding |
| **H2: Economic Relationship** | **UNVALIDATED** | Theoretically plausible; no validated predictor |
| **H3: Trading** | **MARGINAL** | Funding (1-3 bp) < Costs (5-12 bp) |

**H1 is the gatekeeper — it FAILS completely.**

---

## CANDIDATE PREDICTORS ASSESSED

| Predictor | Validated For | Funding Prediction |
|-----------|---------------|-------------------|
| HIGH_VOL (BTC) | RV persistence | **UNVALIDATED** |
| LNO scale | RV dispersion | **UNVALIDATED** |
| BOS+OB | Spot direction | **UNVALIDATED** |
| CHOCH | Reversal | **UNVALIDATED** |
| Funding autocorrelation | Statistical persistence | Not APEX primitive |

**No APEX primitive validated for funding prediction.**

---

## CANDIDATE ARCHITECTURES

| Architecture | Assessment |
|--------------|------------|
| A: Directional Carry | Marginal — funding < costs per interval |
| B: Hedged Carry | Not viable — no M4 hedge module; adds basis risk/cost |
| C: Funding as Conditioner | Not viable — no M4 engine exists |

---

## OBSERVATION UNIT

**Correct**: Funding Interval (natural economic transfer unit)

**M48 Error**: Used M1 signals → multiple signals per funding interval = duplicate exposure

---

## ECONOMIC DISTINCTNESS

**Funding/Carry IS genuinely distinct** from closed paths:
- vs Options/Vol: Linear carry vs convexity
- vs LNO/Session: Carry transfer vs RV scale
- vs BOS+OB: Carry transfer vs spot direction

---

## CANDIDATE SCORING (M49 §22)

| Dimension | Score/5 | Rationale |
|-----------|---------|-----------|
| Economic coherence | 3 | Theoretically coherent; unvalidated |
| Information alignment | 1 | **No validated predictor** |
| Direction legitimacy | 2 | Direction must follow mechanism; unvalidated |
| Payoff completeness | 4 | Correctly modeled |
| Observation clarity | 2 | Funding interval natural; few observations |
| Instrument feasibility | 4 | Perp swaps well-suited |
| Data observability | 3 | Public API available |
| Execution realism | 3 | Costs known; funding < costs |
| Ex-ante freezeability | 2 | Many unresolved; no validated predictor |
| Distinctness | 4 | Genuinely different from vol/option paths |
| **TOTAL (50 max)** | **26** | **WELL BELOW THRESHOLD (35-40)** |

---

## HARD ELIMINATION RULES CHECK

| Rule | Status |
|------|--------|
| Direction depends on observing outcomes | **VIOLATED** (M48 froze direction) |
| No economic rationale for HIGH_VOL→funding | PARTIAL (plausible but unproven) |
| Funding as free income | PARTIAL (M48 assumed funding > costs) |
| Price risk ignored | PARTIAL (acknowledged but funding < costs) |
| Observation unit for sample size | **VIOLATED** (M48 used signals) |

**Multiple hard rules VIOLATED.**

---

## DECISION

**B — FUNDING MECHANISM NOT ESTABLISHED — CLOSE PATH**

### Primary Reason

**H1 (Prediction) FAILS completely.** No APEX primitive validated for funding prediction. The M48 attempt used HIGH_VOL (validated for RV, not funding). H2 is theoretically plausible but unvalidated. H3 is marginal (funding 1-3bp < costs 5-12bp).

The funding/carry path lacks a scientifically coherent foundation in APEX knowledge base.

---

## NEXT AUTHORIZED MILESTONE

**NONE AUTHORIZED** — Funding/carry path closed at mechanism discovery stage.

**Programme Status**: PAUSED. Awaiting Control Session decision on new direction.

---

## External API Calls: 0 | New Data Acquired: 0 | Spend: $0.00