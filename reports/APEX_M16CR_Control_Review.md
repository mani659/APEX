# APEX M16-CR: Control Review of Predictor Redundancy & Cox Methodology

## 1. Structural Redundancy Assessment
M16 revealed a fatal correlation ($r = 0.9886$) between two of the pre-frozen predictors: `Breakout Intensity` and `Regime Depth`. 
Mathematically, this occurs because both variables normalize the contemporaneous onset variance ($RV20_{onset}$) by a trailing 252-day percentile. The ratio between the 80th and 50th percentiles of a massive rolling window is essentially a static scale factor in the short term. The variables are mathematically proportional and structurally encode the exact same physical property of the market state.

## 2. Impact on Cox Proportional Hazards Model
The inclusion of nearly deterministically collinear variables in a Cox PH model violates the requirement for an invertible Information/Hessian matrix during partial likelihood maximization. The model will either fail to converge or will produce highly unstable, meaningless hazard coefficients (infinite variance inflation). The redundancy is a fatal mathematical flaw, not just an inefficiency.

## 3. Variance Momentum Audit
`Variance Momentum` ($RV20_{onset} - RV20_{onset-4}$) measures the immediate trajectory/acceleration of variance heading into the breakout, rather than its absolute level. It is conceptually and algebraically orthogonal to the level ratios. It will remain in the methodology.

## 4. Null Hypothesis and Sample Audit
- The `C-index <= 0.50` null hypothesis remains a mathematically coherent and standard discriminative threshold for a survival model proving no predictability.
- The sample split (397 Train / 397 OOS) remains entirely robust and is uncompromised by dropping a redundant covariate. 

## 5. Technical Software Feasibility
The requirement to run `pip install lifelines` is a standard, non-violating environmental dependency resolution. It will be explicitly mandated at the start of M17.

## 6. Chosen Resolution
**Resolution B — Formally remove one redundant predictor.**
`Regime Depth` is dropped. `Breakout Intensity` is retained because measuring the magnitude of the breakout relative to the exact threshold that triggered it is conceptually tighter to the structural mechanism of the episode. This decision was made entirely through algebraic reasoning and matrix stability requirements, completely independent of predictive outcomes.
