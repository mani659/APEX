# RC009 Study 006 — HTF Regime Analysis

## 1. H4 Construction Methodology & Timezone
- **Resampling:** 4H boundaries (closed left, labeled left)
- **Timezone Format:** Naive timestamps
- **Lookback Volatility Window:** 480 completed H4 bars
- **State:** 9-state (Vol/Dir) identically matched to M1

## 2. Lookahead Audit
- Total M1 Anchors: 135612
- Matched H4 States: 128232
- Unmatched (Missing): 7380
- Lookahead Violations (h4_close_time > m1_timestamp): **0**

## 3. Model A — M1 Baseline
| M1 State | N | Mean 60 | Med 60 | Mean 240 | Med 240 | Mean MFE | Mean MAE | Cont % | Rev % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| HIGH_VOL_BEAR | 13660 | 0.00003 | 0.00005 | 0.00001 | 0.00003 | 0.00101 | 0.00099 | 48.1% | 51.5% |
| HIGH_VOL_BULL | 13339 | -0.00003 | -0.00003 | -0.00005 | -0.00006 | 0.00100 | 0.00101 | 48.6% | 51.0% |
| HIGH_VOL_FLAT | 4860 | 0.00001 | -0.00001 | 0.00002 | 0.00002 | 0.00115 | 0.00116 | 48.4% | 49.0% |
| LOW_VOL_BEAR | 8178 | 0.00001 | 0.00001 | 0.00003 | 0.00005 | 0.00043 | 0.00044 | 48.3% | 50.8% |
| LOW_VOL_BULL | 8599 | -0.00001 | -0.00001 | -0.00002 | 0.00002 | 0.00041 | 0.00046 | 48.2% | 50.9% |
| LOW_VOL_FLAT | 14975 | -0.00000 | 0.00000 | 0.00002 | 0.00003 | 0.00046 | 0.00048 | 45.9% | 45.9% |
| NORMAL_VOL_BEAR | 22286 | 0.00002 | 0.00003 | 0.00002 | 0.00003 | 0.00067 | 0.00065 | 47.9% | 51.4% |
| NORMAL_VOL_BULL | 22394 | -0.00003 | -0.00002 | -0.00004 | -0.00003 | 0.00063 | 0.00067 | 48.0% | 51.3% |
| NORMAL_VOL_FLAT | 19941 | -0.00000 | -0.00001 | -0.00002 | -0.00001 | 0.00076 | 0.00076 | 47.9% | 48.3% |

## 4. Multiple-Testing Disclosure
- 9 M1 states, 9 H4 states, 81 theoretical combinations
- Number populated: 81
- Number with N >= 100: 80
- Number with N >= 500: 68
- Number highlighted (|d| >= 0.2 & N >= 500): 0

## 5. Candidate Register
None.

## 6. Top Exploratory / Limited Sample Combinations (100 <= N < 500)
| M1 State | H4 State | N | Mean | Base Mean | Cohen D |
| :--- | :--- | :--- | :--- | :--- | :--- |
| HIGH_VOL_BEAR | HIGH_VOL_FLAT | 214 | 0.00023 | 0.00003 | 0.140 |
| HIGH_VOL_FLAT | LOW_VOL_BULL | 231 | -0.00017 | 0.00001 | -0.111 |
| NORMAL_VOL_FLAT | HIGH_VOL_FLAT | 380 | 0.00011 | -0.00000 | 0.098 |
| LOW_VOL_BEAR | HIGH_VOL_FLAT | 163 | -0.00005 | 0.00001 | -0.084 |
| NORMAL_VOL_BEAR | HIGH_VOL_FLAT | 442 | 0.00008 | 0.00002 | 0.066 |
| LOW_VOL_BULL | HIGH_VOL_FLAT | 163 | -0.00005 | -0.00001 | -0.059 |
| LOW_VOL_FLAT | HIGH_VOL_FLAT | 349 | -0.00004 | -0.00000 | -0.052 |
| HIGH_VOL_BULL | HIGH_VOL_FLAT | 235 | 0.00001 | -0.00003 | 0.026 |
| HIGH_VOL_FLAT | LOW_VOL_BEAR | 302 | -0.00001 | 0.00001 | -0.012 |
| NORMAL_VOL_BULL | HIGH_VOL_FLAT | 473 | -0.00004 | -0.00003 | -0.012 |
| LOW_VOL_BEAR | LOW_VOL_BULL | 391 | -0.00000 | 0.00001 | -0.009 |
| LOW_VOL_BULL | LOW_VOL_BULL | 435 | -0.00001 | -0.00001 | 0.004 |

## 7. Rejected Register (N >= 500, |d| < 0.2)
| M1 State | H4 State | N | Mean | Base Mean | Cohen D |
| :--- | :--- | :--- | :--- | :--- | :--- |
| LOW_VOL_BEAR | HIGH_VOL_BULL | 831 | 0.00006 | 0.00001 | 0.088 |
| HIGH_VOL_FLAT | HIGH_VOL_BEAR | 685 | -0.00009 | 0.00001 | -0.061 |
| HIGH_VOL_FLAT | NORMAL_VOL_FLAT | 602 | 0.00010 | 0.00001 | 0.057 |
| HIGH_VOL_BULL | HIGH_VOL_BEAR | 1671 | -0.00011 | -0.00003 | -0.054 |
| HIGH_VOL_BEAR | HIGH_VOL_BULL | 1706 | -0.00004 | 0.00003 | -0.049 |
| HIGH_VOL_BEAR | HIGH_VOL_BEAR | 1688 | 0.00009 | 0.00003 | 0.043 |
| HIGH_VOL_BULL | HIGH_VOL_BULL | 1569 | -0.00009 | -0.00003 | -0.043 |
| NORMAL_VOL_FLAT | NORMAL_VOL_BULL | 3335 | -0.00005 | -0.00000 | -0.041 |
| LOW_VOL_FLAT | HIGH_VOL_BULL | 1532 | -0.00003 | -0.00000 | -0.041 |
| NORMAL_VOL_BEAR | HIGH_VOL_BULL | 2395 | -0.00002 | 0.00002 | -0.038 |
| LOW_VOL_BULL | LOW_VOL_BEAR | 518 | -0.00004 | -0.00001 | -0.036 |
| HIGH_VOL_FLAT | LOW_VOL_FLAT | 667 | -0.00005 | 0.00001 | -0.036 |
| LOW_VOL_BEAR | NORMAL_VOL_BULL | 1456 | -0.00002 | 0.00001 | -0.032 |
| HIGH_VOL_FLAT | NORMAL_VOL_BULL | 716 | 0.00006 | 0.00001 | 0.032 |
| HIGH_VOL_BULL | LOW_VOL_BULL | 730 | 0.00002 | -0.00003 | 0.032 |
| LOW_VOL_FLAT | LOW_VOL_BULL | 688 | -0.00002 | -0.00000 | -0.031 |
| HIGH_VOL_BEAR | LOW_VOL_BEAR | 844 | -0.00001 | 0.00003 | -0.031 |
| NORMAL_VOL_FLAT | LOW_VOL_BEAR | 1220 | 0.00003 | -0.00000 | 0.030 |
| NORMAL_VOL_BULL | NORMAL_VOL_BULL | 3783 | 0.00000 | -0.00003 | 0.029 |
| LOW_VOL_BEAR | LOW_VOL_BEAR | 523 | -0.00001 | 0.00001 | -0.028 |

## 8. Final RC009 Decision
**RC009 FINAL RESULT — NEGATIVE**

The H4 regime does NOT provide meaningful incremental predictive structure over the M1 state in isolation. All structural behavioral hypotheses tested under RC009 are rejected. The discovery campaign is permanently closed.
