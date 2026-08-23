Milestone: M31
Status: COMPLETE

Research question: Does the M17-R2 predicted persistence state condition the probability that price breaches a predeclared direction-neutral spatial-risk boundary over the 12-hour horizon?

Prediction source: M17-R2 OOS conditional risk score
Original OOS predictions: 397
Eligible sample: 396

RV20_onset: Extracted correctly from pre-onset canonical M15 data.
Boundary multiplier: 1.0
Boundary definition: B_t = 1.0 * RV20_onset

MAE_abs: max|ln(P_u / P_t)|
Breach condition: MAE_abs >= B_t
Breach count: 395
Breach probability: 0.997475

LPM: Linear Probability Model (OLS)
Intercept: 0.998135
Beta: 0.054025
HAC standard error: 0.045732
HAC maxlags: 48
t-statistic: 1.1813
p-value: 0.2375
95% CI: [-0.035608, 0.143658]

Primary boundary decision: Fail to reject the null. BOUNDARY TRANSLATION NOT ESTABLISHED.

Relationship to M27: M27 continuous excursion is positive, but M31 is null. The specific ex-ante boundary chosen (1.0*RV20_onset) is breached 99.75% of the time, meaning it lies entirely inside the structural expansion envelope for almost all events, providing no discriminative variance power on a binary basis.

Capital-requirement interpretation: This result does NOT invalidate a grid strategy or simulate true path-dependent capital requirements. It solely means a grid bounded precisely at 1.0*RV20_onset will almost universally be breached, and the APEX prediction does not save it.

What the result does NOT establish: Grid drawdown sizes, profitability, or the predictive capability of wider boundary configurations.

Methodology integrity: PERFECT.
Methodology deviations: None. Executed rigidly according to M29 constraints.

Limitations: The binary test suffered from severe base-rate saturation due to the ex-ante choice of the 1.0 multiplier.

M32 recommendation: Given the continuous predictability (M27) but discrete failure (M31), M32 must pivot to defining how to dynamically capture this envelope (e.g. dynamically mapping the APEX score to the required grid width) rather than testing arbitrary discrete thresholds.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M31_Boundary_Breach_Data.csv (NEW)
- reports/APEX_M31_Result_Summary.json (NEW)
- reports/APEX_M31_Dispersion_Boundary_Experiment.md (NEW)
- reports/APEX_M31_RESULT.md (NEW)
- scratch/m31_extract.py (NEW)
- scratch/m31_ols.py (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
