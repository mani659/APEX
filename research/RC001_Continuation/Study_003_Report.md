# Research Study 003: Candidate Edge Robustness Analysis

## Final Research Conclusion
**FRAGILE**

### Target Setup: Trend Continuation
- **Bullish Continuation (20-bar)**: Mean=0.54272, 95% CI=[0.22023, 0.86521], Effect Size=0.043, Win Rate=49.8%
- **Bearish Continuation (20-bar)**: Mean=-0.40619, 95% CI=[-0.82685, 0.01448], Effect Size=-0.025, Win Rate=46.9%

### Horizon Comparison (Is the edge stable?)
- Bull Sweep in Bull Trend Mean Returns: H5=0.08548 -> H10=0.27106 -> H20=0.54272
- Bear Sweep in Bear Trend Mean Returns: H5=-0.02399 -> H10=-0.19984 -> H20=-0.40619
The edge strengthens significantly across horizons, indicating stable and persistent momentum rather than a fleeting anomaly.

### Tail-Risk & Distribution
- Bullish Continuation Skew: 1.14, Kurtosis: 16.81
- Bearish Continuation Skew: -1.83, Kurtosis: 24.97
The distributions exhibit positive skew in the direction of the trade (favorable tail behavior).

### Practical Interpretation
The candidate edge is **FRAGILE**. While the Bullish Sweep inside a Bull Trend produced a positive mean return, its effect size is negligible (< 0.05) and its win rate sits at a coin flip (49.8%). More critically, the Bearish Sweep inside a Bear Trend produced a 95% Confidence Interval that crosses zero, meaning the signal is statistically indistinguishable from random noise.
