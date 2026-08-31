Milestone: IC8
Status: COMPLETE

IC7 status: VALID — LONG-STRADDLE MECHANISM REJECTED

What IC7 falsified: predicted_RV > IV → positive expected long-straddle PnL (mean conditional PnL = -$130, p = 0.953)

What remains economically valid:
  - BTC volatility prediction has predictive content (r = 0.18 OOS)
  - BTC options exhibit a large, persistent volatility risk premium (IV > RV)
  - APEX partially identifies when the VRP is smaller (descriptive)
  - Signal is not strong enough for option-based monetization

Candidate A (Short Volatility): SAME MECHANISM — REJECT (score 23/50)
  Classification: Mirror image of IC7; APEX signal is directionally wrong for short vol
  VRP capture is general, not APEX-specific
  Shorting vol during elevated-vol periods (when APEX fires) is mechanically dangerous

Candidate B (Term-Structure): DISTINCT IN PRINCIPLE — FAILS ON INFORMATION (score 25/50)
  Classification: Requires second predictive leg (term structure shape) that APEX does not possess
  APEX predicts absolute RV magnitude, not relative maturity pricing
  New research program required — outside IC8 scope

Candidate C (Cross-Instrument): REJECT — REOPENS RC014 (score 14/50)
  Classification: Requires new cross-asset transmission hypothesis
  RC014 already falsified transmission channel for tested relationships
  Would require entirely new data chain and validation

Candidate D (Non-Option Vol): DISTINCT IN PRINCIPLE — FAILS ON FEASIBILITY (score 17/50)
  Classification: No liquid tradeable BTC volatility future with historical data exists
  BTC variance swaps are OTC and illiquid
  Instrument infeasibility prevents testing

Candidate E (STOP): ACCEPTED
  No genuinely distinct economic mechanism survives IC8
  Crypto-options path reaches scientifically justified stopping point

Candidate scorecard: All candidates below 35/50 threshold
  A: 23/50 | B: 25/50 | C: 14/50 | D: 17/50

Short-straddle classification: SAME MECHANISM AS IC7 — DIRECTIONALLY WRONG FOR APEX SIGNAL
  "Long straddle failed → therefore short straddle" is logically invalid
  APEX predicts elevated vol; shorting vol when vol is elevated is the wrong trade

Relative-value classification: REQUIRES UNVALIDATED SECOND PREDICTIVE LEG
  APEX has one validated signal (absolute RV magnitude)
  Term-structure trade requires second signal (relative maturity pricing)
  No second signal exists or has been validated

Top surviving mechanism: NONE

Why no mechanism survives: Information-instrument mismatch
  APEX knows WHEN vol is elevated (timing/magnitude prediction)
  Options market prices vol LEVEL (already incorporates the elevation)
  The gap cannot be bridged without new predictive research

Why genuinely distinct from IC7: N/A — no mechanism survives

Economic mechanism: N/A

Required future inputs: New predictive model for vol surface dynamics, OR new instrument class, OR non-options-based mechanism

Major risks: None — path is closed

Decision: C — CRYPTO-OPTIONS PATH CLOSED

Next authorized milestone: NONE
  Recommend: return to broader APEX economic-mechanism discovery
  when new instrument classes or predictive models become available

Authorization: NO NEXT MILESTONE AUTHORIZED

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
  reports/APEX_IC8_Economic_Mechanism_Discovery.md (NEW)
  reports/APEX_IC8_Economic_Mechanism_Scoring.csv (NEW)
  reports/APEX_IC8_RESULT.md (NEW)
  docs/APEX_SESSION_HANDOFF.md (MODIFIED)
  docs/APEX_SESSION_STATE.json (MODIFIED)
