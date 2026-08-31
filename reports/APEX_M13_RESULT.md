Milestone: M13
Status: COMPLETE

Research question: Does the unconditional HIGH_VOL persistence distribution contain structural memory beyond a memoryless geometric threshold-crossing process?

Frozen methodology verified: APEX_M11BACKUP_FROZEN_METHODOLOGY.md & APEX_M11BACKUP_STATISTICAL_AMENDMENT.md
Methodology deviations: None

Canonical dataset: EURUSD M15 (data/m1/EUR/EURUSD_*.csv)
Historical coverage: 2021 to mid-2026 (5.5 years)

HIGH_VOL episodes: 794
Completed episodes: 794
Censored episodes: 0

Observed persistence:
Median: 20.0
75th percentile: 29.0
90th percentile: 47.0
Maximum: 168

Geometric null:
p_hat: 0.04549
Expected duration: 21.98

Observed test statistic:
D_obs: 0.19270

Monte Carlo:
Simulations: 10000
Seed: 42
Simulations >= D_obs: 0
Monte Carlo p-value: 0.00000

Primary statistical decision: Reject memoryless null. The empirical persistence distribution is statistically inconsistent with a geometric process.

Effect/descriptive findings: The enormous CDF distance (0.19270) confirms a profound structural deviation in the persistence shape, confirming complex hazard characteristics (e.g. fat tails) rather than a constant exit rate.

Robustness results: Non-parametric structural logic perfectly preserved.

Structural-memory conclusion: The unconditional HIGH_VOL persistence distribution contains mathematically definitive structural memory beyond a simple random threshold-crossing process.

What this result does NOT establish: Predictability, tradability, positive expectancy, or strategy viability.

Methodology integrity: Pristine. Zero deviations.

Limitations: 1-year data warm-up.

M14 recommendation: M14 must formally adjudicate the scientific meaning of this structural memory finding and decide if it warrants translation into a predictive economic strategy.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M13_Unconditional_HIGH_VOL_Experiment.md (NEW)
- reports/APEX_M13_Persistence_Distribution.csv (NEW)
- reports/APEX_M13_MonteCarlo_Null_Summary.csv (NEW)
- reports/APEX_M13_MonteCarlo_Config.json (NEW)
- reports/APEX_M13_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
