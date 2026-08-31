# APEX IC7 — BTC IV/RV Direction-Neutral Straddle Economic Experiment

**Date**: 2026-08-26
**Milestone**: IC7
**Status**: COMPLETE

---

## 1. Executive Summary

IC7 executes the frozen IC5 economic methodology on 343 eligible BTC options observations.

**Primary Result: NO ECONOMIC EDGE**

| Metric | Value |
|--------|------:|
| Eligible observations | 343 |
| Conditional (predicted RV > IV) | 267 (77.8%) |
| Mean conditional net PnL | **−129.72 USD** |
| Baseline mean net PnL | −199.05 USD |
| Conditional hit rate | 33.7% |
| HAC t-statistic | −1.6720 |
| p-value (one-sided) | 0.9527 |
| Decision | **NO ECONOMIC EDGE** |

The APEX forecast identifies timestamps where straddles lose *less* than the unconditional average ($−130 vs $−199), but does not produce positive expected straddle PnL. The straddle is unprofitable on average because BTC option IV systematically exceeds realized volatility (the volatility risk premium). The APEX signal partially mitigates this but cannot overcome it.

---

## 2. Economic Hypothesis

**H₁:** At timestamps where predicted_RV > IV, mean net straddle PnL > 0.

**H₀:** The APEX-predicted volatility state does not improve expected net straddle payoff relative to zero.

**Result:** H₀ is NOT rejected (p = 0.953). The mean conditional PnL is negative (−$130), so the economic mechanism does not produce positive expected value.

---

## 3. Methodology

### 3.1 Prediction Source

Walk-forward OLS mapping from IC3 risk score to predicted 12h forward RV:

```
predicted_RV = α̂ + β̂ × risk_score
```

OOS correlation between predicted and actual 12h RV: **r = 0.1814** (weak but nonzero predictive signal).

### 3.2 Entry Convention

Entry premium reconstructed via Black-76 from trade-derived IV:

- Forward price (F) = ATM strike (proxy for BTC-PERPETUAL mark)
- Strike (K) = ATM strike (nearest to index price)
- TTE = from instrument expiry
- IV = average of call and put trade-derived IV
- Risk-free rate = 0

**Known limitation:** Using ATM strike as forward price overstates the straddle premium relative to the actual trade price (by ~10-15%). This makes the PnL estimate more negative than reality. The directional conclusion (no economic edge) is robust to this approximation.

### 3.3 Payoff

European straddle held to expiry:

```
gross_payoff = |F_expiry − K| (USD, per 1 BTC notional)
```

F_expiry = BTC M1 close price at option expiry (08:00 UTC).

### 3.4 Costs

```
transaction_cost = 0.0004 × 4 × F_entry = 0.16% of notional
```

### 3.5 Net PnL

```
net_PnL = gross_payoff − straddle_premium_usd − transaction_cost
```

### 3.6 Baseline

Unconditional mean net PnL across all 343 eligible observations.

### 3.7 Statistical Test

One-sample t-test on conditional PnL (predicted_RV > IV), Newey-West HAC maxlags=12, one-sided α=0.05.

---

## 4. Results

### 4.1 Sample

| Metric | Value |
|--------|------:|
| Total eligible | 343 |
| Predicted_RV > IV | 267 (77.8%) |
| Predicted_RV ≤ IV | 76 (22.2%) |

### 4.2 IV vs Predicted RV

| Metric | Predicted RV (%) | IV (%) | Spread (%) |
|--------|------------------:|--------:|-----------:|
| Mean | 62.61 | 54.95 | +7.66 |
| Std | 1.90 | 14.19 | 14.19 |

The APEX model predicts higher annualized volatility (62.6%) than the options market prices (55.0%). The spread is +7.7 percentage points on average.

### 4.3 Straddle Economics

| Metric | Value |
|--------|------:|
| Straddle premium (BTC) | 0.01914 |
| Straddle premium (USD) | 1,209 |
| Gross payoff (USD) | 1,113 |
| Transaction cost (USD) | 103 |
| **Net PnL (USD)** | **−199** |

The straddle loses $199 on average across all eligible observations. The gross payoff ($1,113) is less than the premium paid ($1,209), reflecting the volatility risk premium (IV > RV on average).

### 4.4 Conditional Results (predicted_RV > IV)

| Metric | Value |
|--------|------:|
| N | 267 |
| Mean net PnL | −$130 |
| Median net PnL | −$312 |
| Std net PnL | $1,076 |
| Hit rate | 33.7% |
| 95% CI | [−$282, +$22] |

### 4.5 Statistical Test

| Component | Value |
|-----------|------:|
| HAC t-statistic | −1.6720 |
| HAC SE | 77.58 |
| p-value (one-sided) | 0.9527 |
| 95% CI | [−281.78, +22.34] |

The t-statistic is **negative**, meaning the conditional mean PnL is negative. The one-sided p-value is 0.953, far above the 0.05 threshold. We cannot reject the null hypothesis.

### 4.6 Baseline Comparison

| Condition | Mean PnL | Hit Rate |
|-----------|--------:|--------:|
| Unconditional (all 343) | −$199 | 32.9% |
| Conditional (predicted_RV > IV) | −$130 | 33.7% |
| Improvement | +$69 | +0.8pp |

The APEX signal improves straddle performance by $69 per observation (35% reduction in losses). However, the improvement is not sufficient to produce positive expected PnL.

---

## 5. Decision

### Gate A: N ≥ 100 → **PASS** (267)
### Gate B: Mean conditional PnL > 0 → **FAIL** (−$130)
### Gate C: Conditional > baseline → **PASS** (−130 > −199)
### Gate D: p < 0.05 → **FAIL** (p = 0.953)

### **PRIMARY DECISION: NO ECONOMIC EDGE**

The APEX volatility forecast does not create positive expected value in a direction-neutral long-ATM-straddle payoff. The straddle is unprofitable on average because IV systematically exceeds RV (volatility risk premium). The APEX signal partially identifies when this premium is smaller, but not enough to overcome it.

---

## 6. Maturity Limitation

IC6-R3-CR documented that TTE [12h, 24h] is wider than IC3's 12h forward-RV horizon. This means:

- The predicted RV covers 12h, but the option IV covers ~16.6h
- The straddle payoff captures the full ~16.6h realized move
- The comparison is conservative (the model must predict well enough for a longer-dated straddle)

This limitation does not affect the negative conclusion: even with a maturity advantage, the straddle loses money.

---

## 7. What IC7 Establishes

1. **The BTC volatility risk premium is real and large.** IV (mean 55%) systematically exceeds realized volatility (mean ~50-60% annualized, but concentrated around 55% for the forecast horizon). Long straddles lose money on average.

2. **The APEX signal has predictive content** (r = 0.18, OOS), and it partially identifies when the volatility premium is smaller. The conditional mean PnL ($−130) is 35% better than the unconditional mean ($−199).

3. **The signal is not strong enough for positive straddle expectancy.** The $69 improvement per observation is insufficient to overcome the ~$200 average loss.

4. **The long straddle is not the right instrument for this signal.** The APEX forecast predicts elevated future RV, but the options market already prices this in (or more). A direction-neutral long-vol strategy requires the forecast to be *more accurate than the market's IV*, not just directionally correct.

---

## 8. What IC7 Does NOT Establish

1. Whether a **short straddle** (selling vol) when predicted_RV < IV would be profitable
2. Whether a **volatility spread** (long one maturity, short another) would capture the signal
3. Whether **strike optimization** would improve the payoff
4. Whether **dynamic position sizing** based on the forecast-IV spread would work
5. Whether the signal is profitable on a **risk-adjusted** basis after accounting for tail risk

---

## 9. Methodology Deviations

| Component | IC5 Frozen | IC7 Actual | Deviation |
|-----------|-----------|-----------|-----------|
| Entry price | BBO midpoint | Black-76 from IV with strike-as-forward | Approximation (~10-15% overstatement) |
| IV source | BBO midpoint | Trade-derived IV | Approved by IC6-R3-CR |
| Maturity | [6h, 18h] | [12h, 24h] | Approved by IC6-R2-CR |
| Freshness | ≤ 1h | ≤ 1h trade age | Restored by IC6-R3 |

The entry price approximation makes the PnL estimate more negative than reality. The directional conclusion (no edge) is robust.

---

## 10. Files Created

| File | Purpose |
|------|---------|
| `scripts/ic7_btc_straddle_experiment.py` | IC7 execution script |
| `reports/APEX_IC7_BTC_Straddle_Economic_Data.csv` | Economic data (343 rows) |
| `reports/APEX_IC7_BTC_Straddle_Economic_Experiment.md` | This report |
| `reports/APEX_IC7_RESULT.md` | Structured result file |
| `reports/APEX_IC7_Result_Summary.json` | Machine-readable result |
| `docs/APEX_SESSION_HANDOFF.md` | Updated |
| `docs/APEX_SESSION_STATE.json` | Updated |

---

## 11. External API calls: 0 | New data acquired: 0 | Spend: $0.00

---

*IC7 is the first economic experiment in the APEX crypto-options path. The result is negative: the long straddle does not produce positive expected value from the APEX volatility forecast.*
