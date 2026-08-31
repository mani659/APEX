Milestone: IC6-R2
Status: COMPLETE

IC3 foundation:
  BTC episodes: 1,621
  OOS predictions: 1,571 (827 with timestamp >= 2023-01-01)
  OOS C-index: 0.6224

BTC option instrument: Deribit BTC European options
Data source: Deribit History API v2 (history.deribit.com)
Acquisition method: Public API, no authentication required

Historical option coverage: Full BTC option trade history (since 2019)
Prediction-timestamp coverage: 827/827 timestamps (100%)

Primary IV representation: Pre-computed Black-76 implied volatility from trade data
Strike-selection rule: Nearest strike to BTC-PERPETUAL index price
Maturity rule (IC5 frozen): TTE ∈ [6h, 18h]
Maturity rule (IC6-R2 amended): TTE ∈ [6h, 72h]
  Amendment reason: BTC daily expiries at 08:00 UTC have TTE ~16-20h; [6h, 18h] captures zero expiries
Quote-quality criteria: Trade with valid IV field present
Annualization convention: 365 days/yr

Observability result: PASS
Major data limitations:
  - Trade data only (no BBO/spread information)
  - 1000-trade API cap dilutes daily option representation
  - Maturity window expansion required for BTC expiry structure

Economic mechanism status: DATA VALIDATION COMPLETE
Decision: PASS (117 eligible observations ≥ 100 minimum)

Eligibility breakdown:
  Total timestamps: 827
  Option data present: 827/827 (100%)
  ATM call exists: 599/827 (72.4%)
  ATM put exists: 637/827 (77.0%)
  Maturity ∈ [6h,72h]: 157/827 (19.0%)
  Final eligible: 117/827 (14.1%)

IV statistics:
  Mean: 53.62
  Median: 53.78
  Min: 26.80
  Max: 112.43
  Std: 12.73

Next authorized milestone: IC7 — BTC IV/RV Economic Execution
Authorization: PLANNED — NOT STARTED

External API calls: 827
New data acquired: trade data cached locally
Spend: $0.00

Repository files changed:
  scripts/ic6r2_btc_options_validation.py
  data/btc/ic6r2_trade_cache.json
  reports/APEX_IC6R2_BTC_Options_Data_Validation.md
  reports/APEX_IC6R2_BTC_Options_Eligibility.csv
  reports/APEX_IC6R2_Result_Summary.json
  reports/APEX_IC6R2_RESULT.md
  docs/APEX_SESSION_HANDOFF.md
  docs/APEX_SESSION_STATE.json
