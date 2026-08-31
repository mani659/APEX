# APEX M11-BACKUP FROZEN METHODOLOGY

This document defines the absolute, ex-ante frozen methodology for the Unconditional `HIGH_VOL` Lifecycle Experiment.

## 1. Scientific Objective
Characterize the unconditional lifecycle (persistence and decay) of the `HIGH_VOL` distributional state and determine whether it possesses structural memory beyond a random memoryless threshold excursion.

## 2. Thresholds & Primitives (Strictly Lookahead-Free)
- **Base Metric**: RV20 (20-period standard deviation of log returns on canonical EURUSD M15 data).
- **HIGH_VOL Threshold**: The rolling 80th percentile of RV20, computed over the trailing 252 trading days (24,192 M15 bars) ending at `t-1`.
- **Reset Threshold**: The rolling 50th percentile (median) of RV20 over the identical trailing window.

## 3. Episode Construction & Independence
- **Onset**: Bar `t` where RV20 crosses above the 80th percentile threshold, provided the system is in a "Reset" state.
- **Termination**: The first subsequent bar where RV20 crosses back below the 80th percentile.
- **Regime Reset (Dependence Control)**: The system enters a "Reset" state ONLY when RV20 crosses below the 50th percentile threshold. Successive bursts of volatility above the 80th percentile before a reset are clustered as a single structural regime.

## 4. Analytical Framework
- **Primary Endpoint**: Persistence (Duration in contiguous M15 bars from onset to termination).
- **Censoring**: Episodes active at the dataset boundary are right-censored.
- **Null Model**: Memoryless Markov Baseline. A geometric distribution with parameter $p$ equal to the global empirical exit rate (Total Terminations / Total Bars in HIGH_VOL state).
- **Statistical Test**: Kaplan-Meier non-parametric survival analysis compared against the Geometric Null via a Kolmogorov-Smirnov (K-S) test.

## 5. Falsification
- **Supported**: The K-S test yields `p < 0.05` AND the empirical survival curve demonstrates structural memory (e.g., non-constant hazard rate, or median survival exceeding the memoryless null).
- **Not Supported**: The empirical distribution conforms to the geometric null (`p >= 0.05`), proving `HIGH_VOL` has no intrinsic lifecycle memory.
