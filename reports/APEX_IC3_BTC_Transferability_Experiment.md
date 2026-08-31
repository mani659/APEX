# APEX IC3 — BTC Transferability Pre-Economic Validation

**Date**: 2026-08-25
**Milestone**: IC3
**Status**: COMPLETE
**Classification**: Scientific transfer test — does the HIGH_VOL phenomenon exist on BTC?

---

## 1. Executive Summary

IC3 tested whether the EURUSD-validated HIGH_VOL volatility-persistence predictability phenomenon transfers to BTC under a strictly BTC-native, out-of-sample methodology.

**Result: BTC TRANSFERABILITY SUPPORTED.**

- OOS C-index: **0.6224** (threshold: 0.55)
- Delta C-index: **+0.1360** over baseline
- Forward 12h RV translation: **ESTABLISHED** (p = 0.000011)
- 1,571 strict OOS predictions from 1,621 BTC HIGH_VOL episodes

---

## 2. Frozen IC2 Architecture Applied

| Component | IC2 Specification | BTC Implementation |
|-----------|-------------------|-------------------|
| Volatility measure | Rolling RV_N over M15 bars | RV20 over M15 bars (window=20) |
| HIGH_VOL threshold | 80th percentile of BTC RV distribution | P80 = 0.629753 |
| Episode construction | Contiguous bars above threshold | 1,621 episodes (mean duration=21.3 M15 bars) |
| Onset features | Breakout Intensity, Variance Momentum | Same definitions, BTC-calibrated values |
| Model | Cox PH (statsmodels.PHReg) | statsmodels 0.14.6 |
| Validation | Chronological expanding-window OOS | Initial training: 50 episodes; 1,571 OOS |
| Primary metric | Harrell's C-index > 0.55 | **0.6224** |
| Forward RV | 12h realized volatility | 48 M15 bars, annualized with 365.25×96 |

---

## 3. BTC Data Audit

| Dimension | Value |
|-----------|-------|
| Source | data/m1/BTCUSD_M1.parquet |
| Instrument | BTCUSD M1 |
| Resolution | 1-minute bars |
| Coverage | 2021-05-23 to 2026-05-22 (5 years) |
| M1 bars | 2,539,807 |
| M15 bars (resampled) | 172,805 |
| M15 bars after warm-up | 172,734 |
| Trading days | 1,825 (24/7) |
| Missing timestamps | 29,355 gaps > 1.5 min (normal for M1 data) |
| Duplicate timestamps | 0 |
| Zero/negative close | 0 |
| Weekend data | Included (BTC trades 24/7) |
| Data integrity | PASS |

---

## 4. BTC HIGH_VOL State Construction

| Parameter | Value |
|-----------|-------|
| RV window (N) | 20 M15 bars (5 hours) |
| Annualization constant | 365.25 × 96 = 35,064 |
| Activation threshold | P80 of BTC RV distribution |
| Threshold value | 0.629753 |
| HIGH_VOL bars | 34,547 (20.0% of total) |

The 80th percentile threshold produces a HIGH_VOL state that activates 20% of the time — structurally comparable to the EURUSD activation rate.

---

## 5. Episode Ledger Statistics

| Metric | Value |
|--------|-------|
| Total episodes | 1,621 |
| Completed episodes | 1,621 |
| Censored episodes | 0 |
| Mean duration | 21.3 M15 bars (~5.3 hours) |
| Median duration | 19.0 M15 bars (~4.8 hours) |
| Max duration | 679 M15 bars (~170 hours) |
| Valid episodes (no NaN) | 1,621 |

**Structural comparison with EURUSD:**
- EURUSD: 794 episodes, mean duration ~similar order
- BTC: 1,621 episodes (2× more episodes due to 24/7 trading and higher vol frequency)
- BTC episodes are more numerous but structurally analogous

---

## 6. Walk-Forward Validation Results

### Walk-Forward Configuration

| Parameter | Value |
|-----------|-------|
| Initial training episodes | 50 |
| Total episodes | 1,621 |
| OOS predictions | 1,571 |
| Successful Cox fits | 1,571 |
| Failed fits | 0 |
| Convergence warnings | 0 |

### OOS C-Index

| Metric | Value |
|--------|-------|
| OOS C-index | **0.6224** |
| Baseline C-index | 0.4864 |
| Delta C-index | **+0.1360** |
| Falsification threshold | 0.55 |
| **Gate result** | **PASS** |

### Pair Statistics

| Metric | Value |
|--------|-------|
| Comparable pairs | 1,233,235 |
| Concordant | 734,563 (59.6%) |
| Discordant | 432,660 (35.1%) |
| Tied | 66,012 (5.4%) |

**Interpretation:** The BTC onset features (Breakout Intensity, Variance Momentum) predict BTC HIGH_VOL episode duration with C-index = 0.6224 — well above the 0.55 threshold and comparable to the EURUSD result (0.6656). The predictive signal transfers.

---

## 7. Forward RV Translation

| Metric | Value |
|--------|-------|
| Forward horizon | 12 hours (48 M15 bars) |
| Valid observations | 1,571 |
| OLS beta | -0.072000 |
| OLS SE | 0.016300 |
| OLS t-stat | -4.4171 |
| OLS p-value | 0.000011 |
| Pearson r | -0.1108 (p = 0.000011) |
| Spearman rho | -0.1653 (p < 0.000001) |
| **Decision** | **BTC FORWARD RV TRANSLATION ESTABLISHED** |

**Interpretation:** The BTC Cox PH risk score significantly predicts forward 12h realized volatility (p = 0.000011). Higher risk score (shorter predicted duration) → lower forward RV, exactly as on EURUSD. The structural relationship transfers.

---

## 8. IC3 Integrity Gates

| Gate | Criterion | Result |
|------|-----------|--------|
| A: BTC data integrity | Data available, no duplicates, valid prices | ✅ PASS |
| B: BTC HIGH_VOL construction | Causal onset, percentile-based threshold | ✅ PASS |
| C: Episode construction | Deterministic, contiguous, no overlap | ✅ PASS |
| D: Predictors frozen | Breakout Intensity + Variance Momentum, no selection | ✅ PASS |
| E: Chronological walk-forward | Strict expanding window, no shuffling | ✅ PASS |
| F: No leakage | Features at onset only, forward RV is future | ✅ PASS |
| G: Cox implementation | statsmodels.PHReg, 1,571/1,571 successful | ✅ PASS |
| H: C-index on OOS | Computed on 1,571 genuinely OOS predictions | ✅ PASS |
| I: No outcome-driven exclusions | All 1,621 episodes included | ✅ PASS |

**All 9 gates: PASS**

---

## 9. Comparison with EURUSD

| Dimension | EURUSD (M17-R2) | BTC (IC3) |
|-----------|-----------------|-----------|
| Asset | EURUSD spot | BTCUSD |
| Trading hours | ~24h (weekdays) | 24/7 |
| Data period | 5.5 years | 5.0 years |
| M15 bars | ~350K | 172,734 |
| RV window | 20 M15 | 20 M15 |
| Threshold | P80 | P80 |
| Episodes | 794 | 1,621 |
| Predictors | Breakout Intensity, Variance Momentum | Same definitions, BTC-calibrated |
| OOS C-index | 0.6656 | 0.6224 |
| Delta C-index | +0.1656 | +0.1360 |
| Forward RV translation | p = 0.0032 | p = 0.000011 |
| Directional translation | NOT established (p = 0.6418) | Not tested (IC3 scope) |

**The BTC result is structurally analogous to the EURUSD result, with C-index and translation significance in the same range.**

---

## 10. What IC3 Establishes

1. **BTC HIGH_VOL persistence is predictable from onset features** (C-index = 0.6224, OOS)
2. **The predicted persistence translates to forward BTC realized volatility** (p = 0.000011)
3. **The EURUSD-validated architectural concept transfers to BTC** using BTC-native parameters
4. **The phenomenon is not EURUSD-specific** — it exists on a fundamentally different asset class with different microstructure (24/7, crypto, different liquidity profile)

---

## 11. What IC3 Does NOT Establish

1. **BTC options mispricing** — no options data was used
2. **RV > IV** — no implied volatility was computed
3. **Straddle profitability** — no options strategy was tested
4. **Execution edge** — no execution was simulated
5. **Economic expectancy** — no PnL was calculated
6. **Cross-asset causality** — the EURUSD and BTC results are independent; no causal mechanism linking them is claimed

---

## 12. Economic Path Status

| Gate | Status |
|------|--------|
| IC1: Instrument feasibility | ✅ COMPLETE — crypto options selected |
| IC2: Transfer methodology | ✅ COMPLETE — BTC re-estimation approach |
| **IC3: BTC transferability** | **✅ COMPLETE — SUPPORTED (C-index = 0.6224)** |
| IC4: IV-RV observability | PLANNED — NOT STARTED |
| IC5: Economic methodology | PLANNED — NOT STARTED |
| IC6: Economic execution | PLANNED — NOT STARTED |

**IC3 is the critical scientific gate. It has PASSED.** The crypto-options economic path has a scientifically defensible foundation.

---

## 13. External API calls: 0 | New data acquired: 0 | Spend: $0.00

---

*IC3 is a scientific transfer test. No options were traded. No IV was computed. No PnL was calculated.*
