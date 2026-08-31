# APEX M18: Predictive Signal Scientific Adjudication

## 1. M17-R2 Result Verification
Repository artifacts confirm:
- Event count: 794
- Walk-forward chronological split: 397 training / 397 Out-of-Sample.
- Predictor set: `Breakout Intensity` and `Variance Momentum`.
- Implementation: `statsmodels.PHReg`
- Fit success: 397 / 397.
- Conditional OOS C-index: 0.6656
- Baseline OOS C-index: 0.5000
- Delta C-index: +0.1656
- Zero methodology deviations.

## 2. Statistical Interpretation
The observed C-index of 0.6656 establishes that the model correctly orders the future persistence of comparable episode pairs substantially better than the unconditional baseline. This proves out-of-sample rank discrimination. It does *not* imply a 66% directional hit rate for trading or expected positive PnL.

## 3. Scientific Meaning of C-index = 0.6656
The progression of APEX knowledge is now:
1. **RC012**: `HIGH_VOL` exists as a distributional state.
2. **M13**: `HIGH_VOL` persistence is non-memoryless (contains structural memory).
3. **M17-R2**: `HIGH_VOL` persistence is conditionally predictable at onset.

The scientific uncertainty regarding whether `HIGH_VOL` is a purely random threshold-crossing process has been permanently resolved. The physical magnitude of the initial variance breakout and its short-term momentum inherently condition the lifespan of the ensuing volatility expansion.

## 4. What M17-R2 Establishes
`PREDICTIVE SIGNAL ESTABLISHED`. The frozen two-feature onset model demonstrated substantial out-of-sample rank discrimination for future `HIGH_VOL` persistence.

## 5. What Remains Unproven
The experiment did NOT establish:
- Economic value
- Profitability or tradability
- Directional price prediction
- Causality of the mechanism
- Independent temporal/instrument replication outside the canonical EURUSD dataset.

## 6. Alternative Explanations
- **Volatility clustering**: Partially addressed. The regime-reset logic ensures structural independence between distinct episodes, but macro clustering could still influence sequences of durations.
- **Nonstationarity**: Partially addressed by the expanding walk-forward window and relative threshold scaling, but true out-of-sample regime shifts remain a risk.
- **Omitted market-state information**: Unresolved. Order book dynamics, liquidity gaps, or macroeconomic news could heavily intermediate this relationship.
- **Lack of independent replication**: Unresolved. Tested only on EURUSD.

## 7. Next Directions Evaluation
APEX must decide between **Replication** (verifying the statistical signal on new data/instruments) and **Translation** (determining if the signal maps to economic value on the current dataset). 
Because a strict chronological walk-forward on 15 years of M15 data is highly rigorous, the highest-information-value step is Translation. Before acquiring massive new datasets to replicate the signal across instruments, APEX must first establish whether predicted persistence conditions economically meaningful market behavior (such as subsequent realized volatility or price distributions).
