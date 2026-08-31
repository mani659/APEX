Milestone: IC2
Status: COMPLETE

Economic mechanism:
Predicted BTC realized volatility > BTC options-implied volatility → long straddle → profit from IV-RV spread via convex payoff.

Instrument:
BTC options on Deribit (European, inverse & linear, daily/weekly/monthly expiries, ~85% market share).

Core transfer hypothesis:
The EURUSD-validated architectural concept — that realized volatility regime onsets contain predictive information about future volatility duration, which maps to forward realized volatility — can be reconstructed on BTC using BTC-native parameters.

Transfer architecture:
Approach B — BTC Re-estimation (SELECTED)
Same mathematical architecture as EURUSD M17-R2, but ALL parameters re-estimated from BTC data.
EURUSD findings serve as architectural motivation, not as a source of parameters.
This is the scientifically defensible approach.

Rejected approaches:
- A: Direct Structural Transfer (REJECT — EURUSD parameters not applicable to BTC)
- C: Cross-Market Latent State (REJECT — RC014 rejected cross-asset transmission)
- D: No Transfer (MAINTAIN AS FALLBACK — correct action if Approach B fails)

Primary BTC state definition:
Rolling realized volatility (RV_N) over N M15 bars, with 80th percentile threshold activation.
All parameters (N, percentile, lookback) to be frozen in IC3 from BTC data.

Primary future-RV representation:
12-hour forward realized volatility computed from BTC M15 close prices.
Annualized using 252 × 24 × 4 = 24,192 constant.

Primary IV representation:
ATM implied volatility from Deribit BTC options.
Most liquid option at each timestamp; direct comparison with RV.

Maturity matching concept:
12h forward RV matched with 12h or 24h option expiry.
Maximum maturity mismatch: 6 hours.
No interpolation permitted.

Information boundary:
At BTC HIGH_VOL onset timestamp t:
- Observable: BTC price history, RV, onset features, risk score, predicted RV, current ATM IV
- NOT observable: Future BTC prices, future RV, future IV, future option prices

Required data:
- BTC M15 OHLCV (~500K rows, free via Tardis/CryptoDataDownload)
- BTC options OHLCV (~10M rows, free via Tardis)
- Option instrument definitions (~10K, free via Deribit API)
- BTC perpetual prices (~3M rows, free via Deribit API)
Total: ~2-3 GB, $0.00

Future external data:
All data is publicly available at zero cost.
No acquisition required until IC3 execution.

Major risks:
1. BTC may not exhibit the HIGH_VOL primitive or its onset may not be predictable
2. BTC volatility dynamics may differ structurally from EURUSD
3. IV may systematically exceed predicted RV even during vol expansion
4. Options execution during vol events may have wide spreads
5. BTC options liquidity may be insufficient for straddle execution at signal time

Candidate transfer approaches:
A: Direct Structural Transfer — Score 33/50 — REJECT
B: BTC Re-estimation — Score 43/50 — SELECTED
C: Cross-Market Latent State — Score 24/50 — REJECT
D: No Transfer — Score 42/50 — FALLBACK

Primary approach:
B: BTC Re-estimation (same architecture, BTC-native parameters)

Decision:
CONTINUE

Next authorized milestone:
IC3 — BTC Transferability Pre-Economic Validation

IC3 scope:
- Reconstruct BTC HIGH_VOL state (BTC-native parameters)
- Validate BTC onset predictability (walk-forward Cox PH on BTC)
- Compute BTC forward RV forecast
- Falsification gate: C-index ≤ 0.55 → STOP

Authorization:
PLANNED — NOT STARTED

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_IC2_CryptoVol_Transfer_Methodology.md (NEW)
- reports/APEX_IC2_Transfer_Approach_Scoring.csv (NEW)
- reports/APEX_IC2_Instrument_Data_Requirements.md (NEW)
- reports/APEX_IC2_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
