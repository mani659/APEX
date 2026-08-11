# Research Study 005: Liquidity Sweep + Session Conditioning

## Final Research Conclusion
**FRAGILE (Invalidated by QA)**

### Target Hypothesis
Does conditioning liquidity sweeps by trading session produce a statistically stronger continuation edge?

### Experiment Execution
- **Experiment ID**: experiment_000006
- **Dataset Size**: 99980
- **Conditioning Variable**: `market_session`

### Step-by-Step Edge Construction (20-Bar Horizon)

#### 1. Base Hypothesis (Liquidity Sweep Alone)
- Bullish: Mean=0.04184 | Effect Size=0.003 | Win Rate=51.6% | 95% CI=[-0.15022, 0.23390]
- Bearish: Mean=-0.05055 | Effect Size=-0.004 | Win Rate=51.3% | 95% CI=[-0.25453, 0.15343]
*(Observation: Study 001 Base - Inconclusive, noisy)*

#### 2. Session Conditioned Sweeps

##### Asian Session
- **Bullish**: Mean=0.15505 | Effect=0.011 | Win Rate=52.3% | CI=[-0.15932, 0.46943] | Expectancy=0.15059
- **Bearish**: Mean=0.18286 | Effect=0.013 | Win Rate=52.6% | CI=[-0.15902, 0.52474] | Expectancy=0.18286

##### London Session
- **Bullish**: Mean=-0.14102 | Effect=-0.011 | Win Rate=51.1% | CI=[-0.48447, 0.20243] | Expectancy=-0.14733
- **Bearish**: Mean=-0.53853 | Effect=-0.044 | Win Rate=48.5% | CI=[-0.92014, -0.15691] | Expectancy=-0.54642

##### London/NY Overlap Session
- **Bullish**: Mean=-1.34525 | Effect=-0.069 | Win Rate=49.3% | CI=[-2.04225, -0.64825] | Expectancy=-1.34525
- **Bearish**: Mean=-0.83530 | Effect=-0.049 | Win Rate=51.2% | CI=[-1.50034, -0.17025] | Expectancy=-0.85048

##### New York Session
- **Bullish**: Mean=0.29608 | Effect=0.022 | Win Rate=51.8% | CI=[-0.08388, 0.67603] | Expectancy=0.29275
- **Bearish**: Mean=-0.15045 | Effect=-0.012 | Win Rate=51.1% | CI=[-0.54544, 0.24453] | Expectancy=-0.15859

##### Other Session
- **Bullish**: Mean=1.67648 | Effect=0.104 | Win Rate=53.4% | CI=[0.93974, 2.41322] | Expectancy=1.67648
- **Bearish**: Mean=1.90368 | Effect=0.112 | Win Rate=53.9% | CI=[1.03075, 2.77661] | Expectancy=1.90368

### Verdict
The session configuration was strictly evaluated against statistical significance (CI != 0), economic significance (abs(Effect) >= 0.05), and relative improvement over the base edge. 
Based on QA verification, the hypothesis is **FRAGILE** and Study 005 is INVALIDATED due to temporal instability or rule failures.

The strongest edge was observed during the **Other** session.
