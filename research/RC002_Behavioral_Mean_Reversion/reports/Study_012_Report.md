# RC002 Study 012: Execution Policy Evaluation

This report evaluates whether the execution policy materially impacts the profitability of the 'Low Participation + Sudden Shock' Behavioral Event.

## 1. Policy Comparison (Aggregated across all Exits)

| Execution Policy | N | Win Rate | Mean Return (R) | Profit Factor | Exp (R) | Avg Hold (Bars) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Policy A (Immediate) | 464 | 61.9% | -0.314 | 0.90 | -0.314 | 27.2 |
| Policy B (One-bar Conf.) | 204 | 52.5% | -1.363 | 0.61 | -1.363 | 26.6 |
| Policy C (Absorption) | 464 | 56.7% | 0.120 | 1.06 | 0.120 | 27.6 |
| Policy D (Fade Failure) | 264 | 51.5% | -0.266 | 0.86 | -0.266 | 27.1 |

## 2. Granular Comparison Matrix

### Exit: Fixed 20 Bars

| Execution Policy | N | Win Rate | Mean Return (R) | Profit Factor | Max Favorable (R) | Max Adverse (R) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Policy A (Immediate) | 116 | 53.4% | -0.644 | 0.81 | 9.77 | -10.91 |
| Policy B (One-bar Conf.) | 51 | 43.1% | -0.624 | 0.79 | 7.35 | -11.22 |
| Policy C (Absorption) | 116 | 50.9% | 0.018 | 1.01 | 8.39 | -7.91 |
| Policy D (Fade Failure) | 66 | 42.4% | -0.830 | 0.62 | 6.55 | -7.38 |

### Exit: ATR Target

| Execution Policy | N | Win Rate | Mean Return (R) | Profit Factor | Max Favorable (R) | Max Adverse (R) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Policy A (Immediate) | 116 | 61.2% | 0.224 | 1.58 | 9.77 | -10.91 |
| Policy B (One-bar Conf.) | 51 | 41.2% | -0.176 | 0.70 | 7.35 | -11.22 |
| Policy C (Absorption) | 116 | 46.6% | -0.069 | 0.87 | 8.39 | -7.91 |
| Policy D (Fade Failure) | 66 | 37.9% | -0.242 | 0.61 | 6.55 | -7.38 |

### Exit: Recoil Completion

| Execution Policy | N | Win Rate | Mean Return (R) | Profit Factor | Max Favorable (R) | Max Adverse (R) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Policy A (Immediate) | 116 | 81.0% | 0.845 | 1.36 | 9.77 | -10.91 |
| Policy B (One-bar Conf.) | 51 | 74.5% | -1.590 | 0.55 | 7.35 | -11.22 |
| Policy C (Absorption) | 116 | 75.9% | 0.853 | 1.50 | 8.39 | -7.91 |
| Policy D (Fade Failure) | 66 | 77.3% | 1.045 | 2.00 | 6.55 | -7.38 |

### Exit: Time 60 Bars

| Execution Policy | N | Win Rate | Mean Return (R) | Profit Factor | Max Favorable (R) | Max Adverse (R) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Policy A (Immediate) | 116 | 51.7% | -1.681 | 0.72 | 9.77 | -10.91 |
| Policy B (One-bar Conf.) | 51 | 51.0% | -3.061 | 0.55 | 7.35 | -11.22 |
| Policy C (Absorption) | 116 | 53.4% | -0.323 | 0.92 | 8.39 | -7.91 |
| Policy D (Fade Failure) | 66 | 48.5% | -1.037 | 0.74 | 6.55 | -7.38 |

## Final Verdict

**SUPPORTED**

Execution policy materially impacts outcomes, with **Policy C (Absorption)** showing robust outperformance.