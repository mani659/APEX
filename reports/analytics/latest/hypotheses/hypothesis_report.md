# APEX Quant Research Framework - Hypothesis Discovery Report

**Generated:** 2026-07-27 14:53:31  
**Dataset Shape:** 2,000 rows x 116 columns  
**Total Hypotheses Discovered:** 624  

---

## 1. Executive Summary

This module automatically discovers statistically supported research hypotheses across numeric features, boolean indicators, market regimes, and trading sessions against label outcomes.

- **Total Hypotheses Discovered:** 624
- **Strongest Supported Hypothesis:** Regime good_execution (1 vs 0) -> future_return (confidence: 100.0)
- **Average Absolute Effect Size (Cohen's d):** 320513.2581
- **Inconclusive Findings:** 327 hypotheses
- **Top Predictor Features for Validation:** `good_execution, future_max_up, price_velocity, london, market_structure`

---

## 2. Strongest Supported Hypotheses (Top 10)

Hypotheses ranked by statistical confidence score (0.40 * correlation + 0.30 * effect_size + 0.30 * t_stat_scale):

| hypothesis | category | predictor | target | cohen_d | pct_improvement | sample_size | confidence_score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Regime good_execution (1 vs 0) -> future_return | Regime -> Label | good_execution | future_return | 1.689 | 475.2 | 2000 | 100 |
| Regime good_execution (1 vs 0) -> future_direction | Regime -> Label | good_execution | future_direction | 1.634 | 217.5 | 2000 | 100 |
| Regime good_execution (1 vs 0) -> mfe | Regime -> Label | good_execution | mfe | 1.836 | 548.1 | 2000 | 100 |
| Regime good_execution (1 vs 0) -> mae | Regime -> Label | good_execution | mae | 1.206 | 64.65 | 2000 | 100 |
| Regime good_execution (1 vs 0) -> good_execution | Regime -> Label | good_execution | good_execution | 1e+08 | 1e+10 | 2000 | 100 |
| High vs Low price_velocity -> return | Numeric Feature -> Label | price_velocity | return | 3.153 |  | 1014 | 100 |
| High vs Low future_max_up -> mfe | Numeric Feature -> Label | future_max_up | mfe | 2.57 |  | 1000 | 100 |
| Session london (1 vs 0) -> mfe | Session -> Label | london | mfe | 1.011 | 261.4 | 2000 | 100 |
| Regime market_structure (2 vs -2) -> return | Regime -> Label | market_structure | return | 1.325 | 204.1 | 1432 | 100 |
| High vs Low future_max_down -> mae | Numeric Feature -> Label | future_max_down | mae | 5.104 |  | 1000 | 100 |


---

## 3. Weakest Supported Hypotheses (Bottom 10)

| hypothesis | category | predictor | target | cohen_d | pct_improvement | sample_size | confidence_score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| swing_high (True vs False) -> future_direction | Boolean Feature -> Label | swing_high | future_direction | 0.0044 | 0.47 | 2000 | 0.68 |
| liquidity_sweep_low (True vs False) -> mfe | Boolean Feature -> Label | liquidity_sweep_low | mfe | 0.0042 | 0.55 | 2000 | 0.64 |
| newyork (True vs False) -> return | Boolean Feature -> Label | newyork | return | 0.0027 | 64.85 | 2000 | 0.49 |
| lower_high (True vs False) -> mfe | Boolean Feature -> Label | lower_high | mfe | -0.0023 | -0.3 | 2000 | 0.43 |
| High vs Low price_acceleration -> mae | Numeric Feature -> Label | price_acceleration | mae | 0.0007 |  | 1002 | 0.36 |
| future_down (True vs False) -> return | Boolean Feature -> Label | future_down | return | 0.0018 | 36.7 | 2000 | 0.28 |
| High vs Low rsi_acceleration -> good_execution | Numeric Feature -> Label | rsi_acceleration | good_execution | 0 |  | 1000 | 0.18 |
| lower_high (True vs False) -> good_execution | Boolean Feature -> Label | lower_high | good_execution | -0.0008 | -0.12 | 2000 | 0.14 |
| Session overlap (0 vs 1) -> return | Session -> Label | overlap | return | 0.0006 | 14.76 | 2000 | 0.12 |
| overlap (True vs False) -> return | Boolean Feature -> Label | overlap | return | -0.0006 | -12.86 | 2000 | 0.08 |


---

## 4. Inconclusive Findings

Hypotheses showing weak effect sizes (|d| < 0.05) or low statistical confidence (< 20.0):

| hypothesis | category | predictor | target | cohen_d | confidence_score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| High vs Low hour -> future_direction | Numeric Feature -> Label | hour | future_direction | -0.1454 | 19.87 |
| Session overlap (0 vs 1) -> good_execution | Session -> Label | overlap | good_execution | 0.0886 | 19.85 |
| ema_stack_bull (True vs False) -> return | Boolean Feature -> Label | ema_stack_bull | return | 0.1253 | 19.66 |
| High vs Low upper_wick -> future_return | Numeric Feature -> Label | upper_wick | future_return | 0.1362 | 19.41 |
| swing_high (True vs False) -> return | Boolean Feature -> Label | swing_high | return | 0.1244 | 19.32 |
| bear_fvg (True vs False) -> future_return | Boolean Feature -> Label | bear_fvg | future_return | 0.145 | 19.19 |
| overlap (True vs False) -> future_direction | Boolean Feature -> Label | overlap | future_direction | -0.1277 | 19 |
| High vs Low rsi_21 -> future_direction | Numeric Feature -> Label | rsi_21 | future_direction | -0.1327 | 18.86 |
| High vs Low range_pct -> future_return | Numeric Feature -> Label | range_pct | future_return | 0.1297 | 18.51 |
| High vs Low roc_10 -> mae | Numeric Feature -> Label | roc_10 | mae | -0.1313 | 18.07 |


---

## 5. Features Requiring Further Validation

The following predictor features appear most frequently among the highest-confidence hypotheses:
- `good_execution, future_max_up, price_velocity, london, market_structure`

---

## 6. Recommended Next Experiments

1. **Conduct Feature Importance & SHAP Ranking:** Target top predictor features (`good_execution, future_max_up, price_velocity`) in the Feature Importance module to evaluate non-linear predictive contribution.
2. **Analyze Parameter Surfaces:** Evaluate parameter stability across surface slices for high-effect hypotheses.
3. **Prune Redundant Predictors:** Cross-reference weak or inconclusive features with Correlation Analysis to streamline feature sets.
