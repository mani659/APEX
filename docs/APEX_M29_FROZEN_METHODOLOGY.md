# APEX M29 FROZEN METHODOLOGY
**Phase**: Economic Monetization (Direction-Neutral Boundary)
**Status**: FROZEN (Awaiting M30 Validation)

## 1. Primary Research Question
Does the M17-R2 predicted persistence state condition a predeclared direction-neutral spatial-risk boundary over the 12-hour horizon?

## 2. Rigid Constraints
- **Prediction Artifact**: M17-R2 Walk-Forward OOS predictions (Eligible 396 episodes only).
- **Predictor**: `conditional_risk_score`
- **Ex-Ante Boundary ($B_t$)**: $1.0 \times \text{RV20}_{onset}$ (extracted from the pre-trigger M15 dataset).
- **Target Outcome ($I_i$)**: $1$ if $MAE_{abs} \ge B_t$, else $0$.
- **Horizon**: Exactly 12 hours (48 M15 bars).

## 3. Inferential Framework
- **Model**: Linear Probability Model (OLS)
- **Specification**: $I_i = \alpha + \beta \times \text{RiskScore} + \epsilon$
- **Covariance Treatment**: Newey-West HAC (`maxlags = 48`)
- **Hypothesis**: $H_0: \beta = 0$ vs $H_1: \beta \neq 0$
- **Alpha**: $0.05$ (two-sided)

## 4. Diagnostics & Baseline
- **Primary Baseline**: Unconditional mean of $I_i$ (naive breach probability) over the OOS episodes.

## 5. Falsification
If $p \geq 0.05$ under the frozen HAC LPM model, the finding of economic boundary translation is falsified.

## 6. M30 Validation Requirements
M30 must structurally audit this methodology without computing the regression. It must verify that `RV20_onset` can be cleanly mapped to the 396 episodes, that the threshold $B_t$ is purely historical, and that the binary indicator $I_i$ can be constructed seamlessly without leakage.
