Milestone: M11-Backup
Status: COMPLETE

Original M11 session-conditioned branch abandoned due to sample scarcity. The M10 backup (Unconditional HIGH_VOL lifecycle) is now the primary hypothesis.

Research Question: What is the unconditional lifecycle (persistence and decay) of the validated HIGH_VOL state?
HIGH_VOL Definition: RV20 > 80th percentile of a trailing 252-trading-day reference. (Validated in M12R2).
Regime Reset Rule: A new episode cannot trigger until RV20 drops below the trailing 50th percentile.
Episode Construction: Onset on crossing 80th percentile after reset. Termination on crossing back below 80th percentile.
Dependence Treatment: Clustered volatility is absorbed into single continuous episodes via the Regime Reset rule.

Primary Endpoint: Persistence (duration in M15 bars).
Null Model: Memoryless Markov Baseline. Persistence distributions are compared against a geometric distribution fitted to the empirical exit probability.
Statistical Framework: Kaplan-Meier survival curves compared against the geometric null via a Kolmogorov-Smirnov (K-S) or Anderson-Darling test.
Effect Measure: Empirical median persistence, 75th/90th percentiles, and hazard function shape vs the null.

Falsification Framework: 
- Supported: The empirical survival function significantly deviates from the memoryless null (p < 0.05), proving a structural lifecycle beyond simple threshold crossing.
- Not Supported: The persistence matches the memoryless null, implying no structural lifecycle memory.

Unresolved Items: None. The methodology is scientifically coherent and entirely ex-ante.
M12-Backup Prerequisites: Validate the causal construction of thresholds, episode boundaries, event coverage (expected ~794 episodes), and the feasibility of computing the Markov Baseline parameter.

Freeze Status: FROZEN. (APEX_M11BACKUP_FROZEN_METHODOLOGY.md generated).

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M11BACKUP_Methodology_Design.md (NEW)
- reports/APEX_M11BACKUP_Research_Degrees_of_Freedom.csv (NEW)
- reports/APEX_M11BACKUP_Methodology_Risk_Register.csv (NEW)
- reports/APEX_M11BACKUP_RESULT.md (NEW)
- docs/APEX_M11BACKUP_FROZEN_METHODOLOGY.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
