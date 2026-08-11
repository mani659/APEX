# Research Study 002: Liquidity Sweep + Market Regime

## Final Research Conclusion
**SUPPORTED**

### Results Summary
- **Experiment ID**: experiment_000003
- **Dataset Size**: 99980 records
- **Validation**: PASSED
- **Features Evaluated**: liquidity_sweep_strength, market_regime_trend_strength
- **Target Horizons**: 5, 10, 20 bars

### Conditional Return Analysis (Horizon=20)
| Condition | Sample Size | Mean Forward Return |
|-----------|-------------|---------------------|
| Bull Sweep in Bull Trend | 5949 | 0.54272 |
| Bull Sweep in Ranging | 8625 | -0.08088 |
| Bull Sweep in Bear Trend | 7935 | -0.20027 |
| Bear Sweep in Bear Trend | 5753 | -0.40619 |
| Bear Sweep in Ranging | 7273 | -0.16278 |
| Bear Sweep in Bull Trend | 5250 | 0.49465 |

### Findings
The conditioning variable (Market Regime) produced the strongest effect under: **Trend Continuation (Bull sweep in Bull trend, Bear sweep in Bear trend)**.

### Archival Status
Successfully written to Phase 2 Experiment Repository at `D:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex\research\RC001_Continuation\repository`.
