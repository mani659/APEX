# RC002 Study 001: Behavioral Event Definition

## Final Research Conclusion
**SUPPORTED**

### Target Hypothesis
Can a Behavioral Event be defined objectively using only observable market data?

### Behavioral Event Definition
The **Displacement Exhaustion Event** was defined as a single-bar volatility imbalance where the absolute body size of the candle `abs(close - open)` is strictly greater than **3.0x its local ATR (14)**.
- **Bullish Exhaustion (+1.0)**: Up-close displacement. Represents panic buying, establishing a potential setup for a bearish mean reversion.
- **Bearish Exhaustion (-1.0)**: Down-close displacement. Represents capitulation selling, establishing a potential setup for a bullish mean reversion.

### Experiment Execution
- **Experiment ID**: experiment_000001
- **Dataset Size**: 99980

### Statistics & Distribution (20-Bar Horizon)

#### Bullish Exhaustion
- **Sample Count**: 67
- **Mean Return**: -0.46679
- **Median Return**: -1.81700
- **Standard Deviation**: 18.12495
- **95% CI**: [-4.80685, 3.87327]
- **Effect Size**: -0.026
- **Win Rate (Absolute Price increase)**: 44.8%
- **Expectancy**: -0.46679

#### Bearish Exhaustion
- **Sample Count**: 96
- **Mean Return**: 3.32953
- **Median Return**: 3.30450
- **Standard Deviation**: 19.46999
- **95% CI**: [-0.56528, 7.22434]
- **Effect Size**: 0.171
- **Win Rate (Absolute Price increase)**: 62.5%
- **Expectancy**: 3.32953

### Initial Interpretation
*Note: This study evaluates the mathematical reproducibility of the event, not its profitability.*
The requirement was simply that the behavioral anomaly (3.0 ATR displacement) could be systematically quantified and that it occurs frequently enough in the real market to enable future research. 
With 67 Bullish events and 96 Bearish events, the formulation provides a solid, deterministic foundation.

### Verdict
Because the event was objectively modeled without lookahead bias and produced sufficient occurrences for analysis, the hypothesis that a behavioral exhaustion event can be deterministically defined is **SUPPORTED**. This displacement event will serve as the base signal for subsequent Mean Reversion studies.
