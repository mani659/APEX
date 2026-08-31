Milestone: M40
Status: COMPLETE

M39-R2 finding: DISTRIBUTIONAL DIFFERENCE ESTABLISHED (AD=228.38, p=0.0001)
M40 scientific question: Which component of the CDF difference is responsible?

Candidate decomposition architectures: 5 evaluated
  A: Sequential Hierarchical — SELECTED (48/50)
  B: Single Omnibus — NOT SELECTED (39/50)
  C: Simultaneous Tests — NOT SELECTED (40/50)
  D: Descriptive Only — NOT SELECTED (36/50)
  E: Quantile Regression — NOT SELECTED (29/50)

Primary architecture: Sequential Hierarchical Moment Decomposition

Primary component hierarchy:
  1. LOCATION — mean difference (one-sided upper)
  2. SCALE — std difference (two-sided)
  3. SKEWNESS — skewness difference (two-sided)
  4. TAIL — |Q_0.05 difference| (one-sided upper)
  5. RESIDUAL SHAPE — KS on standardized residuals (one-sided upper)

Secondary descriptors (not tested):
  5th, 25th, 75th, 95th percentiles
  Full moment table for both groups
  Cohen's d

Multiplicity framework: Sequential testing at α = 0.05
  FWER ≤ 0.05 under closed testing procedure
  First rejection stops the hierarchy
  Subsequent components reported descriptively only

Dependence framework: Day-block permutation (M39-R2 architecture)
  Blocks: 1,331 day-boundary blocks
  Replications: 10,000
  Seed: 42
  RNG: PCG-64
  Single permutation run: all statistics computed on each replicate
  Group sizes preserved: N_LNO=2,757, N_CTRL=29,184

Primary data: reports/APEX_M39R2_Session_Transition_Return_Data.csv
  LNO: 2,757 observations
  Control: 29,184 observations
  Total: 31,941 observations

Falsification criteria:
  If no component rejects at α=0.05:
    CDF difference is unexplained distributional-shape phenomenon
    No simple low-dimensional economic interpretation
    STOP — no post-hoc metric search
  Each non-rejected component individually interpreted as:
    "LNO does not differ from control in [component]"

Economic interpretation boundary:
  Location → directional return premium
  Scale → changed volatility / movement risk
  Skewness → asymmetric tail risk
  Tail → extreme-movement risk
  Residual → unexplained shape (no simple mechanism)

Major risks:
  1. Moment-based decomposition may miss non-moment distributional features
  2. The 5th percentile may not capture the relevant tail
  3. Small Cohen's d (0.004) suggests location effect may be undetectable
  4. High kurtosis in both groups may dominate higher-moment tests

Decision: A — AUTHORIZE M41 EMPIRICAL EXECUTION DESIGN

Next authorized milestone: M41 — Session-Transition Distributional Component Experiment
Authorization: PLANNED — NOT STARTED

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
  reports/APEX_M40_Distributional_Decomposition_Methodology.md (NEW)
  reports/APEX_M40_Decomposition_Architecture_Scoring.csv (NEW)
  reports/APEX_M40_RESULT.md (NEW)
  docs/APEX_SESSION_HANDOFF.md (MODIFIED)
  docs/APEX_SESSION_STATE.json (MODIFIED)
