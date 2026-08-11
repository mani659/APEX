# RC002 Study 002: Behavioral Event Recoil Analysis

## Final Research Conclusion
**NOT SUPPORTED**

### Target Hypothesis
After a Behavioral Exhaustion Event (3.0x ATR Displacement), does statistically significant mean reversion (recoil) occur?

### Experiment Execution
- **Experiment ID**: experiment_000002
- **Dataset Size**: 99960
- **Horizons Analyzed**: 5, 10, 20, 40 bars

### Horizon Comparison

#### Bullish Exhaustion (Expecting Bearish Recoil / Negative Mean)
- **H=5**: Mean=1.5257 | 95% CI=[-2.0214, 5.0727] | Effect=0.103 | Skew=4.49 | Kurt=29.86
- **H=10**: Mean=0.2991 | 95% CI=[-3.6369, 4.2350] | Effect=0.018 | Skew=1.34 | Kurt=9.16
- **H=20**: Mean=-0.4668 | 95% CI=[-4.8068, 3.8733] | Effect=-0.026 | Skew=0.40 | Kurt=1.42
- **H=40**: Mean=4.7144 | 95% CI=[-1.3472, 10.7760] | Effect=0.186 | Skew=2.36 | Kurt=8.01

#### Bearish Exhaustion (Expecting Bullish Recoil / Positive Mean)
- **H=5**: Mean=1.6138 | 95% CI=[-0.7359, 3.9635] | Effect=0.137 | Skew=-0.41 | Kurt=1.33
- **H=10**: Mean=2.2372 | 95% CI=[-1.0477, 5.5222] | Effect=0.136 | Skew=-0.44 | Kurt=1.10
- **H=20**: Mean=3.3295 | 95% CI=[-0.5653, 7.2243] | Effect=0.171 | Skew=-0.16 | Kurt=1.96
- **H=40**: Mean=2.4262 | 95% CI=[-2.9809, 7.8333] | Effect=0.090 | Skew=-0.43 | Kurt=0.77

### Behavioral Interpretation
- **Time Evolution**: By observing the means across 5, 10, 20, and 40 bars, we can see the time evolution of the mean reversion. 
- **Distribution Analysis**: High kurtosis indicates "fat tails" or explosive moves. Significant skewness indicates asymmetry in the payout.

### Verdict
The hypothesis is **NOT SUPPORTED**. Based on the strict requirement for robust CI excluding zero in the appropriate direction (negative for bullish exhaustion, positive for bearish exhaustion) and an absolute effect size > 0.05 on at least 2 horizons.
