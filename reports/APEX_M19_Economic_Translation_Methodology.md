# APEX M19: Economic Translation Methodology Design

## 1. Scientific Objective
M17-R2 demonstrated that the `HIGH_VOL` duration is conditionally predictable at onset. M19 establishes the methodology to answer whether this statistical persistence prediction maps to a materially different future realized-volatility path. 

## 2. Methodology Rules

### Prediction Representation
M19 will consume the raw continuous predicted relative risk score (`conditional_risk_score`) generated strictly out-of-sample in M17-R2. Higher scores indicate shorter expected persistence. No arbitrary quantile bucketing will be used.

### Realized Volatility Definition
The standard annualized standard deviation of M15 logarithmic returns, measured exclusively over the forward window.

### Primary Horizon & Leakage Boundary
- **Prediction Boundary (`t`)**: Close of the `HIGH_VOL` onset M15 bar.
- **Outcome Window**: `[t+1, t+48]` (Forward 12 hours).

### Baseline
The unconditional distribution and mean of the forward 12-hour RV for all `HIGH_VOL` episodes, ignoring their predicted risk score.

### Statistical Framework & Effect Measure
A continuous-outcome regression evaluating the translation linkage:
$Forward\_RV_{12h} = \alpha + \beta \times Conditional\_Risk\_Score + \epsilon$
The primary effect measure is the slope coefficient ($\beta$). 

### Dependence Treatment
Because multiple `HIGH_VOL` episodes can trigger within 12 hours of each other, overlapping forward windows will create autocorrelated error terms. M19 will utilize Newey-West HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors to prevent artificially inflated significance.

### Multiple Testing Safeguards
- Primary horizon: 12h (Frozen)
- Secondary horizons: 4h, 24h (Descriptive only)
- Robustness: Spearman rank correlation (to check if the relationship is monotonic despite non-linearity).

## 3. Falsification Framework
- **Translation supported**: The slope coefficient ($\beta$) is statistically significant under HAC robust errors, and the Spearman rank correlation supports a monotonic relationship.
- **Translation not established**: The coefficient is indistinguishable from zero, meaning predicted duration does not correlate with actual realized variance magnitude.

## 4. M20 Prerequisites
Before execution, M20 must validate:
1. M17 prediction vector integrity.
2. Timestamp alignment (strict isolation of `t+1`).
3. Correct Newey-West implementation.
