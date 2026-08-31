Milestone: M12-BACKUP
Status: COMPLETE

Research question: What is the unconditional lifecycle (persistence and decay) of the validated HIGH_VOL distributional state, and does it possess structural memory beyond a random threshold-crossing process?
Frozen methodology: APEX_M11BACKUP_FROZEN_METHODOLOGY.md

Canonical data: EURUSD M1 -> M15 resampled (136787 bars)
Historical coverage: 5.5 years (2021 to mid-2026)

HIGH_VOL construction: PASS
252-day reference: PASS (24192 bars)
Lookahead: PASS (Strict t-1 separation)

Regime reset: PASS (50th percentile)
Episode construction: PASS (Causal and sequential)
Causality: PASS (Information boundaries sealed)

Episode count: 794
Completed episodes: 794
Censored episodes: 0

Independence assessment: INDEPENDENCE PLAUSIBLE (Regime Reset adequately enforces independence)

Primary endpoint: PASS (Discrete M15 bars)
Survival feasibility: PASS

Geometric null definition: PASS (Memoryless Markov Baseline)
Exit parameter definition: PASS (p = Terminations / Total HIGH_VOL bars = 0.04549)
Discrete-null K-S feasibility: BLOCKED (Methodology does not specify discrete/Monte Carlo K-S calibration for integer persistence data)

Research degrees of freedom: ALL FROZEN, but K-S discrete framework requires resolution.

Gate decision: BLOCKED — METHODOLOGY

Fatal issues:
- Discrete Null Inference Design: The methodology specifies a Kolmogorov-Smirnov test, but persistence is measured in discrete integers (bars). A standard K-S implementation assumes continuous data and will yield statistically invalid (conservative) bounds.

Non-fatal limitations:
- 1-year warm-up period.

M13 prerequisites:
- The Control Session must authorize a methodological amendment to formally define the discrete K-S test calibration (e.g., Monte Carlo permutation) or replace the K-S test with a discrete-compatible alternative.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M12BACKUP_Pre_Economic_Validation.md (NEW)
- reports/APEX_M12BACKUP_Data_Validation_Matrix.csv (NEW)
- reports/APEX_M12BACKUP_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
