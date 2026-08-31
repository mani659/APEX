Milestone: M19
Status: COMPLETE

Exact economic-translation question: Does the predicted persistence of a newly triggered HIGH_VOL episode condition the subsequent 12-hour realized-volatility trajectory in a materially different way from the unconditional HIGH_VOL baseline?

Prediction representation: Continuous predicted risk score (M17-R2 Walk-Forward OOS vector).
Primary realized-volatility endpoint: Annualized standard deviation of M15 log-returns.
Primary horizon: Forward 12 hours (48 M15 bars).

Baseline: Unconditional forward 12h RV across all HIGH_VOL OOS episodes.
Statistical framework: Continuous-outcome OLS regression.
Dependence treatment: Newey-West HAC robust standard errors.

Leakage controls: Prediction timestamp strictly frozen at onset close (t). Forward RV window is exclusively [t+1, t+48].
Primary effect measure: Slope coefficient (Beta) of Forward RV on Risk Score.

Falsification framework: Translation is not established if the slope coefficient is indistinguishable from zero under HAC standard errors.
Unresolved items: None. The methodology is completely freezable.

M20 prerequisites: Validate prediction vector integrity, timestamp alignment [t+1], and HAC standard error implementation before executing the M21 empirical experiment.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- docs/APEX_M19_FROZEN_METHODOLOGY.md (NEW)
- reports/APEX_M19_Economic_Translation_Methodology.md (NEW)
- reports/APEX_M19_Research_Degrees_of_Freedom.csv (NEW)
- reports/APEX_M19_Methodology_Risk_Register.csv (NEW)
- reports/APEX_M19_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
