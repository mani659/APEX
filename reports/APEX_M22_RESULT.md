Milestone: M22
Status: COMPLETE

Exact directional translation question: Does the M17-R2 predicted persistence state of a newly triggered HIGH_VOL episode condition the directional distribution of subsequent price returns?
Primary return endpoint: Forward cumulative 12-hour log return, ln(P_{t+48} / P_t)
Primary horizon: 12 hours (48 M15 bars)
Prediction source: M17-R2 OOS conditional risk score
Baseline: Unconditional mean of the forward 12-hour cumulative log return over the OOS sample
Statistical framework: OLS
Alpha/tail: 0.05 / Two-sided
Dependence treatment: Newey-West HAC standard errors (maxlags = 48)
Secondary descriptor: Forward return distribution skewness
Falsification rule: If the HAC-robust p-value >= 0.05, H0 is not rejected, and NO DIRECTIONAL TRANSLATION is established.

Unresolved issues: None. All methodological degrees of freedom are fully frozen.
M23 prerequisites: M23 must validate the data-construction integrity of the R_48 outcome variable, ensuring it perfectly aligns with the onset timestamp `t` and prevents future-data leakage, without calculating the actual regression.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M22_Directional_Translation_Methodology.md (NEW)
- reports/APEX_M22_Research_Degrees_of_Freedom.csv (NEW)
- reports/APEX_M22_Methodology_Risk_Register.csv (NEW)
- reports/APEX_M22_RESULT.md (NEW)
- docs/APEX_M22_FROZEN_METHODOLOGY.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
