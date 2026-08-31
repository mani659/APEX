# APEX M47 RESULT

**Milestone**: APEX-M47
**Date**: 2026-08-29
**Status**: COMPLETE

---

## Mission

Integrated Economic Research-Direction Discovery — determine if a genuinely new, economically coherent, falsifiable research direction deserves another APEX methodology-design cycle.

---

## Current APEX State

| Metric | Value |
|--------|-------|
| M4 Validated Modules | 0 |
| M5 Deployment Candidates | 0 |
| Active Experiments | NONE |
| Programme Status | PAUSED (M45) + SMC Integrated (M46) |
| Authorization | NO NEW EXPERIMENT |

---

## APEX Validated Scientific Knowledge

- HIGH_VOL primitive (D=0.1927)
- HIGH_VOL persistence (non-memoryless, p<0.0001)
- HIGH_VOL predictability (C-index=0.6656)
- HIGH_VOL → forward RV (p=0.0032)
- HIGH_VOL → excursion envelope (p=7.5e-05)
- LNO CDF difference (p=0.0001)
- LNO scale component (p=0.0001, 1.65×)
- BTC transferability (C-index=0.6224)
- BTC forward RV translation (p=0.000011)
- BTC options VRP (large)

---

## SMC-Derived Knowledge

- 7 structural primitives (BOS, OB, FVG, CHOCH, Sweep, Swings, Freshness)
- BOS+OB gross effect: +1.01 bps/event (123k events)
- CHOCH gross effect: +0.89 bps/event (7.5k events)
- Both failed M2/M3 on M1 XAUUSD under tested cost architecture

---

## Validated Economic Findings

**ZERO M3 candidates, ZERO M4 modules, ZERO M5 candidates**

Closed economic paths (12 definitive):
1. BOS+OB M1 XAUUSD (SMC-R7)
2. CHOCH M1 XAUUSD (SMC-R9-CR)
3. LNO scale standalone (M42)
4. LNO scale modular (M42)
5. BTC long straddle (IC7/IC8)
6. HIGH_VOL standalone (M34)
7. HIGH_VOL boundary (M31)
8. HIGH_VOL dynamic translation (M33)
9. Crypto-options alternatives (IC8)
10. RC012 spot monetization
11. RC014 cross-asset transmission
12. RC015 CME listed options

---

## Candidate Research Directions Surveyed

| Candidate | Domain | Novelty | Status |
|-----------|--------|---------|--------|
| C1: LNO scale → vol swaps | A | GENUINELY NEW | Scored |
| C2: SMC rare subset | C | REPACKAGED | ELIMINATED |
| C3: SMC higher timeframe | B | REPACKAGED | ELIMINATED |
| C4: SMC regime for APEX | E | REPACKAGED | ELIMINATED |
| C5: Funding rate / carry on perps | C | GENUINELY NEW | **TOP (42/50)** |
| C6: SMC event-thinning | G | REPACKAGED | ELIMINATED |
| C7: Untested SMC models | F | GENUINELY NEW | Scored |
| C8: Cross-asset structural | A | GENUINELY NEW | Scored |

---

## Candidate Scorecard (1-5 per dimension)

| Dimension | C1 | C5 | C7 | C8 |
|-----------|----|----|----|----|
| Scientific novelty | 4 | 5 | 4 | 4 |
| Economic mechanism clarity | 4 | 5 | 3 | 4 |
| Instrument alignment | 3 | 4 | 3 | 3 |
| Positive-expectancy plausibility | 4 | 4 | 2 | 3 |
| Ex-ante freezeability | 4 | 4 | 4 | 3 |
| Evidence feasibility | 2 | 3 | 3 | 2 |
| Cost feasibility | 3 | 4 | 4 | 3 |
| OOS feasibility | 4 | 4 | 3 | 3 |
| Module/strategy potential | 4 | 4 | 3 | 3 |
| Information value | 4 | 5 | 3 | 4 |
| **TOTAL** | **36** | **42** | **33** | **33** |

---

## Top Candidate: C5 — Funding Rate / Carry Prediction on Perpetual Swaps

### Why Genuinely New
- Predicts funding rate / basis / carry — NOT realized volatility
- Instrument: perpetual swaps (linear funding payoff) — NOT options
- Mechanism: Market makers pay for inventory risk; structural state predicts funding cost
- Completely different from: HIGH_VOL→RV, LNO→RV, BTC straddle

### Why Not Rescue Engineering
- Does not reuse failed BOS+OB, CHOCH, LNO, or HIGH_VOL economic mechanisms
- Does not add filters to failed strategies
- Predicts a quantity (funding rate) representing direct economic compensation for defined risk

### Economic Mechanism Chain
```
Observable: SMC structural state + APEX HIGH_VOL state
    ↓
Predicted: Funding rate / basis / carry on perpetual swaps
    ↓
Risk identified: Market maker inventory risk / funding rate exposure
    ↓
Who bears: Market makers providing liquidity on perps
    ↓
Payoff: Funding rate paid by one side to the other (linear, no convexity)
    ↓
Instrument: Perpetual swap long/short capturing funding
    ↓
Why APEX/SMC advantage: Structural state predicts funding regime shifts before market prices them
```

### M3 Hypothesis
`E[R_net] > 0` for a funding-rate capture strategy conditioned on structural state, after realistic perp trading costs (fees, slippage, funding timing).

### Evidence Requirement
- Chronological OOS on ≥ 2 years of perp data (freely available)
- ≥ 100 independent structural events per regime
- HAC-robust t-test on net PnL > 0

### Falsification
- Net PnL ≤ 0 after costs in OOS
- No structural state has significantly different funding rate distribution
- Funding rate regime shifts are unpredictable from structural state

---

## Decision

**B — AUTHORIZE ONE METHODOLOGY-DESIGN CYCLE**

**Selected Candidate**: C5 — Funding Rate / Carry Prediction on Perpetual Swaps

**Authorization Scope**: METHODOLOGY DESIGN ONLY (M48). Empirical execution remains PROHIBITED pending subsequent Control Session review of frozen methodology.

---

## Next Authorized Milestone

**M48 — Funding Rate Prediction Methodology Design**

**Scope**: 
- Frozen structural definitions (APEX + SMC primitives)
- Perpetual swap data acquisition/validation (freely available)
- Walk-forward prediction framework
- Realistic perp cost model (fees, slippage, funding timing)
- Falsification gates (net PnL ≤ 0, no regime difference)

**Empirical execution**: NOT AUTHORIZED

---

## Programme Status

```
APEX = PAUSED (with one authorized methodology-design milestone)
M4 modules = 0
M5 candidates = 0
```

---

## External API Calls: 0 | New Data Acquired: 0 | Spend: $0.00