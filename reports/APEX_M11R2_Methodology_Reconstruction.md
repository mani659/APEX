# APEX M11-R2 Methodology Reconstruction

## 1. Supersession of M11
The original M11 methodology contained fatal lookahead flaws (global RV20 threshold calculation), arbitrary falsification metrics (2-bar minimum), and a fatal macro-confounding blocker during the NY overlap. M11-R2 supersedes it completely.

## 2. Revised Scientific Question
**Primary:** Does the onset of a HIGH_VOL state have a systematically different duration (persistence) when triggered by the endogenous institutional liquidity transition of `ASIA_TO_LONDON`, compared to off-peak onset?

*Methodological Pivot*: By restricting the primary exposure strictly to the `ASIA_TO_LONDON` transition (07:00-09:00 UTC) and dropping `LONDON_NY_OVERLAP`, we elegantly bypass the fatal US macro-event confounder (NFP, CPI, FOMC), which exclusively contaminates the NY transition.

## 3. Revised HIGH_VOL Methodology (Lookahead Eliminated)
- **Rule (Option C)**: Rolling historical reference. The 80th percentile threshold for bar `t` is calculated using the trailing 252 trading days (approx. 1 calendar year) of RV20 data ending at `t-1`.
- **Justification**: Eliminates future information leakage. The 80th percentile is retained as a valid representation of the right-tail volatility quintile, structurally freezing the RC012 definition.

## 4. Session/DST Treatment
- **Rule**: `ASIA_TO_LONDON` is defined by fixed UTC proxies (07:00-09:00 UTC).
- **Justification**: Since exact historical local-time DST shifts are unavailable in the canonical data, we accept this as a `DST ACCEPTABLE LIMITATION`. The 1-hour noise during mismatched daylight saving weeks is treated as unmodeled structural variance over the 5.5-year sample.

## 5. Macro-Event Treatment
- **Rule**: Do not exclude macro events, but restrict the primary exposure cohort to `ASIA_TO_LONDON`.
- **Justification**: US macro events (which cause the largest exogenous shocks) do not occur during the Asian-European transition. This redesign isolates the endogenous structural transition without requiring external economic calendar data.

## 6. Primary Endpoint
- **Endpoint**: Persistence (Survival Time).
- **Definition**: The number of contiguous M15 bars from episode onset until termination.

## 7. Dependence, Overlap, and Episode Construction
*The arbitrary 12-bar separation rule is removed and replaced with a structural state-transition rule.*
- **Onset**: RV20 crosses above the rolling 80th percentile threshold.
- **Termination**: RV20 crosses below the rolling 80th percentile threshold.
- **Regime Reset (Dependence Control)**: A new episode cannot trigger until RV20 has fully mean-reverted by crossing below the trailing 50th percentile (median). Any spikes above the 80th percentile before a reset are clustered into the original episode.

## 8. Control Construction
- **Control Cohort**: HIGH_VOL episodes whose onset occurs between 20:00 UTC and 06:00 UTC (the structurally quiet Asian session and late NY session). 
- **Justification**: Cleanly isolates off-peak, non-transitional volatility expansion.

## 9. Statistical & Falsification Framework
- **Test**: Kaplan-Meier survival analysis with a Log-rank test.
- **Effect Estimate**: Median survival time difference and its 95% Confidence Interval.
- **Falsification Rule**: 
  - *Supported*: Log-rank p < 0.05 AND the 95% CI for the median duration difference excludes zero.
  - *Not Supported*: Log-rank p ≥ 0.05 OR the 95% CI includes zero.
  - *Arbitrary thresholds removed*: The ≥ 2-bar requirement is discarded in favor of pure interval estimation of the effect size.

## 10. Robustness Checks
- Compare the primary `ASIA_TO_LONDON` results against the explicitly confounded `LONDON_NY_OVERLAP` cohort to quantify the magnitude of the US macro-shock distortion.

## 11. M12R2 Revalidation Requirements
M12R2 must empirically validate:
1. The rolling 252-day RV20 threshold calculation (requires an initial 1-year warm-up period).
2. The revised event counts using the Regime Reset separation rule.
3. The sample sizes of the new `ASIA_TO_LONDON` exposure cohort and the `20:00-06:00 UTC` control cohort.
