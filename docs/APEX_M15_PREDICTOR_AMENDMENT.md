Original predictor set:
1. Breakout Intensity (RV20_onset / Threshold80_onset)
2. Variance Momentum (RV20_onset - RV20_onset-4)
3. Regime Depth (RV20_onset / Threshold50_onset)

Identified redundancy:
Breakout Intensity and Regime Depth are fundamentally collinear (r = 0.9886).

Mathematical basis:
Both Threshold80 and Threshold50 are derived from the exact same trailing 252-day distribution of RV20. The relationship is mathematically defined as:
Regime Depth = Breakout Intensity * (Threshold80 / Threshold50)
Because the ratio of the 80th to 50th percentile of a 252-day window changes extremely slowly, the two variables are nearly deterministically proportional.

Scientific interpretation:
While Breakout Intensity measures distance from the activation boundary and Regime Depth measures distance from the baseline median, both structurally encode the exact same fundamental concept: the contemporaneous level of variance normalized by the recent historical distribution.

Corrected predictor set:
1. Breakout Intensity (RV20_onset / Threshold80_onset)
2. Variance Momentum (RV20_onset - RV20_onset-4)
(Regime Depth is explicitly removed).

Why the correction is outcome-independent:
The decision to remove Regime Depth is based entirely on mathematical algebra and Cox model numerical stability (avoiding singular matrix inversion), without any calculation of target correlation, out-of-sample performance, or C-index optimization. Breakout Intensity was selected to remain because the episode is structurally triggered by the 80th percentile threshold, making it the most proximate boundary to measure from.

What remains unchanged:
- The target definition (survival duration)
- The Walk-Forward split structure
- The Cox PH model framework
- Variance Momentum (measures acceleration, not level, hence mathematically orthogonal)
- The primary metric (C-index)
- The predictive null (C <= 0.50)

New researcher degrees of freedom:
None. The predictor set is simply reduced from 3 to 2 deterministic variables.

How each is frozen:
The 2-variable set is permanently locked for M17.

M17 implementation requirements:
M17 must install the `lifelines` package, load the 794 validated events, construct the 2-variable predictor set, apply the walk-forward logic, and compute the out-of-sample C-index without further optimization.
