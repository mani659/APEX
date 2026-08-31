# APEX M11-BACKUP: Unconditional HIGH_VOL Methodology Design

## 1. Scientific Objective
Determine the unconditional lifecycle of the validated `HIGH_VOL` distributional state (RV20 > 80th percentile) after onset. The study will quantify the persistence, decay, and survival function of this variance-expansion regime without session conditioning.

## 2. Reused Infrastructure (Lookahead-Free)
The methodology structurally reuses the causal infrastructure validated in M12R2:
- **Base Metric**: EURUSD M15 RV20 (20-period standard deviation of log returns).
- **HIGH_VOL Threshold**: The rolling 80th percentile of RV20, computed over a trailing 252-trading-day window (24,192 M15 bars), ending strictly at `t-1`.
- **Regime Reset Threshold**: The rolling 50th percentile (median) of RV20, using the identical 252-day trailing window.

## 3. Episode Lifecycle Definition
The lifecycle is defined sequentially and causally:
- **Onset**: The first M15 bar where RV20 crosses above the 80th percentile, provided the regime is currently in a "Reset" state.
- **Termination**: The first subsequent M15 bar where RV20 falls below the 80th percentile.
- **Regime Reset**: Following termination, the system is blocked from triggering a new episode until RV20 drops below the 50th percentile. Any volatility spikes above the 80th percentile before a full reset are considered structurally part of the same volatility cluster and do not trigger a new onset.
- **Censoring**: If the dataset ends while an episode is active, the episode is right-censored.

## 4. Primary Endpoint
**Persistence Duration**: The number of consecutive M15 bars from onset to termination.

## 5. Statistical Framework
Because episodes vary in length and can be right-censored, the study will utilize **Survival Analysis**.
- **Estimator**: Kaplan-Meier survival curve for the empirical persistence duration.
- **Secondary Descriptors**: Median survival time, 75th and 90th percentile durations, and the empirical hazard function (to assess whether the probability of decay accelerates or decelerates over time).

## 6. Null Model
**Memoryless Markov Baseline (Geometric Distribution)**
- **Definition**: If `HIGH_VOL` is merely a threshold-crossing process with no structural "lifecycle" or memory, the probability of exiting the state at any bar should be constant. The persistence durations under this null follow a geometric distribution.
- **Construction**: The parameter $p$ (exit probability) is estimated as the total number of terminations divided by the total number of bars spent in the `HIGH_VOL` state across all episodes. The null survival function is then generated from this geometric distribution.

## 7. Falsification Framework
- **Null Hypothesis ($H_0$)**: The empirical survival function of `HIGH_VOL` persistence is statistically indistinguishable from the memoryless Markov baseline.
- **Alternative Hypothesis ($H_A$)**: `HIGH_VOL` episodes exhibit a structural lifecycle (e.g., initial lock-in momentum or complex decay) resulting in a survival function that deviates significantly from the memoryless null.
- **Test**: A Kolmogorov-Smirnov (K-S) test or Anderson-Darling test comparing the empirical distribution to the fitted geometric null distribution.
- **Supported**: Test yields `p < 0.05`, and the empirical median survival significantly exceeds the null median.
- **Not Supported**: The empirical distribution conforms to the null, implying `HIGH_VOL` has no intrinsic lifecycle beyond a memoryless threshold excursion.

## 8. Robustness Checks
1. **Subperiod Stability**: Split the 4.5-year usable dataset into two halves to confirm the survival function shape is stable across distinct macro regimes.
2. **Alternative Reset Threshold**: Test sensitivity by defining the Regime Reset at the 60th percentile instead of the 50th.

## 9. M12-Backup Validation Requirements
M12-Backup must verify:
- The causal construction of the rolling thresholds over the full dataset.
- The correct application of the Regime Reset rule.
- The total number of valid episodes (expected to match the 794 robust events found in M12R2).
- The feasibility of computing the Markov Baseline parameter $p$.
