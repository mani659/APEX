Milestone: M30
Status: COMPLETE

Research question: Does the M17-R2 predicted persistence state condition a predeclared direction-neutral spatial-risk boundary over the 12-hour horizon?

Prediction vector: Verified
Original OOS predictions: 397
Eligible boundary sample: 396

Prediction boundary: t (onset close)
RV20_onset: Successfully computable from M15 closes at t.
Boundary multiplier: Fixed exactly at 1.0.
Boundary definition: B_t = 1.0 * RV20_onset (Verified)

MAE_abs: max|ln(P_u / P_t)| (Verified)
Horizon: 12 hours (48 M15 bars)
Breach indicator: I_i = 1 if MAE >= B_t, else 0 (Verified)

Baseline: Feasible

LPM: Feasible (statsmodels.OLS natively handles it)
HAC maxlags: 48
Alpha: 0.05
Tail: Two-sided

Leakage audit: Passed. B_t is strictly derived from historical data at t.
Capital-requirement distinction: Formally separated. Methodology restricts itself to measuring spatial exhaustion, not full mark-to-market drawdown simulation.
Software validation: Passed.

Gate decision: PASS — READY FOR M31

Fatal issues: None.
Non-fatal limitations: None.

M31 prerequisites: M31 must execute the frozen LPM + HAC empirical experiment across the 396 valid boundary arrays to calculate the final scientific result.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M30_Pre_Boundary_Data_Validation.md (NEW)
- reports/APEX_M30_Data_Validation_Matrix.csv (NEW)
- reports/APEX_M30_RESULT.md (NEW)
- scratch/m30_validation.py (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
