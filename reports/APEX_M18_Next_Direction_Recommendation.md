# APEX M18: Next Direction Recommendation

## Primary Recommendation
**Candidate B — Predicted-persistence to realized-volatility translation**

### 1. Information Value
We know `HIGH_VOL` duration is conditionally predictable. The highest-information-value next step is to answer: *Does a predicted short-duration episode exhibit materially different forward realized volatility trajectories than a predicted long-duration episode?* If predicted duration doesn't map to actual variance paths, the signal has statistical rank power but zero economic relevance.

### 2. M17-R2 Evidence Support
M17-R2 proved the initial state variables (Intensity/Momentum) predict the *time* the episode will last. Translation research evaluates the *intensity* of the market during that predicted time.

### 3. What Remains Unknown
It remains unknown if longer predicted persistence corresponds to higher total cumulative variance, directional drift, or simply a slow, mean-reverting chop. 

### 4. Data Requirements
None. This can be tested entirely on the canonical EURUSD M1/M15 dataset and the existing 794 `HIGH_VOL` event ledger.

### 5. Frozen Methodology Prerequisites
M19 must freeze:
- The translation target (e.g., Forward 12-hour Realized Volatility, or Cumulative RV over the predicted lifespan).
- The exposure mapping (e.g., binning M17-R2 OOS predictions into top/bottom quartiles of expected persistence).
- The statistical difference metric (e.g., Mann-Whitney U test on the realized volatility distributions of the distinct predicted subsets).

### 6. Falsifiability
The hypothesis is falsified if the forward realized volatility trajectories of predicted short-persistence and predicted long-persistence episodes are statistically indistinguishable.

### 7. Superiority over Alternatives
It is superior to Replication (Candidate A/E) because it avoids costly data acquisition for a signal that may lack economic utility. It is superior to Price-Distribution Translation (Candidate C) because Realized Volatility is a direct mechanical extension of the variance variables used in M17, maintaining strict scientific continuity before advancing to directional price returns.

## Backup Recommendation
**Candidate C — Predicted-persistence to price-distribution translation**
If forward realized volatility is deemed too closely related to the duration itself, evaluating whether predicted persistence conditions the forward directional return distribution (e.g., skewness or kurtosis of forward returns) is the next logical step toward economic translation.
