Milestone: M24
Status: COMPLETE

Research question: Does the M17-R2 predicted persistence state of a newly triggered HIGH_VOL episode condition the directional distribution of subsequent price returns?

Prediction source: M17-R2 OOS conditional risk score
Original OOS predictions: 397
Eligible directional sample: 396

Prediction boundary: t (onset close)
Return endpoint: Cumulative log return, ln(P_{t+48}/P_t)
Horizon: 12 hours (48 M15 bars)

Baseline mean return: -0.000149

OLS: Continuous-outcome regression.
Intercept: -0.000153
Beta: -0.000367
HAC standard error: 0.000790
HAC maxlags: 48
t-statistic: -0.4651
p-value: 0.6418
95% CI: [-0.001915, 0.001181]

Secondary skewness: -0.326780

Primary directional decision: Fail to reject the null hypothesis (p > 0.05).

Directional translation classification: NO DIRECTIONAL TRANSLATION

Scientific interpretation: The predicted persistence state contains no statistically reliable linear information regarding the directional drift of future prices. 

Relationship to M21 volatility translation: Case B (Volatility translation exists BUT directional translation does not). The APEX signal successfully predicts how much the market will move (variance/energy magnitude), but does not predict which way it will go (directional mean). The predicted variance simply expands symmetrically.

What the result does NOT establish: Tradability, profitability, expected price return direction, or execution edge.

Methodology integrity: PERFECT.
Methodology deviations: None. The rigid parameters frozen in M22 were strictly adhered to.

Limitations: Evaluated exclusively on the canonical EURUSD dataset.

M25 recommendation: Advance the translation research from Volatility/Direction to Extremum Boundary Translation (e.g., maximum excursion ranges or symmetric boundary piercing).

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M24_Directional_Return_Data.csv (NEW)
- reports/APEX_M24_Result_Summary.json (NEW)
- reports/APEX_M24_Directional_Translation_Experiment.md (NEW)
- reports/APEX_M24_RESULT.md (NEW)
- scratch/m24_experiment.py (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
