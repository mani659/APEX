# APEX M25: Extremum Boundary Translation Methodology Design

## 1. Scientific Objective
M21 confirmed that the predicted persistence state accurately scales the physical *magnitude* of future realized volatility. M24 proved that this state carries *zero* linear information about future directional *drift*. M25 now asks: Does this unsigned thermodynamic energy specifically condition the **absolute excursion envelope** (i.e., the maximum distance price travels from onset) over the exact same 12-hour horizon?

## 2. Hypothesis Definition
- **Null Hypothesis ($H_0$)**: $\beta = 0$. The M17-R2 predicted persistence state has no linear association with the maximum absolute price excursion.
- **Alternative Hypothesis ($H_1$)**: $\beta \neq 0$. The predicted persistence state significantly conditions the maximum absolute price excursion.
- **Inference Threshold**: $\alpha = 0.05$ (two-sided).

## 3. Primary Outcome Variable: Maximum Absolute Excursion ($MAE_{abs}$)
The future price envelope will be defined by the maximum absolute log-distance from the onset price over the forward 48 M15 bars:
[
MAE_{abs} = \max_{u\in[t+1,t+48]} \left| \ln(P_u/P_t) \right|
]
Where $P_t$ is the closing price of the 15-minute bar exactly at `HIGH_VOL` onset. $P_u$ represents the sequence of closing prices for the subsequent 48 bars.

**Rationale**: Log-normalization renders the excursion dimensionless, allowing stationary comparison across 15 years. Maximum absolute distance perfectly captures the structural boundary of the volatility expansion established in M21, free from the directional constraints of M24.

## 4. Statistical Framework
**OLS with HAC Standard Errors**
[
MAE_{abs} = \alpha + \beta \times \text{RiskScore} + \epsilon
]
Because the 48-bar maximum searches structurally overlap for clustered events, the residuals will exhibit serial dependence. To correct for this, Newey-West HAC standard errors must be applied with `maxlags = 48` (identical to the M21/M24 treatment).

## 5. Baseline and Secondary Descriptors
- **Baseline**: The unconditional mean of $MAE_{abs}$ across the eligible OOS episodes.
- **Secondary Descriptor**: The ratio of the mean Upside Maximum Excursion to the mean Downside Maximum Excursion across the sample. This offers insight into whether the bounds are strictly symmetric.

## 6. Falsification Rule
If the two-sided p-value for $\beta$ under the HAC-robust OLS specification is $\geq 0.05$, the conclusion must be:
> `EXTREMUM TRANSLATION NOT ESTABLISHED`.

If the p-value is $< 0.05$, the conclusion is:
> `EXTREMUM TRANSLATION ESTABLISHED`.
