Milestone: IC7-CR
Status: COMPLETE

Sample lineage:
  IC5: methodology design only (no population)
  IC6-R2: 827 timestamps, 117 eligible (INVALID — TTE bug)
  IC6-R3: 827 timestamps, 343 eligible (VALID — bugs fixed)
  IC7: 343 observations (maps 1:1 to IC6-R3)
  117→343 reconciliation: TTE scoping bug fix + call/put joint-check fix + maturity window correction; 72 IC6-R2-eligible dropped (wrong instruments), 298 new (correct instruments found)

H1 prediction hypothesis:
  Status: SUPPORTED (r=0.1814 OOS, 77.8% of timestamps have predicted_RV > IV)
  IC7 does not test H1 directly

H2 pricing hypothesis:
  Status: PARTIALLY SUPPORTED but INSUFFICIENT
  APEX identifies timestamps where VRP is 35% smaller (conditional loss $130 vs unconditional $199)
  But VRP remains positive: IV > RV on average even in favorable conditions

H3 trading hypothesis:
  Status: REJECTED
  Mean conditional net PnL = -$130 (negative)
  p = 0.953 (far above 0.05)
  Long straddle loses money even when model predicts elevated volatility

Entry-premium implementation:
  IC5: BBO midpoint (bid+ask)/2
  IC7: Black-76 from trade-derived IV with F=K (strike-as-forward)
  Classification: MINOR IMPLEMENTATION LIMITATION
  Impact: overstates premium by ~10-15%, makes PnL more negative (conservative)

PnL scaling:
  Status: PASS — internally consistent, matches IC5 frozen cost model

Conditional sample definition:
  Status: PASS — pre-registered in IC5 Section 8
  Condition: forecast_IV_spread > 0 (predicted_RV > IV)
  N = 267 / 343

Baseline interpretation:
  IC7 reports "35% better than baseline"
  IC5 does NOT freeze a formal baseline comparison test
  Classification: DESCRIPTIVE ONLY — not statistical improvement

Maturity interpretation:
  IC7 says "robust to maturity limitation"
  No alternative maturity was tested
  Correct: "IC7 failed under [12h,24h]; robustness not tested"

Statistical interpretation:
  Status: PASS — correct implementation of IC5 frozen test
  t = -1.672, p = 0.953, failure to reject H0

IC7 validity:
  VALID — faithful implementation of approved methodology

Long-straddle mechanism:
  REJECTED — falsified by IC7

Alternative mechanisms:
  NOT AUTHORIZED — short straddle and volatility spread require separate frozen methodology

Crypto-options path:
  OPEN BUT FROZEN — long-straddle closed; new mechanism requires IC7-CR Stop Rule compliance

IC8 status:
  BLOCKED — no alternative mechanism proposed or validated

Required future action:
  Control session decides: (a) close crypto-options path entirely, or (b) accept a new mechanism proposal that passes the Stop Rule

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
  reports/APEX_IC7CR_Economic_Result_Integrity.md (NEW)
  reports/APEX_IC7CR_Decision.md (NEW)
  reports/APEX_IC7CR_RESULT.md (NEW)
  docs/APEX_SESSION_HANDOFF.md (MODIFIED)
  docs/APEX_SESSION_STATE.json (MODIFIED)
