# APEX M22 FROZEN METHODOLOGY
**Phase**: Economic Translation (Directional Price Distribution)
**Status**: FROZEN (Awaiting M23 Validation)

## 1. Primary Research Question
Does the M17-R2 predicted persistence state of a newly triggered HIGH_VOL episode condition the directional distribution of subsequent price returns?

## 2. Rigid Constraints
- **Prediction Artifact**: M17-R2 Walk-Forward OOS predictions (396 valid episodes).
- **Predictor**: `conditional_risk_score`
- **Boundary**: `t` (Onset close timestamp).
- **Target Outcome**: $R_{48} = \ln(P_{t+48}/P_t)$
- **Horizon**: Exactly 12 hours (48 M15 bars).

## 3. Inferential Framework
- **Model**: Ordinary Least Squares (OLS)
- **Specification**: $R_{48} = \alpha + \beta \times \text{RiskScore} + \epsilon$
- **Covariance Treatment**: Newey-West HAC (`maxlags = 48`)
- **Hypothesis**: $H_0: \beta = 0$ vs $H_1: \beta \neq 0$
- **Alpha**: $0.05$ (two-sided)

## 4. Diagnostics & Baseline
- **Primary Baseline**: Unconditional mean of $R_{48}$ over the 396 episodes.
- **Predefined Robustness**: Spearman rank correlation.
- **Predefined Descriptive Statistic**: Sample skewness of $R_{48}$.

## 5. Falsification
If $p \geq 0.05$, the finding of directional translation is falsified.

## 6. M23 Validation Requirements
M23 must structurally audit this methodology against the canonical data without calculating the actual regression $\beta$ or p-value. M23 must verify that the cumulative log return $R_{48}$ can be accurately constructed and aligned with the `t` boundary without leakage.
