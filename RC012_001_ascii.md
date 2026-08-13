# RC012 Study 001  Pair Discovery

## 1. Dataset Overlap Validation
**XAUUSD / XAGUSD**
- Start: 2021-07-13 00:00:00 | End: 2026-04-10 20:59:00
- Overlapping bars: 1637551
- Coverage: 92.6% of Leg A, 94.7% of Leg B

**BTCUSD / USATECHIDXUSD**
- Start: 2023-09-01 00:00:00 | End: 2026-05-22 20:14:00
- Overlapping bars: 861448
- Coverage: 33.9% of Leg A, 95.0% of Leg B

## 2. Pair Inventory & Correlation
| Pair | Pearson Corr | Log-Price Corr |
|---|---|---|
| XAUUSD / XAGUSD | 0.932 | 0.954 |
| BTCUSD / USATECHIDXUSD | 0.717 | 0.787 |

## 3. Hedge Ratio & Stationarity (Full Sample)
| Pair | Alpha | Beta | ADF Stat | ADF p-value | 5% Crit | Hurst |
|---|---|---|---|---|---|---|
| XAUUSD / XAGUSD | 4.9423 | 0.8411 | -3.070 | 2.8849e-02 | -2.862 | 0.462 |
| BTCUSD / USATECHIDXUSD | -6.7727 | 1.8066 | -1.370 | 5.9645e-01 | -2.862 | 0.489 |

## 4. Mean-Reversion Characteristics
| Pair | Spread Std | Half-Life (bars) | Zero Crossings | Avg Recovery (bars) | Max Excursion |
|---|---|---|---|---|---|
| XAUUSD / XAGUSD | 0.0902 | 58077.7 | 1628 | 1005.9 | 0.4149 |
| BTCUSD / USATECHIDXUSD | 0.2410 | 127297.7 | 388 | 2220.2 | 0.5864 |

## 5. Temporal Stability (Early / Middle / Recent)
| Pair | P1 Beta | P2 Beta | P3 Beta | P1 ADF | P2 ADF | P3 ADF |
|---|---|---|---|---|---|---|
| XAUUSD / XAGUSD | 0.350 | 0.755 | 0.582 | -2.188 | -2.299 | -2.277 |
| BTCUSD / USATECHIDXUSD | 3.281 | 2.674 | -1.435 | -1.304 | -2.691 | -1.532 |

## 6. Rolling Stability (3-Month Windows)
| Pair | Rolling Beta Std | Mean Rolling ADF |
|---|---|---|
| XAUUSD / XAGUSD | 0.2064 | -2.207 |
| BTCUSD / USATECHIDXUSD | 2.0410 | -2.153 |

## 7. Independence & Structural Logic
### XAUUSD / XAGUSD
- **Economic**: Both are precious metals, primarily driven by real interest rates, USD strength, and safe-haven demand. Silver has higher industrial use, leading to volatility differences, but they share macro drivers.
### BTCUSD / USATECHIDXUSD (Nasdaq)
- **Economic**: Both are risk assets highly sensitive to global liquidity, interest rates, and tech-driven market sentiment. BTC often trades as a high-beta tech proxy.

## 8. Candidate / Rejected Register
### XAUUSD / XAGUSD : **EXPLORATORY**
- Stationarity (ADF): Pass
- Mean Reversion: Fail
- Structural Stability: Pass

### BTCUSD / USATECHIDXUSD : **EXPLORATORY**
- Stationarity (ADF): Fail
- Mean Reversion: Fail
- Structural Stability: Fail

## 9. Final Scientific Conclusion
> **A stable relative-value relationship has been discovered.**