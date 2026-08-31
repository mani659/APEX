# APEX M11 Candidate Research Methodology

## 1. Research Question
**Primary:** Does the RC013 session-transition state (specifically ASIA_TO_LONDON and LONDON_NY_OVERLAP) systematically condition the subsequent lifecycle (persistence and decay) of the RC012 HIGH_VOL state?

## 2. Scientific Motivation
RC012 validated that HIGH_VOL is a structural distributional primitive indicating variance expansion. RC013 validated that specific session transitions alter movement distributions. This methodology tests whether these two primitives interact—specifically, whether a HIGH_VOL event triggered during a major session transition has a structurally different duration and decay profile than a HIGH_VOL event occurring during off-peak hours.

## 3. Reused RC012 Definition (HIGH_VOL)
* **Definition:** Realized Volatility over a 20-period lookback (RV20) > 80th historical percentile.
* **Frequency:** EURUSD M15.
* **Status:** FROZEN.

## 4. Reused RC013 Definition (Session Transition)
* **Definition:** `ASIA_TO_LONDON` and `LONDON_NY_OVERLAP` deterministic time-of-day blocks.
* **Timezone:** Standardized to canonical APEX timezone (usually UTC or EST, requires M12 verification).
* **Status:** FROZEN.

## 5. Unit of Observation
A single continuous **HIGH_VOL episode**.
* **Status:** FROZEN.

## 6. Event Construction
* **Onset:** The first M15 bar `t` where RV20 crosses above the 80th percentile, provided no active episode occurred in the prior 12 bars (minimum separation rule to prevent pseudo-replication).
* **Termination:** The first subsequent M15 bar where RV20 crosses back below the 80th percentile.
* **Status:** FROZEN.

## 7. Exposure / Conditional-State Definition
A HIGH_VOL episode is "associated with" a session transition if its **onset bar `t`** occurs strictly within the predefined `ASIA_TO_LONDON` or `LONDON_NY_OVERLAP` windows.
* **Status:** FROZEN.

## 8. Control Construction
* **Control Population:** HIGH_VOL episodes whose onset bar `t` occurs entirely outside the `ASIA_TO_LONDON` and `LONDON_NY_OVERLAP` windows. 
* **Justification:** Answers the counterfactual: how does variance decay when not propelled by a major institutional liquidity transition?
* **Status:** FROZEN.

## 9. Primary Endpoint
**Persistence (Survival Time):** The duration of the HIGH_VOL episode, measured as the number of consecutive M15 bars from onset until termination.
* **Status:** FROZEN.

## 10. Secondary Endpoints
1. **Forward Realized Volatility:** The calculated RV over the fixed horizon [t+1, t+12] (next 3 hours).
2. **Decay Slope:** The linear slope of the RV20 metric from `t` to `t+12`.
* **Status:** FROZEN.

## 11. Statistical Framework
* **Primary Test:** Kaplan-Meier survival analysis with a Log-rank test to compare the survival curves of the exposure vs. control populations.
* **Secondary Test:** Mann-Whitney U test for non-parametric comparison of Forward RV distributions.
* **Significance Level:** alpha = 0.05.
* **Status:** FROZEN.

## 12. Confounder Handling
* **Macro Events:** Episodes originating exactly on NFP or FOMC release bars will be EXCLUDED, as exogenous macro shocks heavily confound endogenous session mechanics.
* **Day of Week:** Friday late-session episodes will be right-censored at Friday close to prevent weekend gap distortion.
* **Status:** REQUIRES M12 VALIDATION.

## 13. Lookahead Controls
* Event classification at bar `t` must rely EXCLUSIVELY on OHLCV data up to and including the close of `t`.
* RV20 at `t` uses `[t-19, t]`. 
* Session windows are deterministic time-of-day.
* Forward metrics `[t+1, t+N]` are strictly quarantined for outcome measurement only.
* **Status:** FROZEN.

## 14. Sample Rules
* **Instrument:** EURUSD.
* **Frequency:** M15.
* **Period:** Canonical historical sample (e.g., 2010–2023).
* **Data Completeness:** Discard events with missing bars in their forward 12-bar window.
* **Status:** FROZEN.

## 15. Missing-Data Rules
If a sequence is interrupted by a missing M15 bar during an active episode, the duration measurement is right-censored at the last known valid bar.
* **Status:** FROZEN.

## 16. Robustness Plan
1. **Alternative Threshold:** Test HIGH_VOL onset at the 75th and 85th percentiles.
2. **Alternative Baseline:** Measure time until RV20 returns to the 50th percentile (median) rather than simply falling below the 80th.
* **Status:** FROZEN.

## 17. Multiple-Testing Policy
Strict hierarchy: The Log-rank test on persistence is the sole primary endpoint. Secondary metrics are exploratory. Bonferroni correction applied if multiple session windows are tested independently against the control.
* **Status:** FROZEN.

## 18. Falsification Criteria
* **Supported:** The Log-rank test yields p < 0.05 AND the median survival time difference is ≥ 2 bars (meaningful economic difference).
* **Not Supported:** p ≥ 0.05 OR the median survival difference is < 2 bars (statistically significant but economically irrelevant).
* **Inconclusive:** Severe data quality issues or insufficient sample size (e.g., < 100 conditional events) discovered in M12.
* **Status:** FROZEN.

## 19. Data Requirements
* **Canonical Data:** EURUSD M15 historical OHLCV.
* **No New Data:** The existing APEX dataset is sufficient.
* **Status:** FROZEN.

## 20. M12 Validation Gate (Prerequisites for M13)
M12 must empirically verify:
1. EURUSD M15 data covers the required history without fatal gaps.
2. RV20 calculation maps perfectly to the 80th percentile threshold without lookahead.
3. At least 200 HIGH_VOL episodes exist in both the exposure and control populations after applying the 12-bar separation rule.
* **Status:** PENDING.

## 21. Known Limitations
* Rigid session windows may fail to capture daylight saving transitions perfectly if the underlying data timezone shifted historically.
* The 12-bar separation rule may discard legitimate clustered volatility shocks.
* **Status:** UNRESOLVED (requires M12 timezone audit).

## 22. Explicit Statements of What is NOT Being Tested
* This is NOT a trading strategy.
* We are NOT testing directional prediction (up/down).
* We are NOT calculating PnL, drawdowns, or expectancy.
* We are NOT optimizing thresholds to maximize a return metric.
* **Status:** FROZEN.
