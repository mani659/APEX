# RC009 Study 004 Cross-Market Analysis

## 1. Synchronization Coverage
Total eligible EURUSD anchors: 135612

| Context Market | Lag | Matched | Missing | Coverage % |
| :--- | :--- | :--- | :--- | :--- |
| XAUUSD | t | 115152 | 20460 | 84.9% |
| XAUUSD | t-15 | 115416 | 20196 | 85.1% |
| XAUUSD | t-30 | 115684 | 19928 | 85.3% |
| XAGUSD | t | 111912 | 23700 | 82.5% |
| XAGUSD | t-15 | 112185 | 23427 | 82.7% |
| XAGUSD | t-30 | 112437 | 23175 | 82.9% |
| BTCUSD | t | 121374 | 14238 | 89.5% |
| BTCUSD | t-15 | 121380 | 14232 | 89.5% |
| BTCUSD | t-30 | 121387 | 14225 | 89.5% |
| USATECHIDXUSD | t | 58204 | 77408 | 42.9% |
| USATECHIDXUSD | t-15 | 58346 | 77266 | 43.0% |
| USATECHIDXUSD | t-30 | 58489 | 77123 | 43.1% |

## 2. EURUSD State Frequency
| State | Count | % |
| :--- | :--- | :--- |
| NORMAL_VOL_BULL | 23772 | 17.5% |
| NORMAL_VOL_BEAR | 23553 | 17.4% |
| NORMAL_VOL_FLAT | 21018 | 15.5% |
| LOW_VOL_FLAT | 15814 | 11.7% |
| HIGH_VOL_BEAR | 14416 | 10.6% |
| HIGH_VOL_BULL | 14049 | 10.4% |
| LOW_VOL_BULL | 9138 | 6.7% |
| LOW_VOL_BEAR | 8703 | 6.4% |
| HIGH_VOL_FLAT | 5149 | 3.8% |

## 3. Model A Baselines (EURUSD Only)
| EURUSD State | N | Mean Ret 60 | Med Ret 60 | Mean Ret 240 | Med Ret 240 | Mean MFE | Mean MAE | Cont % | Rev % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| HIGH_VOL_BEAR | 14416 | 0.00003 | 0.00005 | 0.00002 | 0.00003 | 0.00100 | 0.00098 | 48.0% | 51.6% |
| HIGH_VOL_BULL | 14049 | -0.00002 | -0.00003 | -0.00005 | -0.00005 | 0.00099 | 0.00100 | 48.8% | 50.8% |
| HIGH_VOL_FLAT | 5149 | 0.00001 | -0.00001 | 0.00003 | 0.00003 | 0.00114 | 0.00115 | 48.3% | 49.0% |
| LOW_VOL_BEAR | 8703 | 0.00000 | 0.00001 | 0.00002 | 0.00004 | 0.00043 | 0.00044 | 48.2% | 50.8% |
| LOW_VOL_BULL | 9138 | -0.00001 | -0.00001 | -0.00002 | 0.00002 | 0.00041 | 0.00045 | 48.3% | 50.7% |
| LOW_VOL_FLAT | 15814 | -0.00000 | 0.00000 | 0.00002 | 0.00002 | 0.00046 | 0.00048 | 46.0% | 45.8% |
| NORMAL_VOL_BEAR | 23553 | 0.00002 | 0.00002 | 0.00001 | 0.00002 | 0.00066 | 0.00065 | 48.1% | 51.2% |
| NORMAL_VOL_BULL | 23772 | -0.00003 | -0.00002 | -0.00005 | -0.00004 | 0.00063 | 0.00067 | 48.0% | 51.3% |
| NORMAL_VOL_FLAT | 21018 | -0.00000 | 0.00000 | -0.00002 | -0.00001 | 0.00075 | 0.00076 | 47.9% | 48.2% |

## 4. Multiple-Testing Disclosure
- 4 context markets, 3 lags, 9 EURUSD states, 9 context states
- Total evaluated combinations: 972
- Number meeting N >= 100: 954
- Number meeting N >= 500: 763
- Number highlighted (|d| >= 0.2 & N >= 500): 0

## 5. Candidate Register
No candidates found.

## 6. Top Exploratory / Limited Sample Combinations (100 <= N < 500)
| Market | Lag | EU State | Ctx State | N | Mean | Base Mean | Cohen D |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| USATECHIDXUSD | t-30 | HIGH_VOL_BEAR | LOW_VOL_BULL | 184 | 0.00032 | 0.00003 | 0.212 |
| XAUUSD | t | LOW_VOL_BEAR | HIGH_VOL_FLAT | 127 | -0.00012 | 0.00000 | -0.203 |
| USATECHIDXUSD | t-30 | LOW_VOL_BEAR | HIGH_VOL_BEAR | 117 | -0.00012 | 0.00000 | -0.201 |
| USATECHIDXUSD | t | HIGH_VOL_FLAT | LOW_VOL_FLAT | 105 | 0.00031 | 0.00001 | 0.195 |
| USATECHIDXUSD | t-30 | LOW_VOL_BULL | HIGH_VOL_BEAR | 157 | -0.00013 | -0.00001 | -0.193 |
| USATECHIDXUSD | t-15 | HIGH_VOL_BEAR | LOW_VOL_BULL | 195 | 0.00028 | 0.00003 | 0.178 |
| XAGUSD | t | LOW_VOL_BEAR | HIGH_VOL_FLAT | 162 | -0.00011 | 0.00000 | -0.175 |
| XAUUSD | t-30 | LOW_VOL_BEAR | HIGH_VOL_FLAT | 111 | -0.00010 | 0.00000 | -0.159 |
| XAGUSD | t-15 | LOW_VOL_BEAR | HIGH_VOL_FLAT | 167 | -0.00010 | 0.00000 | -0.159 |
| USATECHIDXUSD | t-30 | LOW_VOL_FLAT | HIGH_VOL_BULL | 323 | -0.00011 | -0.00000 | -0.157 |
| XAGUSD | t | HIGH_VOL_FLAT | LOW_VOL_BEAR | 109 | 0.00025 | 0.00001 | 0.153 |
| BTCUSD | t-30 | HIGH_VOL_FLAT | LOW_VOL_BEAR | 112 | 0.00024 | 0.00001 | 0.149 |
| USATECHIDXUSD | t | HIGH_VOL_FLAT | NORMAL_VOL_BEAR | 255 | 0.00024 | 0.00001 | 0.148 |
| USATECHIDXUSD | t-30 | LOW_VOL_FLAT | HIGH_VOL_BEAR | 357 | -0.00010 | -0.00000 | -0.143 |
| USATECHIDXUSD | t-15 | LOW_VOL_FLAT | HIGH_VOL_BEAR | 358 | -0.00010 | -0.00000 | -0.141 |
| XAGUSD | t-30 | LOW_VOL_BEAR | HIGH_VOL_BULL | 496 | -0.00009 | 0.00000 | -0.140 |
| XAGUSD | t-15 | HIGH_VOL_BEAR | LOW_VOL_BULL | 422 | 0.00022 | 0.00003 | 0.137 |
| XAGUSD | t-30 | LOW_VOL_FLAT | HIGH_VOL_FLAT | 326 | -0.00009 | -0.00000 | -0.137 |
| BTCUSD | t-30 | HIGH_VOL_FLAT | LOW_VOL_BULL | 112 | 0.00022 | 0.00001 | 0.136 |
| USATECHIDXUSD | t-30 | LOW_VOL_BEAR | HIGH_VOL_BULL | 129 | -0.00008 | 0.00000 | -0.132 |

## 7. Rejected Register (N >= 500, |d| < 0.2)
| Market | Lag | EU State | Ctx State | N | Mean | Base Mean | Cohen D |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| XAUUSD | t-15 | LOW_VOL_BULL | HIGH_VOL_BEAR | 598 | -0.00012 | -0.00001 | -0.168 |
| XAUUSD | t-30 | LOW_VOL_BEAR | HIGH_VOL_BEAR | 532 | -0.00008 | 0.00000 | -0.130 |
| XAGUSD | t | NORMAL_VOL_BULL | HIGH_VOL_FLAT | 913 | -0.00015 | -0.00003 | -0.129 |
| XAUUSD | t | LOW_VOL_BULL | HIGH_VOL_BEAR | 569 | -0.00009 | -0.00001 | -0.123 |
| XAUUSD | t-30 | LOW_VOL_BULL | HIGH_VOL_BULL | 555 | 0.00005 | -0.00001 | 0.107 |
| XAUUSD | t-30 | LOW_VOL_BULL | HIGH_VOL_BEAR | 543 | -0.00008 | -0.00001 | -0.106 |
| XAUUSD | t-15 | LOW_VOL_BEAR | HIGH_VOL_BULL | 550 | -0.00006 | 0.00000 | -0.105 |
| XAUUSD | t-30 | NORMAL_VOL_BULL | HIGH_VOL_FLAT | 786 | -0.00013 | -0.00003 | -0.104 |
| XAUUSD | t-30 | NORMAL_VOL_BEAR | HIGH_VOL_FLAT | 790 | 0.00012 | 0.00002 | 0.099 |
| XAUUSD | t | LOW_VOL_BEAR | HIGH_VOL_BULL | 550 | -0.00006 | 0.00000 | -0.096 |
| XAUUSD | t-15 | LOW_VOL_BEAR | LOW_VOL_BULL | 619 | 0.00006 | 0.00000 | 0.095 |
| XAGUSD | t | LOW_VOL_BEAR | NORMAL_VOL_BEAR | 1207 | 0.00006 | 0.00000 | 0.094 |
| XAUUSD | t-15 | NORMAL_VOL_FLAT | HIGH_VOL_BULL | 2006 | -0.00011 | -0.00000 | -0.091 |
| XAGUSD | t-30 | LOW_VOL_BEAR | HIGH_VOL_BEAR | 536 | -0.00005 | 0.00000 | -0.089 |
| XAUUSD | t-15 | HIGH_VOL_BEAR | HIGH_VOL_FLAT | 795 | -0.00009 | 0.00003 | -0.087 |
| XAUUSD | t-30 | LOW_VOL_BEAR | LOW_VOL_BULL | 623 | 0.00006 | 0.00000 | 0.087 |
| USATECHIDXUSD | t | NORMAL_VOL_FLAT | LOW_VOL_FLAT | 946 | 0.00009 | -0.00000 | 0.085 |
| XAGUSD | t-15 | LOW_VOL_FLAT | LOW_VOL_BEAR | 899 | 0.00005 | -0.00000 | 0.084 |
| XAUUSD | t-30 | HIGH_VOL_FLAT | NORMAL_VOL_BULL | 783 | 0.00014 | 0.00001 | 0.084 |
| XAUUSD | t | LOW_VOL_BEAR | LOW_VOL_BEAR | 569 | 0.00006 | 0.00000 | 0.083 |

## 8. Conclusion
**1. Incremental Information:** No relationships met the criteria for candidate selection (N >= 500, |d| >= 0.2, and temporal stability).

**2. Lead/Lag Relationship:** N/A

**3. Temporal Consistency:** N/A

**4. Sufficiently Populated:** N/A

**5. Explained by EURUSD?** N/A

