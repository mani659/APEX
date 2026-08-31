Milestone: IC6-R3-CR
Status: COMPLETE

IC5 economic quantity:
  Forecast 12h forward BTC realized volatility at t
  vs contemporaneously observable ATM option IV at t
  for option whose maturity approximates 12h horizon

IC6-R3 observed quantity:
  Forecast 12h forward BTC realized volatility at t
  vs trade-derived ATM option IV within 1h of t
  for option with TTE in [12h, 24h] (mean ~16.6h)
  Same strike, same expiry, call+put pair

Eligibility N: 343 (IC5 minimum: 100; PASS)

TTE: range [12.00h, 24.00h], mean 16.63h
  Concentrated in [15h, 18h] (46.9%)
  Consistent with BTC daily 08:00 UTC expiry

Freshness: trade age mean 5.8 min, max 53.0 min
  91.8% under 15 min
  All ≤ 1h
  All trades strictly before prediction timestamp

IV source:
  Deribit pre-computed Black-76 IV from trade price
  Uses BTC index price as underlying
  Trade-derived (not BBO midpoint)
  Standard approximation for liquid ATM options

Call/put timestamp alignment:
  Mean diff: 9.3 min
  Median diff: 5.2 min
  Max diff: 58.5 min
  All ≤ 1h
  92.1% ≤ 30 min
  80.5% ≤ 15 min

Strike integrity:
  Nearest to BTC-PERPETUAL index price from trade record
  Deterministic, no future information
  Same strike for both call and put

Maturity integrity:
  [12h, 24h] captures nearest daily expiry at 08:00 UTC
  Conservative: IV covers ~16.6h vs 12h prediction horizon
  Strengthens economic test

Cost-model consistency:
  0.04% taker × 4 legs (frozen)
  Compatible with trade-derived IV observation
  IC7 will use BBO midpoints for payoff construction

Amendment classification:
  Trade IV: OBSERVATION-PROCESS CHANGE
  TTE [12h,24h]: OBSERVATION-PROCESS CHANGE (conservative)
  1h freshness: OBSERVATION-PROCESS CHANGE (restored)
  All other components: OPERATIONAL

Primary decision:
  B — APPROVE IC7 WITH EXPLICIT LIMITATION

  Limitation: TTE [12h,24h] means IV covers ~16.6h, wider than
  IC3's 12h prediction horizon. This is conservative and must be
  documented in IC7 interpretation.

IC7 status:
  AUTHORIZED

Required methodology amendment:
  NONE — limitation is interpretive, not procedural

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
  reports/APEX_IC6R3_CR_Observation_Integrity_Review.md (NEW)
  reports/APEX_IC6R3_CR_Decision.md (NEW)
  reports/APEX_IC6R3_CR_RESULT.md (NEW)
  docs/APEX_SESSION_HANDOFF.md (MODIFIED)
  docs/APEX_SESSION_STATE.json (MODIFIED)
