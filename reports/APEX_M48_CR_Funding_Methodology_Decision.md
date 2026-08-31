# APEX-M48-CR — Funding Methodology Control Decision

**Milestone**: APEX-M48-CR
**Date**: 2026-08-29
**Status**: COMPLETE

---

## Decision

**C — M48 BLOCKED — ECONOMIC MECHANISM NOT ESTABLISHED**

---

## Rationale

M48 is blocked because it **assumes the very funding relationship it is supposed to discover**. The methodology contains fundamental errors that cannot be fixed by controlled amendment.

### 1. Fundamental Sign Error (Blocking)

The methodology freezes a **SHORT position** but the economic mechanism chain argues for **positive funding premium** (which would make SHORT **pay** funding, not receive it).

- M48 §6.3: "Funding rate premium (F_{t+1} > baseline)" → implies **positive funding** (longs pay shorts)
- M48 §7.2: SHORT position receives "Positive funding (longs pay shorts)" → **mathematically impossible**. SHORT receives funding only when funding is **negative** (shorts pay longs)
- M48 §9.2: `FundingCashFlow = -F_{t+1} × Notional` — if F is positive, SHORT pays (negative cash flow)

The methodology freezes SHORT position assuming it receives funding, but the mechanism chain argues for positive funding (which SHORT pays). This is a **fundamental sign contradiction**.

### 2. Circularity in Economic Mechanism (Blocking)

The methodology freezes position direction (SHORT) based on an assumption about funding direction (negative), but the economic mechanism chain (§6.2-6.3) argues for **positive funding premium** during HIGH_VOL.

- M48 §6.2: "Funding rate increases — longs pay higher premium" → positive funding
- M48 §6.3: "Funding rate premium (F_{t+1} > baseline)" → positive funding
- M48 §7.2: SHORT position → "receives positive funding" → requires **negative funding**

The methodology **assumes the funding direction it claims to test**. This is circular reasoning.

### 3. Funding Cash Flow Formula Error (Blocking)

M48 §9.2: `FundingCashFlow = -F_{t+1} × Notional`

**Binance linear perpetual funding formula**:
```
Funding = Position_Size × Mark_Price × Funding_Rate
```
For SHORT 1 BTC: `Funding = -1 BTC × Mark_Price × F`

M48's formula: `-F × Notional` (missing `× Mark_Price`)

This is a **material error** in the payoff definition. The methodology's primary economic endpoint is dimensionally incorrect.

### 4. Circular Position Direction (Blocking)

M48 freezes: **SHORT when HIGH_VOL=1**

But:
- Mechanism chain (§6.3): "Funding rate premium (F_{t+1} > baseline)" → positive funding → SHORT **pays** funding
- Position table (§7.2): SHORT "receives positive funding" → requires negative funding
- No validated evidence establishes funding direction during HIGH_VOL

The position direction is frozen based on an unproven assumption about funding sign. The methodology assumes the funding direction it claims to test.

### 5. Incomplete Frozen Methodology (Blocking)

Multiple critical parameters remain **unresolved** in M48:

| Parameter | Status |
|-----------|--------|
| Event unit (signal vs funding interval vs episode) | **UNRESOLVED** |
| OOS split (chronological split point) | **UNRESOLVED** |
| Primary test statistic | **UNRESOLVED** |
| Dependence treatment (episode-block bootstrap details) | **UNRESOLVED** |
| Alpha level | **UNRESOLVED** |
| Evidence sufficiency rule | **UNRESOLVED** |

M48 is **not a complete frozen methodology**. A frozen methodology must specify all these before empirical execution.

### 6. Event Identity Unresolved (Blocking)

M48 allows "multiple signals per HIGH_VOL episode" but:
- Multiple M1 signals → same funding interval → same funding event
- Multiple positions for same funding interval = duplicate economic exposure
- M48 does not define the economic observation unit
- Multiple signals treated as independent observations would be invalid

### 7. Unvalidated Predictor for New Target

- HIGH_VOL validated for **RV persistence prediction** (IC3)
- M48 uses HIGH_VOL to predict **funding rate** (new target)
- Resolution changed from M15 (validated in IC3) to M1 (unvalidated)
- 80th percentile threshold validated for RV persistence, not funding
- This is a **new researcher parameter** for a new target

---

## Decision: **C — M48 BLOCKED — ECONOMIC MECHANISM NOT ESTABLISHED**

---

## Required Actions Before Restart

If the funding/carry direction is to be pursued, a new methodology must:

1. **Not freeze position direction** — let the experiment discover funding sign/direction
2. **Fix funding cash flow formula** — include mark price: `Funding = Position × Mark_Price × F`
3. **Define event unit** — funding interval (not signal); map signals to episodes
4. **Validate HIGH_VOL as funding predictor** — separate prediction test before economic test
5. **Freeze ALL statistical design parameters** — OOS split, test statistic, dependence treatment, alpha, evidence rule
6. **Define economic observation unit** — funding interval, not signal
7. **Fix funding sign convention** — explicitly define what "positive funding" means for SHORT/LONG
7. **Separate prediction test from economic test** — M48 conflates them

These are **fundamental redesigns**, not controlled amendments. The methodology returns to Control.

---

## Authorization Status

- **M49 (Control Review)**: NOT AUTHORIZED — M48 blocked
- **M50 (Data Feasibility)**: NOT AUTHORIZED
- **M51 (Economic Experiment)**: NOT AUTHORIZED
- **M52 (Economic Adjudication)**: NOT AUTHORIZED

**Programme Status**: PAUSED. Awaiting Control Session decision on whether to pursue funding/carry direction with a properly specified methodology, or pursue a different direction.

---

## External API Calls: 0 | New Data Acquired: 0 | Spend: $0.00