Milestone: M20
Status: COMPLETE

Research question: Does the predicted persistence of a newly triggered HIGH_VOL episode condition the subsequent 12-hour realized-volatility trajectory in a materially different way from the unconditional HIGH_VOL baseline?

Prediction vector: Intact and aligned.
OOS episode count: 397

Prediction boundary: t (Close of onset bar)
Outcome start: t + 1 M15 bar
Outcome end: t + 48 M15 bars

RV construction: M15 log-returns.
Annualization: AMBIGUOUS (Annualization constant not frozen).

Complete outcome windows: 397
Incomplete windows: 0

Overlap/dependence: Overlap exists; requires HAC.
HAC specification: AMBIGUOUS (Lag truncation parameter not frozen).
HAC software validation: statsmodels cov_type='HAC' is structurally capable of the required matrix correction.

OLS specification: Verified (Continuous risk score as sole predictor).
Baseline: Verified (Unconditional 397 OOS cohort).
Primary effect: Slope coefficient (Beta).
Inference threshold: AMBIGUOUS (Alpha level and tail specification not frozen).

Leakage audit: PASS. Complete isolation of prediction boundary from the outcome window.
Time-order audit: PASS. No future shuffling or CV leakage.

Gate decision: BLOCKED — METHODOLOGY

Fatal issues:
1. HAC LAG NOT PREDEFINED
2. INFERENCE THRESHOLD NOT FROZEN
3. ANNUALIZATION DEFINITION AMBIGUOUS

Non-fatal limitations: None.

M21 prerequisites: M20-CR must formally freeze the exact numerical parameters for the annualization constant, the HAC lag limit, and the statistical alpha threshold.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M20_Pre_Economic_Data_Validation.md (NEW)
- reports/APEX_M20_Data_Validation_Matrix.csv (NEW)
- reports/APEX_M20_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
