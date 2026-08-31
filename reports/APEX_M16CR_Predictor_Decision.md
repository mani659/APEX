# APEX M16-CR: Predictor Decision Matrix

## The Redundant Predictors
1. **Breakout Intensity**: $RV20_{onset} / Threshold80_{onset}$
   - *Scientific Meaning*: The magnitude by which the current variance exceeded the exact activation threshold at the moment the episode was structurally triggered.
2. **Regime Depth**: $RV20_{onset} / Threshold50_{onset}$
   - *Scientific Meaning*: The magnitude of the current variance relative to the long-term baseline median.

## Decision: Drop Regime Depth
- **Rationale**: Both variables are mathematically collinear (differing only by a slow-moving scale factor). They cannot coexist in the Cox PH model. We retain Breakout Intensity because the `HIGH_VOL` episode is mathematically defined into existence by the 80th percentile crossing. The intensity relative to that specific trigger boundary is conceptually more direct than the depth relative to the baseline reset boundary.
- **Independence**: This decision was made *ex ante* to predictive testing. No outcome data, p-values, or C-indices were calculated or consulted. The decision prevents a purely mechanical matrix inversion failure.

## Final Authorized Predictor Set for M17
1. `Breakout Intensity` ($RV20_{onset} / Threshold80_{onset}$)
2. `Variance Momentum` ($RV20_{onset} - RV20_{onset-4}$)
