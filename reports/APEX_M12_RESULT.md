Milestone: M12
Status: COMPLETE

Canonical dataset: data/m1/EUR/EURUSD_*.csv
Instrument: EURUSD
Timeframe: M15 (resampled from M1)
Historical coverage: 2021-01 to 2026-06 (136,787 M15 bars)

HIGH_VOL observable: Yes (threshold dynamically computed at 0.000563)
Session transitions observable: Yes (using fixed static hours)
DST handling: No (unresolved risk of 1-hour misalignment during non-aligned DST periods)
Event construction: Yes (1,182 total episodes)
Exposure classification: Yes (based on onset time)
Control classification: Yes (based on onset time)
12-bar separation: Yes (strict programmatic separation)

Exposure sample count: 336
Control sample count: 846

Data gaps: None fatal in price data
Macro-event timestamp availability: UNAVAILABLE / BLOCKED (no NFP/FOMC data locally)
Lookahead audit: PASS (no backward leakage of forward observations)

Primary validation result: Sample sizes are robust (>200 each), but macro-event exclusion rule cannot be implemented.
Gate decision: BLOCKED — DATA / OBSERVABILITY

Fatal issues:
- Cannot exclude NFP/FOMC events because the timestamps do not exist in the repository.

Non-fatal limitations:
- Historical DST shifts may cause a 1-hour discrepancy at session boundaries.

Control-session issues:
- Control session must either authorize external acquisition of an economic calendar OR formally amend M11 to accept macro confounding as an explicit limitation.

M13 prerequisites:
- Resolution of the macro-event timestamp blocker.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M12_Pre_Economic_Data_Validation.md (NEW)
- reports/APEX_M12_Data_Validation_Matrix.csv (NEW)
- reports/APEX_M12_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
