# APEX M20-CR: Methodology Completeness Review

## 1. Resolution of Unresolved Parameters
M20 correctly suspended empirical execution because M19 failed to hardcode three mathematical parameters, creating the risk of outcome-dependent selection. This review resolves them ex-ante.

### A. Annualization Convention
The underlying data is EURUSD, a 24/5 continuous Forex market. A 365-day calendar convention mathematically suppresses the annualized volatility figure because it divides true trading volatility over 104 weekend days where the market is frozen. The standard and correct convention is the 252-day trading year. 
- M15 periods per trading day = 96.
- Trading days per year = 252.
- `N_annual` = $96 \times 252 = 24,192$.
- The frozen calculation is: $RV = Standard\_Deviation \times \sqrt{24192}$.

### B. Newey-West HAC Lag Truncation
Newey-West corrects for serial correlation in the error terms. In this methodology, the dominant source of serial correlation is the overlapping 12-hour (48-bar) forward window between closely clustered `HIGH_VOL` episodes. Because the structural span of this induced overlap is mechanically capped at the forward window length, the theoretically optimal lag length is exactly the window size.
- `maxlags` = 48.

### C. Inferential Alpha and Tail
M19 did not stipulate whether a higher risk score (shorter duration) should lead to higher or lower variance. It merely asked if it translates to a "materially different" state.
- **Null Hypothesis ($H_0$)**: $\beta = 0$.
- **Alternative Hypothesis ($H_1$)**: $\beta \neq 0$.
- **Alpha**: 0.05.
- **Tail**: Two-sided.

## 2. Methodology Status
All researcher degrees of freedom are now permanently closed. M21 is fully defined.
