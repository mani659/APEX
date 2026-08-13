# RC012 Study 011 — Bounded Two-Unit Inventory Analysis

## 1. Frozen Architecture
- **Validation Window:** `2024-07-01` to `2026-06-30` (HIGH_VOL only).
- **Exit Mechanic:** Pure 60-minute time expiry (no TP, no SL). This forces the basket to survive the entire chop window.
- **Model A (Reference):** 1-unit maximum.
- **Model B (Candidate):** 2-unit maximum. Unit 2 is activated only if the active trade experiences an adverse movement of `0.5 ATR20`.

## 2. Core Economic Findings
Did adding a bounded, fixed-size second unit safely harvest the oscillatory path length?

### Model A (Single Unit)
- **Expectancy:** -1.13 pips
- **Win Rate:** 42.3%
- **Average Win/Loss:** +7.8 pips / -7.6 pips
- **Profit Factor:** 0.745

### Model B (Two-Unit Bounded)
- **Expectancy:** **-1.46 pips**
- **Win Rate:** 47.6%
- **Average Win/Loss:** +10.4 pips / -12.2 pips
- **Profit Factor:** 0.772

*Interpretation:* Model B improved the Win Rate by roughly 5% and slightly improved the Profit Factor. However, it **worsened** the overall expectancy (from -1.13 to -1.46 pips). 

## 3. Inventory Mechanics & Recovery Rate
- **Unit 2 Activation Rate:** 54.2% (More than half of all trades experience an adverse excursion large enough to activate the second unit).
- **Recovery Success Rate:** **31.9%**.
  
Of the trades that activated the second unit, only ~32% bounced back enough to generate a positive basket PnL by the end of the 60 minutes. The remaining ~68% of the time, the market continued moving adversely, leaving the basket holding 2 units of losing inventory at horizon expiry.

## 4. Tail-Risk Geometry
This architecture explicitly recreates the negative-tail phenomenon of the Apex grid, despite being strictly bounded to 2 units:
- **Maximum Drawdown (Short-Side):** Increased from 1,925 pips (Model A) to 2,618 pips (Model B).
- **Worst 1% Tail Contribution:** Increased from 7.7% of total losses (Model A) to 9.4% (Model B).

When the second unit fails to catch a mean-reverting bounce, it doubles the exposure during the worst adverse directional paths. The value gained from the 32% of successful recoveries is completely destroyed by the compounded losses in the 68% of failed recoveries.

## 5. Candidate Classification

### REJECTED

The bounded 2-unit inventory fails to safely monetize the `HIGH_VOL` oscillatory path. It worsens net expectancy and materially increases drawdown and tail-risk relative to the 1-unit baseline.

## 6. Final Scientific Conclusion

> **Can one additional equal-sized, bounded inventory unit harvest enough of the validated HIGH_VOL oscillatory movement to improve expectancy without recreating the tail-risk mechanism that invalidated the original Apex grid architecture?**

No. Even a strictly bounded 2-unit architecture with no size escalation (martingale) fails. 

**Final Verdict:** The observed path-length advantage (identified in Study 009 and 010) cannot be safely monetized by accumulating adverse inventory. The market's geometry is highly elastic, but the variance of that elasticity is too wide. Adding inventory when the market moves against you mathematically guarantees that during the inevitable structural directional trends, you will hold maximum exposure at the worst possible prices, destroying any edge gained during the chop.
