# Research Study 004: Liquidity Sweep + Expansion Confirmation

## Final Research Conclusion
**NOT SUPPORTED**

### Target Hypothesis
Does requiring an immediate post-sweep market expansion (normalized > 1 ATR) transform the fragile candidate edge into a robust predictive signal?

### Experiment Execution
- **Experiment ID**: experiment_000005
- **Dataset Size**: 99980
- **Conditioning Variables**: `market_regime_trend_strength` and `normalized_expansion`

### Step-by-Step Edge Construction (20-Bar Horizon)

#### 1. Base Hypothesis (Liquidity Sweep Alone)
- Bullish: Mean=0.04184 | Effect Size=0.003 | 95% CI=[-0.15022, 0.23390]
- Bearish: Mean=-0.05055 | Effect Size=-0.004 | 95% CI=[-0.25453, 0.15343]
*(Observation: Study 001 - Inconclusive, noisy)*

#### 2. Sweep + Regime (Trend Alignment)
- Bullish: Mean=0.54272 | Effect Size=0.043 | 95% CI=[0.22023, 0.86521]
- Bearish: Mean=-0.40619 | Effect Size=-0.025 | 95% CI=[-0.82685, 0.01448]
*(Observation: Study 003 QA - Fragile, crosses zero or weak effect)*

#### 3. Sweep + Expansion (Impulse Alignment > 1 ATR)
- Bullish: Mean=-0.27399 | Effect Size=-0.020 | 95% CI=[-1.06853, 0.52056]
- Bearish: Mean=0.08994 | Effect Size=0.007 | 95% CI=[-0.69324, 0.87311]
*(Observation: How does expansion alone perform?)*

#### 4. Multi-Factor (Sweep + Regime + Expansion)
- Bullish: Mean=0.40492 | Effect Size=0.033 | Win Rate=47.3% | 95% CI=[-0.84660, 1.65644]
- Bearish: Mean=-0.11310 | Effect Size=-0.008 | Win Rate=53.7% | 95% CI=[-1.45383, 1.22763]
*(Observation: The ultimate combined edge)*

### Verdict
The multi-factor configuration was strictly evaluated against the statistical significance (CI != 0) and economic significance (abs(Effect) >= 0.05) criteria. Based on the rules, the hypothesis is **NOT SUPPORTED**.
