Milestone: M29
Status: COMPLETE

Exact economic boundary question: Does the M17-R2 predicted persistence state condition a predeclared direction-neutral spatial-risk boundary over the 12-hour horizon?
Primary boundary representation: Binary boundary-breach probability.
Boundary-definition rationale: B_t = 1.0 * RV20_onset. This uses a completely historical, pre-onset physical unit of variance to define the symmetric threshold, avoiding data-mining the M27 outcomes.
Prediction source: M17-R2 OOS conditional risk score.
Primary outcome: I_i = 1 if MAE_abs >= B_t else 0.
Baseline: Unconditional mean breach probability over the OOS sample.
Statistical framework: Linear Probability Model (OLS).
Dependence treatment: Newey-West HAC standard errors (maxlags = 48).
Alpha/tail: 0.05 / Two-sided.
Distinction between boundary information and capital requirement: The binary breach tests pure spatial exhaustion; it does not model the path-dependent sequence of interim drawdowns, margin sizing, or the drag of spread/swap financing required for a full capital-requirement simulation.
Unresolved items: None. All methodological degrees of freedom are fully frozen.

M30 prerequisites: M30 must validate the extraction mapping of RV20_onset to define the dynamic boundary B_t, and verify the binary indicator logic I_i without calculating the actual regression outcome.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M29_Dispersion_Boundary_Methodology.md (NEW)
- reports/APEX_M29_Research_Degrees_of_Freedom.csv (NEW)
- reports/APEX_M29_Methodology_Risk_Register.csv (NEW)
- reports/APEX_M29_RESULT.md (NEW)
- docs/APEX_M29_FROZEN_METHODOLOGY.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
