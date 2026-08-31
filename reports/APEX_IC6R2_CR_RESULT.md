Milestone: IC6-R2-CR
Status: COMPLETE

IC5 economic quantity:
  Predicted: 12h forward BTC realized volatility (from walk-forward OLS of IC3 risk score)
  Observed: contemporaneous ATM option IV with maturity matching the12h forecast horizon
  Mechanism: predicted RV > IV -> long straddle -> positive expected payoff

IC6-R2 observation quantity:
  Predicted: same (correct API fetch, correct data)
  Observed: ATM option IV from WRONG maturity (mean TTE error 307.4h; 57.3% errors >=100h)
  Mechanism: INVALID — comparing12h forecast with IV from options expiring weeks/months later

Amendment classification:

  Maturity [6h,18h] -> [6h,72h]:
    Classification: ESTIMAND CHANGED
    Decision: NOT APPROVED
    Corrected rule: [12h, 24h] (nearest daily expiry only)

  IV source: BBO midpoint -> trade precomputed IV:
    Classification: OPERATIONAL
    Decision: APPROVED (same Black-76 model)

  Freshness: <= 1h -> unbounded (hardcoded True):
    Classification: OBSERVATION-PROCESS CHANGE
    Decision: NOT APPROVED
    Corrected rule: trade timestamp within 1h of prediction timestamp

  TTE computation bug:
    Classification: FATAL IMPLEMENTATION BUG
    Decision: INVALIDATES IC6-R2 ELIGIBILITY RESULTS

Timestamp directionality:
  API query window: [ts-24h, ts] — NO LOOKAHEAD in data fetching
  TTE computation: WRONG reference timestamp (batch scoping bug)
  Net: data is temporally valid but maturity selection is wrong

Strike integrity:
  Source: index_price from trade record (correct, available at trade time)
  Rule: nearest strike to index price (deterministic)
  Status: CORRECT — not affected by TTE bug

Call/put joint observation:
  Check: both legs exist for same strike and expiry within query window
  Issue: legs may not be truly contemporaneous (different timestamps within 24h window)
  Status: ACCEPTABLE with freshness correction

Eligibility saturation assessment:
  Progression was driven by maturity expansion + TTE bug, not outcome selection
  The N=100 gate was passed while measuring the wrong economic quantity
  Status: INVALIDATED

Economic-estimand preservation:
  Amendment A (maturity): NO — different economic quantity
  Amendment B (IV source): YES — same economic quantity
  Amendment C (freshness): WEAKLY — same but weaker
  TTE bug: NO — wrong instruments entirely
  Overall: IC6-R2 DOES NOT preserve the IC5 economic quantity

Primary control decision:
  C — REJECT IC6-R2
  Reason: TTE computation bug invalidates eligibility results

IC7 status:
  BLOCKED

Required next milestone:
  IC6-R3 — Corrected BTC Options Data Validation
  Must fix TTE bug, apply [12h,24h] maturity, apply 1h freshness

Required methodology amendment:
  NONE — original IC5 methodology remains frozen

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
  reports/APEX_IC6R2_CR_Observation_Architecture_Review.md (NEW)
  reports/APEX_IC6R2_CR_Methodology_Amendment_Decision.md (NEW)
  reports/APEX_IC6R2_CR_RESULT.md (NEW)
  docs/APEX_SESSION_HANDOFF.md (MODIFIED)
  docs/APEX_SESSION_STATE.json (MODIFIED)
