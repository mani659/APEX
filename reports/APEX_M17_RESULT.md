Milestone: M17
Status: COMPLETE (BLOCKED)

Research question: Is the persistence of a newly triggered HIGH_VOL episode predictable from market-state information available strictly before or exactly at the onset bar?

Frozen predictor set:
Breakout Intensity: Included
Variance Momentum: Included

Event count: 794
Training episodes: 397
Out-of-sample episodes: 397

Prediction boundary: Verified (Close of t_onset).
Walk-forward design: Attempted (Expanding Window).

Cox PH implementation: FAILED.
Package/version: `lifelines` (Installation blocked by autograd-gamma distutils bug in Python 3.11).
Fit failures: ALL (Model could not be initialized).

Conditional OOS C-index: N/A
Baseline OOS C-index: N/A
Delta C-index: N/A

Primary predictive decision: Inconclusive / methodology invalid.

Robustness: N/A

Methodology integrity: Maintained (Refused to swap statistical package without control authorization).
Methodology deviations: None.

Predictive conclusion: Inconclusive.

What this does NOT establish: The conditional predictability of HIGH_VOL persistence remains completely unknown.

Limitations: Python 3.11 build dependencies prevent compilation of the specified statistical package (`lifelines`).

M18 recommendation: APEX Control Session must authorize a package substitution (e.g., `statsmodels` or `scikit-survival`) or repair the environment.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M17_Conditional_Predictability_Experiment.md (NEW)
- reports/APEX_M17_WalkForward_Predictions.csv (NEW)
- reports/APEX_M17_Result_Summary.json (NEW)
- reports/APEX_M17_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
