Milestone: M41
Status: COMPLETE

M39-R2 foundation: DISTRIBUTIONAL DIFFERENCE ESTABLISHED (AD=228.38, p=0.0001)

Observed sample:
  Transition: 2,757
  Control: 29,184
  Total: 31,941

Frozen null: Day-block permutation with randomized labels
  Blocks: 1,331 day-boundary blocks
  Replications: 10,000
  Seed: 42
  RNG: PCG-64
  Group sizes preserved

M40 hierarchy: Sequential hierarchical decomposition
  Component 1: Location (mean difference, one-sided upper)
  Component 2: Scale (std difference, two-sided)
  Component 3: Skewness (skewness difference, two-sided)
  Component 4: Tail (|Q_0.05 difference|, one-sided upper)
  Component 5: Residual Shape (KS on standardized residuals)

Component 1 — Location:
  Observed statistic: +0.00000363
  LNO mean: +0.00000158
  Control mean: −0.00000205
  Exceedance count: 4,366 / 10,000
  Empirical p: 0.4367
  Decision: FAIL TO REJECT
  Hierarchy position: 1

Component 2 — Scale:
  Observed statistic: +0.00058731
  LNO std: 0.00149361
  Control std: 0.00090630
  Exceedance count: 0 / 10,000
  Empirical p: 0.0001
  Decision: REJECT
  Hierarchy position: 2

Component 3 — Skewness: SKIPPED (hierarchy stopped at Scale)
Component 4 — Tail: SKIPPED (hierarchy stopped at Scale)
Component 5 — Residual Shape: SKIPPED (hierarchy stopped at Scale)

Hierarchy stopping point: 2 (Scale)
Primary component: SCALE
Primary decision: COMPONENT IDENTIFIED

Interpretation:
  LNO returns are approximately 1.65× more dispersed than control returns.
  The scale difference is statistically significant (p = 0.0001, 0/10,000 exceedances).
  There is NO directional return premium (Location p = 0.437).
  The M39-R2 CDF difference is driven by dispersion, not location.

What M41 establishes:
  1. The primary component of the CDF difference is SCALE (dispersion)
  2. LNO has 1.65× wider return distribution than control
  3. No directional return shift during LNO
  4. The session-transition finding is a volatility phenomenon, not a directional phenomenon

What M41 does NOT establish:
  1. Whether skewness or tails also differ (not tested)
  2. Whether the scale difference is economically exploitable
  3. Any trading strategy or PnL
  4. The economic mechanism
  5. Causality

Methodology integrity: ALL CHECKS PASS

M42 recommendation:
  Control session should determine whether the scale difference warrants
  economic-mechanism design (M42) or whether the session-transition
  branch should close. The scale difference is scientifically validated
  but its economic relevance requires separate assessment.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
  scripts/m41_distributional_component_experiment.py (NEW)
  reports/APEX_M41_Distributional_Component_Results.csv (NEW)
  reports/APEX_M41_Result_Summary.json (NEW)
  reports/APEX_M41_Distributional_Component_Experiment.md (NEW)
  reports/APEX_M41_RESULT.md (NEW)
  docs/APEX_SESSION_HANDOFF.md (MODIFIED)
  docs/APEX_SESSION_STATE.json (MODIFIED)
