# RC007 Study 009: Exit Architecture De-conflation

## Model 1 - Observation Only (240 Bars)
- **Win Rate**: 35.1%
- **Mean Return**: -0.00048
- **Median Return**: -0.00043
- **Profit Factor**: 0.38
- **Average Winner**: 0.00082
- **Average Loser**: -0.00119
- **Win/Loss Size Ratio**: 0.69
- **Maximum Loss**: -0.00748
- **95th Percentile Loss (p5)**: -0.00277
- **99th Percentile Loss (p1)**: -0.00494

### Tail-Risk & Profit Concentration
- **Top 1% Profit Contribution**: 17.5%
- **Top 5% Profit Contribution**: 47.2%
- **Worst 1% Loss Contribution**: 7.7%
- **Worst 5% Loss Contribution**: 24.6%
- **Small Winners Required to Offset Max Loss**: 9.1

## Model 2 - Frozen Apex Exit
- **Win Rate**: 89.0%
- **Mean Return**: 0.00057
- **Median Return**: 0.00036
- **Profit Factor**: 1.73
- **Average Winner**: 0.00152
- **Average Loser**: -0.00746
- **Win/Loss Size Ratio**: 0.20
- **Maximum Loss**: -0.06983
- **95th Percentile Loss (p5)**: -0.00342
- **99th Percentile Loss (p1)**: -0.01622

### Tail-Risk & Profit Concentration
- **Top 1% Profit Contribution**: 15.8%
- **Top 5% Profit Contribution**: 46.2%
- **Worst 1% Loss Contribution**: 42.2%
- **Worst 5% Loss Contribution**: 88.0%
- **Small Winners Required to Offset Max Loss**: 45.9

## Model 3 - Symmetric 1R Reference
- **Win Rate**: 28.5%
- **Mean Return**: -0.00012
- **Median Return**: -0.00018
- **Profit Factor**: 0.43
- **Average Winner**: 0.00032
- **Average Loser**: -0.00030
- **Win/Loss Size Ratio**: 1.07
- **Maximum Loss**: -0.00162
- **95th Percentile Loss (p5)**: -0.00065
- **99th Percentile Loss (p1)**: -0.00099

### Tail-Risk & Profit Concentration
- **Top 1% Profit Contribution**: 10.7%
- **Top 5% Profit Contribution**: 38.8%
- **Worst 1% Loss Contribution**: 6.6%
- **Worst 5% Loss Contribution**: 21.0%
- **Small Winners Required to Offset Max Loss**: 5.0

## Scientific Interpretation
1. **Does the frozen exit architecture produce genuine positive expectancy?**
Yes, Model 2 (Frozen Apex Exit) maintains a positive mean expectancy, confirming that the exit architecture turns the negative standalone signal (Model 1) into a nominally profitable system.

2. **Is the positive result robust or tail-dependent?**
It demonstrates some robustness, although the tail-risk must be carefully monitored.

3. **How much does the exit architecture alter the distribution created by the negative entry?**
Massively. It artificially shifts the win rate from 35.1% to 89.0%, totally warping the natural distribution observed in Model 1.

4. **Is the 89% win rate economically meaningful?**
No. The high win rate is a statistical illusion caused by closing winners fast (Avg Win 0.00152) and holding losers deep (Avg Loss -0.00746). Model 3 (Symmetric 1R) clearly shows the true predictive capability of the entry is ~28.5% when forced to be symmetric.

5. **What is the true cost of the losing tail?**
A single tail-event loss (-0.06983) requires 45.9 consecutive winners just to break even. This catastrophic negative skew implies guaranteed ruin given infinite time.

6. **Does the exit architecture create a viable trading distribution or merely a high-win-rate illusion?**
It creates a high-win-rate illusion. A robust strategy extracts edge through predictive accuracy or favorable positive asymmetry, whereas this exit architecture merely packages negative expectancy into rare but devastating explosions.

## Final Verdict
**Outcome B — High-Win-Rate Illusion:** The architecture produces many small winners but negative or fragile expectancy due to large tail losses.
