# RC002 Study 003: Cross-Market Behavioral Reproducibility

## Final Research Conclusion
**PARTIALLY SUPPORTED**

### Target Hypothesis
Does the Behavioral Event (Displacement Exhaustion) produce a consistent directional recoil across independent asset classes?

### Experiment Execution
- **Markets Evaluated**: XAUUSD, XAGUSD, EURUSD, BTCUSD, NAS100
- **Horizons Evaluated**: 5, 10, 20, 40 bars
- **Dataset Constraint**: Up to 100,000 most recent M1 records per market.

---

## 1. Cross-Market Comparison (Horizon = 20 Bars)

### Bullish Exhaustion Recoil (Expecting Negative Mean)
| Market | Sample Size (N) | Mean Return | Effect Size | 95% CI | Win Rate (Absolute) | Directional Alignment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| XAUUSD | 67 | -0.46679 | -0.026 | [-4.80685, 3.87327] | 44.8% | ✅ Yes |
| XAGUSD | 99 | 0.07204 | 0.209 | [0.00423, 0.13985] | 51.5% | ❌ No |
| EURUSD | 118 | -0.00001 | -0.013 | [-0.00017, 0.00015] | 50.0% | ✅ Yes |
| BTCUSD | 471 | -5.42293 | -0.038 | [-18.40618, 7.56032] | 46.7% | ✅ Yes |
| NAS100 | 57 | 7.65993 | 0.103 | [-11.60916, 26.92902] | 50.9% | ❌ No |

### Bearish Exhaustion Recoil (Expecting Positive Mean)
| Market | Sample Size (N) | Mean Return | Effect Size | 95% CI | Win Rate (Absolute) | Directional Alignment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| XAUUSD | 96 | 3.32953 | 0.171 | [-0.56528, 7.22434] | 62.5% | ✅ Yes |
| XAGUSD | 103 | 0.02040 | 0.056 | [-0.05004, 0.09084] | 57.3% | ✅ Yes |
| EURUSD | 112 | 0.00013 | 0.176 | [-0.00001, 0.00027] | 59.8% | ✅ Yes |
| BTCUSD | 138 | -35.56812 | -0.138 | [-78.50962, 7.37339] | 54.3% | ❌ No |
| NAS100 | 66 | 6.73603 | 0.082 | [-13.04786, 26.51993] | 68.2% | ✅ Yes |


## 2. Meta Summary & Qualitative Consistency Analysis

### Consistent Markets
- The directional recoil effect following a bearish exhaustion (panic selling) tends to produce a positive mean reversion. 
- Bullish exhaustion (panic buying) tends to produce a negative mean reversion.
- **Markets supporting Bullish Exhaustion Recoil**: XAUUSD, EURUSD, BTCUSD
- **Markets supporting Bearish Exhaustion Recoil**: XAUUSD, XAGUSD, EURUSD, NAS100

### Outliers and Contradictory Markets
- Any market where a bullish exhaustion leads to positive forward returns, or bearish exhaustion leads to negative forward returns, indicates the market absorbed the displacement and continued accelerating.
- **Outliers against Bullish Recoil**: XAGUSD, NAS100
- **Outliers against Bearish Recoil**: BTCUSD

### Verdict
Based on directional alignment at the 20-bar horizon, the hypothesis that behavioral exhaustion is universally reproducible is **PARTIALLY SUPPORTED**.

---

## 3. Individual Market Reports (All Horizons)

### XAUUSD
- **Experiment ID**: experiment_000015

#### Bullish Exhaustion (Expecting Negative Means)
- **H=5**: N=67 | Mean=1.5257 | CI=[-2.0214, 5.0727] | Effect=0.103 | Skew=4.49 | Kurt=29.86
- **H=10**: N=67 | Mean=0.2991 | CI=[-3.6369, 4.2350] | Effect=0.018 | Skew=1.34 | Kurt=9.16
- **H=20**: N=67 | Mean=-0.4668 | CI=[-4.8068, 3.8733] | Effect=-0.026 | Skew=0.40 | Kurt=1.42
- **H=40**: N=67 | Mean=4.7144 | CI=[-1.3472, 10.7760] | Effect=0.186 | Skew=2.36 | Kurt=8.01

#### Bearish Exhaustion (Expecting Positive Means)
- **H=5**: N=96 | Mean=1.6138 | CI=[-0.7359, 3.9635] | Effect=0.137 | Skew=-0.41 | Kurt=1.33
- **H=10**: N=96 | Mean=2.2372 | CI=[-1.0477, 5.5222] | Effect=0.136 | Skew=-0.44 | Kurt=1.10
- **H=20**: N=96 | Mean=3.3295 | CI=[-0.5653, 7.2243] | Effect=0.171 | Skew=-0.16 | Kurt=1.96
- **H=40**: N=96 | Mean=2.4262 | CI=[-2.9809, 7.8333] | Effect=0.090 | Skew=-0.43 | Kurt=0.77

### XAGUSD
- **Experiment ID**: experiment_000016

#### Bullish Exhaustion (Expecting Negative Means)
- **H=5**: N=99 | Mean=0.0498 | CI=[-0.0014, 0.1010] | Effect=0.192 | Skew=1.30 | Kurt=6.24
- **H=10**: N=99 | Mean=0.0751 | CI=[0.0121, 0.1381] | Effect=0.235 | Skew=1.31 | Kurt=2.97
- **H=20**: N=99 | Mean=0.0720 | CI=[0.0042, 0.1399] | Effect=0.209 | Skew=0.94 | Kurt=1.64
- **H=40**: N=99 | Mean=0.0511 | CI=[-0.0450, 0.1472] | Effect=0.105 | Skew=-0.92 | Kurt=7.15

#### Bearish Exhaustion (Expecting Positive Means)
- **H=5**: N=103 | Mean=0.0362 | CI=[-0.0104, 0.0827] | Effect=0.150 | Skew=-0.66 | Kurt=5.77
- **H=10**: N=103 | Mean=0.0116 | CI=[-0.0443, 0.0675] | Effect=0.040 | Skew=-0.65 | Kurt=6.23
- **H=20**: N=103 | Mean=0.0204 | CI=[-0.0500, 0.0908] | Effect=0.056 | Skew=-0.22 | Kurt=0.52
- **H=40**: N=103 | Mean=0.0022 | CI=[-0.0967, 0.1012] | Effect=0.004 | Skew=-1.05 | Kurt=2.77

### EURUSD
- **Experiment ID**: experiment_000017

#### Bullish Exhaustion (Expecting Negative Means)
- **H=5**: N=118 | Mean=0.0001 | CI=[-0.0001, 0.0002] | Effect=0.083 | Skew=2.05 | Kurt=12.68
- **H=10**: N=118 | Mean=0.0001 | CI=[-0.0001, 0.0002] | Effect=0.061 | Skew=1.70 | Kurt=14.61
- **H=20**: N=118 | Mean=-0.0000 | CI=[-0.0002, 0.0002] | Effect=-0.013 | Skew=-0.17 | Kurt=4.28
- **H=40**: N=118 | Mean=0.0000 | CI=[-0.0002, 0.0002] | Effect=0.039 | Skew=0.28 | Kurt=2.25

#### Bearish Exhaustion (Expecting Positive Means)
- **H=5**: N=112 | Mean=0.0001 | CI=[0.0000, 0.0002] | Effect=0.235 | Skew=0.17 | Kurt=4.47
- **H=10**: N=112 | Mean=0.0002 | CI=[0.0001, 0.0003] | Effect=0.316 | Skew=1.22 | Kurt=4.95
- **H=20**: N=112 | Mean=0.0001 | CI=[-0.0000, 0.0003] | Effect=0.176 | Skew=0.55 | Kurt=4.02
- **H=40**: N=112 | Mean=0.0001 | CI=[-0.0000, 0.0003] | Effect=0.158 | Skew=1.41 | Kurt=5.35

### BTCUSD
- **Experiment ID**: experiment_000018

#### Bullish Exhaustion (Expecting Negative Means)
- **H=5**: N=471 | Mean=-2.9357 | CI=[-12.7144, 6.8430] | Effect=-0.027 | Skew=2.19 | Kurt=30.80
- **H=10**: N=471 | Mean=-0.7796 | CI=[-12.1739, 10.6147] | Effect=-0.006 | Skew=2.30 | Kurt=25.70
- **H=20**: N=471 | Mean=-5.4229 | CI=[-18.4062, 7.5603] | Effect=-0.038 | Skew=0.48 | Kurt=8.72
- **H=40**: N=471 | Mean=-2.8605 | CI=[-20.1964, 14.4754] | Effect=-0.015 | Skew=0.55 | Kurt=6.11

#### Bearish Exhaustion (Expecting Positive Means)
- **H=5**: N=138 | Mean=-22.3906 | CI=[-49.0896, 4.3084] | Effect=-0.140 | Skew=-2.37 | Kurt=7.33
- **H=10**: N=138 | Mean=-27.5022 | CI=[-64.7366, 9.7322] | Effect=-0.123 | Skew=-2.74 | Kurt=10.42
- **H=20**: N=138 | Mean=-35.5681 | CI=[-78.5096, 7.3734] | Effect=-0.138 | Skew=-2.66 | Kurt=9.24
- **H=40**: N=138 | Mean=-20.7341 | CI=[-64.4339, 22.9658] | Effect=-0.079 | Skew=-1.46 | Kurt=6.02

### NAS100
- **Experiment ID**: experiment_000019

#### Bullish Exhaustion (Expecting Negative Means)
- **H=5**: N=57 | Mean=6.2361 | CI=[-9.8649, 22.3371] | Effect=0.101 | Skew=2.41 | Kurt=8.65
- **H=10**: N=57 | Mean=-5.2171 | CI=[-24.2360, 13.8019] | Effect=-0.071 | Skew=0.02 | Kurt=1.92
- **H=20**: N=57 | Mean=7.6599 | CI=[-11.6092, 26.9290] | Effect=0.103 | Skew=0.51 | Kurt=3.76
- **H=40**: N=57 | Mean=16.8967 | CI=[-7.2850, 41.0785] | Effect=0.181 | Skew=0.50 | Kurt=1.64

#### Bearish Exhaustion (Expecting Positive Means)
- **H=5**: N=66 | Mean=-0.6632 | CI=[-16.0980, 14.7716] | Effect=-0.010 | Skew=1.34 | Kurt=14.16
- **H=10**: N=66 | Mean=-2.3890 | CI=[-17.8603, 13.0822] | Effect=-0.037 | Skew=1.49 | Kurt=13.78
- **H=20**: N=66 | Mean=6.7360 | CI=[-13.0479, 26.5199] | Effect=0.082 | Skew=0.75 | Kurt=9.43
- **H=40**: N=66 | Mean=12.7422 | CI=[-12.0334, 37.5178] | Effect=0.124 | Skew=1.06 | Kurt=8.02

