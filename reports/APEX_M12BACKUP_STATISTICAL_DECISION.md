# APEX M12-BACKUP Statistical Decision

## Final Decision
**STATISTICAL AMENDMENT APPROVED — M13 PENDING**

## Rationale
The Control Session has audited the statistical flaw identified in M12-BACKUP. The original methodology relied on a standard Kolmogorov-Smirnov test to compare empirical durations against a memoryless geometric null. This was mathematically invalid because the empirical data is discrete (integer bars) and the geometric parameter is estimated from the sample, invalidating the continuous asymptotic K-S distribution.

The Control Session has formally adopted a **Parametric Monte Carlo Calibration** of the K-S distance metric. This elegantly solves both the discreteness and the parameter-estimation problems simultaneously by simulating the exact null distribution of the test statistic computationally.

The `docs/APEX_M11BACKUP_STATISTICAL_AMENDMENT.md` document has been generated, strictly freezing the Monte Carlo parameters (10,000 simulations, deterministic seed 42) and ensuring no hidden research degrees of freedom remain.

## Next Authorized Action
The statistical methodology is now genuinely frozen, internally coherent, and ready. M13 Economic Experiment is now **PENDING AUTHORIZATION**. The next milestone is the execution of M13 strictly adhering to the combined frozen methodology and the new statistical amendment.
