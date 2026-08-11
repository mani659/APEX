# RC002 Study 013: Cross-Market Execution Robustness

This study evaluates the robustness of the Absorption Entry policy across multiple liquid markets without parameter tuning.

## 1. Cross-Market Performance Matrix

### Exit Strategy: Fixed 20 Bars

| Market | Executed Trades | Win Rate | Expectancy (R) | Profit Factor | MAE (R) | MFE (R) | Avg Hold |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| XAUUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| XAGUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| EURUSD | 116 | 50.9% | 0.018 | 1.01 | -7.91 | 8.39 | 20.0 |
| BTCUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| NAS100 | 0 | N/A | N/A | N/A | N/A | N/A | N/A |

**Cross-Market Stability (Fixed 20 Bars)**
- **Mean Expectancy**: 0.018 R
- **Standard Deviation**: 0.000 R
- **Coefficient of Variation**: 0.00
- **Best Market**: EURUSD (0.018 R)
- **Worst Market**: EURUSD (0.018 R)
- **Positive Markets**: 1 out of 1 (100.0%)

### Exit Strategy: ATR Target

| Market | Executed Trades | Win Rate | Expectancy (R) | Profit Factor | MAE (R) | MFE (R) | Avg Hold |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| XAUUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| XAGUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| EURUSD | 116 | 46.6% | -0.069 | 0.87 | -7.91 | 8.39 | 3.6 |
| BTCUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| NAS100 | 0 | N/A | N/A | N/A | N/A | N/A | N/A |

**Cross-Market Stability (ATR Target)**
- **Mean Expectancy**: -0.069 R
- **Standard Deviation**: 0.000 R
- **Coefficient of Variation**: 0.00
- **Best Market**: EURUSD (-0.069 R)
- **Worst Market**: EURUSD (-0.069 R)
- **Positive Markets**: 0 out of 1 (0.0%)

### Exit Strategy: Recoil Completion

| Market | Executed Trades | Win Rate | Expectancy (R) | Profit Factor | MAE (R) | MFE (R) | Avg Hold |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| XAUUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| XAGUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| EURUSD | 116 | 75.9% | 0.853 | 1.50 | -7.91 | 8.39 | 26.9 |
| BTCUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| NAS100 | 0 | N/A | N/A | N/A | N/A | N/A | N/A |

**Cross-Market Stability (Recoil Completion)**
- **Mean Expectancy**: 0.853 R
- **Standard Deviation**: 0.000 R
- **Coefficient of Variation**: 0.00
- **Best Market**: EURUSD (0.853 R)
- **Worst Market**: EURUSD (0.853 R)
- **Positive Markets**: 1 out of 1 (100.0%)

### Exit Strategy: Time 60 Bars

| Market | Executed Trades | Win Rate | Expectancy (R) | Profit Factor | MAE (R) | MFE (R) | Avg Hold |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| XAUUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| XAGUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| EURUSD | 116 | 53.4% | -0.323 | 0.92 | -7.91 | 8.39 | 60.0 |
| BTCUSD | 0 | N/A | N/A | N/A | N/A | N/A | N/A |
| NAS100 | 0 | N/A | N/A | N/A | N/A | N/A | N/A |

**Cross-Market Stability (Time 60 Bars)**
- **Mean Expectancy**: -0.323 R
- **Standard Deviation**: 0.000 R
- **Coefficient of Variation**: 0.00
- **Best Market**: EURUSD (-0.323 R)
- **Worst Market**: EURUSD (-0.323 R)
- **Positive Markets**: 0 out of 1 (0.0%)

## Final Verdict

**NOT SUPPORTED**

The execution policy fails to generalize across markets, indicating that its performance was likely a Gold-specific artifact or over-fit to a specific asset's microstructure.