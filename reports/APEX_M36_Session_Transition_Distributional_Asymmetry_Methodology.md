# APEX M36: Session-Transition Distributional Asymmetry Methodology

## 1. Research Question

Does the validated RC013 LONDON_NY_OVERLAP session state produce a statistically distinct cumulative distribution function of 1-hour forward returns relative to non-overlap periods, independent of the rejected raw-breakout monetization path?

## 2. Why This Is Genuinely New vs. RC013

RC013 tested:
- Tail probability uplift (P90) — a single quantile
- Directional neutrality (binary positive/negative percentage)
- Path geometry (length, efficiency, whipsaw)
- Raw range-breakout monetization (rejected)

M36 tests the full conditional CDF of forward returns. This would detect:
- Mean shifts that binary neutrality testing misses
- Variance changes that P90 testing partially captures but does not fully characterize
- Skewness changes that binary neutrality testing misses entirely
- Tail changes beyond the single P90 quantile

RC013's direction-neutrality finding (50.1% positive / 49.2% negative for LONDON_NY_OVERLAP) is a binary test at α not reported. A full CDF comparison has strictly more power to detect distributional asymmetry.

## 3. RC013 Evidence Reused

### Session Definitions (Frozen)
- Timezones: `Europe/London`, `America/New_York`
- ASIA: approximately 00:00–08:00 UTC
- LONDON_PRE_OVERLAP: approximately 08:00–13:00 UTC
- LONDON_NY_OVERLAP: approximately 13:00–16:30 UTC
- NEW_YORK_POST_OVERLAP: approximately 16:30–21:00 UTC
- POST_SESSION: approximately 21:00–00:00 UTC

### Validated Findings Reused
1. LONDON_NY_OVERLAP is a validated structural primitive (RC013 Study 002)
2. Session effects are approximately direction-neutral
3. Session expansion exhibits TYPE A path geometry (directionally efficient)
4. Raw range-breakout monetization architecture is rejected

### What Is NOT Reused
- P90 uplift values (tail probability, not distributional comparison)
- Relative Risk values (risk ratio, not distributional comparison)
- Path length/efficiency values (path geometry, not distributional comparison)
- Raw range-breakout monetization results (rejected architecture)

## 4. Primary Endpoint

**Conditional forward-return CDF** — the cumulative distribution function of 1-hour forward returns during LONDON_NY_OVERLAP versus non-overlap periods.

The endpoint is the full CDF, not a single moment or quantile. The primary test statistic is the Anderson-Darling two-sample statistic, which measures integrated squared difference between the two CDFs with emphasis on the tails.

## 5. Candidate Distributional Outcomes Evaluated

| Candidate | Description | Selected? |
|---|---|---|
| A. Conditional return-distribution asymmetry | Full CDF comparison of forward returns | **YES — PRIMARY** |
| B. Conditional volatility asymmetry | CDF of forward realized volatility | No — partially captured by RC013 P90 |
| C. Tail asymmetry | Tail probability comparison | No — RC013 already tested P90 |
| D. Range/excursion asymmetry | Upward vs downward excursion | No — M27 already tested for HIGH_VOL |
| E. Distribution-shape change | Skewness/kurtosis comparison | No — subsumed by full CDF comparison |

Candidate A is selected because it is the broadest test and subsumes candidates B–E. A significant CDF difference could manifest as a mean shift, variance change, skewness change, or tail change — all detected by the Anderson-Darling test.

## 6. Prediction / Observation Boundary

| Component | Definition |
|---|---|
| Event/state timestamp | End of LONDON_NY_OVERLAP session (approximately 16:30 UTC) |
| When state becomes known | Session boundaries are deterministic; known in advance for all history |
| Forward observation start | End of LONDON_NY_OVERLAP session (approximately 16:30 UTC) |
| Forward horizon | 1 hour (60 minutes) |
| Forward observation end | 1 hour after forward start (approximately 17:30 UTC) |
| Pre-event conditioning variables | None. Session state is deterministic and timestamp-based. |

No future information enters the state classification. The session state at any M1 bar is determined solely by its timestamp and the frozen session definitions.

## 7. Primary Horizon

**1 hour (60 minutes)**.

Rationale:
- Matches RC013's validated Horizon A for LONDON_NY_OVERLAP
- Minimizes overlap between consecutive sessions (LONDON_NY_OVERLAP is followed by NEW_YORK_POST_OVERLAP)
- Most likely to capture the immediate distributional effect of the session transition
- Sufficient sample size at M1 resolution

## 8. Session and Event Definitions

### Primary Session State
**LONDON_NY_OVERLAP**: The M1 bar whose timestamp falls within the overlap of London and New York trading hours (approximately 13:00–16:30 UTC, adjusted for DST using `Europe/London` and `America/New_York` timezone rules).

### Forward Return
For the last M1 bar in each LONDON_NY_OVERLAP window (ending at time T):
```
r = (Close_T+60min - Close_T) / Close_T
```

### Control Population
**Non-LONDON_NY_OVERLAP**: The M1 bar whose timestamp does NOT fall within the LONDON_NY_OVERLAP window. For each non-overlap hour ending at time T, the forward return is computed identically:
```
r = (Close_T+60min - Close_T) / Close_T
```

### Non-Overlap Forward Returns
To avoid overlap with LONDON_NY_OVERLAP forward returns, the control population includes only non-overlap hours whose forward window does not intersect LONDON_NY_OVERLAP. Specifically, for a non-overlap hour ending at time T, the forward return is included only if the interval [T, T+60min] does not overlap with any LONDON_NY_OVERLAP window.

This ensures non-overlapping, independent forward observations for both groups.

## 9. Statistical Framework

### Primary Test
**Two-sample Anderson-Darling test** comparing the CDF of forward returns during LONDON_NY_OVERLAP versus non-overlap periods.

- H0: F_overlap(r) = F_non_overlap(r) for all r
- H1: F_overlap(r) ≠ F_non_overlap(r) for some r
- Significance level: α = 0.05 (two-sided)

### Why Anderson-Darling Over Alternatives
- **vs. Kolmogorov-Smirnov**: Anderson-Darling has more power in the tails, which is where RC013 found the largest effects (P90 uplift)
- **vs. Mann-Whitney U**: Anderson-Darling tests the full CDF, not just stochastic dominance
- **vs. Cramér-von Mises**: Anderson-Darling gives more weight to tails, which is scientifically appropriate given RC013's tail findings
- **vs. parametric tests**: No distributional assumption is imposed; the test is fully non-parametric

### Secondary Descriptive Statistics
The following are reported for interpretation but are NOT decision criteria:
- Sample mean and standard deviation for each group
- Median and IQR for each group
- Skewness and excess kurtosis for each group
- Effect size (Cohen's d for mean difference; overlaid CDF plot)

## 10. Null Hypothesis

**Primary null**: The session-transition state (LONDON_NY_OVERLAP) does not alter the cumulative distribution function of 1-hour forward returns.

Formally: F_transition(r) = F_non_transition(r) for all r ∈ ℝ, where F_transition and F_non_transition are the true CDFs of 1-hour forward returns during LONDON_NY_OVERLAP and non-overlap periods, respectively.

## 11. Dependence Treatment

### Primary Method: Block Bootstrap
Forward returns from adjacent hours are serially correlated. To account for this:

- **Method**: Block bootstrap
- **Block length**: 24 (corresponding to 1 day of hourly observations)
- **Number of bootstrap replications**: 10,000
- **P-value**: Fraction of bootstrap replications with Anderson-Darling statistic ≥ observed statistic
- **Block boundary**: Day boundaries (00:00 UTC) to preserve within-day serial correlation while breaking across-day dependence

### Rationale
- Block length = 24 preserves the hourly serial correlation structure within each day
- Day-boundary blocks ensure that overnight dependence is not artificially broken
- 10,000 replications give p-value resolution to 0.0001

### Robustness Check: HAC-Corrected KS Test
As a robustness check, a Kolmogorov-Smirnov test with HAC-corrected variance (Newey-West, maxlags=24) will be applied to the difference in sample means. This provides a parametric-adjacent check on the non-parametric primary result.

## 12. Multiple Testing Control

- **Primary test**: Single test (LONDON_NY_OVERLAP vs. non-overlap)
- **α**: 0.05 (two-sided)
- **No Bonferroni correction needed** (single primary test)
- **Secondary sessions** (ASIA_TO_LONDON, LONDON_PRE_OVERLAP, etc.): Descriptive only, not used for primary decision, reported with unadjusted p-values

## 13. Comparison / Control Definition

### Treatment Group
All 1-hour forward returns where the preceding hour falls within the LONDON_NY_OVERLAP window.

### Control Group
All 1-hour forward returns where the preceding hour does NOT fall within the LONDON_NY_OVERLAP window AND the forward window does not overlap with any LONDON_NY_OVERLAP window.

### Comparability
Both groups:
- Use identical forward-return computation (1-hour return from M1 close prices)
- Use identical data source (canonical EURUSD M1 OHLCV)
- Cover the same historical period
- Are non-overlapping (no forward window appears in both groups)

The only difference is the session state (LONDON_NY_OVERLAP vs. non-overlap). This is a clean, pre-declared comparison.

## 14. Confounder Audit

| Confounder | Assessment | Mitigation |
|---|---|---|
| Time of day | LONDON_NY_OVERLAP occurs at a specific time of day; any time-of-day effect could confound | This IS the research question — time-of-day effects are the structural property being tested |
| Day of week | Some days may have different transition effects | Exclude weekends (already absent in M1 data); report day-of-week breakdown as secondary descriptor |
| Pre-session volatility | Higher pre-session volatility might predict different forward returns | Not a confounder — this is a potential mediator, not a confounder. The session state is the cause; pre-session volatility is a consequence of the preceding session |
| Recent return | Recent returns might predict forward returns through mean-reversion | Not a confounder for the same reason — the session state is the structural cause |
| Holidays | Major holidays may have different session effects | Exclude pre-declared holiday dates (Christmas, New Year, Good Friday, Thanksgiving) |
| NFP / central bank events | Scheduled releases may create distributional asymmetry | Exclude first Friday of each month (NFP) and pre-declared FOMC/ECB dates |

### Sample Restrictions (Frozen)
The following dates are excluded from both treatment and control groups:
1. Saturdays and Sundays (already absent in M1 data)
2. December 25–January 1 (year-end holidays)
3. Good Friday
4. Thanksgiving (fourth Thursday of November)
5. First Friday of each month (NFP)
6. Pre-declared FOMC announcement dates (11 dates per year)
7. Pre-declared ECB announcement dates (8 dates per year)

## 15. Data Reuse Audit

### Existing Resources
| Resource | Type | Status |
|---|---|---|
| Canonical EURUSD M1 OHLCV | Primary data | 5.5 years, ready |
| RC013 session definitions | Frozen methodology | Available in RC013_FREEZE.md |
| RC013 validated primitives | Scientific knowledge | LONDON_NY_OVERLAP validated at 1H |
| Python infrastructure | Code | pandas, scipy, existing analysis scripts |

### New Data Required
None. Uses existing canonical EURUSD M1 data.

## 16. Methodology Risk Register

| # | Risk | Description | Ex-Ante Mitigation |
|---|---|---|---|
| 1 | Lookahead | Forward return computed using future prices | Forward return defined as price change from T to T+60min; T is end of session; no future information in state classification |
| 2 | Timezone errors | Session boundaries computed in wrong timezone | Use RC013 frozen timezone definitions (Europe/London, America/New_York) with pytz DST handling |
| 3 | DST | Daylight saving time shifts session boundaries | Use pytz timezone objects with automatic DST transitions; verify session boundaries against RC013 observation counts |
| 4 | Session-boundary ambiguity | Unclear which bars belong to which session | Use RC013 frozen session definitions with exact UTC boundary rules; classify each M1 bar by its timestamp |
| 5 | Sample-selection bias | Non-random selection of sessions | Use all available LONDON_NY_OVERLAP hours; no filtering based on outcomes or volatility state |
| 6 | Overlapping windows | Forward returns overlap across sessions | Forward windows are non-overlapping by construction (1-hour forward for 1-hour sessions); control population excludes hours whose forward window overlaps LONDON_NY_OVERLAP |
| 7 | Non-independence | Serial correlation in forward returns | Block bootstrap with block length = 24 (1 day); preserves within-day serial correlation |
| 8 | Multiple testing | Testing multiple sessions or quantiles | Single primary test (LONDON_NY_OVERLAP vs. non-overlap); secondary sessions reported descriptively only |
| 9 | Proxy mismatch | Using wrong price series | Use canonical EURUSD M1 OHLCV data; verify data integrity before execution |
| 10 | Nonstationarity | Session effects change over time | Walk-forward validation with expanding window (secondary check); report temporal stability in secondary descriptors |
| 11 | Confounding | Holiday/NFP effects confound session effects | Exclude pre-declared holiday, NFP, and FOMC/ECB dates from both groups |
| 12 | Hidden strategy optimization | Tuning test to produce preferred result | All decisions frozen in M36; no outcome-dependent changes; Anderson-Darling test is a single, pre-declared test |

## 17. Research Degrees of Freedom

| Decision | Proposed Rule | Rationale | Frozen? | Outcome-Dependent? |
|---|---|---|---|---|
| Session definition | LONDON_NY_OVERLAP vs. all other hours | RC013 validated structural primitive; largest sample size | FROZEN | No |
| Event timestamp | End of LONDON_NY_OVERLAP window | Clean forward observation start; no future information leakage | FROZEN | No |
| Primary endpoint | Forward-return CDF (Anderson-Darling test) | Broadest distributional test; subsumes mean, variance, skewness, tails | FROZEN | No |
| Primary horizon | 1 hour (60 minutes) | Matches RC013 Horizon A; minimizes overlap; captures immediate effect | FROZEN | No |
| Control population | Non-LONDON_NY_OVERLAP hours (forward window non-overlapping) | Clean comparison group; matched resolution and data source | FROZEN | No |
| Statistical model | Two-sample Anderson-Darling test | Non-parametric; tests full CDF; more power in tails than KS | FROZEN | No |
| Dependence method | Block bootstrap (length=24, replications=10,000) | Preserves within-day serial correlation; day-boundary blocks | FROZEN | No |
| Alpha/tail | 0.05 two-sided | Standard scientific convention | FROZEN | No |
| Secondary descriptors | Mean, std, median, IQR, skewness, kurtosis | Descriptive only; not decision criteria | FROZEN | No |
| Robustness checks | KS test with HAC variance; Cohen's d; CDF overlay plot | Cross-validation of primary result | FROZEN | No |
| Sample restrictions | Exclude holidays, NFP, FOMC, ECB dates | Confounder control; pre-declared list | FROZEN | No |
| Walk-forward validation | Expanding window, 2-year minimum training | Temporal robustness check (secondary) | FROZEN | No |

## 18. M37 Validation Requirements

M37 must validate before execution:

1. **RC013 session-state reconstruction**: Verify that LONDON_NY_OVERLAP hours in the canonical M1 dataset match RC013 observation counts (5,192 observations at 4-bar M15 thinning ≈ 5,192 hours; verify within ±5%)
2. **Timezone correctness**: Verify that session boundaries computed with pytz match RC013 frozen definitions
3. **DST handling**: Verify that DST transitions do not create ambiguous or duplicate hour classifications
4. **Event counts**: Verify treatment and control group sizes before execution
5. **Forward-return availability**: Verify that forward returns can be computed for all treatment and control observations
6. **Overlap exclusion**: Verify that no forward window in the control group overlaps with LONDON_NY_OVERLAP
7. **Sample restrictions**: Verify that excluded dates (holidays, NFP, FOMC, ECB) are correctly identified and removed
8. **Statistical software**: Verify that `scipy.stats.anderson_ksamp` or equivalent is available and produces correct results on test data
9. **Leakage**: Verify that no future information enters the session-state classification
10. **Frozen degrees of freedom**: Verify that no decision in Section 17 has been modified

## 19. Freeze Classification

| Component | Classification |
|---|---|
| Research question | FROZEN |
| Primary endpoint | FROZEN |
| Primary horizon | FROZEN |
| Session definition | FROZEN |
| Control population | FROZEN |
| Statistical framework | FROZEN |
| Null hypothesis | FROZEN |
| Dependence treatment | FROZEN |
| Multiple-testing control | FROZEN |
| Confounder restrictions | FROZEN |
| Research degrees of freedom | FROZEN |
| M37 validation requirements | REQUIRES M37 VALIDATION |

**Overall status**: FROZEN. No unresolved material choices.

## 20. Expected Outcome Space

### If H0 is rejected (p < 0.05):
The LONDON_NY_OVERLAP session produces a statistically distinct distribution of forward returns. This would be a genuinely new finding — RC013 tested tail probability and binary neutrality, not the full CDF. The secondary descriptors (mean, variance, skewness, kurtosis) would characterize the nature of the distributional asymmetry.

### If H0 is not rejected (p ≥ 0.05):
The LONDON_NY_OVERLAP session does not produce a detectable distributional asymmetry in forward returns. This would be a clean negative result — the structural primitive validated by RC013 does not extend to the full conditional distribution.

### In either case:
The result is scientifically informative. A positive result opens a new research direction (characterizing the distributional asymmetry). A negative result closes this specific question with a clean falsification.

## 21. Mandated Exclusions

The following are NOT permitted in M36 or any subsequent milestone:
- Testing HIGH_VOL × session interactions (HIGH_VOL branch is CLOSED)
- Testing dynamic session boundaries
- Testing directional prediction within sessions (M24 already established direction neutrality for HIGH_VOL)
- Testing monetization architectures (RC013 already rejected raw breakout)
- Testing multiple session transitions as a grid (single primary test frozen)
- Optimizing session boundaries to maximize effect size
