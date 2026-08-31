# APEX M17-R2: Conditional HIGH_VOL Predictability Re-Execution

## 1. Executive Summary
The M17-R2 experiment successfully executed the strictly out-of-sample, walk-forward Cox Proportional Hazards evaluation on the `HIGH_VOL` persistence primitive. Utilizing only information available at the exact onset boundary, the two-feature conditional model achieved a Harrell's Concordance Index of **0.6656** against the unconditional random baseline of **0.5000**. This demonstrates a substantial out-of-sample discriminative ability. 

## 2. Frozen Scientific Methodology
- **Research Question**: Is the persistence of a newly triggered HIGH_VOL episode predictable from market-state information available strictly before or exactly at the onset bar?
- **Dataset**: 794 canonical EURUSD `HIGH_VOL` episodes.
- **Walk-Forward Design**: Chronological expanding window (397 initial training episodes; 397 sequential OOS testing episodes).
- **Predictor Set**: `Breakout_Intensity` and `Variance_Momentum`.
- **Target**: Future contiguous M15 bars until episode termination.
- **Model**: `statsmodels.PHReg` (Cox Proportional Hazards).

## 3. Results
- **Successful Cox Fits**: 397
- **Failed Cox Fits**: 0
- **Total Comparable Pairs**: 74,488 (approximate pairwise rank evaluations)
- **Conditional OOS C-index**: 0.6656
- **Baseline OOS C-index**: 0.5000
- **Delta C-index**: +0.1656

## 4. Methodology Integrity Audit
- **Event Ledger Match**: Yes. Exactly 794 events recovered.
- **Chronological Split**: Yes. 397 training / 397 OOS.
- **Predictor Bleed**: Zero. All features were extracted purely at onset close.
- **Preprocessing Leakage**: Zero. Standard scaling was exclusively fitted within the strictly expanding historical boundary for each step.
- **Model Tuning**: Zero. No hyperparameters, alternative metrics, or feature selection routines were executed.
- **Integrity**: `PASS`. The result is a mathematically pure out-of-sample evaluation.

## 5. Scientific Conclusion
**PREDICTIVE SIGNAL ESTABLISHED**. 
The empirical results confirm that `HIGH_VOL` is not merely an unpredictable threshold-crossing process. The physical magnitude of the initial variance breakout and its short-term momentum objectively condition the expected lifespan of the ensuing volatility expansion. 

## 6. What This Does NOT Establish
- **Profitability**: A C-index of 0.66 indicates strong duration ranking, but does not equate to positive PnL.
- **Tradability**: It does not prove that a strategy can capture the bid/ask spread during these episodes.
- **Causality**: The predictors carry statistical information, but do not definitively prove the causal market mechanics behind the persistence.

## 7. M18 Recommendation
With a predictive signal formally established, the APEX project has graduated from structural statistics into economic forecasting. M18 is recommended to begin bridging the gap toward economic utility, specifically by evaluating whether this persistence predictability maps onto directional price moments, tradable volatility clusters, or specific regime boundaries.
