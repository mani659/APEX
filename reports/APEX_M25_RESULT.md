Milestone: M25
Status: COMPLETE

Exact extremum-translation question: Does the M17-R2 predicted HIGH_VOL persistence state condition the magnitude of subsequent price excursions over the same 12-hour horizon?
Primary endpoint: Maximum Absolute Excursion (MAE_abs), defined as max_{u in [t+1,t+48]} |ln(P_u/P_t)|
Horizon: 12 hours (48 M15 bars)
Normalization: Log-distance
Prediction source: M17-R2 OOS conditional risk score
Baseline: Unconditional mean MAE_abs over the OOS sample
Statistical framework: OLS
Dependence treatment: Newey-West HAC standard errors (maxlags = 48)
Primary hypothesis: H0: beta = 0, H1: beta != 0
Alpha/tail: 0.05 / Two-sided
Secondary descriptor: Ratio of mean upside excursion to mean downside excursion
Unresolved items: None. All methodological degrees of freedom are fully frozen.

M26 prerequisites: M26 must validate the array-indexing mechanics for the MAE_abs outcome variable, ensuring the maximum search isolates exactly the `[t+1, t+48]` forward window without calculating the actual OLS regression.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M25_Extremum_Translation_Methodology.md (NEW)
- reports/APEX_M25_Research_Degrees_of_Freedom.csv (NEW)
- reports/APEX_M25_Methodology_Risk_Register.csv (NEW)
- reports/APEX_M25_RESULT.md (NEW)
- docs/APEX_M25_FROZEN_METHODOLOGY.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
