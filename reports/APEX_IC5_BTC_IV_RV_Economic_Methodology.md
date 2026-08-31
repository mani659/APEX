# APEX IC5 — BTC IV/RV Economic Mechanism Methodology Design

**Date**: 2026-08-25
**Milestone**: IC5
**Status**: COMPLETE
**Classification**: Methodology design only — no economic test, no data acquisition, no PnL

---

## 1. Core Economic Question

> **Does the BTC-native APEX volatility forecast identify timestamps at which expected future realized volatility exceeds the contemporaneous BTC option-implied volatility sufficiently to create a positive expected value direction-neutral convex payoff after realistic option costs?**

IC5 designs this question. IC6 validates the data. IC7 executes the test.

---

## 2. Primary Economic Hypothesis

**H₁:** At BTC HIGH_VOL onset timestamps where the frozen BTC model produces a risk score in the lowest quintile (lowest predicted hazard = longest predicted duration = highest predicted future RV), the mean net straddle payoff after frozen costs is positive and statistically significantly greater than zero.

**H₀:** The APEX-predicted volatility state does not improve expected net direction-neutral option payoff relative to an unconditional baseline after frozen costs.

---

## 3. Prediction Source — Frozen

| Component | Specification |
|-----------|--------------|
| Source | IC3 BTC-native OOS risk score |
| Model | Cox PH (statsmodels.PHReg) |
| Predictors | Breakout Intensity, Variance Momentum |
| Validation | Chronological expanding-window walk-forward |
| Episode range | Episodes 51–1,621 (OOS: episodes 51–1,621) |
| OOS predictions | 1,571 |

**Do not retrain. Do not change predictors. Do not alter the IC3 walk-forward architecture.**

---

## 4. Predicted-RV Mapping — Frozen

### Problem

The IC3 Cox PH model produces a continuous risk score (linear predictor), not a direct forward-RV forecast. IC5 must map this score to a predicted forward-RV value.

### Selected Approach: Walk-Forward OLS Mapping

For each OOS prediction episode i:

1. **Training window:** All episodes j < i (strictly historical, expanding)
2. **Fit OLS:** forward_RV_12h[j] = α + β × risk_score[j] + ε[j], using episodes 0 to i-1
3. **Predict:** predicted_RV[i] = α̂ + β̂ × risk_score[i]

This produces a walk-forward, strictly OOS predicted-RV value for every eligible episode.

### Properties

- No look-ahead bias: each mapping uses only historically available data
- No parameter selection: OLS with two inputs (intercept + risk score)
- Deterministic: given the same historical window, produces the same prediction
- Evaluated OOS: the predicted-RV values are used in the economic test, not the mapping coefficients

### Why Not Other Approaches

| Approach | Rejection Reason |
|----------|-----------------|
| Direct model-implied survival mapping | Requires specifying a baseline hazard function; adds complexity without clarity |
| Rank-based percentile mapping | Loses level information; harder to compare with IV |
| Fixed full-sample regression | Uses future information in the mapping; violates OOS principle |
| Nonparametric mapping | Introduces researcher degrees of freedom in bandwidth/shape selection |

---

## 5. IC4 Frozen IV Architecture — Inherited

| Component | Frozen Value | Source |
|-----------|-------------|--------|
| IV representation | ATM implied volatility | IC4 |
| Pricing model | Black-76 inversion | IC4 |
| Price input | midpoint = (bid + ask) / 2 | IC4 |
| Strike selection | Nearest strike to BTC-PERPETUAL mark price | IC4 |
| Option type | Both call and put; average if both available at same strike | IC4 |
| Maturity rule | Nearest expiry with TTE ∈ [6h, 18h] | IC4 |
| Fallback | Nearest expiry with TTE > 0 (flag as maturity-mismatched) | IC4 |
| Maximum mismatch | 24 hours | IC4 |
| Interpolation | NOT permitted | IC4 |
| Quote freshness | ≤ 1 hour (staleness threshold) | IC4 |
| Primary quote tier | Tier 1: fresh bid/ask, spread < 5 vol points | IC4 |
| Secondary quote tier | Tier 2: ≤ 1 hour stale | IC4 |
| Risk-free rate | 0 (standard for crypto options analysis) | IC5 |

---

## 6. Straddle Definition — Frozen

### Structure

- **Position:** Long ATM straddle = long 1 ATM call + long 1 ATM put
- **Underlying:** BTC-PERPETUAL (or BTC spot index on Deribit)
- **Strike (K):** Nearest strike to BTC-PERPETUAL mark price at entry timestamp
- **Expiry (T):** Nearest expiry with TTE ∈ [6h, 18h] from entry timestamp
- **Settlement:** European; cash-settled at expiry
- **Notional:** 1 BTC per straddle (normalized for comparison)

### Entry Convention

- **Timestamp:** IC3 onset timestamp (the BTC HIGH_VOL onset M15 bar close)
- **Entry price (straddle premium):**
  - Call entry = (call_bid + call_ask) / 2 (midpoint)
  - Put entry = (put_bid + put_ask) / 2 (midpoint)
  - Straddle entry = call_entry + put_entry
- **Entry fee:** Deribit taker fee = 0.04% of notional per leg × 2 legs

### Exit Convention

- **Exit timestamp:** Option expiry
- **Exit value:**
  - Call payoff = max(F_expiry - K, 0)
  - Put payoff = max(K - F_expiry, 0)
  - Straddle exit value = call_payoff + put_payoff
- **Exit fee:** Deribit taker fee = 0.04% of notional per leg × 2 legs (on exit settlement)

### Net Payoff

```
net_payoff = straddle_exit_value - straddle_entry_premium - entry_fees - exit_fees
```

### Note on Holding Period

The straddle is held from entry to expiry. The holding period is determined by the maturity rule, not by a fixed time interval. For TTE ∈ [6h, 18h], the holding period varies per observation.

---

## 7. Cost Model — Frozen

| Cost Component | Specification | Source |
|---------------|---------------|--------|
| Entry bid/ask spread | Implicit in midpoint entry (half-spread cost) | Market observation |
| Exit bid/ask spread | Not applicable (European expiry, settled at intrinsic) | N/A |
| Entry exchange fee | 0.04% of notional × 2 legs | Deribit fee schedule |
| Exit exchange fee | 0.04% of notional × 2 legs (on settlement) | Deribit fee schedule |
| Slippage | NOT modeled in IC7; acknowledged as limitation | — |
| Funding/carry | NOT modeled; risk-free rate = 0 | — |
| Theta/decay | Captured implicitly by holding to expiry | — |
| IV re-pricing | NOT modeled; option held to expiry | — |

### Total Explicit Cost per Straddle

```
total_cost = 0.0004 × 2 × BTC_price (entry) + 0.0004 × 2 × BTC_price (exit)
           = 0.0016 × BTC_price (approximately, since entry ≈ exit ≈ BTC_price)
```

For BTC at $80,000: total explicit cost ≈ $128 per straddle.

---

## 8. Economic Entry Condition — Frozen

### Primary Test: Continuous Forecast-vs-IV Spread

For each eligible observation, compute:

```
forecast_IV_spread = predicted_RV - observed_IV
```

The primary economic test evaluates whether **straddle payoff is systematically positive when forecast_IV_spread > 0**.

### Why Continuous (Not Threshold-Based)

- Avoids introducing an arbitrary threshold before the first economic test
- No parameter to optimize
- The economic mechanism is: "predicted RV > IV → positive expected straddle payoff"
- This is tested as a conditional relationship, not as a binary signal

### Threshold for Future Refinement

If IC7 finds a significant relationship, a future milestone may investigate optimal thresholds. IC5 does not freeze a threshold.

---

## 9. Primary Economic Outcome — Frozen

**Selected: Net straddle P&L per observation (after frozen costs)**

```
net_PnL[i] = straddle_exit_value[i] - straddle_entry[i] - fees[i]
```

This is the raw economic outcome for each eligible observation.

### Secondary Descriptive Metrics (Not Primary)

- Mean net PnL per observation
- Fraction of observations with positive net PnL (hit rate)
- Mean net PnL conditional on forecast_IV_spread > 0
- Mean net PnL conditional on forecast_IV_spread ≤ 0
- Sharpe-like ratio (mean / std of net PnL series)

These are descriptive only. The primary decision uses the conditional mean test.

---

## 10. Baseline — Frozen

### Primary Baseline: Unconditional ATM Straddle

The average net PnL of an ATM straddle held to expiry at **all** eligible timestamps (not just HIGH_VOL onsets).

This answers: "Does the APEX signal improve straddle performance beyond what you'd get by buying straddles randomly?"

### Why This Baseline

- Directly tests the economic value of the signal
- Does not require a no-position baseline (which would trivially produce zero)
- Controls for the general volatility risk premium (IV > RV on average)
- If APEX-selected straddles outperform unconditional straddles, the signal has economic value

### Secondary Baseline (Descriptive Only)

- Zero payoff (no position)
- Random timestamps (if needed for robustness)

---

## 11. Statistical Framework — Frozen

### Primary Test: Conditional Mean Comparison with HAC

```
H₀: E[net_PnL | forecast_IV_spread > 0] = 0
H₁: E[net_PnL | forecast_IV_spread > 0] > 0
```

**Method:** One-sample t-test on the conditional PnL series, with Newey-West HAC standard errors.

**HAC lag:** 12 (to account for overlapping holding windows and within-episode serial correlation)

**Decision rule:** Reject H₀ if p < 0.05 (one-sided).

### Why HAC

- Straddle observations may cluster within episodes (multiple onset timestamps per episode)
- Holding periods may overlap (adjacent timestamps with similar expiries)
- Newey-West HAC corrects for autocorrelation and heteroskedasticity

### Why One-Sided

- The economic hypothesis is directional: predicted RV > IV → positive payoff
- A negative result (payoff < 0) would falsify the mechanism, not require a two-sided test

---

## 12. Sample Eligibility — Frozen

An observation is eligible only if ALL of the following hold:

| # | Criterion |
|---|-----------|
| 1 | IC3 OOS prediction exists for this timestamp |
| 2 | BTC option data is available at this timestamp |
| 3 | Valid ATM strike exists (nearest to BTC-PERPETUAL mark price) |
| 4 | Valid bid and ask exist for both call and put at the ATM strike |
| 5 | Quote freshness ≤ 1 hour (Tier 1 or Tier 2) |
| 6 | Maturity rule satisfied: nearest expiry with TTE ∈ [6h, 18h] |
| 7 | Spread < 5 vol points for the ATM option |
| 8 | BTC-PERPETUAL price is available at entry and at expiry |
| 9 | Black-76 IV inversion converges for both call and put |
| 10 | No missing data in the forward underlying path through expiry |

**Exclusion criteria (prohibited):**
- Excluding observations based on realized PnL
- Excluding extreme PnL observations
- Excluding observations where forecast_IV_spread < 0
- Excluding observations based on market conditions

---

## 13. No Outcome-Driven Filtering — Frozen

Explicitly prohibited:

| Prohibited Action | Reason |
|-------------------|--------|
| Removing losing trades | Cherry-picking |
| Removing extreme PnL outliers | Selection bias |
| Selecting only liquid winners | Survivorship bias |
| Selecting maturities after outcome | Horizon selection bias |
| Selecting strikes after outcome | Strike selection bias |
| Selecting timestamps where IV is favorable | Signal selection bias |
| Adding filters based on PnL direction | Data-snooping |

---

## 14. Multiple Testing — Frozen

| Dimension | Frozen Value |
|-----------|-------------|
| Instrument | BTC options on Deribit (1 instrument) |
| Underlying | BTC-PERPETUAL |
| Payoff | Long ATM straddle (1 structure) |
| Maturity rule | Nearest TTE ∈ [6h, 18h] (1 rule) |
| Holding period | Entry to expiry (determined by maturity) |
| Primary metric | Mean net PnL conditional on forecast_IV_spread > 0 |
| Baseline | Unconditional ATM straddle PnL |
| Decision threshold | p < 0.05 (one-sided) |
| Primary statistical test | One-sample t-test with HAC (Newey-West, lag=12) |

**No grid of:** strikes, maturities, holding periods, thresholds, instruments, or payoff structures.

---

## 15. Eligibility Validation Gate — IC6 Prerequisite

IC6 must validate the actual BTC options dataset before IC7 executes. IC6 must verify:

| Check | Criterion |
|-------|-----------|
| Historical option coverage | Options data exists at IC3 prediction timestamps |
| Strike availability | ATM strike available at each timestamp |
| Bid/ask availability | Both sides present for ATM options |
| Quote freshness | Quotes within 1 hour of prediction timestamp |
| Maturity coverage | Expiry with TTE ∈ [6h, 18h] available |
| Spread quality | Spread < 5 vol points for ATM options |
| IV inversion | Black-76 converges for both call and put |
| Forward path | BTC-PERPETUAL price available through expiry |
| Eligible observations | Sufficient count for statistical power |

**IC6 does NOT calculate PnL.** It validates data observability only.

---

## 16. Falsification Gates — Frozen

| Gate | Milestone | Criterion | Action if Failed |
|------|-----------|-----------|-----------------|
| Data observability | IC6 | < 100 eligible observations with valid IV | STOP — insufficient data |
| Data observability | IC6 | > 30% of predictions have no valid option data | STOP — data too sparse |
| Economic mechanism | IC7 | Mean conditional PnL not significantly > 0 (p ≥ 0.05) | STOP — mechanism not established |
| Cost sensitivity | IC7 | Mean conditional PnL ≤ 0 after costs | STOP — costs destroy edge |
| Baseline comparison | IC7 | Conditional PnL ≤ unconditional baseline | STOP — signal has no economic value |

---

## 17. Candidate Economic Methodologies — Ranking

| Rank | Candidate | Score / 20 | Main Reason |
|------|-----------|-----------:|-------------|
| 1 | B: Long ATM straddle | 18 | Directly captures RV-IV spread; simple; well-defined |
| 2 | A: Direct forecast-RV vs IV spread | 15 | Clean comparison but doesn't capture option payoff geometry |
| 3 | D: Direction-neutral convex normalized by risk | 12 | Adds complexity without clarity for first test |
| 4 | C: Volatility-risk-premium capture | 10 | Requires selling vol; opposite of APEX signal direction |

### Why B (Long Straddle) Is Selected

- Directly implements the economic mechanism: predicted RV > IV → long convex
- Captures the actual option payoff (not just the spread)
- Well-understood in vol trading
- Simplest to implement and interpret
- Costs are explicit and measurable

### Why C (VRP Capture) Is Rejected

- VRP strategies typically **sell** vol (short straddle) because IV > RV on average
- APEX predicts when RV > IV → this is the **opposite** of VRP
- APEX is a long-vol signal, not a short-vol signal
- Selling vol would be directionally wrong for this mechanism

---

## 18. Economic Risk Register

| Risk | Description | Mitigation | Residual Risk |
|------|------------|-----------|---------------|
| Data sparsity | Insufficient eligible observations | IC6 validation gate | Medium — early period may have thin data |
| Maturity mismatch | Option TTE ≠ 12h RV horizon | Frozen rule [6h, 18h]; flagged if mismatched | Low — 8h options available since 2022 |
| Quote staleness | Options quotes may be stale during vol events | 1-hour staleness threshold | Medium — vol events may widen spreads |
| Cost underestimation | Real costs may exceed frozen model | Explicit cost model; slippage acknowledged | Medium — slippage not modeled |
| Path dependency | Straddle payoff depends on path, not just terminal RV | Holding to expiry eliminates path dependency for European options | Low |
| IV repricing | IV may spike after onset, eroding edge before execution | Information boundary: IV observed at onset only | Medium — this is a real risk |
| Multiple episodes | Multiple onset timestamps per episode may cluster | HAC standard errors with lag=12 | Low |
| Regime change | BTC vol dynamics may change over 5-year sample | Chronological OOS design captures regime changes | Low |

---

## 19. What IC5 Establishes

1. The frozen economic methodology for testing the BTC volatility-premium hypothesis
2. The exact straddle definition, entry/exit conventions, and cost model
3. The walk-forward predicted-RV mapping from IC3 risk score
4. The statistical inference framework (HAC t-test, one-sided, α=0.05)
5. The eligibility rules and falsification gates
6. The baseline comparison (unconditional ATM straddle)

## 20. What IC5 Does NOT Establish

1. That the mechanism produces positive expected value (untested)
2. That BTC option data is sufficient (IC6 must validate)
3. That the straddle is profitable (IC7 must test)
4. That the signal has economic edge (IC7 must determine)
5. That the strategy is tradable (not yet tested)

---

## 21. External API calls: 0 | New data acquired: 0 | Spend: $0.00

---

*IC5 is a methodology design milestone. No options were traded. No IV was computed. No PnL was calculated. No data was acquired.*
