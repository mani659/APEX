Milestone: M12-BACKUP Control Review
Status: COMPLETE

Original Flaw: Continuous K-S test applied to discrete, parameter-estimated data.
Geometric-null parameter audit: Passed. MLE estimator (Terminations / Total Bars) is mathematically correct.
Parameter-estimation issue: Resolved via Parametric Bootstrap simulation.
Discreteness issue: Resolved via exact Monte Carlo calibration of the K-S statistic.
Censoring implication: Irrelevant for current dataset (0 censored events).
Dependence assumption: Independence mathematically plausible due to strict Regime Reset structural barrier.

Candidate-method selected: Option C (Discrete CDF-distance test with Parametric Monte Carlo calibrated null).
Amended inference procedure: Generate 10,000 synthetic geometric datasets (Seed=42). Re-estimate parameter p for each. Compute simulated K-S statistics. Derive exact empirical p-value for the observed K-S statistic.
Remaining degrees of freedom: ALL FROZEN.

Final decision: STATISTICAL AMENDMENT APPROVED — M13 PENDING.
M13 Prerequisites: M13 must strictly implement the Monte Carlo pipeline specified in APEX_M11BACKUP_STATISTICAL_AMENDMENT.md.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- docs/APEX_M11BACKUP_STATISTICAL_AMENDMENT.md (NEW)
- reports/APEX_M12BACKUP_CONTROL_REVIEW.md (NEW)
- reports/APEX_M12BACKUP_STATISTICAL_DECISION.md (NEW)
- reports/APEX_M12BACKUP_CONTROL_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
