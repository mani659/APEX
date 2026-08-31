# APEX M17: Conditional HIGH_VOL Persistence Predictability Experiment

## 1. Environment Execution Failure
M17 attempted to execute the frozen methodology by installing the required statistical modeling dependency `lifelines`. The installation systematically failed.
The dependency graph for `lifelines` requires `autograd-gamma`, which fails to build its wheel on the current Python 3.11 environment due to a `distutils/setuptools` internal conflict (`AssertionError: distutils/core.py`). Upgrading the build environment (pip/setuptools/wheel) did not resolve the error.

## 2. Methodology Enforcement
Per the strict M17 rules:
> "If installation fails: `M17 BLOCKED — ENVIRONMENT`"
> "Do not substitute a materially different statistical implementation without control approval."

Therefore, the experiment cannot compute the Cox Proportional Hazards Model. Substituting an alternative package (e.g., `scikit-survival` or `statsmodels`) is explicitly forbidden without an M17-CR (Control Review) to amend the frozen methodology.

## 3. Pre-Execution Setup Verification
Prior to the block, the script correctly loaded the 794 canonical EURUSD `HIGH_VOL` episodes and initialized the Walk-Forward expanding window (397 training, 397 OOS).
The predictor set contained exactly two variables:
1. `Breakout_Intensity`
2. `Variance_Momentum`

## 4. Final Conclusion
**Inconclusive / methodology invalid**. The experiment cannot produce a valid predictive answer because of a predefined implementation software failure. No predictive output (C-index) could be generated.

## 5. M18 Recommendation
M18 cannot proceed. The APEX Control Session must intervene to either:
1. Authorize an alternative survival analysis package (e.g., `scikit-survival` or `statsmodels`) to run the Cox PH model.
2. Provide an environment capable of compiling `lifelines`.
