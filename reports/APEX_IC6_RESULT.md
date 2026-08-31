Milestone: IC6
Status: COMPLETE

IC3 OOS prediction count: 1,571

Option data source: Deribit public API (attempted), CryptoDataDownload (attempted)
Acquisition period: 2021-06-28 to 2026-05-04 (IC3 coverage)
Historical coverage: Deribit API provides recent data only (last 24-48h); historical data NOT available

Prediction-timestamp coverage: 0 / 1,571 (0.0%)
Option definition coverage: 0 / 1,571 (0.0%)
Strike coverage: 1,571 / 1,571 (100.0%) — constructed deterministically
Call coverage: 0 / 1,571 (0.0%) — no trade data
Put coverage: 0 / 1,571 (0.0%) — no trade data

Maturity rule: Nearest daily expiry (08:00 UTC) with TTE in [6h, 18h]
TTE coverage: 1,571 / 1,571 (100.0%) — all timestamps have valid expiry
Fallback usage: 540 / 1,571 (34.4%) — TTE > 18h, <= 24h
Max mismatch violations: 0

Quote freshness: N/A (no quotes available)
Tier-1 observations: 0
Tier-2 observations: 0

Black-76 input validity: Structurally feasible (all inputs except option price available)

Joint call/put eligibility: 0 / 1,571 (0.0%)

Future expiry-path coverage: 1,571 / 1,571 (100.0%) — BTC data extends through all expiry dates

Final eligible sample: 0

IC5 minimum sample requirement: 100
Pass / Fail: FAIL

Major data-quality issues:
- Deribit public API does NOT provide historical trade data for periods before the most recent 24-48 hours
- Monthly batch queries returned 0 trades for all historical periods (2021-2025)
- CryptoDataDownload provides DVOL index but not individual option bid/ask data
- Tardis.dev has comprehensive data but was not downloaded during IC6

Methodology issues:
- None — IC5 frozen methodology is implementable
- Maturity matching: structurally valid (100% coverage)
- Strike construction: structurally valid (100% coverage)
- Black-76: mathematically feasible (all non-price inputs available)
- Cost model: implementable (0.04% taker x 4 legs)

Acquisition cost: $0.00
API calls: ~60 (monthly batch queries)
New data acquired: 0 (Deribit API returned no historical data)

IC7 readiness: BLOCKED

Blocking reason:
Historical BTC option trade data (bid/ask, IV) is not available through free public API sources.
Required: Tardis.dev download of historical Deribit BTC option data (~2-3 GB, free).

Next authorized milestone:
IC6-R2 — Re-run with Tardis-downloaded BTC options data (requires user to download data first)

Authorization:
BLOCKED — DATA DOWNLOAD REQUIRED

Repository files changed:
- scripts/ic6_btc_options_validation.py (NEW)
- reports/APEX_IC6_BTC_Options_Data_Validation.md (NEW)
- reports/APEX_IC6_BTC_Options_Eligibility.csv (NEW)
- reports/APEX_IC6_Data_Coverage_Matrix.csv (NEW)
- reports/APEX_IC6_Acquisition_Record.md (NEW)
- reports/APEX_IC6_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
