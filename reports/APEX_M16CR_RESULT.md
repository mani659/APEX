Milestone: M16-CR
Status: COMPLETE

Mathematical redundancy finding: Breakout Intensity and Regime Depth are mathematically collinear (r=0.9886) because they normalize the exact same RV20 value by percentiles derived from the exact same trailing 252-day distribution. They differ only by a slow-moving scalar.

Scientific meaning of Breakout Intensity: The magnitude by which variance exceeded the exact activation threshold at onset.
Scientific meaning of Regime Depth: The magnitude of variance relative to the historical baseline median.

Variance Momentum assessment: Distinct. It measures recent trajectory and acceleration, not absolute level. Retained.

Can both coexist?: No. Inclusion of perfectly proportional variables causes extreme multicollinearity, destabilizing the Cox PH partial likelihood estimation and preventing matrix inversion.

Final predictor decision: Resolution B. Formally remove Regime Depth. Retain Breakout Intensity.

Impact on Cox PH: Resolves the singular matrix threat, allowing the 2-feature model to fit smoothly on the 397 training observations.

Predictive-null decision: C-index <= 0.50 remains scientifically and mathematically sound.

Exact M17 prerequisites:
- Run `pip install lifelines`
- Extract 794 episodes
- Construct ONLY Breakout Intensity and Variance Momentum
- Run Walk-Forward expanding window starting at 397 training events
- Compute aggregated Out-of-Sample C-index

Gate decision: PREDICTOR AMENDMENT APPROVED — M17 PENDING

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- docs/APEX_M15_PREDICTOR_AMENDMENT.md (NEW)
- reports/APEX_M16CR_Control_Review.md (NEW)
- reports/APEX_M16CR_Predictor_Decision.md (NEW)
- reports/APEX_M16CR_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
