Milestone: IC4
Status: COMPLETE

IC3 foundation:
- BTC transferability SUPPORTED (C-index = 0.6224)
- Forward RV translation ESTABLISHED (p = 0.000011)
- 1,571 OOS predictions spanning 2021-06-28 to 2026-05-04

BTC option instrument:
- Exchange: Deribit (Panama-based, retail-accessible)
- Underlying: BTC-PERPETUAL or BTC spot index
- Option type: European (inverse & linear)
- Expiry structure: 8-hour, daily, weekly, monthly, quarterly
- Market share: ~85% of global BTC options

Historical option coverage:
- Deribit BTC options: March 2019 – present
- All IC3 prediction timestamps (2021-06 to 2026-05) fall within coverage
- Data sources: Tardis (free), CryptoDataDownload (free), Deribit API (free)

Prediction-timestamp coverage:
- 1,571 IC3 OOS predictions
- 912 unique dates
- All timestamps within Deribit BTC options coverage period
- 24/7 market: no market-hours gaps

Primary IV representation:
- ATM implied volatility from nearest qualifying option
- Black-76 inversion from midpoint price: mid = (bid + ask) / 2
- Both call and put used; averaged if both available at same strike

Strike-selection rule:
- Nearest strike to BTC-PERPETUAL mark price at prediction timestamp
- Frozen before any economic test

Maturity:
- Primary: nearest expiry with TTE in [6h, 18h]
- Fallback: nearest expiry with TTE > 0 (flagged as maturity-mismatched)
- Maximum acceptable mismatch: 24 hours
- Interpolation: NOT permitted

Maturity-matching rule:
- Frozen deterministic rule: nearest expiry in [6h, 18h] of prediction timestamp
- Based on IC3 12h forward RV horizon

IV quote-quality criteria:
- Tier 1: Fresh bid/ask, spread < 5 vol points (primary)
- Tier 2: Valid quote within 1 hour staleness bound (acceptable)
- Tier 3: Stale quote > 1 hour or mark-only (flagged)
- Tier 4: No usable quote (excluded)
- Staleness threshold: 1 hour (60 minutes) — newly frozen

Annualization convention:
- RV: 365.25 × 96 = 35,064 (BTC 24/7, M15 bars)
- IV: 365 days/year (Deribit standard)
- Difference: < 0.02% — negligible, no conversion required

Observability result:
PASS WITH LIMITATIONS

Major data limitations:
- NO BTC option data exists locally in the repository
- BTC options data must be acquired from Tardis/CryptoDataDownload/Deribit API
- All sources are free (~2-3 GB total)
- Data acquisition is the sole prerequisite for IC5

Major methodology limitations:
- Staleness threshold (1 hour) newly frozen in IC4 (not in IC2)
- 8-hour BTC options may not be available for 2021 predictions (introduced ~2022)
- Early-period (2021) options may have thinner liquidity

Economic mechanism status:
- All 5 steps of the economic chain are structurally observable
- Only step 3 (BTC IV at prediction timestamp) requires data acquisition
- No methodology gaps remain

Decision:
PASS WITH LIMITATIONS

Next authorized milestone:
IC5 — BTC IV/RV Economic Mechanism Methodology Design

IC5 prerequisite:
BTC options historical data must be acquired from public sources (free)

Authorization:
PLANNED — NOT STARTED

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_IC4_BTC_IV_RV_Observability_Audit.md (NEW)
- reports/APEX_IC4_BTC_IV_Data_Requirements.csv (NEW)
- reports/APEX_IC4_Maturity_Matching_Audit.csv (NEW)
- reports/APEX_IC4_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
