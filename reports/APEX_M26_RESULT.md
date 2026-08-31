Milestone: M26
Status: COMPLETE

Research question: Does the M17-R2 predicted HIGH_VOL persistence state condition the magnitude of subsequent price excursions over the same 12-hour horizon?

Prediction vector: Verified
Original OOS predictions: 397
Eligible M25 sample: 396

Prediction boundary: t (onset close)
Primary MAE endpoint: max|ln(P_u / P_t)|
Horizon: 12 hours (48 M15 bars)
Normalization: Log-distance

t+1 alignment: Verified
t+48 alignment: Verified
Forward-window completeness: Verified (396 complete arrays)
Price integrity: Verified

Baseline: Feasible
OLS: Feasible
HAC: Feasible (maxlags=48)
Alpha: Feasible (0.05)
Tail: Feasible (two-sided)

Secondary excursion descriptor: Feasible
Leakage audit: Passed
Software validation: Passed

Gate decision: PASS — READY FOR M27

Fatal issues: None.
Non-fatal limitations: None.

M27 prerequisites: M27 must construct the actual MAE arrays for the 396 eligible episodes and run the frozen OLS+HAC inference to generate the final scientific result.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M26_Pre_Extremum_Data_Validation.md (NEW)
- reports/APEX_M26_Data_Validation_Matrix.csv (NEW)
- reports/APEX_M26_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
