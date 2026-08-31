Milestone: IC5
Status: COMPLETE

Economic question:
Does the BTC-native APEX volatility forecast identify timestamps at which expected future realized volatility exceeds contemporaneous BTC option-implied volatility sufficiently to create positive expected value direction-neutral convex payoff after realistic option costs?

Validated inputs:
- IC3 BTC risk score (C-index = 0.6224, OOS)
- IC3 forward RV translation (p = 0.000011)
- IC4 frozen IV architecture (ATM Black-76, nearest TTE ∈ [6h, 18h])

Prediction source:
IC3 BTC-native OOS risk score (Cox PH linear predictor)

Predicted-RV representation:
Walk-forward OLS mapping: forward_RV = α + β × risk_score
Fitted on expanding historical window; evaluated OOS

IV representation:
ATM implied volatility from Black-76 inversion of midpoint (bid+ask)/2

Strike:
Nearest strike to BTC-PERPETUAL mark price at entry timestamp

Maturity:
Nearest expiry with TTE ∈ [6h, 18h]
Fallback: nearest TTE > 0 (flagged as maturity-mismatched)
Maximum mismatch: 24 hours
Interpolation: NOT permitted

Quote-quality rule:
Tier 1: fresh bid/ask, spread < 5 vol points (primary)
Tier 2: ≤ 1 hour staleness (acceptable)
Staleness threshold: 1 hour (60 minutes)

Primary payoff:
Long ATM straddle = long 1 ATM call + long 1 ATM put
Held to European expiry; cash-settled

Entry:
At IC3 onset timestamp
Entry premium = call_mid + put_mid
Entry fee = 0.04% × 2 legs × BTC price

Exit:
At option expiry
Exit value = max(F-K, 0) + max(K-F, 0)
Exit fee = 0.04% × 2 legs × BTC price (on settlement)

Cost model:
- Entry/exit bid/ask: implicit in midpoint entry
- Exchange fees: 0.04% taker × 4 leg-transactions
- Slippage: NOT modeled (acknowledged limitation)
- Funding/carry: NOT modeled (risk-free rate = 0)
- Theta/decay: captured by holding to expiry
- Total explicit cost: ~0.16% of notional per straddle

Primary baseline:
Unconditional ATM straddle (all eligible timestamps, not just HIGH_VOL onsets)

Primary null:
APEX-predicted volatility state does not improve expected net direction-neutral option payoff relative to unconditional baseline after frozen costs

Primary statistical framework:
One-sample t-test on conditional PnL series
H₀: E[net_PnL | forecast_IV_spread > 0] = 0
H₁: E[net_PnL | forecast_IV_spread > 0] > 0 (one-sided)
HAC: Newey-West, lag = 12
Alpha: 0.05

Eligibility:
All 10 criteria frozen (IC3 prediction, option data, ATM strike, bid/ask, freshness, maturity, spread, underlying price, Black-76 convergence, forward path)

Major risks:
- Data sparsity (IC6 gate: < 100 eligible observations → STOP)
- IV repricing before execution (medium risk)
- Cost underestimation (slippage not modeled)
- Early period liquidity (2021 options may be thin)

Data still required:
- BTC options historical data from Tardis/CryptoDataDownload (free, ~2-3 GB)
- IC6 must validate actual data observability before IC7

Decision:
CONTINUE

Next authorized milestone:
IC6 — BTC Options Data Validation

IC6 scope:
- Acquire BTC options historical data
- Validate actual quote coverage at IC3 prediction timestamps
- Verify eligibility criteria on real data
- Count eligible observations
- Do NOT calculate PnL

Authorization:
PLANNED — NOT STARTED

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_IC5_BTC_IV_RV_Economic_Methodology.md (NEW)
- reports/APEX_IC5_Economic_Methodology_Scoring.csv (NEW)
- reports/APEX_IC5_Economic_Risk_Register.csv (NEW)
- reports/APEX_IC5_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
