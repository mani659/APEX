# APEX M36 Frozen Methodology: Session-Transition Distributional Asymmetry

**Frozen**: 2026-08-24
**Status**: FROZEN — READY FOR M37 VALIDATION
**Milestone**: M36 — Candidate Research Methodology Design

---

## 1. Research Question

Does the validated RC013 LONDON_NY_OVERLAP session state produce a statistically distinct cumulative distribution function of 1-hour forward returns relative to non-overlap periods, independent of the rejected raw-breakout monetization path?

## 2. Primary Endpoint

Conditional forward-return CDF — the cumulative distribution function of 1-hour forward returns during LONDON_NY_OVERLAP versus non-overlap periods.

## 3. Primary Horizon

1 hour (60 minutes).

## 4. Session Definition

**LONDON_NY_OVERLAP**: The M1 bar whose timestamp falls within the overlap of London and New York trading hours (approximately 13:00–16:30 UTC, adjusted for DST using `Europe/London` and `America/New_York` timezone rules via pytz).

**Non-LONDON_NY_OVERLAP**: All other M1 bars whose timestamp does not fall within the LONDON_NY_OVERLAP window.

## 5. Forward Return

For the last M1 bar in each session window (ending at time T):
```
r = (Close_T+60min - Close_T) / Close_T
```

## 6. Control Population

Non-LONDON_NY_OVERLAP hours whose forward window [T, T+60min] does not overlap with any LONDON_NY_OVERLAP window.

## 7. Statistical Framework

Two-sample Anderson-Darling test comparing the CDF of forward returns during LONDON_NY_OVERLAP versus non-overlap periods.

- H0: F_transition(r) = F_non_transition(r) for all r
- H1: F_transition(r) ≠ F_non_transition(r) for some r
- α = 0.05 (two-sided)

## 8. Dependence Treatment

Block bootstrap with block length = 24 (1 day), 10,000 replications, day-boundary blocks.

## 9. Sample Restrictions

Exclude:
- Saturdays and Sundays
- December 25–January 1
- Good Friday
- Thanksgiving (fourth Thursday of November)
- First Friday of each month (NFP)
- Pre-declared FOMC announcement dates
- Pre-declared ECB announcement dates

## 10. Secondary Descriptors (Not Decision Criteria)

Mean, standard deviation, median, IQR, skewness, excess kurtosis for each group. Cohen's d for mean difference. CDF overlay plot.

## 11. Robustness Checks

- Kolmogorov-Smirnov test with HAC-corrected variance (Newey-West, maxlags=24)
- Walk-forward validation with expanding window (2-year minimum training)

## 12. Mandatory Exclusions

- No HIGH_VOL × session interactions
- No dynamic session boundaries
- No directional prediction within sessions
- No monetization architecture testing
- No session-boundary optimization
