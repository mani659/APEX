# APEX M12R2 Pre-Economic Data Validation

## 1. Objective
To execute a strict observability and data-integrity gate on the frozen M11-R2 methodology, verifying the rolling 252-day lookahead-free reference, the Regime Reset separation rule, and the revised `ASIA_TO_LONDON` exposure construct, prior to any economic testing.

## 2. 252-Day Lookahead Audit
- **Rule Tested**: 252 trading days = 24,192 M15 bars (assuming ~96 bars per day).
- **Implementation Audit**: The calculation of the 80th and 50th percentiles used a rolling `min_periods=12096` and `window=24192`, explicitly shifted by 1 bar (`rv20_lag1`). 
- **Finding**: **PASS**. Information leakage is completely sealed. Thresholds at bar `t` rely strictly on `[t-24192, t-1]`.

## 3. Regime Reset Audit
- **Rule Tested**: An episode initiates on crossing the 80th percentile and cannot restart until RV20 mean-reverts below the 50th percentile.
- **Implementation Audit**: The logic was implemented sequentially, passing chronologically through the data array without backward assignment.
- **Finding**: **PASS**. The reset logic is causal and deterministic. However, structurally, it causes massive clustering of volatility—shocks that would have been multiple events under the old 12-bar rule are absorbed into massive single multi-day episodes.

## 4. Exposure and Control Observability
- **Exposure (`07:00-09:00 UTC`)**: Deterministic and mutually exclusive.
- **Control (`20:00-06:00 UTC`)**: Deterministic and mutually exclusive (0 overlaps found).
- **Finding**: **PASS**.

## 5. Sample Sufficiency & Attrition (FATAL BLOCKER)
- Total eligible HIGH_VOL episodes in 4.5 years (after 1-year warm-up): **794**
- Exposure (ASIA_TO_LONDON) episodes: **8**
- Control (Off-Peak) episodes: **80**
- **Finding**: **BLOCKED**. The combination of the strict Regime Reset rule (which massively limits total discrete episodes) and the narrow 2-hour `ASIA_TO_LONDON` onset window resulted in near-total attrition of the exposure cohort. A sample size of `n=8` is statistically unviable for robust Kaplan-Meier survival inference.

## 6. Persistence & Censoring Feasibility
- **Finding**: **PASS**. Endpoints (survival duration) and right-censoring at the end of the dataset are mathematically sound and observable.

## 7. DST & Macro-Event Independence
- **DST**: The fixed UTC proxy functions deterministically, confirming its status as a documented limitation.
- **Macro-Event Independence**: Restricting to `ASIA_TO_LONDON` successfully removed the dependency on an external NFP/CPI calendar.

## 8. Statistical Feasibility
- **Kaplan-Meier & Log-rank Test**: **BLOCKED**. While mathematically computable, computing a survival difference and p-value on an exposure group of `n=8` has effectively zero statistical power and massive variance. The test would be scientifically meaningless.

## 9. Gate Decision
**BLOCKED — DATA / OBSERVABILITY**

**Reason**: Severe sample insufficiency. The structural rigor introduced in M11-R2 (specifically the Regime Reset rule combined with a strict 2-hour exposure window) successfully eliminated lookahead and macro-confounding but mathematically choked the eligible exposure sample to 8 observations. M13 cannot proceed with an unviable sample.
