Milestone: M11
Status: COMPLETE

Approved research direction: Determine whether the validated RC013 session-transition primitive systematically conditions the lifecycle of the validated RC012 HIGH_VOL distributional primitive.
Primary scientific question: Does the onset of HIGH_VOL during a major session transition result in a structurally different persistence and decay profile compared to HIGH_VOL onset during off-peak hours?

RC012 definition reused: HIGH_VOL = RV20 > 80th percentile (EURUSD M15).
RC013 definition reused: ASIA_TO_LONDON and LONDON_NY_OVERLAP session blocks.

Primary endpoint: Persistence (Survival time in M15 bars from onset to termination).
Secondary endpoints: Forward 12-bar Realized Volatility; Decay slope.

Unit of observation: Continuous HIGH_VOL episode.
Exposure definition: Episode onset occurs within the ASIA_TO_LONDON or LONDON_NY_OVERLAP windows.
Control definition: Episode onset occurs entirely outside those windows.

Statistical framework: Kaplan-Meier survival analysis (Log-rank test) for duration.
Lookahead controls: Event classification strictly uses `t` and prior data.
Confounder controls: Exclusion of NFP/FOMC release bars; day-of-week stratification.
Overlap/dependence treatment: 12-bar minimum separation rule between events.
Multiple-testing policy: Single pre-declared primary endpoint. Bonferroni correction for subgroups.

Falsification criteria: p ≥ 0.05 on the Log-rank test OR median survival difference < 2 bars (economically irrelevant).

Existing data sufficient: Yes (EURUSD M15 OHLCV).
Future data required: Macro event timestamps (NFP/FOMC) for exclusion filtering.

Major methodology risks: Pseudo-replication (mitigated via separation rule), Session timezone misalignment (requires M12 audit).

Frozen decisions: Unit of observation, endpoints, statistical framework, falsification criteria.
Requires M12 validation: Timezone/DST alignment, macro-event timestamp availability, sample size threshold (>= 200 per cohort).
Unresolved issues: Exact daylight-saving boundary shifts in the historical dataset.

M12 entry criteria: M12 authorized to verify canonical data completeness, sample sizes, and timezone integrity. NO economic testing authorized.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M11_Candidate_Research_Methodology.md (NEW)
- reports/APEX_M11_Methodology_Risk_Register.csv (NEW)
- reports/APEX_M11_Data_Reuse_Audit.csv (NEW)
- reports/APEX_M11_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
