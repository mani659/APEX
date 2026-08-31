# APEX M20: Pre-Economic Data Validation

## 1. Prediction Vector Integrity
The prediction vector generated in M17-R2 is structurally sound. It contains exactly 397 chronological Out-of-Sample predictions. The predictions strictly align with the predefined `HIGH_VOL` onset boundary (`t`). There are no duplicate IDs and no training-era predictions contaminating the array.

## 2. Forward Window & Leakage Constraints
The M19 requirement of evaluating the forward 12 hours via `[t+1, t+48]` M15 bars is causally pristine. It absolutely prevents the onset bar from bleeding into the outcome window, effectively isolating the out-of-sample prediction from the subsequent RV trajectory. The 794-event EURUSD ledger is long enough that all 397 OOS events possess sufficient subsequent data to populate the 48-bar forward window.

## 3. Methodological Blockers
While the structural boundaries are sound, M19 failed to explicitly freeze three critical numerical conventions, violating the absolute scientific rigor required prior to empirical testing.

### Blocker A: HAC Lag Not Predefined
M19 mandates Newey-West HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors to adjust for overlapping 12-hour forward windows. However, Newey-West requires an explicit bandwidth/lag truncation parameter (e.g., `maxlags = 48` or an automated heuristic). M19 failed to freeze this. Permitting the analyst to select the lag length after running the OLS is a fatal methodological degree of freedom.

### Blocker B: Inference Threshold Not Frozen
M19 establishes the falsification rule as: "Translation is not established if the slope coefficient is statistically indistinguishable from zero." It failed to explicitly declare the alpha significance threshold (e.g., $\alpha = 0.05$) and failed to freeze whether the hypothesis is one-sided or two-sided. 

### Blocker C: Annualization Definition
M19 specifies "Annualized standard deviation of M15 log-returns," but leaves the annualization constant ambiguous. In 24-hour FX markets, the choice between trading-day periods (e.g., $\sqrt{252 \times 96}$) versus 24/7 calendar-day periods significantly alters the nominal RV scaling. This scalar must be frozen deterministically.

## 4. Final Gate Decision
**BLOCKED — METHODOLOGY**.
M21 cannot proceed. The M19 methodology contains three ambiguous definitions that would act as outcome-dependent researcher degrees of freedom if left unresolved.
