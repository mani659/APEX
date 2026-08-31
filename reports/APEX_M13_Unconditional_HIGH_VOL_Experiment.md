# APEX M13: Unconditional HIGH_VOL Structural Memory Experiment

## 1. Research Question
**Does the unconditional HIGH_VOL persistence distribution contain structural memory beyond a memoryless geometric threshold-crossing process?**
- **Null Hypothesis**: HIGH_VOL persistence follows a memoryless geometric process (structural amnesia).
- **Alternative Hypothesis**: HIGH_VOL persistence differs systematically from the memoryless process, demonstrating structural memory.

## 2. Frozen Methodology
The experiment strictly adhered to the `APEX_M11BACKUP_FROZEN_METHODOLOGY.md` and its Parametric Monte Carlo `APEX_M11BACKUP_STATISTICAL_AMENDMENT.md` without deviation.

## 3. Dataset & Sample Construction
- **Dataset**: Canonical EURUSD M1 data resampled to M15 (136,787 bars).
- **Threshold**: Rolling 252-trading-day 80th percentile of RV20.
- **Reset Rule**: 50th percentile of RV20.
- **Coverage**: The resulting causal extraction yielded exactly **794 discrete `HIGH_VOL` episodes**.

## 4. Episode Statistics (Observed Persistence)
- **Total Eligible Episodes**: 794
- **Completed**: 794
- **Censored**: 0
- **Minimum Duration**: 1 bar
- **Median Duration**: 20.0 bars
- **75th Percentile**: 29.0 bars
- **90th Percentile**: 47.0 bars
- **Maximum Duration**: 168 bars

## 5. Null Parameterization
- **Estimator**: $\hat{p} = \frac{\text{Terminations}}{\text{Total HIGH\_VOL bars}}$ = 794 / 17,456
- **Fitted Exit Probability ($\hat{p}$)**: 0.04549
- **Null Expected Duration ($1/\hat{p}$)**: 21.98 bars

## 6. Observed Test Statistic
- **Statistic**: $D_{obs} = \sup |F_{emp}(d) - F_{null}(d)|$
- **Value**: **$D_{obs} = 0.19270$**

## 7. Monte Carlo Calibration
- **Simulations**: 10,000 (Seed = 42)
- **Procedure**: For each replicate, $n=794$ variables were sampled using $\hat{p}=0.04549$, $\hat{p}_{sim}$ was re-estimated, and $D_{sim}$ was computed to construct the exact discrete null distribution.
- **Result**: Exactly **0** out of 10,000 simulations produced a $D_{sim} \geq 0.19270$.
- **Final p-value**: **0.00000**

## 8. Primary Statistical Decision
**REJECT MEMORYLESS NULL.**
The probability of observing a CDF distance of 0.19270 under a true geometric memoryless process is functionally zero (p < 0.0001). The empirical distribution is statistically inconsistent with structural amnesia.

## 9. Structural Interpretation & Effects
The unconditional `HIGH_VOL` state definitively possesses structural memory. While the empirical median (20.0 bars) is slightly shorter than the geometric expectation (21.98 bars), the massive CDF distance implies a complex hazard shape (e.g., a mix of rapidly decaying false-starts and a highly persistent fat tail) that categorically violates a constant memoryless exit rate. The state has an intrinsic, non-random lifecycle.

## 10. Methodology Deviation Audit
- Threshold: Unchanged
- Reference period: Unchanged
- Reset rule: Unchanged
- Event definition: Unchanged
- Test statistic: Unchanged (K-S)
- MC count: Unchanged (10,000)
- Seed: Unchanged (42)
**Result**: Methodology integrity is strictly pristine.

## 11. What this result does NOT establish
This result **does not** establish predictability, economic tradability, positive expectancy, or trading strategy viability. It purely establishes that the volatility expansion phase has structural memory distinct from a random walk.

## 12. M14 Recommendation
M14 Scientific Adjudication must determine whether this proven structural memory constitutes a sufficiently exploitable anomaly to warrant designing an economic prediction model, or whether the descriptive finding concludes the APEX hypothesis tree.
