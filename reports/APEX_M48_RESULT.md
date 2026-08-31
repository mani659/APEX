# APEX M48 RESULT

**Milestone**: APEX-M48
**Date**: 2026-08-29
**Status**: COMPLETE
**Authorization**: METHODOLOGY DESIGN ONLY — Empirical Execution PROHIBITED

---

## Mission

Turn M47's funding-rate idea into ONE economically coherent, ex-ante frozen hypothesis that can later be tested without turning the funding research into another parameter-search programme.

---

## M47 Selected Candidate

**Candidate**: C5 — Funding Rate / Carry Prediction on Perpetual Swaps
**Score**: 42/50
**Novelty**: GENUINELY NEW — predicts funding/carry (linear perp payoff), NOT realized volatility

---

## Research Question

> Can a validated APEX/SMC structural market state predict the future funding-rate regime on a BTC perpetual swap sufficiently that a directionally hedged perpetual-swap position can earn positive expected net funding-adjusted return after all relevant costs and directional risk?

**Answer**: Methodology designed to test this. Experiment NOT authorized.

---

## Frozen Methodology Summary

### 3. Funding Variable
- **Primary Variable**: Next-Period Funding Rate (bps)
- **Definition**: Funding rate paid at next funding timestamp for BTC-USDT perpetual on Binance
- **Sign**: Positive = longs pay shorts
- **Source**: Binance BTCUSDT perpetual (8-hour intervals: 00/08/16 UTC)
- **Not**: funding sign, cumulative funding, premium relative to reference

### 4. Information Source
- **Single Source**: APEX HIGH_VOL Market State (binary)
- **Definition**: BTC M1 rolling RV (288 bars) > 80th percentile of trailing 2-year distribution
- **State**: `H_t ∈ {0, 1}`
- **Validated**: IC3 transfer (C-index=0.6224); predicts forward RV (p=0.000011)
- **Excluded**: SMC states, LNO scale, multivariate combinations

### 5. Instrument & Exchange
- **Instrument**: Binance BTCUSDT USDT-margined linear perpetual
- **Funding**: 8-hour intervals, ±3.75 bps cap
- **Exchange**: Binance (deepest liquidity, public API)
- **Frozen**: BTC only; no ETH/other comparison

### 6. Economic Mechanism
- **Trader paid for**: Bearing BTC inventory risk during elevated funding demand
- **Hypothesis**: HIGH_VOL → elevated leveraged long demand → market-maker short inventory risk → funding premium
- **Mechanism Chain**: HIGH_VOL=1 → funding premium → SHORT position → receive funding + price PnL - costs

### 7. Position Structure
- **Mechanism**: A — Directional Carry (selected; score 46/50)
- **Rejected**: B (Hedged), C (Conditioning), D (Cross-asset)
- **Position**: SHORT 1 BTC when `H_t = 1`; FLAT when `H_t = 0`
- **Duration**: Open at signal `t`; close at next funding timestamp `t_F` (0-8h variable)

### 8. Timing Architecture
- **Signal**: M1 bar close `t`
- **Next Funding**: `t_F` = first 00/08/16 UTC after `t`
- **Open**: Market at `t` | **Close**: Market at `t_F`
- **Holding**: Variable 0-8h (determined by funding calendar, not parameter)

### 9. Payoff Definition
```
NetPayoff = FundingCashFlow + PricePnL - ExecutionCosts
FundingCashFlow = -F_{t+1} × N          (SHORT receives funding)
PricePnL = (P_entry - P_exit) × N       (SHORT profits if price falls)
ExecutionCosts = Spread + 0.02% commission + 0.5 bps slippage per leg
```
**Primary Endpoint**: `E[NetPayoff | H_t = 1] > 0` (Expected Net Payoff per signal event, USDT)

### 10. Cost Framework
| Cost | Classification | Value |
|------|---------------|-------|
| Entry Spread | OBSERVED | (Ask-Bid)/2 at `t` |
| Exit Spread | OBSERVED | (Ask-Bid)/2 at `t_F` |
| Entry Commission | FROZEN ASSUMPTION | 0.02% notional × Price |
| Exit Commission | FROZEN ASSUMPTION | 0.02% notional × Price |
| Slippage/leg | FROZEN ASSUMPTION | 0.5 bps notional |
| Total/round-trip | ESTIMATED | ~5-8 bps notional |

### 11. M3 Hypothesis
> `E[NetPayoff | H_t = 1] > 0`

**Null**: `E[NetPayoff | H_t = 1] ≤ 0`

### 12. Falsification Rules
| ID | Condition | Falsifies |
|----|-----------|-----------|
| F1 | `E[NetPayoff | H=1] ≤ 0` | Primary |
| F2 | `E[Funding] ≤ E[Costs]` | Funding doesn't cover costs |
| F3 | `E[PricePnL] < -E[Funding]` | Price loss > funding |
| F4 | No funding rate difference `H=1` vs `H=0` (α=0.05) | Predictive signal |
| F5 | < 30 independent HIGH_VOL episodes in OOS | Evidence insufficiency |

**No rescue pathways**: If falsified → mechanism rejected.

### 13. Candidate Architectures

| Architecture | Score | Status |
|--------------|-------|--------|
| A — Directional Funding Capture | 46/50 | **SELECTED** |
| B — Hedged Funding Capture | 34/50 | REJECTED (unvalidated hedge params) |
| C — Funding as Conditioning | 27/50 | REJECTED (no M4 engine) |
| D — Cross-Asset Arbitrage | 26/50 | REJECTED (multi-asset, combination mining) |

### 14. Material Uncertainties
1. Whether HIGH_VOL actually predicts funding (explanatory hypothesis)
2. Price PnL variance swamping funding signal
3. Actual execution costs vs frozen assumptions
4. Binance ±3.75 bps cap truncation
5. Regime stability across 2021-2026
6. Episode-block bootstrap validity

---

## Decision

**M48 COMPLETE — METHODOLOGY FROZEN**

**Selected Configuration**:
- **Funding Variable**: Next-period funding rate (bps) on Binance BTCUSDT
- **Information Source**: APEX HIGH_VOL state on BTC M1 (binary)
- **Instrument**: Binance BTCUSDT USDT-margined linear perpetual
- **Mechanism**: Directional carry — SHORT when HIGH_VOL=1
- **Payoff**: `NetPayoff = -F×N + (P_entry-P_exit)×N - Costs`
- **M3 Hypothesis**: `E[NetPayoff | HIGH_VOL=1] > 0`
- **Falsification**: `E[NetPayoff] ≤ 0` or funding doesn't cover costs or price loss > funding
- **Architecture**: A — Directional Carry (46/50)

---

## Next Authorized Milestone

**M49 — Methodology Control Review** (PLANNED — NOT AUTHORIZED)

**Future Sequence**:
```
M49 — Methodology Control Review
M50 — Data / Observation Feasibility (BTC perp data acquisition)
M51 — Economic Experiment (OOS test)
M52 — Economic Adjudication
```

**No automatic experiment after M48.** Control Session must review M48 before any further execution.

---

## External API Calls: 0 | New Data Acquired: 0 | Spend: $0.00