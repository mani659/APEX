# APEX M45 — Restart Conditions & Forbidden Triggers

**Date**: 2026-08-27
**Milestone**: M45 (supplementary document)

---

## 1. Valid Restart Conditions

APEX may legitimately restart if ANY ONE of the following occurs:

### Condition A — New Instrument Class

A new instrument becomes realistically observable with an economically aligned payoff.

**Examples:**
- Liquid BTC volatility futures with historical data
- DeFi options on decentralized exchanges
- Prediction markets for volatility events
- Structured products with volatility-linked payoffs
- Cross-asset volatility swap markets

**Requirement:** The instrument must exist, be historically observable, and have a payoff structure that could reward APEX-type information.

### Condition B — New Validated Scientific Primitive

A genuinely new phenomenon is discovered outside the closed branches.

**Examples:**
- New market microstructure finding on a different asset class
- New cross-asset relationship (not RC014 transmission)
- New intraday pattern on a different instrument
- New volatility regime behavior not captured by HIGH_VOL

**Requirement:** The phenomenon must be genuinely new, not a reparameterization of closed findings.

### Condition C — New Predictive Model for Economic Variable

A new prediction targets an economically compensated quantity.

**Examples:**
- Funding rate prediction for perpetual swaps
- Liquidity provision return prediction
- Inventory risk prediction for market makers
- Carry/premium prediction for structured products

**Requirement:** The model must predict a variable that represents economic compensation for a defined risk.

### Condition D — External Market/Data Development

A previously unavailable data architecture becomes realistically observable.

**Examples:**
- New exchange API providing historical depth data
- New market structure creating observable risk premia
- New regulatory framework enabling previously impossible strategies
- New data provider offering institutional-grade historical data

**Requirement:** The development must be external to APEX and create new observability.

### Condition E — New Economic Mechanism

A genuinely distinct mechanism becomes identifiable without parameter mining.

**Examples:**
- A non-options convexity instrument
- A carry-based volatility harvesting approach
- A microstructure-based edge from order flow
- A funding-rate-based timing mechanism

**Requirement:** The mechanism must be genuinely distinct from all closed paths and not require new predictive research before economic meaning can be articulated.

---

## 2. Forbidden Restart Triggers

The following are explicitly FORBIDDEN as restart triggers:

### Parameter Adjustments
- Changing a rejected threshold
- Changing a rejected maturity
- Flipping long to short
- Adjusting cost assumptions

### Rescue Attempts
- Adding filters to rescue a failed strategy
- Adding a second predictor solely because it improves PnL
- Trying a different holding period
- Trying a different strike selection

### Combinatorial Approaches
- Brute-force module combinations
- Testing every instrument until one works
- Grid search across parameter spaces
- Feature stacking to improve backtest PnL

### Reopenings
- Reopening a closed branch without a genuinely new hypothesis
- Reopening HIGH_VOL as a standalone strategy
- Reopening crypto-options
- Reopening RC013 raw breakout
- Reopening RC014 cross-asset transmission

### Psychological Triggers
- "We feel like testing another strategy"
- "The previous result was close, let's try again"
- "We should keep the programme moving"
- "We haven't tried X yet"

---

## 3. Restart Protocol

When a valid restart condition is met:

```
1. Document the triggering development
2. Verify it satisfies one of Conditions A-E
3. Confirm it does not trigger any forbidden condition
4. Begin at DISCOVERY (M0) for the new phenomenon
5. Follow the AR1 module lifecycle: M0 → M1 → M2 → M3 → M4 → M5
6. Do not skip steps
7. Do not combine with existing artifacts until each independently qualifies
```

---

## 4. APEX PAUSED State Definition

**APEX PAUSED** means:

| Component | Status |
|-----------|--------|
| Active economic experiments | NONE |
| Automatic next milestone | NONE |
| Validated knowledge | PRESERVED in repository |
| Repository usability | FULLY USABLE |
| Closed paths | REMAIN CLOSED |
| Bot architecture principles | REMAIN IN EFFECT |
| Module qualification framework | REMAIN IN EFFECT |
| Combination mining prohibition | REMAINS IN EFFECT |

---

## 5. Governance Principle

> The scientifically correct state is PAUSED with no automatic next milestone.

> A restart requires a genuinely new external development, not internal parameterization.

> Every module must independently earn its place.

> Combination mining is permanently forbidden.
