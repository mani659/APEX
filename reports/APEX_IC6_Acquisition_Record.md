# APEX IC6 — Data Acquisition Record

**Date**: 2026-08-25

## Sources Attempted

### 1. Deribit Public API

| Detail | Value |
|--------|-------|
| Endpoint | `get_last_trades_by_currency` |
| Authentication | None (public) |
| Rate limit | ~100 requests/minute |
| Historical coverage | Last 24-48 hours only |
| Monthly batch queries | 60 (all returned 0 trades for historical periods) |
| Recent data test | 417 trades in last hour (WORKS for recent data) |
| Cost | $0.00 |

**Verdict:** Deribit public API does not provide historical trade data for periods before the most recent 24-48 hours. This is a known limitation of the public API.

### 2. CryptoDataDownload

| Detail | Value |
|--------|-------|
| URL | cryptodatadownload.com/data/deribit/ |
| BTC data found | `DeriBit_volatility_OHLC_BTC.csv` |
| Content | Daily DVOL index (1,984 rows, 2021-present) |
| Option bid/ask data | NOT available |
| Cost | $0.00 |

**Verdict:** Provides DVOL volatility index but not individual option bid/ask data required by IC5.

### 3. Tardis.dev (Not Attempted)

| Detail | Value |
|--------|-------|
| Coverage | March 2019 – present |
| Data format | JSON/CSV |
| Data volume | ~10M+ rows for BTC options |
| Cost | Free for historical Deribit data |
| Download status | NOT attempted (requires specialized download) |

**Verdict:** Tardis has the required data but was not downloaded during IC6. This is the recommended data source for re-running IC6.

## Total Acquisition Cost

| Item | Cost |
|------|------|
| API calls | ~60 (free) |
| Data downloads | $0.00 |
| **Total** | **$0.00** |

## Recommended Next Step

Download historical BTC option data from Tardis.dev (free), then re-run IC6 validation.
