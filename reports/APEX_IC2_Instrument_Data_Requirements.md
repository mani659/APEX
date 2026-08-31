# APEX IC2 — Instrument & Data Requirements

**Date**: 2026-08-25
**Milestone**: IC2

---

## 1. Instrument: BTC Options on Deribit

### Why BTC Options

| Criterion | Detail |
|-----------|--------|
| Payoff alignment | Convex (straddle/strangle) matches non-directional vol prediction |
| Market access | Retail-accessible via Deribit (KYC required) |
| Market share | ~85% of global BTC options |
| Daily volume | ~$4.2B (as of 2026) |
| Contract type | European options, both inverse (BTC-settled) and linear (USD-settled) |
| Expiry structure | Daily, weekly, monthly, quarterly — sufficient granularity for maturity matching |
| Historical data | Available since March 2019 via free public sources |
| Greeks | Full surface (delta, gamma, vega, theta) available via API |
| Regulated | Panama-based; not US-regulated; accessible for most non-US jurisdictions |

### Why Not Other Instruments

| Instrument | Rejection Reason |
|-----------|-----------------|
| EURUSD options (CME) | RC015: data/liquidity infeasible |
| ETH options | Possible secondary instrument; BTC has higher liquidity |
| VIX/VIX futures | Equity-specific; not comparable to BTC vol |
| Volatility ETFs | Equity-specific; wrapped product; not directly comparable |
| Crypto perpetuals | Directional instrument; M24 eliminates directional edge |

---

## 2. BTC Price Data

### BTC M15 OHLCV

| Field | Requirement |
|-------|-------------|
| Provider | Tardis.dev, CryptoDataDownload, or Deribit public API |
| Instrument | BTC-PERPETUAL or BTC spot (Deribit index) |
| Granularity | 15-minute bars |
| Period | March 2019 – present (minimum 5 years) |
| Fields | Timestamp (UTC), Open, High, Low, Close, Volume |
| Approximate size | ~500K rows |
| Cost | Free |

**Use:**
- BTC realized volatility computation (RV_N)
- HIGH_VOL state construction (percentile threshold)
- Onset feature extraction (Breakout Intensity, Variance Momentum)
- Forward RV computation (12h horizon)

### BTC M1 OHLCV (Alternative)

| Field | Requirement |
|-------|-------------|
| Same providers | 1-minute bars |
| Period | March 2019 – present |
| Approximate size | ~3M rows |
| Cost | Free |

**Use:**
- Alternative RV calculation (realized variance using 1-minute returns)
- Higher-resolution intraday analysis if needed

---

## 3. BTC Options Data

### Per-Option OHLCV

| Field | Requirement |
|-------|-------------|
| Provider | Tardis.dev (most comprehensive), CryptoDataDownload |
| Instrument | All BTC options on Deribit |
| Granularity | Per-option OHLCV (tick or 1-minute) |
| Period | March 2019 – present |
| Fields | Instrument ID, Timestamp, Open, High, Low, Close, Volume, Bid, Ask |
| Approximate size | ~10M+ rows |
| Cost | Free (Tardis historical Deribit data is free) |

**Use:**
- ATM IV extraction at each timestamp
- IV surface construction
- Bid/ask spread measurement
- Option liquidity assessment

### Option Instrument Definitions

| Field | Requirement |
|-------|-------------|
| Provider | Deribit API (public endpoint) |
| Fields | Instrument ID, Underlying, Expiry Timestamp, Strike Price, Option Type (call/put), Settlement Currency |
| Approximate size | ~10K instruments |
| Cost | Free |

**Use:**
- Map instrument IDs to strike/expiry/type
- Identify ATM strike at each timestamp
- Match option expiry to forward RV horizon

### BTC Perpetual/Futures Prices

| Field | Requirement |
|-------|-------------|
| Provider | Deribit API or Tardis |
| Instrument | BTC-PERPETUAL |
| Granularity | 1-minute |
| Period | March 2019 – present |
| Fields | Timestamp, Price, Funding Rate |
| Approximate size | ~3M rows |
| Cost | Free |

**Use:**
- Mark price for option valuation
- Funding rate for cost modeling (IC5/IC6)

---

## 4. Data Volume Summary

| Dataset | Rows (approx) | Size (approx) | Cost |
|---------|---------------|---------------|------|
| BTC M15 OHLCV | 500K | ~20 MB | Free |
| BTC M1 OHLCV | 3M | ~120 MB | Free |
| BTC options OHLCV | 10M+ | ~1-2 GB | Free |
| Option definitions | 10K | ~1 MB | Free |
| BTC perpetual prices | 3M | ~120 MB | Free |
| **Total** | **~17M** | **~2-3 GB** | **Free** |

---

## 5. Data Quality Checklist

| Check | Criterion | Action if Failed |
|-------|-----------|-----------------|
| Timestamp alignment | All datasets use UTC timestamps | Convert to UTC |
| Missing days | Check for exchange downtime | Filter out incomplete days |
| Option expiry coverage | Daily expiries available from 2021+; weekly from 2019 | Restrict early analysis to available expiries |
| ATM strike availability | BTC options have $500-$1000 strike intervals | Sufficient for ATM identification |
| Bid-ask quality | Filter options with spread > 5 vol points | Exclude illiquid options |
| Volume filter | Exclude options with zero daily volume | Focus on actively traded options |
| Price continuity | Check for BTC price jumps / exchange events | Document and handle |

---

## 6. Existing Repository Resources

| Resource | Available? | Use in IC3 |
|----------|-----------|-----------|
| EURUSD M1/M15 data | ✅ Yes | NOT USED — BTC data required |
| APEX Python infrastructure | ✅ Yes | Adapt for BTC analysis |
| Cox PH implementation (statsmodels) | ✅ Yes | Same model, BTC data |
| Walk-forward validation framework | ✅ Yes | Same methodology, BTC data |
| RC012 M17-R2 experiment script | ✅ Yes | Reference architecture for BTC rebuild |

---

*IC2 is a control/research-design milestone. No data was acquired. All data requirements are for future milestones (IC3+).*
