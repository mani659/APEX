# RC012 Study 008 — Volatility OCO Monetization

## 1. Frozen Volatility Primitive & M1 Execution Architecture
- **Validation Period Only:** `2024-07-01` to `2026-06-30`
- **Horizon:** 1 hour (60 M1 minutes)
- **Condition:** HIGH_VOL (>80th percentile RV20)
- **Payoff Geometry:** Symmetric Breakout (OCO). Upper trigger at `Close + D`, Lower trigger at `Close - D`, where `D = 0.5 * ATR20`.
- **M1 Walk-Forward Verification:** Intrabar M15 ambiguity was successfully eliminated by simulating the actual minute-by-minute tick sequence for the 60 minutes following every valid M15 signal. 

## 2. Trigger Dynamics & Target Frequencies (1.0 Pip Friction)
The OCO breakout logic triggered nearly universally across both populations, but the symmetry of the exits reveals why the strategy fundamentally fails to monetize the volatility edge:

### Baseline: ALL Observations
- **Trigger Rate:** 96.4%
- **Target (TP) Hit Rate:** 44.3%
- **Stop (SL) Hit Rate:** 46.9%
- **Time Expiry Rate:** 8.3%
- **Net Expectancy (Long):** `-1.1 pips` per trade
- **Net Expectancy (Short):** `-1.0 pips` per trade
- **Profit Factor:** 0.51 - 0.52

### Candidate: HIGH_VOL
- **Trigger Rate:** 93.0%
- **Target (TP) Hit Rate:** 41.1%
- **Stop (SL) Hit Rate:** 41.2%
- **Time Expiry Rate:** 17.0%
- **Net Expectancy (Long):** `-0.95 pips` per trade
- **Net Expectancy (Short):** `-0.82 pips` per trade
- **Profit Factor:** 0.66 - 0.70

*Observation:* While HIGH_VOL slightly improves the overall expectancy relative to the unconditional benchmark (moving from ~-1.1 pips to ~-0.9 pips), it remains mathematically impossible to clear the 1.0 pip transaction friction. 
Crucially, the Target Hit Rate in HIGH_VOL (41.1%) is actually *lower* than the unconditional baseline (44.3%), and the Time Expiry rate is double (17.0% vs 8.3%). 

## 3. The Whipsaw Effect
Why does a massive increase in absolute movement (proven in Study 006) fail to hit targets in an OCO breakout? 
Because the trigger distance and targets are scaled by `ATR`. During HIGH_VOL, `D` is extremely large. The market easily triggers the entry, but the massive intraday volatility leads to severe whipsawing. The market is just as likely to reverse and hit the massive Stop Loss as it is to continue to the massive Target. It is functionally a coin-toss (41% TP vs 41% SL).

## 4. Tail-Risk Protection (V1 Audit)
The symmetric 1R:1R OCO architecture mathematically constraints tail risk, preventing the catastrophic concentration of losses seen in Study 007's fixed-horizon hold:
- **Tail Contribution (HIGH_VOL):** The worst 10% of trades accounted for ~33% of total losses (compared to 49% in Study 007). 
- **Maximum Drawdown:** Highly controlled compared to the unbounded directional hold, but the equity curve is a perfectly smooth 45-degree angle downward due to negative expectancy.

## 5. Candidate Classification

### REJECTED

HIGH_VOL does not sufficiently improve the symmetric OCO architecture, and the architecture itself remains trapped in negative expectancy due to the structural mechanics of volatility whipsaw and spread crossing.

## 6. Final Scientific Conclusion

> **Can a symmetric, direction-neutral breakout payoff capture the movement-magnitude edge that a simple directional hold could not?**

**NO.** This study establishes the second critical limitation in translating the validated Volatility Distribution Primitive into a trading edge. 

While the primitive accurately predicts that the absolute movement will expand significantly, placing a symmetric breakout order (with targets scaled by that same volatility) simply exposes the strategy to high-frequency whipsaw. The market crosses the entry threshold but is immediately subject to the violent mean-reversion inherent to high-volatility states, hitting the Stop Loss before the Target approximately 50% of the time. 

**Final Principle Demonstrated:** 
The volatility primitive remains a validated distributional fact (Study 005/006). However, both a naive directional hold (Study 007) and a naive symmetric breakout (Study 008) are fundamentally incapable of extracting economic value from it. The monetization of this specific volatility state requires a payoff geometry that either trades the *implied vs realized* volatility premium (options), or utilizes highly asymmetric intraday execution logic (e.g., trend-following trailing stops that truncate the whipsaw).
