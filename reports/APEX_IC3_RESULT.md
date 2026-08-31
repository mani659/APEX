Milestone: IC3
Status: COMPLETE

BTC data source: data/m1/BTCUSD_M1.parquet
BTC instrument: BTCUSD M1 (resampled to M15)
Historical coverage: 2021-05-23 to 2026-05-22 (5 years)
Resolution: M15 (15-minute bars)
Total M15 bars: 172,734

Warm-up: RV_WINDOW + 50 bars (70 M15 bars)

BTC HIGH_VOL definition:
- Rolling RV20 over M15 close-to-close log returns
- Annualization: 365.25 × 96 = 35,064 (BTC 24/7)
- Threshold: 80th percentile of BTC RV distribution
- Threshold value: 0.629753

BTC episode count: 1,621
Completed episodes: 1,621
Censored episodes: 0
Mean duration: 21.3 M15 bars (~5.3 hours)
Median duration: 19.0 M15 bars (~4.8 hours)

Predictor set: [Breakout_Intensity, Variance_Momentum]
Prediction boundary: onset timestamp (zero lookahead)

Walk-forward architecture:
- Chronological expanding window
- Initial training: 50 episodes
- OOS predictions: 1,571

Cox implementation: statsmodels.duration.hazard_regression.PHReg
Version: 0.14.6
Successful fits: 1,571
Failed fits: 0

OOS C-index: 0.6224
Baseline C-index: 0.4864
Delta C-index: +0.1360
Decision threshold: 0.55
Falsification gate: PASS

Comparable pairs: 1,233,235
Concordant: 734,563 (59.6%)
Discordant: 432,660 (35.1%)
Tied: 66,012 (5.4%)

BTC transferability decision: BTC TRANSFERABILITY SUPPORTED

Forward BTC RV translation:
- Horizon: 12 hours (48 M15 bars)
- OLS beta: -0.072000
- OLS SE: 0.016300
- OLS t-stat: -4.4171
- OLS p-value: 0.000011
- Pearson r: -0.1108 (p = 0.000011)
- Spearman rho: -0.1653 (p < 0.000001)
- Result: BTC FORWARD RV TRANSLATION ESTABLISHED

What IC3 establishes:
- BTC HIGH_VOL persistence is predictable from onset features (C-index = 0.6224, OOS)
- Predicted persistence translates to forward BTC realized volatility (p = 0.000011)
- The EURUSD-validated architectural concept transfers to BTC using BTC-native parameters
- The phenomenon is not EURUSD-specific

What IC3 does NOT establish:
- BTC options mispricing (no options data used)
- RV > IV (no implied volatility computed)
- Straddle profitability (no options strategy tested)
- Execution edge (no execution simulated)
- Economic expectancy (no PnL calculated)

Economic path status:
- IC1: ✅ COMPLETE — crypto options selected
- IC2: ✅ COMPLETE — BTC re-estimation approach frozen
- IC3: ✅ COMPLETE — BTC TRANSFERABILITY SUPPORTED
- IC4: PLANNED — NOT STARTED
- IC5: PLANNED — NOT STARTED
- IC6: PLANNED — NOT STARTED

IC4 recommendation:
IC3 has established that the BTC volatility-persistence phenomenon exists and is predictable.
IC4 should verify that BTC options IV data is observable and maturity-matchable with the 12h forward RV horizon.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- scripts/ic3_btc_transferability.py (NEW)
- reports/APEX_IC3_BTC_Transferability_Experiment.md (NEW)
- reports/APEX_IC3_BTC_Transferability_Data.csv (NEW)
- reports/APEX_IC3_BTC_Episode_Ledger.csv (NEW)
- reports/APEX_IC3_Result_Summary.json (NEW)
- reports/APEX_IC3_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
