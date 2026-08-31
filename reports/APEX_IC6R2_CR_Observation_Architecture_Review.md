# APEX IC6-R2-CR — BTC Options Observation Architecture & Economic-Estimand Integrity Review

**Date**: 2026-08-26
**Milestone**: IC6-R2-CR
**Status**: COMPLETE
**Classification**: CONTROL / METHODOLOGY REVIEW

---

## 0. EXECUTIVE FINDING

### CRITICAL: FATAL IMPLEMENTATION BUG DISCOVERED

A Python loop-variable scoping bug in `scripts/ic6r2_btc_options_validation.py` caused the TTE (time-to-expiry) computation and maturity selection to use the **wrong prediction timestamp** for the majority of observations.

**Impact**: Of the 117 reported "eligible" observations:
- **Only 14 (12.0%)** have approximately correct maturity matching (TTE error < 2h)
- **67 (57.3%)** have catastrophically wrong maturity matching (TTE error ≥ 100h)
- **Mean absolute TTE error: 307.4 hours** (~13 days)

Most "eligible" observations have IV from long-dated weekly/monthly options rather than the near-daily options IC5 intended. **The 117 eligible observations do not observe the IC5 economic quantity.**

This is not an amendment classification question. This is a **data-integrity failure** that invalidates IC6-R2's eligibility count.

**IC7 remains BLOCKED.**

---

## 1. Bug Description

### Root Cause

In the batch processing loop of `scripts/ic6r2_btc_options_validation.py`:

```python
for batch_start in range(0, total, batch_size):
    tasks = []
    for idx, row in batch.iterrows():
        ts = row["ts"]               # <-- ts reassigned each iteration
        ...
        tasks.append((idx, row, ts_str, ts_key, start_ms, end_ms))
    
    for idx, row, ts_str, ts_key, start_ms, end_ms in tasks:
        trades = await fetch_trades_batch(client, semaphore, start_ms, end_ms)
        ...
        atm_options = find_atm_options(trades, ts, index_price)  # <-- ts is LAST batch value
```

The variable `ts` is defined in the outer loop but used in the inner loop. After the outer loop completes, `ts` holds the **last prediction timestamp in the batch**, not the timestamp for the current task. The inner loop then computes all TTEs relative to this wrong reference time.

### Consequence

1. **API queries are correct**: `start_ms` and `end_ms` are computed per-task and passed into the inner loop. The correct time window of trades is fetched.
2. **TTE computation is wrong**: `find_atm_options` receives the wrong `reference_dt`, so all TTE calculations are offset.
3. **Maturity selection is wrong**: The "nearest to 12h" selection uses wrong TTEs, selecting wrong expiries.
4. **IV values are from wrong instruments**: The IV returned is for the wrongly-selected expiry.
5. **Strike selection is correct**: Strike uses `index_price` from the trade data itself, not from the wrong `ts`.

### Error Distribution (117 "eligible" observations)

| Error Band | Count | Percentage | Meaning |
|------------|-------|------------|---------|
| < 2h | 14 | 12.0% | Approximately correct |
| 2–24h | 18 | 15.4% | Materially wrong (wrong daily expiry) |
| 24–100h | 18 | 15.4% | Severely wrong (off by 1–4 days) |
| ≥ 100h | 67 | 57.3% | Catastrophically wrong (off by weeks/months) |

Mean absolute error: **307.4 hours** (~13 days)
Max absolute error: **1,637.2 hours** (~68 days)

### Example

| Obs | Prediction Timestamp | Selected Instrument | Recorded TTE | Correct TTE | Error |
|-----|---------------------|--------------------:|-------------:|------------:|------:|
| 0 | 2023-03-12 18:00 | BTC-14MAR23-21000-C | 10.0h | 38.0h | -28h |
| 5 | 2023-08-17 16:30 | BTC-27OCT23-27000-C | 58.2h | 1695.5h | -1637h |
| 7 | 2023-08-29 14:15 | BTC-27OCT23-26000-C | 58.2h | 1409.8h | -1352h |
| 14 | 2023-10-16 13:15 | BTC-27OCT23-28000-C | 58.2h | 258.8h | -201h |

Obs 5: The prediction is for August 17, 2023. The selected option expires October 27, 2023 (71 days later). The correct near-daily option would expire August 18, 2023 (1 day later). The IV recorded (from a71-day option) has nothing to do with the IC5 economic quantity.

---

## 2. Frozen IC5 Economic Quantity

```text
At prediction time t:

A = forecast of BTC realized volatility over the frozen future horizon (12 hours)

B = contemporaneously observable BTC option-implied volatility
    for an option whose maturity is sufficiently aligned with A

Economic comparison:

A versus B

Potential mechanism:

forecast realized volatility > priced implied volatility
        ↓
potential positive-value direction-neutral convex payoff
```

The IC5 architecture requires IV from an option whose maturity approximates the12h forward RV horizon. The maturity expansion to [6h, 72h] already stretches this; the TTE bug stretches it catastrophically to weeks/months.

---

## 3. Amendment Classification Table

| IC5 → IC6-R2 change | Classification | Economic quantity affected? | Scientific equivalence? | Risk |
|----------------------|----------------|------------------------------|-------------------------|------|
| Maturity: [6h,18h] → [6h,72h] | ESTIMAND CHANGED | Yes — compares12h forecast vs20-68h IV | NO — different term exposure | HIGH |
| IV source: BBO midpoint → trade `iv` | OPERATIONAL | No — same Black-76 model | YES — equivalent formula | LOW |
| Freshness: ≤1h → ≤24h (actual: unbounded) | OBSERVATION-PROCESS CHANGE | Yes — potentially stale IV | WEAK — may not represent t | MEDIUM |
| **TTE bug: wrong reference timestamp** | **FATAL IMPLEMENTATION BUG** | **Yes — selects wrong instrument entirely** | **NO — observes wrong economic quantity** | **FATAL** |

---

## 4. Amendment A — Maturity Window

### A1: IC3 Future-RV Horizon

IC3 forward RV horizon = **12 hours** (48 M15 bars). The OLS mapping produces a predicted_RV for this specific horizon.

### A2: What a20h, 44h, and 68h Option IV Prices

- 20h option IV: prices total realized variance over approximately20 hours
- 44h option IV: prices total realized variance over approximately44 hours
- 68h option IV: prices total realized variance over approximately68 hours

These are fundamentally different economic quantities. A68-day option's IV reflects nearly 6× the time exposure of the12h prediction horizon.

### A3: Can These Maturities Proxy the IC3 Horizon?

**No.** The IC5 methodology compares predicted_RV_12h against option IV. For the comparison to be economically meaningful, the option IV must approximate the12h forward realized volatility. An option with68h TTE prices a different variance integral.

### A4: Homogeneous or Different Term Exposures?

The observations span TTEs of 7.5h to 65.75h. These are **materially different term exposures**. The IV for a T+1 daily option reflects different volatility dynamics than a T+3 option, especially during HIGH_VOL episodes where term structure is typically in contango or backwardation.

### A5: Does Expansion Change the Estimand?

**Yes.** Even without the TTE bug, mixing T+1 and T+3 maturities in a single sample changes the economic comparison from "forecast vs contemporaneous IV at matched maturity" to "forecast vs IV at heterogeneous, unmatched maturities."

### A6: Is a Narrower Rule Defensible?

**Yes, scientifically.** A maturity window of [6h, 24h] would capture only the nearest daily expiry (T+1). This would reduce N but preserve the economic quantity. The T+1 expiry at 08:00 UTC is the natural instrument for a12h forecast horizon.

### Classification: **ESTIMAND CHANGED**

The maturity expansion changes what economic quantity is being compared. However, the nearest daily expiry (T+1, ~16-20h TTE) is a defensible approximation for the12h horizon. The problem is the TTE bug, which selects instruments far beyond even the [6h, 72h] window.

---

## 5. Amendment B — IV Source

### Deribit Pre-Computed IV

The `iv` field in Deribit trade data is the Black-76 implied volatility computed from the trade price. The underlying inputs are:
- **Option trade price**: the executed price (not a quote/midpoint)
- **Underlying**: `index_price` from the trade record (BTC spot index)
- **Strike**: from instrument name
- **TTE**: from expiry date and trade timestamp
- **Rate**: 0 (standard for crypto options)
- **Model**: Black-76 (standard for European options on futures/spot)

### Mathematical Equivalence

Using trade price as midpoint proxy is a standard approximation for liquid ATM options. The mathematical pricing formula is identical to IC5's specification.

### Observation-Process Distinction

There is a critical distinction between:
1. **Mathematical pricing formula**: Black-76 — IDENTICAL
2. **Market-price observation process**: trade price vs BBO midpoint — DIFFERENT

A trade price is an executed price, not a two-sided quote. It embeds:
- One-sided liquidity selection (buyer-initiated or seller-initiated)
- Possible bid/ask spread (half-spread cost)
- Transaction selection bias (trades occur at bid/ask, not necessarily midpoint)

For liquid ATM options, this approximation is standard. The error is typically small.

### Classification: **OPERATIONAL**

The IV source change is an operational implementation detail. The mathematical model is identical, and the trade-price-as-midpoint approximation is standard for ATM options.

---

## 6. Amendment C — Freshness

### What IC6-R2 Actually Implemented

The code sets `freshness_ok = True` unconditionally:

```python
freshness_ok = True  # we queried within 1h, so any trade is ≤1h old
```

The comment is incorrect — the query window is 24 hours, not 1 hour. But no actual freshness computation is performed. All 827 observations pass the freshness criterion regardless of when the selected trade occurred within the 24h window.

### Can a24h-Old Trade Represent Market IV at t?

**Potentially, but unreliably.** BTC option IV can change dramatically within24 hours:
- During HIGH_VOL episodes, IV can spike 20-50+ vol points intraday
- BTC spot can move 5-15% in24h, affecting moneyness and IV
- Term structure can invert or flatten during vol events
- Option time decay reduces sensitivity to spot moves

A trade executed at t-23h may represent a completely different market state than the IC3 prediction timestamp.

### Does It Violate the Information Boundary?

**Yes, in principle.** IC5 requires "contemporaneously observable" IV. A23-hour-old trade is not contemporaneous. It may be stale in a market that reprices volatility within hours.

### Scientific Interpretability

If the economic test uses stale trades, the result would answer: "Is there a relationship between the APEX forecast and the IV of an option that traded within 24h of the prediction?" This is weaker than the IC5 question: "Is there a relationship between the APEX forecast and contemporaneous IV?"

### Classification: **VALID WITH STRICT LIMITATION** (for ≤24h freshness)

The24h freshness rule is scientifically interpretable as a weaker version of the IC5 question. However, the actual IC6-R2 implementation has **no freshness filter at all**, which is stronger than even the24h relaxation.

---

## 7. Timestamp Directionality

### API Query Window

The API queries trades from `[ts - 24h, ts]` (start_timestamp to end_timestamp). This means trades are **strictly before** the prediction timestamp (assuming the API's end_timestamp is exclusive or the most recent trade in the window is at or before ts).

### Selected Trade Timestamp

The script selects the most recent trade within the query window. This trade should be at or near the prediction timestamp, but potentially up to 24h before.

### No Lookahead in Data Fetching

The data-fetching step does not introduce lookahead. The query bounds are correctly set per observation.

### BUT: Wrong TTE Due to Bug

While the trade data is fetched from the correct time window, the TTE computation uses the wrong reference timestamp. This means the maturity selection is wrong, but the trade data itself is temporally valid.

### Classification: **NO LOOKAHEAD** (in data fetching); **INCORRECT MATURITY SELECTION** (due to bug)

---

## 8. Strike Selection Integrity

### Underlying Source

The `index_price` comes from the trade record itself (each Deribit trade includes the BTC index price at trade time). This is correct and available at the trade timestamp.

### Nearest-Strike Rule

The code finds the strike closest to `index_price`:
```python
atm_strike = min(strikes, key=lambda s: abs(s - index_price))
```

This is deterministic and uses information available at the trade timestamp.

### No Outcome-Based Selection

Strike selection is not influenced by future outcomes. The `index_price` is from the historical trade.

### Classification: **OPERATIONAL** — Strike selection is correct and uses only information available at the trade timestamp.

---

## 9. Call/Put Joint Observation

The script checks whether both call and put trades exist for the same strike and expiry within the query window. This is a structural requirement for the straddle construction.

The check is performed correctly — it filters trades by option_type, strike, and expiry_dt.

### Potential Issue

Call and put trades may occur at very different times within the 24h window. A call trade at t-22h and a put trade at t-1h would both pass, but they represent different market states. IC5 requires a contemporaneous straddle.

### Classification: **OBSERVATION-PROCESS CHANGE** — Both legs exist but may not be truly contemporaneous.

---

## 10. Eligibility Saturation Audit

### Progression Analysis

| Step | Maturity Rule | Eligible | Cumulative Change |
|------|--------------|----------|-------------------|
| Original IC5 | [6h, 18h] | ~44 | Baseline (with bug) |
| First expansion | [6h, 48h] | ~64 | +20 (maturity relaxation) |
| Second expansion | [6h, 72h] | ~81 | +17 (more maturity relaxation) |
| Final IC6-R2 | [6h, 72h] + bug | 117 | +36 (bug + maturity) |

The progression shows both legitimate maturity expansion (BTC's daily expiry structure) and the bug inflating the count. The bug actually selects instruments from FAR outside the [6h, 72h] window (with correct TTEs of 100-1600h), but these are incorrectly recorded as being within the window due to the wrong TTE computation.

### Was Progression Driven by Science or Sample Pressure?

The maturity expansion was scientifically justified (BTC's daily 08:00 UTC expiry). The bug was unintentional. However, the combination produced an inflated eligibility count that passed the N=100 gate while measuring the wrong economic quantity.

### Classification: **BUG-DRIVEN**, not outcome-driven p-hacking, but equally invalidating.

---

## 11. Economic-Estimand Preservation Test

For each amendment, answering: "If IC5 were rewritten using this rule before seeing any outcome, would it ask the same economic question?"

| Amendment | Same Economic Quantity? | Verdict |
|-----------|------------------------|---------|
| Maturity [6h,72h] | NO — 12h forecast vs20-68h IV | ESTIMAND CHANGED |
| IV from trade price | YES — same Black-76 model | SAME QUANTITY |
| Freshness ≤24h | WEAKLY YES — weaker but interpretable | SAME QUANTITY WITH LIMITATION |
| **TTE bug** | **NO — observes wrong instruments entirely** | **INVALID** |

---

## 12. IC5 Methodology vs IC6-R2 Data Reality

| Component | IC5 intended quantity | IC6-R2 actual observable | Same? | Consequence |
|-----------|----------------------|--------------------------|-------|-------------|
| Future RV | 12h forward realized volatility | 12h forward realized volatility | YES | Unchanged |
| IV | ATM IV at prediction timestamp | ATM IV at prediction timestamp (correct fetch) | YES (data) | Correct data fetched |
| **Maturity** | **TTE ∈ [6h, 18h]** | **Wrong instrument selected (TTE error up to1637h)** | **NO** | **Wrong economic quantity** |
| Strike | Nearest to index price | Nearest to index price (correct) | YES | Unchanged |
| Timestamp | At prediction timestamp | Before prediction timestamp (≤24h) | APPROX | Acceptable |
| **Quote freshness** | **≤ 1 hour** | **No freshness check (all pass)** | **NO** | **Potentially stale** |
| **Call/put pair** | **Contemporaneous** | **Within 24h window (may differ)** | **WEAK** | **Different market states** |
| Execution price | Midpoint of BBO | Trade price (pre-computed IV) | YES (approx) | Standard approximation |

---

## 13. Is Trade-Level IV Acceptable?

**Yes, with conditions.** A precomputed trade-level IV is an acceptable proxy for contemporaneous IV when:

1. The trade is temporally close to the observation timestamp (ideally < 1h)
2. The option is liquid (ATM, active market)
3. The trade price represents a fair market value (not an outlier)

**The24h freshness relaxation weakens this acceptability** but does not destroy it for most observations, since ATM BTC options on Deribit trade frequently.

**The TTE bug destroys this acceptability** because the wrong option is selected entirely.

### Minimum Scientifically Defensible Freshness Rule

**Trade within 1 hour of prediction timestamp.** This is tighter than IC5's BBO-based rule but achievable for Deribit's active BTC options market during24h trading.

---

## 14. Final Control Decision

### Decision: **C — REJECT IC6-R2**

**IC6-R2's eligibility results are invalidated by the TTE computation bug.**

The 117 "eligible" observations do not observe the IC5 economic quantity. The majority (57.3%) have IV from options expiring weeks or months after the prediction timestamp, rather than the near-daily options IC5 requires.

### Required Next Steps

1. **Fix the TTE bug** in `scripts/ic6r2_btc_options_validation.py` (pass `ts` into `find_atm_options` per-task, not as a batch-level variable)
2. **Re-run IC6** as **IC6-R3** with the corrected script
3. **Apply stricter maturity rule**: [6h, 24h] to capture only the nearest daily expiry
4. **Apply actual freshness check**: trade timestamp within 1h of prediction timestamp
5. **Re-evaluate eligibility count** under corrected rules
6. If eligible observations ≥ 100, authorize IC7

### No Methodology Amendment Is Approved

The three IC6-R2 amendments (maturity, IV source, freshness) are not approved or rejected on their merits because the TTE bug makes the data uninterpretable. The control review must be repeated on corrected data.

---

## 15. What IC6-R2 Got Right

Despite the TTE bug:

1. **Data source selection**: Deribit History API v2 is the correct free source for historical BTC option data
2. **API query design**: The query window [ts-24h, ts] is correct and introduces no lookahead
3. **Strike selection logic**: Uses trade-level `index_price`, correct and deterministic
4. **IV field usage**: Pre-computed Black-76 IV from trade data is methodologically equivalent
5. **Cache architecture**: Progressive caching avoids redundant API calls
6. **No outcome filtering**: Eligibility is determined without reference to future PnL
7. **Cost**: $0.00, 827 API calls, correctly rate-limited

---

## 16. Files Created

| File | Purpose |
|------|---------|
| `reports/APEX_IC6R2_CR_Observation_Architecture_Review.md` | This report |
| `reports/APEX_IC6R2_CR_Methodology_Amendment_Decision.md` | Amendment classification and decision |
| `reports/APEX_IC6R2_CR_RESULT.md` | Structured result file |

No methodology amendment file is created because no amendment was approved.

---

## 17. External API calls: 0 | New data acquired: 0 | Spend: $0.00

---

*IC6-R2-CR is a control review. No data was acquired. No economic test was run. No PnL was calculated.*
