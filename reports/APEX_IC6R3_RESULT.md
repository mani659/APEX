Milestone: IC6-R3
Status: COMPLETE

Fatal IC6-R2 bug:
  Python loop-variable scoping caused TTE computation to use wrong prediction timestamp
  Impact: 57.3% of observations had TTE error >= 100h
  Correction: explicit per-timestamp TTE computation via evaluate_timestamp() function

Correction:
  TTE now computed from each row's own prediction timestamp
  Call/put joint check now searches across all groups at the same expiry
  Freshness now computed from actual trade timestamp (not hardcoded True)

Prediction timestamps: 827 (IC3 OOS, >= 2023-01-01)
Option observations: 827 (all have trade data via Deribit History API v2)

Freshness rule: trade timestamp <= prediction timestamp AND age <= 1 hour
Maturity rule: TTE in [12h, 24h] (nearest daily Deribit BTC expiry at 08:00 UTC)
Strike rule: nearest strike to BTC-PERPETUAL index price from trade record
Call/put rule: same strike, same expiry, both observed within freshness window

Eligibility attrition:
  827 total timestamps
  -> 827 with option data (100%)
  -> 827 with freshness <= 1h (100%)
  -> 374 with fresh call at ATM strike with [12h,24h] maturity
  -> 362 with fresh put at ATM strike with [12h,24h] maturity
  -> 343 with joint call+put at same strike/expiry
  -> 343 final eligible (41.5%)

Final eligible N: 343
IC5 minimum: 100
PASS

TTE validation: ALL in [12h, 24h]; mean=16.63h; no errors
Timestamp validation: ALL trade timestamps <= prediction timestamp
Lookahead validation: NO future information used in any selection
Reproducibility: PASS (identical results on re-run)

IV structural validity:
  All 343 eligible observations have:
    - valid pre-computed IV (call and put)
    - valid strike
    - valid expiry
    - joint call+put pair

Trade age statistics (eligible):
  Mean: 5.8 min
  Median: 2.8 min
  Max: 53.0 min
  <=15 min: 315 (91.8%)

Methodology deviations: NONE (all corrections per IC6-R2-CR decision)

IC7 readiness: READY

Next authorized milestone: IC7 — BTC IV/RV Economic Execution
Authorization: PLANNED — NOT STARTED (requires control-session review of IC6-R3)

External API calls: 827 (first run, cached)
New data acquired: 0 (re-run from cache)
Spend: $0.00

Repository files changed:
  scripts/ic6r3_btc_options_validation.py (NEW)
  data/btc/ic6r3_raw_trade_cache.json (NEW, 827 entries)
  reports/APEX_IC6R3_BTC_Options_Eligibility.csv (NEW, 827 rows)
  reports/APEX_IC6R3_BTC_Options_Eligibility_Validation.md (NEW)
  reports/APEX_IC6R3_RESULT.md (NEW)
  docs/APEX_SESSION_HANDOFF.md (MODIFIED)
  docs/APEX_SESSION_STATE.json (MODIFIED)
