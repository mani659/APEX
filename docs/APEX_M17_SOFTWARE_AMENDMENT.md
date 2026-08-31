Original implementation: `lifelines` (Python package).
Environment failure: `lifelines` dependency `autograd-gamma` fails to compile under Python 3.11 locally due to obsolete setuptools/distutils internal configurations.

Approved replacement: `statsmodels`
Package/version: Local `statsmodels` version via `statsmodels.duration.hazard_regression.PHReg`.

Mathematical equivalence: `statsmodels.PHReg` estimates the exact same standard Cox Proportional Hazards partial likelihood model as the original implementation.

Censoring support: Natively supported via the `status` argument (1=event, 0=censored).
Tie handling: Natively defaults to Breslow's method for tied event durations, standard for Cox PH models.
Risk-score compatibility: `res.predict(exog=...)` returns the expected relative hazard. Higher values denote higher risk (shorter expected persistence), identical to the theoretical Cox hazard function direction.
Baseline compatibility: An intercept-only hazard model is inherently supported.
C-index compatibility: A standalone, deterministic Harrell's Concordance Index function will be strictly defined in the M17 execution script, ensuring complete mathematical compatibility without external library variance.

Why this is not a scientific methodology change:
The replacement exclusively involves the mechanical software computation of the partial likelihood maximization. The mathematical Cox PH model, covariates, target construction, censoring, and C-index objective remain entirely unaltered. 

What remains unchanged:
All aspects of the M15/M16 methodology (including the predictor amendment) are preserved.

M18/M17 execution requirements:
M17 must be rerun using `statsmodels.PHReg` inside the frozen chronological walk-forward expanding window loop, incorporating the deterministic Harrell's C-index function defined during the M17-CR smoke test.
