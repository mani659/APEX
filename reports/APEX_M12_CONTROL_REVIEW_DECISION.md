# APEX M12 Control Review Decision

## Final Decision
**M13 BLOCKED — METHODOLOGY REVISION REQUIRED**

## Rationale
A material methodological redesign is required before any experimentation can proceed. The M11 methodology cannot be safely executed due to the following critical flaws identified during the Control Session Review:

1. **Information Leakage (Lookahead)**: The calculation of the `HIGH_VOL` (RV20 80th percentile) threshold across the full historical sample violates ex-ante principles. A methodology revision must specify a strictly trailing or historically frozen reference window for percentile calculation.
2. **Fatal Confounding**: US macro events (NFP/CPI) are systematically clustered inside the `LONDON_NY_OVERLAP` exposure window. Without macro-event exclusion timestamps, the experiment will measure exogenous news shocks rather than endogenous session transitions. The methodology must be revised to either secure this data, change the exposure windows, or alter the scientific question.
3. **Arbitrary Parameters**: The 2-bar falsification threshold lacks a documented ex-ante rationale and constitutes an unjustified researcher degree of freedom.

## Required Next Steps
A new methodology milestone (e.g., M11b - Methodology Revision) must be authorized to rewrite the experimental design. M13 (Economic Experiment) remains firmly blocked. No methodology amendment is attached to this review, as a complete revision is necessary.
