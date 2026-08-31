# APEX M16: Conditional Predictability Pre-Economic Validation

## 1. Objective
To structurally validate the `APEX_M15_FROZEN_METHODOLOGY.md` without running the actual out-of-sample predictive experiment. This gate ensures that data boundaries, causal feature extraction, and software specifications are executable.

## 2. Canonical Data Verification
- **Dataset**: EURUSD M15 (Resampled from M1).
- **Match**: The extraction identically recovered the exact 794 `HIGH_VOL` episodes used in the M13 experiment. No data discrepancy found.

## 3. Prediction Boundary Audit
- **Boundary**: Exact close of $t_{onset}$.
- **Verification**: The Python extraction verified that `rv20_onset`, `thresh80_onset`, `thresh50_onset`, and `rv20_{onset-4}` are all 100% calculable exactly at the onset bar close. There is zero leakage of future $t_{onset+1}$ information or episode termination data. **PASS**.

## 4. Walk-Forward Segmentation
- **Training Set (Initial)**: 397 episodes.
- **Out-of-Sample Set**: 397 episodes.
- **Verification**: The 50% chronological split provides a massive out-of-sample testing ground. The sequential expanding-window architecture is technically feasible. **PASS**.

## 5. Cox PH Feasibility
- **Software**: The local python environment lacks the `lifelines` survival analysis package. This is a non-fatal prerequisite; `pip install lifelines` must be executed at the beginning of M17.
- **Model Size**: 397 training events per walk-forward fold is ample statistical power for a 3-feature Cox PH model.

## 6. Predictor Redundancy (FATAL BLOCKER)
- **Issue**: A severe mathematical collinearity exists in the frozen predictor set. 
- **Finding**: The correlation between `Breakout Intensity` ($RV20 / Threshold80$) and `Regime Depth` ($RV20 / Threshold50$) is **$\rho = 0.9886$**. 
- **Implication**: Because the 80th and 50th percentiles are drawn from the exact same trailing 252-day distribution, they are highly proportional. Including both in a Cox Proportional Hazards model will result in severe multicollinearity, causing matrix inversion failures, non-convergence, and unstable hazard coefficients. This renders the multivariate model mathematically invalid.

## 7. Gate Decision
**BLOCKED — METHODOLOGY**

The fundamental extraction, data bounds, and walk-forward splits are pristine. However, the model design requires an emergency Control Session review to amend the predictor set and resolve the $0.988$ collinearity before M17 can be executed.
