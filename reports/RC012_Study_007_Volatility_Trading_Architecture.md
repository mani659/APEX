# RC012 Study 007 — Volatility Primitive Trading Architecture

## 1. Frozen Volatility Primitive & Validation Boundary
- **Validation Period Only:** The trading architecture was executed exclusively on the `2024-07-01` to `2026-06-30` out-of-sample period.
- **States:** `HIGH_VOL` (>80th percentile) and `LOW_VOL` (<20th percentile) based on the 480-bar RV20 historical distribution.

## 2. Trading Architecture & Cost Assumptions
The simplest possible fixed-horizon directional architecture was applied to isolate the trading value of the volatility primitive without relying on optimized exit mechanics:
- **Entry:** Close of the signal bar.
- **Exit:** Fixed time holding period corresponding to the evaluated horizon (4 bars or 64 bars). No trailing stops, Take-Profits, or Stop-Losses were utilized.
- **Friction:** 1.0 pip primary round-trip cost assumption per trade.

## 3. Directional Neutrality & Combined PnL Mechanics
To guarantee a direction-neutral evaluation, a Long reference and Short reference were generated independently for every single signal. The **Combined Direction-Neutral Result** treats both the Long and Short outcomes as a single unified population. 
*Note on structural mathematics:* Because every signal generates both a Long and a Short trade with a symmetric fixed-horizon exit, the gross PnL of the combined pair is mathematically exactly zero. Therefore, the theoretical Combined Expectancy is rigidly fixed to `-1.0 pip` (the transaction friction). The purpose of the study is to evaluate if the *win rate, payoff ratio, or tail mechanics* of the conditionally filtered trades improve structurally, even if the naive fixed-time directional expectancy cannot overcome the spread.

## 4. Combined Direction-Neutral Results

### Horizon A (4 bars / 1 hour)
| Condition | N (Trades) | Expectancy | Win Rate | Profit Factor | Payoff Ratio | Max Drawdown |
|:---|---:|---:|---:|---:|---:|---:|
| **ALL (Unconditional)** | 24,864 | -1.00 pips | 43.2% | 0.75 | 0.98 | L: 1.17 / S: 1.31 |
| **HIGH_VOL** | 5,066 | -1.00 pips | **45.3%** | 0.80 | 0.96 | L: 0.19 / S: 0.33 |

### Horizon C (64 bars / 16 hours)
| Condition | N (Trades) | Expectancy | Win Rate | Profit Factor | Payoff Ratio | Max Drawdown |
|:---|---:|---:|---:|---:|---:|---:|
| **ALL (Unconditional)** | 1,554 | -1.00 pips | 48.8% | 0.93 | 0.98 | L: 0.11 / S: 0.22 |
| **LOW_VOL** | 318 | -1.00 pips | **49.4%** | 0.94 | 0.96 | L: 0.06 / S: 0.06 |

*Observation:* While the conditionally filtered states (HIGH_VOL 4-bar and LOW_VOL 64-bar) produce marginally higher win rates and profit factors compared to the unconditional baseline, they remain mathematically constrained to negative expectancy. A simple fixed-horizon directional hold cannot monetize a distributional volatility edge.

## 5. Directional Reference Split (HIGH_VOL 4-Bar)
Did one direction unexpectedly dominate?
- **Long Expectancy:** -0.73 pips
- **Short Expectancy:** -1.26 pips
*Conclusion:* The slight bullish drift over the period marginally favored Longs, but both directions were solidly negative. The primitive provided no hidden directional edge. 

## 6. Tail-Risk Protection (V1 Audit)
The study required verifying that the payoff geometry was not hiding catastrophic tail risk.
**HIGH_VOL 4-Bar Tail Contribution:**
- The worst 1% of trades generated **11.0%** of total losses.
- The worst 10% of trades generated **49.2%** of total losses.

**Leave-Worst-Trades Analysis (HIGH_VOL 4-Bar):**
- Original Expectancy: `-1.00 pips`
- Removing worst 1%: `-0.45 pips`
- Removing worst 10%: `+1.85 pips`

*Conclusion:* The fixed-horizon hold suffers heavily from fat-tailed adverse excursions. If a stop-loss is not employed, a massive percentage of total losses accumulates in a tiny minority of severe adverse moves (the exact opposite of the desired volatility payoff).

## 7. Temporal Stability
- **Early HIGH_VOL 4-bar:** Win Rate = 45.9%, PF = 0.81
- **Late HIGH_VOL 4-bar:** Win Rate = 44.5%, PF = 0.76
The architecture remained stable and consistently negative across both validation halves.

## 8. Candidate Classification

### REJECTED

The validated distributional primitive does NOT produce positive trading expectancy using this simple, fixed-horizon directional architecture.

## 9. Final Scientific Conclusion

> **Can the validated volatility-distribution primitive be converted into positive expectancy using a simple, transparent, direction-neutral trading architecture?**

**NO.** This study provides a highly valuable, definitive negative result. It empirically proves the separation between an *Economic Edge* (Study 006) and a *Trading Edge* (Study 007). 

While HIGH_VOL guarantees a massive increase in absolute movement (proven in Study 006), taking a simple directional trade and holding it for a fixed amount of time *does not capture absolute movement*. Because a fixed-time hold lacks the geometric asymmetry required to harvest volatility (such as a Take-Profit to capture the spike, or a Stop-Loss to truncate the adverse side of the straddle), the excess movement acts equally as favorable and adverse PnL, netting exactly to zero minus the spread.

**Final Verdict:** The distributional information remains scientifically valid and mathematically proven. However, its direct monetization requires an explicitly asymmetric execution architecture (e.g., OCO breakouts, volatility-scaled TP/SL grids, or trailing stops) to convert absolute movement magnitude into directional realized profit. The "simplest possible directional execution" fails the test.
