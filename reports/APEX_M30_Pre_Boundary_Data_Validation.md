# APEX M30: Pre-Boundary Data Validation

## 1. Objective
The M30 milestone executes a structural data audit to ensure that the frozen M29 Dispersion Boundary methodology can be implemented on the existing canonical dataset without future data leakage, indexing errors, or statistical misalignment.

## 2. Validation Findings

### A. Prediction Vector & Boundary Alignment
- **Prediction Vector**: The 397 original `conditional_risk_score` predictions from M17-R2 loaded successfully.
- **Data Availability**: Out of 397 episodes, 396 contain a mathematically complete 48-bar forward window. (The 397th is cleanly dropped due to dataset boundary exhaustion).

### B. RV20 Extraction and Boundary Construction
- **RV20_onset**: The calculation logic verified that the standard historical 20-period log-return variance (RV20) can be securely computed entirely on the data *prior* to and including $t$.
- **Boundary $B_t$**: The formula $B_t = 1.0 \times \text{RV20}_{onset}$ correctly constructed a discrete, unoptimized numerical threshold representing a purely localized definition of expected variance. 
- **Binary Indicator $I_i$**: The logical test `1 if MAE_abs >= B_t else 0` accurately mapped the continuous excursion array into a discrete state boundary, rigorously converting physical distance to a binary economic state condition.

### C. Software & Statistical Feasibility
A synthetic data smoke test proved that the local statistical environment correctly executes the **Linear Probability Model**:
- `statsmodels.OLS` continuous outcome regression applied to a binary target variable `[0, 1]`.
- Newey-West HAC covariance explicitly hardcoded to `maxlags=48`, confirming that LPM natively preserves the APEX serial-dependence framework without needing specialized Generalized Method of Moments (GMM) software.
- Two-sided p-values and 95% Confidence Intervals at $\alpha = 0.05$.

## 3. Leakage Audit
**PASS**. The array construction logically bifurcates the onset state ($P_t$ and $RV20_t$) from the future array ($P_{t+1 \dots t+48}$). The boundary threshold $B_t$ is constructed blindly before the $MAE_{abs}$ search executes. There is zero structural leakage.

## 4. Capital Requirement Distinction
The methodology clearly tests **spatial boundary exhaustion**, meaning the frequency that a market unit crosses a synthetic boundary line. It explicitly does not model the drawdown path, margin lockup, grid sequence, or negative drift of transaction costs required for a capital-requirement simulation. 

## 5. Conclusion
The M29 methodology is perfectly aligned with the M15 canonical data structure. The threshold logic correctly leverages the existing pre-onset variance state, and the LPM HAC framework is technically robust. M31 is cleared for empirical execution.
