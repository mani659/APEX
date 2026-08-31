Milestone: IC7
Status: COMPLETE

Economic hypothesis:
  At timestamps where predicted_RV > IV, mean net straddle PnL > 0
  after frozen option costs

Eligible observations: 343
Conditional (predicted_RV > IV): 267

Primary condition:
  predicted_RV (annualized, %) > IV (annualized, %)

Predicted-RV summary:
  Mean: 62.61% (annualized)
  Std: 1.90%
  OOS correlation with actual 12h RV: 0.1814

IV summary:
  Mean: 54.95% (annualized)
  Std: 14.19%

RV-IV summary:
  Mean spread: +7.66 percentage points
  Fraction positive: 77.8%

Straddle premium:
  Mean (BTC): 0.01914
  Mean (USD): $1,209

Gross payoff:
  Mean: $1,113

Transaction costs:
  Mean: $103

Net PnL:
  Mean (all): -$199
  Median (all): -$334
  Hit rate (all): 32.9%

Baseline PnL:
  Mean: -$199
  Hit rate: 32.9%

Mean net PnL (conditional): -$130
Median net PnL (conditional): -$312
Std net PnL (conditional): $1,076
Positive-PnL fraction (conditional): 33.7%

One-sample HAC t-statistic: -1.6720
HAC SE: 77.58
p-value (one-sided): 0.9527
95% CI: [-$282, +$22]

Primary decision:
  NO ECONOMIC EDGE

  Gate A (N >= 100): PASS (267)
  Gate B (mean > 0): FAIL (-$130)
  Gate C (> baseline): PASS (-130 > -199)
  Gate D (p < 0.05): FAIL (p = 0.953)

Economic interpretation:
  The APEX volatility forecast partially identifies timestamps where the
  volatility risk premium is smaller (conditional mean loss is 35% less
  than unconditional). However, the straddle remains unprofitable on
  average because BTC option IV systematically exceeds realized volatility.
  The forecast is not strong enough to produce positive straddle expectancy.

Maturity limitation:
  TTE [12h,24h] is wider than IC3 12h prediction horizon. This makes
  the test conservative but does not affect the negative conclusion.

What IC7 establishes:
  1. BTC volatility risk premium is real and large (IV > RV on average)
  2. APEX signal has predictive content (r=0.18) and partially identifies
     when the premium is smaller
  3. Signal is not strong enough for positive straddle expectancy
  4. Long straddle is not the right instrument for this signal

What IC7 does NOT establish:
  1. Whether short straddle (selling vol) when predicted_RV < IV works
  2. Whether volatility spread strategies work
  3. Whether strike optimization helps
  4. Whether risk-adjusted returns are positive

Methodology deviations:
  Entry price: Black-76 from IV with strike-as-forward (~10-15% overstatement)
  IV source: trade-derived (approved by IC6-R3-CR)
  Maturity: [12h,24h] (approved by IC6-R2-CR)
  Freshness: <= 1h (restored by IC6-R3)

IC8 recommendation:
  STOP the long-straddle path. The economic mechanism (predicted RV > IV
  -> positive straddle payoff) is falsified by the data. Consider:
  - Whether the APEX signal could work as a short-vol indicator
  - Whether a volatility spread (relative value) would capture the signal
  - Whether the research should pivot to a different economic mechanism

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
  scripts/ic7_btc_straddle_experiment.py (NEW)
  reports/APEX_IC7_BTC_Straddle_Economic_Data.csv (NEW, 343 rows)
  reports/APEX_IC7_BTC_Straddle_Economic_Experiment.md (NEW)
  reports/APEX_IC7_RESULT.md (NEW)
  reports/APEX_IC7_Result_Summary.json (NEW)
  docs/APEX_SESSION_HANDOFF.md (MODIFIED)
  docs/APEX_SESSION_STATE.json (MODIFIED)
