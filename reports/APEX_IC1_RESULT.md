Milestone: IC1
Status: COMPLETE

Current economic bottleneck:
No identified way to convert non-directional volatility prediction into bounded-risk profit using available instruments.

Validated information available:
- HIGH_VOL distributional primitive (RC012)
- HIGH_VOL persistence predictability (M17-R2, C-index=0.6656)
- Predicted persistence scales forward RV (M21, p=0.0032)
- Predicted persistence scales excursion envelope (M27, p=7.5e-05)
- Movement is direction-neutral (M24, M27 ratio=0.9218)
- LNO session has different return distribution (M39-R2, p=0.0001)
- Cross-asset transmission rejected (RC014)

Previously rejected economic paths:
- RC012 spot monetization (Studies 007-011): all architectures failed
- M31 static boundary: 99.75% saturation
- RC015 CME listed-option path: data/liquidity infeasible
- HIGH_VOL dynamic translation: rejected as methodologically weak (M33)

Candidate mechanisms:
A: Crypto Options Vol Monetization — HIGH PRIORITY (score=42/50)
B: Barrier/Range Products — REJECT (score=25/50, M31 saturation)
C: Relative-Value Volatility — REJECT (score=24/50, insufficient predictive legs)
D: Directional Instrument — REJECT (score=36/50, M24 eliminates direction)
E: EURUSD Options Fallback — LOW PRIORITY (score=28/50, data-constrained)

Candidate instruments:
Primary: BTC/ETH options on Deribit
Secondary: EURUSD options (if data becomes available)

Scorecard:
See reports/APEX_IC1_Instrument_Scorecard.csv

Top candidate:
A: Crypto Options Vol Monetization

Economic mechanism:
When M17-R2-style predicted realized volatility exceeds options-implied volatility,
long straddles/strangles capture the IV-RV spread as positive expected value
through convex payoff structure.

Instrument:
BTC options on Deribit (retail-accessible, ~85% market share, historical data since 2019)

Payoff structure:
Long straddle: max loss = premium; upside proportional to realized movement.
If predicted RV > IV, expected value = probability-weighted upside - premium - costs.

Why information may create value:
APEX predicts non-directional vol expansion (M21, M27). Convex instruments (straddles)
profit from exactly this. If the market does not fully price this predictability into
options premiums, expected value exists.

Why the mechanism may fail:
- HIGH_VOL has NOT been validated on BTC (unvalidated cross-asset assumption)
- IV typically exceeds RV by 5-15 vol points (high bar for RV > IV)
- Crypto vol dynamics may differ structurally from EURUSD
- Execution costs during volatile periods may erode edge

Required future data:
- BTC M1/M15 OHLCV data (available via Tardis, CryptoDataDownload)
- BTC Deribit options historical data (available since March 2019)
- BTC perpetual/futures funding rates (available via Deribit API)

Required future methodology:
- IC2: Cross-asset validation + frozen IV-RV divergence methodology
- IC3: Economic execution and validation

Rejected candidates:
- B: Barrier/Range products — M31 saturation already demonstrated failure
- C: Relative-value vol — Insufficient predictive information (only one leg)
- D: Directional instrument — M24 conclusively eliminated directional translation

STOP / CONTINUE decision:
CONTINUE — A credible economic mechanism and instrument exist.

Next authorized milestone:
IC2 — Economic Mechanism Methodology Design

Authorization status:
IC1 COMPLETE; IC2 REQUIRES CONTROL-SESSION AUTHORIZATION

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_IC1_Instrument_Feasibility_Survey.md (NEW)
- reports/APEX_IC1_Instrument_Scorecard.csv (NEW)
- reports/APEX_IC1_Economic_Mechanism_Ranking.md (NEW)
- reports/APEX_IC1_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
