# APEX M15: Conditional Predictability Methodology Design

## 1. Core Research Question
**Is the persistence of a newly triggered HIGH_VOL episode predictable from market-state information available strictly before or at the onset bar?**

## 2. Prediction Boundary
**Option A: Information available through the CLOSE of the onset bar ($t_{onset}$).**
- *Rationale*: The `HIGH_VOL` onset is strictly defined as the exact bar where $RV20$ (calculated on close) crosses above the 80th percentile threshold. Therefore, the market-state at the exact moment the episode mathematically exists requires the close of $t_{onset}$. No predictor may utilize data from $t_{onset+1}$ or later.

## 3. Target Definition
The target variable is the **episode duration**, explicitly defined as the number of contiguous M15 bars from $t_{onset}$ to termination, preserving the frozen M11-Backup event ledger constraints. 
- *Representation*: **Survival Framework (Time-to-Event)**.

## 4. Primary Predictor Set
To prevent feature mining and overfitting, the candidate set is restricted to three deterministically computable, theoretically grounded variance dynamics:
1. **Breakout Intensity**: $RV20_{onset} / Threshold80_{onset}$. The proportional distance the onset variance exceeded the critical threshold.
2. **Variance Momentum**: $RV20_{onset} - RV20_{onset-4}$. The slope/acceleration of variance entering the episode (1-hour momentum).
3. **Regime Depth**: $RV20_{onset} / Threshold50_{onset}$. The proportional distance from the baseline median reset level.

## 5. Baseline & Null Hypothesis
- **Baseline Model**: An unconditional (intercept-only) survival model (representing the empirical hazard without predictors).
- **Null Hypothesis**: The conditional predictor model yields an out-of-sample Concordance Index equal to or worse than random guessing ($C \le 0.50$). The predictors provide zero predictive information beyond the unconditional baseline.

## 6. Model Framework
**Cox Proportional Hazards Model.**
- *Rationale*: It directly models the hazard rate (termination risk) conditionally on the predictors without assuming a specific parametric shape for the baseline hazard. It is highly interpretable, yielding specific directional coefficients (hazard ratios).

## 7. Out-of-Sample Design
**Walk-Forward Evaluation (Expanding Window).**
- *Initial Training Window*: First 50% of chronological episodes.
- *Testing Window*: The subsequent episode. The training window is then expanded chronologically.
- *Rationale*: Strictly preserves temporal sequencing and prevents future lookahead, while continually adapting to potential non-stationarity.

## 8. Leakage Controls
Any feature transformations (e.g., standardization) must be fitted strictly inside the expanding training window. The out-of-sample test episode must be scaled using parameters computed exclusively from its past.

## 9. Primary Predictive Metric
**Harrell's Concordance Index (C-index)** on the out-of-sample predictions.
- *Rationale*: It is the standard discriminative metric for survival models. It evaluates whether the model correctly ranks the persistence of episodes (a C-index of 0.5 is random; 1.0 is perfect).

## 10. Multiple Testing Controls
Exactly one primary model (Cox PH) utilizing all three predictors simultaneously will be evaluated. Feature selection via out-of-sample correlation is strictly prohibited. 

## 11. Missing Data & Dependence
- **Missing Data**: Handled by the existing M12 deterministic resampling and 252-day warm-up. Incomplete episodes are right-censored.
- **Dependence**: The Regime Reset rule adequately resolves inter-episode dependence by forcing the process to return to the 50th percentile baseline before a new episode can trigger. The survival model assumes episodes are conditionally independent.
