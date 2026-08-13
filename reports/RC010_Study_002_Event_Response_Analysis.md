# RC010 Study 002 - Event-Response Discovery

## 1. Data Construction & Event Statistics
- **Methodology**: True calendar-aligned M15 OHLCV resampling (00:00, 00:15, etc.).
- **Total Events**: 27379
- **Response Overlap (4 bars)**: 18017 (65.8%)
- **Outcome Overlap (64 bars)**: 27378 (100.0%)

## 2. Response Classification Distributions & Baselines
| Response Class | N | % Pop | Mean 60 | Med 60 | MFE | MAE | Cont% | Rev% | Cohen D (A) | Cohen D (B) | Cohen D (C) | Early D | Mid D | Rec D |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| RECOIL | 10325 | 37.7% | -0.00003 | -0.00009 | 0.00309 | 0.00311 | 49.7% | 50.2% | 0.003 | 0.003 | 0.003 | -0.055 | 0.047 | 0.018 |
| CONTINUATION | 9546 | 34.9% | -0.00009 | -0.00008 | 0.00307 | 0.00312 | 49.4% | 50.5% | -0.011 | -0.011 | -0.011 | -0.076 | 0.022 | 0.023 |
| ABSORPTION | 2817 | 10.3% | 0.00005 | -0.00013 | 0.00311 | 0.00307 | 50.0% | 50.0% | 0.023 | 0.023 | 0.021 | -0.026 | 0.079 | 0.009 |
| PAUSE | 4691 | 17.1% | -0.00003 | -0.00003 | 0.00289 | 0.00297 | 48.9% | 51.0% | 0.003 | 0.003 | 0.003 | -0.048 | 0.037 | 0.021 |

## 3. Final Scientific Interpretation
**NEGATIVE RESULT**

No response classification consistently deviated from the event baselines (A, B, C) with sufficient magnitude and temporal stability. The immediate response after an expansion event does not appear to contain stable, predictive information beyond the event itself.
