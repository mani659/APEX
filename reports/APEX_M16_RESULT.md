Milestone: M16
Status: COMPLETE

Research question: Is the persistence of a newly triggered HIGH_VOL episode predictable from market-state information available strictly before or at the onset bar?

Frozen methodology verified: APEX_M15_FROZEN_METHODOLOGY.md
Methodology deviations: None

Canonical dataset: EURUSD M15 (data/m1/EUR/EURUSD_*.csv)
Historical coverage: 5.5 years (2021 to mid-2026)
Eligible HIGH_VOL episodes: 794

Prediction boundary: Verified (Close of t_onset). Zero lookahead.
Breakout Intensity: Verified (0 missing values).
Variance Momentum: Verified (0 missing values).
Regime Depth: Verified (0 missing values).

Walk-forward structure: Verified.
Training count: 397 episodes (initial).
Out-of-sample count: 397 episodes.

Leakage audit: Pass. No future index contamination.
Scaling audit: Pass. Implementation design confines scalers to training indices.

Target: Verified.
Censoring: Verified.

Cox PH feasibility: Software package `lifelines` requires installation, but mathematical feasibility is met.
PH assumption specification: Verified.

Baseline: Verified.
Primary metric: Verified.
Predictive null: Verified.

Predictor redundancy: BLOCKED. Severe multicollinearity detected. Correlation between Breakout Intensity and Regime Depth is 0.9886. 
Multiple-testing controls: Verified.

Sample feasibility: Verified (n=397 per walk-forward iteration).

Gate decision: BLOCKED — METHODOLOGY

Fatal issues:
- Severe multicollinearity. The fixed 3-feature model contains two nearly identical mathematical representations of proportional variance. Feeding highly collinear predictors into a Cox model destabilizes the partial likelihood estimator.

Non-fatal limitations:
- `lifelines` package missing from environment.

M17 prerequisites:
- The Control Session must authorize a methodological amendment to drop or combine the redundant feature before M17 can proceed.
- `pip install lifelines` must be run.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M16_Pre_Economic_Validation.md (NEW)
- reports/APEX_M16_Data_Validation_Matrix.csv (NEW)
- reports/APEX_M16_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
