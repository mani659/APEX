# APEX M15 FROZEN METHODOLOGY: Conditional Predictability

## 1. Scientific Objective
Determine whether the persistence of a `HIGH_VOL` episode is conditionally predictable from market-state information available through the close of the onset bar.

## 2. Target Variable
- **Target**: Future episode duration (contiguous M15 bars).
- **Framework**: Survival Time-to-Event analysis with right-censoring support.

## 3. Information Boundary
- **Prediction Timestamp**: Exact close of the $t_{onset}$ bar. No feature may utilize information from $t_{onset+1}$ or later.

## 4. Predeclared Predictors
1. **Breakout Intensity**: $RV20_{onset} / Threshold80_{onset}$
2. **Variance Momentum**: $RV20_{onset} - RV20_{onset-4}$
3. **Regime Depth**: $RV20_{onset} / Threshold50_{onset}$

## 5. Primary Model
- **Model**: Cox Proportional Hazards Model.
- **Inference Mechanism**: Modeling the conditional log-hazard of termination.

## 6. Null Hypothesis
The predictors provide zero predictive improvement over the unconditional baseline, defined formally as an Out-of-Sample Concordance Index $C \le 0.50$.

## 7. Out-of-Sample Evaluation Architecture
- **Design**: Walk-forward (Expanding Window).
- **Initial Training Set**: Chronological first 50% of episodes.
- **Testing**: Train on $[0, t]$, predict for $t+1$. Expand window to $[0, t+1]$, predict for $t+2$.
- **Metric**: Harrell's Concordance Index (C-index) computed on the aggregated out-of-sample predictions.

## 8. Leakage Controls
- All predictor standardization/scaling must be computed using only the data within the specific walk-forward training window.

## 9. Causality Disclaimer
This framework tests for conditional predictive power. Rejection of the null hypothesis demonstrates statistical predictability; it does not prove a causal mechanism driving volatility duration.
