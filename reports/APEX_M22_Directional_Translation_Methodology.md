# APEX M22: Directional Price-Distribution Translation Methodology Design

## 1. Scientific Objective
M21 confirmed that the M17-R2 conditional risk score (which predicts `HIGH_VOL` episode persistence) accurately translates into a difference in the magnitude of forward Realized Volatility. The objective of M22 is to ascertain whether this translated energy is purely symmetric, or if it conditions a directional price vector (drift) over the exact same horizon.

## 2. Hypothesis Definition
- **Null Hypothesis ($H_0$)**: $\beta = 0$. The M17-R2 predicted persistence state has no linear association with the directional 12-hour forward cumulative log return.
- **Alternative Hypothesis ($H_1$)**: $\beta \neq 0$. The predicted persistence state has a non-zero linear association with the forward directional price drift.
- **Inference Threshold**: $\alpha = 0.05$ (two-sided).

## 3. Data & Prediction Vector
- **Data Source**: Canonical EURUSD M1/M15 dataset.
- **Prediction Vector**: Strictly out-of-sample M17-R2 `conditional_risk_score` for the 396 validated OOS `HIGH_VOL` episodes. (The single truncated episode identified in M21-CR remains excluded).

## 4. Primary Outcome Variable
**Forward Cumulative Log Return ($R_{48}$)**
[
R_{48} = \ln(P_{t+48}/P_t)
]
Where $P_t$ is the closing price of the 15-minute bar exactly at `HIGH_VOL` onset. $P_{t+48}$ is the closing price exactly 12 hours (48 bars) later.

**Rationale**: This precisely measures the net directional translation of the market over the exact same period that M21 measured the gross variance translation. Decoupling the horizons would render the directional translation incomparable to the validated volatility magnitude.

## 5. Statistical Framework
**OLS with HAC Standard Errors**
[
R_{48} = \alpha + \beta \times \text{RiskScore} + \epsilon
]
Because the 48-bar windows structurally overlap for clustered events, the residuals will exhibit serial dependence. To correct for this, Newey-West HAC standard errors must be applied with `maxlags = 48` (identical to the M21 treatment).

## 6. Baseline and Secondary Descriptors
- **Baseline**: The unconditional mean of $R_{48}$ across the 396 OOS episodes.
- **Secondary Descriptor**: Return distribution skewness across the sample. This offers insight into asymmetric tail behavior but is purely descriptive.
- **Robustness**: Spearman rank correlation between the risk score and $R_{48}$.

## 7. Falsification Rule
If the two-sided p-value for $\beta$ under the HAC-robust OLS specification is $\geq 0.05$, the conclusion must be:
> `NO DIRECTIONAL TRANSLATION ESTABLISHED`.

If the p-value is $< 0.05$, the conclusion is:
> `DIRECTIONAL TRANSLATION ESTABLISHED`. 
(With the required caveat that this merely denotes statistical association, not actionable trading profitability).
