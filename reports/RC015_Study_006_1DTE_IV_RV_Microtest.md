# RC015 Study 006 — 1-DTE IV/RV Microtest Report

## 1. Quote Quality Audit
| Dataset      |   Rows |   Valid Bids |   Valid Asks |   Bid>Ask Violations |   Zero/Neg Bids |   Zero/Neg Asks |   Duplicate TS |   Valid Quote % |   Median Spread |   P90 Spread |   Max Spread |
|:-------------|-------:|-------------:|-------------:|---------------------:|----------------:|----------------:|---------------:|----------------:|----------------:|-------------:|-------------:|
| SU2 Options  |   1015 |          935 |         1011 |                    0 |               0 |               0 |            273 |         92.1182 |          0.0013 |       0.004  |      0.006   |
| 6EU6 Futures |   1392 |         1392 |         1392 |                    0 |               0 |               0 |              0 |        100      |          5e-05  |       0.0001 |      0.00055 |

## 2. Synchronization & Execution Audit
- Synchronized Option Observations: 1015
- Synchronized Futures Observations: 1392
- Total Synchronized Pairs: 1015
- Successful IV Inversions: 861
- Excluded (Missing Spot or Invalid IV): 154

## 3. Lookahead Audit
- Option quote timestamp <= observation timestamp: PASS
- Futures quote timestamp <= observation timestamp: PASS
- Realized returns begin strictly after observation timestamp: PASS
- Realized variance never uses data after expiry: PASS

**LOOKAHEAD VIOLATIONS = 0**

## 4. Gap Statistics
| Category          |   N |   Mean IV |   Mean RVol |   Mean VarGap |   Median VarGap |   Std VarGap |   P5 VarGap |   P25 VarGap |   P50 VarGap |   P75 VarGap |   P95 VarGap |
|:------------------|----:|----------:|------------:|--------------:|----------------:|-------------:|------------:|-------------:|-------------:|-------------:|-------------:|
| ALL               | 861 | 0.0611755 |   0.0482829 |  -0.00152579  |    -0.00169681  |  0.00106911  | -0.00310641 | -0.0022318   | -0.00169681  | -0.000558264 |  4.61472e-05 |
| HIGH_VOL          |  17 | 0.0838833 |   0.0531209 |  -0.00422098  |    -0.00433207  |  0.000431524 | -0.00474195 | -0.00458527  | -0.00433207  | -0.00390896  | -0.00363003  |
| NON_HIGH_VOL      | 844 | 0.0607181 |   0.0481855 |  -0.0014715   |    -0.00168347  |  0.00100651  | -0.00296657 | -0.00219854  | -0.00168347  | -0.000542007 |  6.36927e-05 |
| ASIA_TO_LONDON    | 205 | 0.0669411 |   0.0510159 |  -0.00191169  |    -0.00186154  |  0.000704125 | -0.00287428 | -0.00234432  | -0.00186154  | -0.0016636   | -0.000826399 |
| LONDON_NY_OVERLAP | 306 | 0.0526599 |   0.0451508 |  -0.000844386 |    -0.000477931 |  0.0010554   | -0.0032128  | -0.000852724 | -0.000477931 | -0.000308783 |  9.5929e-05  |

## 5. Final Classification
### PASS
The exact remaining-life implied variance and realized variance were calculated reliably with zero lookahead violations.
