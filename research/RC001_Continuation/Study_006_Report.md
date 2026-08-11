# Research Study 006: Liquidity Sweep Taxonomy

## Final Research Conclusion
**NOT SUPPORTED**

### Target Hypothesis
Can liquidity sweeps be partitioned into distinct behavioral classes (Strong Rejection vs Weak Rejection), and does one class exhibit statistically meaningful predictive power?

### Experiment Execution
- **Experiment ID**: experiment_000007
- **Dataset Size**: 99980
- **Taxonomy Method**: Rejection Strength (Candle close relative to high-low midpoint)

### Step-by-Step Edge Construction (20-Bar Horizon)

#### 1. Base Hypothesis (All Liquidity Sweeps)
- Bullish: Mean=0.04184 | Effect Size=0.003 | Win Rate=51.6% | 95% CI=[-0.15022, 0.23390]
- Bearish: Mean=-0.05055 | Effect Size=-0.004 | Win Rate=51.3% | 95% CI=[-0.25453, 0.15343]

#### 2. Taxonomy Classes

##### Strong Rejection
- **Bullish**: Mean=-0.06618 | Effect=-0.004 | Win Rate=51.4% | CI=[-0.29305, 0.16069] | Sig=False
- **Bearish**: Mean=-0.10563 | Effect=-0.008 | Win Rate=51.3% | CI=[-0.33692, 0.12565] | Sig=False

##### Weak Rejection
- **Bullish**: Mean=0.31922 | Effect=0.022 | Win Rate=52.1% | CI=[-0.04150, 0.67994] | Sig=False
- **Bearish**: Mean=0.12318 | Effect=0.008 | Win Rate=51.2% | CI=[-0.30791, 0.55427] | Sig=False

### Verdict
The taxonomy configuration was strictly evaluated against statistical significance (directional CI), economic significance (abs(Effect) >= 0.05), and sample adequacy.
Based on the rules, the hypothesis is **NOT SUPPORTED**.

Recommendation: The taxonomy failed to isolate a strictly profitable directional edge. Re-evaluating the underlying continuation premise may be necessary.
