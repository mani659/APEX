# APEX M17-CR: Software Decision Matrix

## Candidate: statsmodels.PHReg
- **Availability**: Pre-installed and fully functional in the native Python 3.11 environment.
- **Scientific Purity**: Preserves exactly the frozen covariates and walk-forward prediction isolation mechanics.
- **Metric Verification**: Although it lacks an explicit internal `c_index` method comparable to `lifelines`, the strict mathematical definition of Harrell's Concordance is easily and deterministically reconstructed in Python to guarantee metric integrity.

## Decision: APPROVED
The transition to `statsmodels.PHReg` is approved. The M17 methodology remains uncompromised. The deterministic C-index function constructed during the smoke test will be utilized to generate the final performance metric.
