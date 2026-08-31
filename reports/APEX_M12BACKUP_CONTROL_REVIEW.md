# APEX M12-BACKUP Control Review: Discrete Null Statistical Adjudication

## 1. Objective
To adjudicate the `BLOCKED — METHODOLOGY` gate failure reported by M12-BACKUP, specifically the flaw regarding the continuous K-S test applied to discrete, parameter-estimated survival data.

## 2. Geometric Null Parameter Audit
- **Bar-level exit probability**: The parameter $p$ represents the probability of transitioning from `HIGH_VOL` back to baseline on any given M15 bar.
- **Episode-duration distribution**: Under a memoryless process, the duration $D$ follows a geometric distribution $P(D=d) = (1-p)^{d-1}p$.
- **Estimator Consistency**: The formula $\hat{p} = \frac{\text{Terminations}}{\text{Total HIGH\_VOL bars}}$ is the exact Maximum Likelihood Estimator (MLE) for the geometric distribution. It is perfectly internally consistent and robust to censoring (since censored bars correctly inflate the denominator without adding to the numerator).

## 3. Parameter Estimation Problem
Because $p$ is estimated from the observed sample rather than known a priori, the standard K-S statistic does not follow the asymptotic Kolmogorov distribution. This is a classic "Lilliefors" problem. Using a standard table or software function will result in highly conservative, invalid p-values, making it nearly impossible to reject the null even if structural memory exists.

## 4. Discreteness Issue
The Kolmogorov distribution assumes a continuous CDF. Because our duration data is strictly discrete (integer M15 bars), this further invalidates standard K-S critical values.

## 5. Candidate Method Comparison
- **Option A (Exact discrete goodness-of-fit)**: Infeasible analytically due to the estimated parameter.
- **Option B (Parametric Monte Carlo Bootstrap)**: Simulates the exact fitted null computationally, automatically accounting for both discreteness and parameter estimation.
- **Option C (Discrete CDF-distance with Monte Carlo Calibration)**: Retains the robust K-S distance metric ($D_{obs}$) but calibrates its exact p-value using the parametric bootstrap from Option B.
- **Decision**: **Option C** is the most rigorous, scientifically appropriate, and reproducible method. It perfectly preserves the original research intent while correcting the mathematical flaw.

## 6. Censoring Implication
M12-BACKUP established exactly 0 right-censored episodes out of 794. Therefore, the Monte Carlo simulation can safely model completely observed geometric random variables. The parameter $\hat{p}$ structurally accounts for censoring if it occurs in future sets, but for the current M13 dataset, it is irrelevant.

## 7. Dependence Assumption
M12-BACKUP noted episode independence is `PLAUSIBLE`. The Regime Reset rule enforces a return to the 50th percentile (median) baseline before a new episode can trigger. This structural separation effectively breaks volatility clustering across episodes, satisfying the conditional independence required for the Monte Carlo bootstrap.
