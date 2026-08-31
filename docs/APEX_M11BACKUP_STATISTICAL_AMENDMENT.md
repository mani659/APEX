Original frozen inference rule:
Standard Kolmogorov-Smirnov (K-S) test to compare the empirical Kaplan-Meier survival curve against the geometric null.

Identified flaw:
Persistence durations are measured in discrete integer M15 bars. Standard K-S tests assume continuous distributions. Furthermore, the geometric null parameter $p$ is estimated from the sample data. Standard continuous K-S critical values are invalid (overly conservative) for discrete data and do not account for parameter estimation (a Lilliefors-type problem).

Why the original rule is invalid/incomplete:
Using a standard continuous K-S test on discrete, parameter-estimated data produces incorrect p-values, making the hypothesis test mathematically invalid.

Corrected primary inference:
Parametric Monte Carlo Calibration of the K-S Statistic.

Null distribution:
Geometric distribution with support $D \in \{1, 2, 3, ...\}$ and probability mass function $P(D=d) = (1-p)^{d-1}p$.

Parameter estimation:
The Maximum Likelihood Estimator (MLE) for the exit probability is strictly defined as $\hat{p} = \frac{\text{Total Terminations}}{\text{Total Bars in HIGH\_VOL state}}$.

Calibration procedure:
1. Fix deterministic seed (e.g., `42`).
2. Generate $N=10000$ synthetic datasets.
3. Each dataset contains $n$ independent geometric variables simulated using the empirical $\hat{p}$ (where $n$ is the number of observed episodes).
4. For each synthetic dataset, calculate a new parameter $\hat{p}_{sim} = \frac{n}{\sum d_{sim}}$.
5. Compute the simulated K-S statistic $D_{sim} = \sup |F_{sim\_emp}(d) - F_{sim\_null}(d)|$.
6. Build the empirical distribution of $D_{sim}$ under the null.

Test statistic:
The Kolmogorov-Smirnov distance metric $D_{obs} = \sup |F_{emp}(d) - F_{null}(d)|$, calibrated exclusively against the Monte Carlo distribution.

Significance level:
$\alpha = 0.05$.

P-value calculation:
The proportion of Monte Carlo replicates where $D_{sim} \geq D_{obs}$.

Censoring treatment:
The M12-BACKUP validation confirmed exactly 0 censored events. Therefore, the Monte Carlo simulation will generate uncensored complete durations. If any future dataset introduces right-censoring, the estimator $\hat{p}$ automatically incorporates it via its denominator, but the M13 inference acts on the completely observed $n=794$ subset.

Dependence assumption:
Episode durations are assumed conditionally independent. The strict Regime-Reset rule (requiring reversion below the 50th percentile) structurally enforces this by breaking volatility clusters into distinct, time-separated regimes.

Effect reporting:
Descriptive only: Empirical median duration, geometric expected duration ($1/\hat{p}$), 75th/90th empirical percentiles, and empirical survival probabilities at 4, 8, and 24 bars.

Multiple-testing policy:
Exactly one primary inferential test (the Monte Carlo K-S p-value). All other metrics are purely descriptive.

What remains unchanged:
The research question, the HIGH_VOL threshold, the Regime Reset rule, the causal episode construction, and the fundamental memoryless Markov baseline concept.

New researcher degrees of freedom:
- Simulation count
- Seed policy

How each new degree of freedom is frozen:
- Simulation count: Fixed exactly at $N=10000$.
- Seed policy: Fixed deterministically (Seed=42) to ensure strict reproducibility.

M13 implementation requirements:
M13 must explicitly construct the Monte Carlo pipeline as defined above. No standard `scipy.stats.kstest` p-values may be used. The test is strictly a comparison of $D_{obs}$ against the Monte Carlo simulated $D$ distribution.
