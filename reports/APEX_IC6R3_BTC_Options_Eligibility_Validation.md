# APEX IC6-R3 — Corrected BTC Options Eligibility Re-Validation

**Date**: 2026-08-26
**Milestone**: IC6-R3
**Status**: COMPLETE

---

## 1. Executive Summary

IC6-R3 corrected the fatal TTE computation bug discovered by IC6-R2-CR and re-evaluated eligibility under the control-approved corrections:

- **TTE bug fixed**: Each prediction timestamp is now used as the reference for its own TTE computation
- **Maturity**: [12h, 24h] (nearest daily expiry at 08:00 UTC)
- **Freshness**: trade timestamp ≤ prediction timestamp AND age ≤ 1 hour
- **IV source**: pre-computed Black-76 from trade data (unchanged)
- **Strike**: nearest to index price from trade record (unchanged)

### Result

| Metric | IC6-R2 (invalid) | IC6-R3 (corrected) |
|--------|-------------------|---------------------|
| Eligible observations | 117 | **343** |
| TTE range | 7.5h–65.8h (wrong) | **12.0h–24.0h** (correct) |
| Mean TTE error | 307.4h | **0** |
| Trade freshness | Unbounded (hardcoded True) | **≤1h (mean 5.8 min)** |
| IC5 minimum (100) | PASS | **PASS** |
| Lookahead | No | **No** |
| Call/put joint | Invalid (wrong expiry) | **Same expiry, same strike** |

**IC7 readiness: READY**

---

## 2. IC6-R2 Bug Fixed

### Root Cause (from IC6-R2-CR)

In the batch processing loop, the variable `ts` was reassigned in the outer loop and used in the inner loop, causing all TTE computations to use the wrong (last-in-batch) prediction timestamp.

### Correction

The `evaluate_timestamp` function now receives each prediction timestamp as an explicit parameter. TTE is computed from that exact timestamp:

```python
def evaluate_timestamp(ts_str, episode_idx, trades):
    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    # ...
    tte = compute_tte(expiry, ts)  # uses THIS ts, not batch residual
```

### Bug Fix Verification

- 0% of observations have TTE error (vs. 57.3% with error ≥100h in IC6-R2)
- Every TTE is in [12h, 24h] (frozen window)
- Reproducibility: same inputs produce identical eligibility

---

## 3. Corrections Applied

### A. Maturity Window: [12h, 24h]

IC6-R2-CR approved: TTE ∈ [12h, 24h] (nearest daily expiry only).

This captures the single nearest daily Deribit BTC expiry at 08:00 UTC, which has TTE of ~16-20h for most prediction timestamps. The midpoint is ~18h, which is a defensible approximation for the 12h IC3 forward-RV horizon.

### B. Freshness: ≤ 1 Hour

The IC6-R2 code set `freshness_ok = True` unconditionally. IC6-R3 computes actual trade age:

```
trade_age = prediction_timestamp - trade_timestamp
```

Only trades with `0 ≤ trade_age ≤ 1 hour` are accepted.

### C. Call/Put Joint Observation

IC6-R2 checked call/put within the same group (which was already split by option_type). IC6-R3 collects all fresh trades at the selected strike+expiry across both C and P, then splits into call and put.

---

## 4. Eligibility Attrition

| Stage | Remaining | Rejected | Primary Reason |
|-------|----------:|---------:|----------------|
| IC3 OOS timestamps (≥2023) | 827 | — | — |
| Option data present | 827 | 0 | — |
| Trade freshness ≤ 1h | 827 | 0 | Very liquid ATM market |
| Underlying/index price | 827 | 0 | — |
| Nearest strike | 827 | 0 | — |
| Call exists (fresh) | 374 | 453 | No fresh call at ATM strike with [12h,24h] maturity |
| Put exists (fresh) | 362 | 12 | (subset of call-existing) |
| Joint call+put | 343 | 19 | Put missing at call's strike/expiry |
| Maturity [12h,24h] | 343 | 0 | — |
| **Final eligible** | **343** | **—** | **14.1% of IC6-R2's 117** |

Note: The primary attrition cause is the combination of freshness (≤1h) and maturity ([12h,24h]) constraints. Within any 1-hour window, not all ATM strikes have traded both call and put for the nearest daily expiry.

---

## 5. TTE Distribution

| TTE Bucket | Count | Percentage |
|------------|------:|-----------:|
| [12h, 15h) | 93 | 27.1% |
| [15h, 18h) | 161 | 46.9% |
| [18h, 21h) | 65 | 19.0% |
| [21h, 24h) | 20 | 5.8% |

Mean: 16.63h | Median: ~16.5h | Range: [12.00, 24.00]

The distribution is concentrated in [15h, 18h], consistent with BTC's daily 08:00 UTC expiry being ~16-20h from most hourly prediction timestamps.

---

## 6. Trade Age Distribution (Eligible)

| Metric | Value |
|--------|------:|
| Mean | 5.8 min |
| Median | 2.8 min |
| Min | 0.0 min |
| Max | 53.0 min |
| ≤15 min | 315 (91.8%) |
| 15–30 min | 20 (5.8%) |
| 30–60 min | 8 (2.3%) |

The vast majority of eligible observations have trade ages under 15 minutes. This is consistent with Deribit's active BTC ATM options market.

---

## 7. IV Statistics (Eligible)

| Statistic | Value |
|-----------|------:|
| Count | 343 |
| Mean | 54.95 |
| Median | 53.21 |
| Min | 25.14 |
| Max | 127.93 |
| Std | 14.17 |

---

## 8. Temporal Coverage

| Year | Eligible | Total | Rate |
|------|--------:|------:|-----:|
| 2023 | 90 | ~250 | ~36% |
| 2024 | 137 | ~300 | ~46% |
| 2025 | 79 | ~200 | ~40% |
| 2026 | 37 | ~77 | ~48% |

Coverage is highest in 2024-2026 as Deribit BTC options liquidity has grown.

---

## 9. Correctness Verification

| Check | Result |
|-------|--------|
| TTE ∈ [12h, 24h] | ✅ PASS |
| Trade ≤ prediction timestamp | ✅ PASS |
| Trade age ≤ 1h | ✅ PASS |
| Call/put same expiry | ✅ PASS |
| Call/put same strike | ✅ PASS |
| Reproducibility | ✅ PASS |
| No lookahead | ✅ PASS |

---

## 10. Data Source

| Property | Value |
|----------|-------|
| Provider | Deribit History API v2 |
| Endpoint | `https://history.deribit.com/api/v2/public` |
| Method | `get_last_trades_by_currency_and_time` |
| Authentication | None (public) |
| API calls (this run) | 0 (used cached raw trades from IC6-R3 first run: 827 calls) |
| Cost | $0.00 |
| Raw cache | `data/btc/ic6r3_raw_trade_cache.json` |

---

## 11. Files Created

| File | Purpose |
|------|---------|
| `scripts/ic6r3_btc_options_validation.py` | Corrected validation script |
| `data/btc/ic6r3_raw_trade_cache.json` | Raw trade cache (827 timestamps) |
| `reports/APEX_IC6R3_BTC_Options_Eligibility.csv` | Eligibility ledger (827 rows) |
| `reports/APEX_IC6R3_BTC_Options_Eligibility_Validation.md` | This report |
| `reports/APEX_IC6R3_RESULT.md` | Structured result file |
| `docs/APEX_SESSION_HANDOFF.md` | Updated |
| `docs/APEX_SESSION_STATE.json` | Updated |

---

## 12. IC7 Readiness

**READY.** The corrected eligibility ledger satisfies all IC5 frozen criteria:

- 343 eligible observations ≥ 100 minimum ✅
- TTE ∈ [12h, 24h] ✅
- Trade freshness ≤ 1h ✅
- Call/put same strike and expiry ✅
- No lookahead ✅
- Reproducible ✅

---

## 13. External API calls: 827 (first run, cached) | New data acquired: 0 (re-run from cache) | Spend: $0.00

---

*IC6-R3 is a data validation milestone. No options were traded. No IV was computed beyond structural validation. No PnL was calculated.*
