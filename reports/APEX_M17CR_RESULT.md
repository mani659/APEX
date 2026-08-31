Milestone: M17-CR
Status: COMPLETE

Exact environment failure: `lifelines` dependency `autograd-gamma` fails during C-wheel build in Python 3.11 due to obsolete distutils API calls.

Candidate implementation assessment: `statsmodels` (via `statsmodels.duration.hazard_regression.PHReg`) is locally available and fully capable of computing the Cox Proportional Hazards model.

Mathematical equivalence: Both packages solve for the same partial likelihood maximization of the standard Cox model.
Censoring/tie compatibility: Natively supports right censoring and Breslow tie handling.
C-index compatibility: A standalone, deterministic Harrell's C-index Python function was verified during the smoke test and will be used to compute the required aggregate Out-of-Sample C-index.

Selected implementation: `statsmodels`
Package/version: Local environment version.
Formal software amendment required: Yes (`docs/APEX_M17_SOFTWARE_AMENDMENT.md` created).

Exact M17 re-entry requirements:
- Use `statsmodels.PHReg` for the Cox fit inside the walk-forward loop.
- Use the deterministic python function to compute the C-index on the OOS partial hazard predictions.
- Adhere to the previously frozen initial 397 training sample size.

Gate decision: ALTERNATIVE IMPLEMENTATION APPROVED (M17 READY)

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- docs/APEX_M17_SOFTWARE_AMENDMENT.md (NEW)
- reports/APEX_M17CR_Software_Control_Review.md (NEW)
- reports/APEX_M17CR_Software_Decision.md (NEW)
- reports/APEX_M17CR_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
