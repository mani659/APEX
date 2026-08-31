Milestone: M36
Status: COMPLETE

Primary research question: Does the validated RC013 LONDON_NY_OVERLAP session state produce a statistically distinct CDF of 1-hour forward returns relative to non-overlap periods, independent of the rejected raw-breakout monetization path?

RC013 evidence reused:
- LONDON_NY_OVERLAP validated structural primitive (RC013 Study 002)
- Session definitions (ASIA, LONDON_PRE_OVERLAP, LONDON_NY_OVERLAP, NEW_YORK_POST_OVERLAP, POST_SESSION)
- Timezone conventions (Europe/London, America/New_York)
- Direction neutrality finding (binary positive/negative approximately 50/50)
- Path geometry finding (TYPE A — directionally efficient expansion)
- Monetization rejection (raw range-breakout architecture rejected)

Primary endpoint: Forward-return CDF (two-sample Anderson-Darling test)

Primary horizon: 1 hour (60 minutes)

Prediction/state boundary:
- Event timestamp: End of LONDON_NY_OVERLAP session (approximately 16:30 UTC)
- State is deterministic; known in advance
- Forward observation start: End of LONDON_NY_OVERLAP session
- Forward observation end: 1 hour later (approximately 17:30 UTC)
- Pre-event conditioning variables: None

Control population: Non-LONDON_NY_OVERLAP hours whose forward window does not overlap with LONDON_NY_OVERLAP

Statistical framework: Two-sample Anderson-Darling test (non-parametric, tests full CDF)

Null hypothesis: F_transition(r) = F_non_transition(r) for all r (session-transition state does not alter the forward-return CDF)

Dependence treatment: Block bootstrap (block length = 24, replications = 10,000, day-boundary blocks)

Multiple-testing control: Single primary test (α = 0.05 two-sided); no Bonferroni correction needed

Data reuse: Canonical EURUSD M1 OHLCV (5.5 years); RC013 session definitions; existing Python infrastructure

New data required: None

Major risks:
1. Lookahead — mitigated by forward-return definition (T to T+60min)
2. Timezone/DST errors — mitigated by pytz with frozen RC013 definitions
3. Non-independence — mitigated by block bootstrap
4. Confounding — mitigated by excluding holidays, NFP, FOMC, ECB dates
5. Hidden strategy optimization — mitigated by frozen degrees of freedom

Research degrees of freedom: All 12 decisions frozen (see APEX_M36_Research_Degrees_of_Freedom.csv)

Unresolved items: None. All material choices frozen.

M37 prerequisites:
1. Verify RC013 session-state reconstruction in canonical M1 data
2. Verify timezone correctness with pytz
3. Verify DST handling
4. Verify treatment/control group sizes
5. Verify forward-return availability
6. Verify overlap exclusion
7. Verify sample restrictions
8. Verify statistical software (scipy.stats.anderson_ksamp)
9. Verify no lookahead leakage
10. Verify frozen degrees of freedom unmodified

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M36_Session_Transition_Distributional_Asymmetry_Methodology.md (NEW)
- reports/APEX_M36_Research_Degrees_of_Freedom.csv (NEW)
- reports/APEX_M36_Methodology_Risk_Register.csv (NEW)
- reports/APEX_M36_RESULT.md (NEW)
- docs/APEX_M36_FROZEN_METHODOLOGY.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
