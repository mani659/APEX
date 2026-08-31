# APEX M21-CR: Translation Result Integrity & Interpretation Review

## 1. Sample Reconciliation (396 vs 397)
M20 asserted 397 complete windows based on a structural assumption that the dataset extended far enough to cover the final episode. M21 actually executed the array mapping and correctly dropped exactly 1 episode because its onset occurred within 48 M15 bars of the absolute end of the `EURUSD_2026_06.csv` dataset boundary. 

The M19 frozen methodology strictly requires a complete `[t+1, t+48]` window. Excluding an episode for lack of physically existing forward data is a structural boundary requirement, not an outcome-driven exclusion. Therefore, M21's sample size of **396** is the mathematically correct implementation of the frozen rule, and M20's assertion of 397 was a descriptive error. No formal amendment is required, as the frozen rule was executed perfectly.

## 2. Methodology Integrity Audit
- **Prediction Vector**: Verified. M21 used exactly the M17-R2 risk scores.
- **RV Construction**: Verified. Computed as the sample standard deviation of exactly 48 forward M15 log-returns, scaled by exactly $\sqrt{24,192}$.
- **Statistical Framework**: Verified. OLS with `cov_type='HAC', maxlags=48` and two-sided $\alpha=0.05$.
- **Robustness**: The reported Spearman rank correlation was explicitly frozen in the `APEX_M19_FROZEN_METHODOLOGY.md` document, meaning its inclusion is fully valid as the predeclared secondary diagnostic.

## 3. Scientific Interpretation of $\beta$
The reported coefficient is **$\beta = -0.014288$**.
The correct statistical interpretation in the units of the model is:
> A one-unit increase in the conditional risk score is associated with a 0.014288 decrease in the subsequent annualized 12-hour realized volatility.

**Directional Meaning**:
Under the Cox PH construction, a *higher* risk score dictates a higher hazard rate (predicting a *shorter* HIGH_VOL persistence). Because $\beta$ is negative, predicting a shorter persistence translates to relatively lower forward physical volatility. Conversely, predicting a longer persistence corresponds to relatively higher subsequent annualized volatility.

## 4. Final Classification
**`TRANSLATION VALIDATED`**.
The negative coefficient is statistically significant under the frozen HAC-robust inference ($p = 0.0032$). The M17-R2 predicted-persistence state correctly and systematically translates into a materially different subsequent 12-hour realized volatility outcome.

## 5. What This Does NOT Mean
This validated relationship establishes a physical thermodynamic association (magnitude translation). It absolutely does **not** establish causality, profitability, tradability, or any expected directional price drift. It proves that the APEX model can predict the magnitude of energy in the system, but not the direction.
