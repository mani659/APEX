# FROZEN METHODOLOGY: M19 Economic Translation (Persistence to RV)

## Scientific Question
Does the predicted persistence of a newly triggered HIGH_VOL episode condition the subsequent realized-volatility trajectory in a materially different way from the unconditional HIGH_VOL baseline?

## Prediction Source
The exact, unaltered `conditional_risk_score` from the M17-R2 walk-forward Out-of-Sample predictions CSV.
Higher risk score = shorter predicted duration.

## Target Construction
**Primary Endpoint**: Forward Realized Volatility.
**Estimator**: Annualized standard deviation of M15 log-returns.
**Horizon**: 12 hours (48 M15 bars).
**Window**: Strictly `[t+1, t+48]`, where `t` is the onset close.

## Statistical Framework
**Baseline**: Unconditional forward 12h RV mean across all OOS episodes.
**Model**: Ordinary Least Squares (OLS) regression: $Forward\_RV = \alpha + \beta(Risk\_Score) + \epsilon$.
**Effect Measure**: Slope coefficient ($\beta$).
**Dependence Treatment**: Newey-West HAC standard errors (to correct for temporal overlap).

## Robustness & Secondary Checks
**Secondary Horizons**: 4-hour and 24-hour forward RV.
**Robustness Metric**: Spearman Rank Correlation between Risk Score and Forward RV.

## Status
All items are **FROZEN** and require strict M20 validation prior to execution.
