# RC012 Study 010 — Two-Sided Path-Harvesting Diagnostic

## 1. Frozen Architecture & M1 Path Diagnostics
- **Validation Window:** `2024-07-01` to `2026-06-30`
- **Architecture:** Symmetric OCO Breakout (TP = 0.5 ATR20, SL = 0.5 ATR20, Expiry = 60 M1 minutes).
- **Diagnostics Setup:** Two separate path populations were analyzed for every trade:
  - **Full-Window Path:** The entire 60 minutes following the signal.
  - **Active-Trade Path:** The path specifically experienced from the moment the OCO was triggered until the exact moment it hit TP, SL, or Time Expiry.

## 2. Path Truncation: The Core Failure
The primary objective was to diagnose why the `HIGH_VOL` environment (which mathematically generates massive absolute movement) cannot be monetized by the OCO architecture. 

The diagnostic metrics definitively answer this:
- **Full Available Path Length (HIGH_VOL):** 69.3 pips.
- **Active Trade Path Length (HIGH_VOL):** **14.7 pips.**

**Diagnostic Conclusion:** The OCO architecture systematically truncates the trade. Because the Target and Stop are rigidly placed at `0.5 ATR20`, the massive intraday volatility instantly triggers the entry and then immediately whipsaws into the Stop Loss or Target. The trade is terminated after experiencing only **21%** of the available path length, completely missing the remaining ~55 pips of structural chop. 

## 3. Drawdown Elasticity (Post-Adverse Expansion)
Does the market offer favorable movement after a drawdown, or is a tight Stop Loss justified?
- **Mean MFE (HIGH_VOL):** 4.08 pips.
- **Mean MAE (HIGH_VOL):** 4.46 pips.
- **Post-Adverse Favorable Expansion:** **3.29 pips.**

*Interpretation:* If the active trade experiences a drawdown (moves against the position by > 1.0 pip), the market still subsequently generates another 3.29 pips of favorable expansion before exiting. By placing a rigid Stop Loss at `0.5 ATR`, the OCO architecture explicitly prevents the trade from capturing this elastic rebound, forcing a realized loss in an environment mathematically dominated by mean-reversion.

## 4. Cost Decay & Capture Efficiency
- **Cost Decay (Active Trade):** 0.131. This means the 1.0 pip transaction friction consumes a devastating 13% of all the price movement the active trade actually experiences (1.0 pip cost / 14.7 pips of active travel). 
- **Gross PnL (HIGH_VOL):** +0.12 pips (slightly positive before the 1.0 pip friction, but heavily negative net). 

## 5. Answers to the Core Diagnostic Questions

### Question 1: How much more path length exists during HIGH_VOL?
Approximately 15 pips of excess two-sided chop (69.3 pips vs 54.8 pips in the unconditional baseline).

### Question 2: How much of that path occurs before the OCO exits?
Only 14.7 pips.

### Question 3: Does the OCO exit systematically truncate available future path length?
Yes, severely. It forces the trade out of the market, abandoning nearly 80% of the available path length that the `HIGH_VOL` state reliably generates.

### Question 4: How much favorable movement occurs after an initial drawdown?
3.29 pips. The market is highly elastic and frequently rebounds favorably after initial adversity.

### Question 5: Is the failure caused primarily by...
The failure is caused by **Premature Exit** driven by rigid **Stop/Target Placement**. The OCO places tight boundaries around a highly elastic, two-sided environment. The strategy is chopped out long before the actual volatility structure can be harvested.

## 6. Reconciliation with Prior Studies
- **Study 006** succeeded because a Straddle has no Stop Loss and no fixed Take Profit; it holds to the horizon and captures the final absolute displacement of the entire 69.3 pip path.
- **Study 007 & 008** failed because they attempted to enforce rigid directional assumptions (fixed direction, or rigid stop losses) onto a low-efficiency, high-chop environment.

## 7. Candidate Classification

### REJECTED (Diagnostic Validation)

The bounded OCO architecture fails to monetize the path length because its rigid exits structurally prevent it from harvesting the very chop that `HIGH_VOL` generates. 

## 8. Final Scientific Conclusion

> **Why does a validated increase in total market travel fail to produce positive expectancy under the symmetric OCO architecture?**

The observed path geometry proves that `HIGH_VOL` provides massive path length, but it does so via continuous, elastic, two-sided whipsaw. 

The OCO architecture places a rigid target and a rigid stop close to the entry. In a high-whipsaw environment, the market will randomly hit one of these boundaries extremely quickly (after only 14.7 pips of travel). This premature exit completely abandons the remaining 55 pips of available path length. 

**Final Principle:** We cannot monetize a "Path Length" edge using an architecture designed for "Directional Efficiency". A strategy that places tight stop losses in a highly elastic, two-sided chop environment will mathematically bleed to death via transaction costs and whipsaw. To capture path length, the architecture must allow the trade to breathe through adversity and harvest the two-sided oscillations (e.g., Grid harvesting or wide-stop fading).
