# RC015 Study 004 — Maturity-Matched Implied vs Realized Variance Pilot

## 1. Feasibility Audit

### Data Coverage
- **Spot Data Available Until:** `2026-08-14 20:59:59 UTC` (Auxiliary MT5 Tick Sample)
- **Option BBO Data Timestamp:** `2026-08-12`

### Expiration Availability
An audit of the available BBO quotes on `2026-08-12` for outright options (`instrument_class` 'C' or 'P') reveals the following shortest available expirations:
1. `2026-09-04 14:00:00 UTC` (~23 days remaining)
2. `2026-10-09 14:00:00 UTC` (~58 days remaining)
3. `2026-11-06 15:00:00 UTC` (~86 days remaining)
4. `2026-12-04 15:00:00 UTC` (~114 days remaining)

*Note: While some instruments expire on `2026-08-14` or `2026-08-15` in the dataset, these are entirely `instrument_class = T` (combinations/spreads/MLEG) and NOT outright Calls or Puts.*

### Maturity Matching Constraint
The shortest valid outright option expires on **September 4th, 2026**. 
However, the available EURUSD spot dataset terminates strictly on **August 14th, 2026**.

Because the required option expiration occurs weeks after the available spot data ends, it is physically impossible to compute the true maturity-matched realized variance for its remaining life. 

Per mandatory constraints:
> **DO NOT extrapolate.**
> **DO NOT forward-fill.**
> **DO NOT use a shorter horizon and pretend it is maturity-matched.**

**Result:** `MATURITY-MATCHED REALIZED VARIANCE NOT AVAILABLE`

## 2. Final Classification
### CONDITIONAL
The methodology works logically, but the available spot-history window prevents complete maturity matching. The pilot cannot proceed without either:
1. Acquiring longer contiguous spot data extending past September 4, 2026.
2. Acquiring additional option quotes for shorter-dated contracts (e.g., 0-DTE or 2-DTE weekly options) that expire before August 14, 2026.
