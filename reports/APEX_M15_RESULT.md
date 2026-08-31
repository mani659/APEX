Milestone: M15
Status: COMPLETE

Research Question: Is the persistence of a newly triggered HIGH_VOL episode predictable from market-state information available strictly before or at the onset bar?

Prediction boundary: Information strictly available up to the CLOSE of the onset bar (t_onset).
Target definition: Survival modeling of future episode duration (contiguous M15 bars).
Primary predictor set: 1) Breakout Intensity, 2) Variance Momentum, 3) Regime Depth.
Baseline: Unconditional baseline empirical hazard.
Model framework: Cox Proportional Hazards Model.
Null hypothesis: Out-of-Sample Concordance Index (C-index) <= 0.50.
Out-of-sample design: Chronological Walk-Forward Expanding Window (initial 50% training subset).
Primary predictive metric: Harrell's Concordance Index (C-index) on the out-of-sample aggregated vector.
Leakage controls: Strict feature scaling exclusively fitted within expanding training windows.
Multiple-testing controls: Pre-frozen 3-feature set evaluated in a single primary model. No feature selection algorithms allowed.
Dependence treatment: Regime-Reset enforced inter-episode independence.

Unresolved items: NONE. All major degrees of freedom are fully frozen.
M16 prerequisites: M16 must procedurally validate the causal feature boundaries, the walk-forward dataset splits, and the model software configuration prior to empirical execution.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M15_Conditional_Predictability_Methodology.md (NEW)
- reports/APEX_M15_Research_Degrees_of_Freedom.csv (NEW)
- reports/APEX_M15_Methodology_Risk_Register.csv (NEW)
- docs/APEX_M15_FROZEN_METHODOLOGY.md (NEW)
- reports/APEX_M15_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
