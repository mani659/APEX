# APEX M29: Dispersion Boundary Economic Methodology Design

## 1. Scientific Objective
M27 established that the conditionally predicted persistence state governs the absolute magnitude of the future price excursion envelope. M29 seeks to transition this physical relationship into an economic one by asking: **Does the predicted persistence state condition the probability of breaching an ex-ante, direction-neutral symmetric price boundary?**

## 2. Hypothesis Definition
- **Null Hypothesis ($H_0$)**: $\beta = 0$. The M17-R2 conditional risk score has no linear association with the probability of breaching the predefined symmetric boundary.
- **Alternative Hypothesis ($H_1$)**: $\beta \neq 0$. The risk score significantly conditions the boundary-breach probability.
- **Inference Threshold**: $\alpha = 0.05$ (two-sided).

## 3. Boundary Definition and Ex-Ante Rule
To avoid data-mining the M27 Maximum Absolute Excursion ($MAE_{abs}$) outcomes for an "optimal" stop or target distance, the boundary $B_t$ must be strictly defined *ex-ante*.
We will define $B_t$ as the localized pre-onset volatility state:
[
B_t = 1.0 \times \text{RV20}_{onset}
]
*Note: `RV20_onset` is the exact 20-period Realized Volatility value already calculated and frozen in the M15 canonical dataset prior to the `HIGH_VOL` trigger.*
This creates a dynamic but strictly historical, non-fitted symmetric distance constraint.

## 4. Primary Outcome Variable
The primary outcome is the binary Boundary Breach Indicator ($I_i$):
[
I_i = 
\begin{cases} 
1 & \text{if } \max_{u\in[t+1,t+48]} |\ln(P_u/P_t)| \ge B_t \\
0 & \text{otherwise}
\end{cases}
]
This converts the continuous M27 excursion into a discrete state representing whether the symmetric spatial risk limit was exhausted.

## 5. Statistical Framework
**Linear Probability Model (LPM) via OLS with HAC Standard Errors**
[
I_i = \alpha + \beta \times \text{RiskScore} + \epsilon
]
While Logistic Regression is traditional for binary outcomes, the 48-bar forward windows in APEX heavily overlap, inducing severe mechanical autocorrelation in the residuals. Standard Logistic MLE estimators do not natively handle Newey-West HAC corrections easily. To preserve the exact dependence architecture used in M21, M24, and M27, we specify a Linear Probability Model (OLS) utilizing `cov_type='HAC'` with `maxlags = 48`. 

## 6. Capital-Relevance Audit
This methodology explicitly models **spatial boundary exhaustion**. It determines whether price moves far enough to breach a synthetic limit. 
It does **NOT** measure:
- True capital/margin requirement.
- Path-dependent drawdown (whether it spiked and reversed vs trended).
- The drag of bid/ask spread and swap financing.
These components require a full execution simulation strategy later in the pipeline.

## 7. Falsification Rule
If the two-sided p-value for $\beta$ under the LPM HAC specification is $\geq 0.05$, the conclusion must be:
> `BOUNDARY TRANSLATION NOT ESTABLISHED`.

If the p-value is $< 0.05$, the conclusion is:
> `BOUNDARY TRANSLATION SUPPORTED`.
