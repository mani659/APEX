# APEX M25 FROZEN METHODOLOGY
**Phase**: Economic Translation (Extremum Price Boundary)
**Status**: FROZEN (Awaiting M26 Validation)

## 1. Primary Research Question
Does the M17-R2 predicted HIGH_VOL persistence state condition the magnitude of subsequent price excursions over the same 12-hour horizon?

## 2. Rigid Constraints
- **Prediction Artifact**: M17-R2 Walk-Forward OOS predictions (Eligible episodes only).
- **Predictor**: `conditional_risk_score`
- **Boundary**: `t` (Onset close timestamp).
- **Target Outcome ($MAE_{abs}$)**: $\max_{u\in[t+1,t+48]} \left| \ln(P_u/P_t) \right|$
- **Horizon**: Exactly 12 hours (48 M15 bars).

## 3. Inferential Framework
- **Model**: Ordinary Least Squares (OLS)
- **Specification**: $MAE_{abs} = \alpha + \beta \times \text{RiskScore} + \epsilon$
- **Covariance Treatment**: Newey-West HAC (`maxlags = 48`)
- **Hypothesis**: $H_0: \beta = 0$ vs $H_1: \beta \neq 0$
- **Alpha**: $0.05$ (two-sided)

## 4. Diagnostics & Baseline
- **Primary Baseline**: Unconditional mean of $MAE_{abs}$ over the OOS episodes.
- **Predefined Descriptive Statistic**: Ratio of mean upside excursion to mean downside excursion.

## 5. Falsification
If $p \geq 0.05$ under the frozen HAC model, the finding of extremum boundary translation is falsified.

## 6. M26 Validation Requirements
M26 must structurally audit this methodology against the canonical data without calculating the actual regression $\beta$ or p-value. M26 must verify that the array search logic for the maximum absolute log-distance can be accurately constructed across `[t+1, t+48]` without leakage from `t`.
