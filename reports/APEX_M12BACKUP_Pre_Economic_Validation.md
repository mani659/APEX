# APEX M12-BACKUP: Unconditional HIGH_VOL Pre-Economic Validation

## 1. Objective
To independently verify the structural observability, causality, and statistical coherence of the frozen M11-Backup methodology prior to executing the M13 economic experiment.

## 2. Canonical Data Verification
- **Source**: Canonical EURUSD M1 dataset (`data/m1/EUR/EURUSD_*.csv`).
- **Resampling**: Deterministically resampled to M15.
- **Coverage**: 136,787 contiguous M15 observations (5.5 years).
- **Finding**: **PASS**. The dataset is continuous and sufficient for the required 1-year warm-up.

## 3. HIGH_VOL and Regime Reset Causal Audit
- **Rule Tested**: 80th percentile threshold and 50th percentile reset computed over a trailing 252-trading-day window (24,192 bars).
- **Causality Check**: The calculation explicitly enforces a `t-1` lag, meaning the threshold at `t` is defined entirely by data strictly before `t`. Future information (e.g., episode termination) is completely isolated from the onset definition.
- **Finding**: **PASS**. Lookahead is comprehensively sealed.

## 4. Episode Independence Assessment
- **Rule Tested**: A new episode cannot trigger until RV20 fully drops below its trailing 50th percentile (median).
- **Assessment**: The reset rule successfully absorbs clustered volatility spikes into unified macro-episodes. Once reset, the process genuinely returns to a baseline state.
- **Finding**: **INDEPENDENCE PLAUSIBLE**. The clustering constraint is scientifically defensible and adequately generates independent episode-level observations.

## 5. Structural Event Diagnostics
- **Total Episodes**: 794
- **Completed Episodes**: 794
- **Right-Censored Episodes**: 0
- **Shortest Duration**: 1 M15 bar
- **Longest Duration**: 168 M15 bars
- **Finding**: **PASS**. The sample size is massive (n=794) and fully observable.

## 6. Null Model Feasibility
- **Definition**: Geometric distribution with parameter `p` (exit probability).
- **Verification**: `p` is cleanly defined and observable as `Total Terminations (794) / Total Bars in HIGH_VOL state (17456)`. The resulting empirical exit probability is `p = 0.04549`.
- **Finding**: **PASS**. The Memoryless Markov Baseline is perfectly calculable and internally consistent.

## 7. Discrete-Null K-S Feasibility (FATAL BLOCKER)
- **Design Review**: The frozen methodology specifies a Kolmogorov-Smirnov (K-S) test to compare the empirical survival curve against the geometric null.
- **Flaw**: Persistence durations are strictly discrete integers (1, 2, 3... bars). The standard continuous K-S test critical values are invalid (overly conservative) for discrete distributions. The methodology fails to specify a discrete K-S calibration (e.g., exact discrete computation, Monte Carlo simulation, or permutation testing).
- **Finding**: **BLOCKED — DISCRETE NULL INFERENCE DESIGN**. A standard statistical package implementation will yield statistically invalid bounds unless the discreteness is mathematically addressed in the frozen methodology.

## 8. Gate Decision
**BLOCKED — METHODOLOGY**

The fundamental structural properties (causality, independence, thresholds, sample size, null parameter definition) are pristine. However, the inferential test (K-S test) lacks the discrete calibration necessary to evaluate integer-based survival data. The methodology must be revised to fix this statistical inference design gap before M13.
