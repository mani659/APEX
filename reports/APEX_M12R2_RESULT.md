Milestone: M12R2
Status: COMPLETE

Frozen methodology verified: M11-R2
Canonical data: data/m1/EUR/EURUSD_*.csv (Resampled to M15)
Historical coverage: 2021-01 to 2026-06

252-day reference: PASS (Lookahead sealed via 1-bar shift)
80th percentile: PASS
50th percentile reset: PASS

HIGH_VOL onset: PASS
HIGH_VOL termination: PASS
Regime reset: PASS (Implemented causally)

Exposure cohort: PASS (07:00-09:00 UTC)
Control cohort: PASS (20:00-06:00 UTC)
Cohort exclusivity: PASS (0 overlaps)

Exposure count: 8
Control count: 80
Total eligible episodes: 794

Persistence endpoint: PASS
Censoring: PASS

DST: PASS (Limitation active)
Lookahead: PASS (Eliminated)
Macro-event dependency: PASS (Bypassed)

Statistical feasibility: BLOCKED (Sample n=8 is too small for Kaplan-Meier/Log-rank inference)

Gate decision: BLOCKED — DATA / OBSERVABILITY

Fatal issues:
- Severe sample attrition. The combination of the strict Regime Reset rule and the narrow 2-hour ASIA_TO_LONDON exposure window reduced the usable exposure population to 8 episodes over 4.5 years.

Non-fatal limitations:
- 1-hour DST drift on UTC boundaries.
- 1-year data warm-up requirement.

M13 prerequisites:
- The control session must adjudicate the sample insufficiency blocker. The methodology is rigorously sound but statistically starved.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M12R2_Pre_Economic_Data_Validation.md (NEW)
- reports/APEX_M12R2_Data_Validation_Matrix.csv (NEW)
- reports/APEX_M12R2_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
