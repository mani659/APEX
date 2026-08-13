# RC007 Study 006: Engineering Correction Report

## Summary
The engineering corrections requested by Study 006 have been fully implemented to repair the data and implementation defects identified in Study 005. 

## Defects Addressed

### 1. Study 004 Volume Data Bug
- **Defect:** `research/run_rc007_study004.py` hardcoded `volume = 1` for all bars.
- **Correction:** Extract the actual `volume` column from the DataFrame using `volume_col = [c for c in df.columns if 'volume' in c.lower()][0]`, and pass it to `runtime.on_bar`.
- **Affected Module:** `research/run_rc007_study004.py`
- **Regression Status:** SAFE. Existing logic untouched, actual volume flows into the engine.

### 2. MarketSnapshot Open Price Requirement
- **Defect:** `MarketSnapshot` did not provide `open` price needed to calculate true candle body.
- **Correction:** Added `opens: List[float]` to `MarketSnapshot`. Added an `opens` deque to `MarketDataLayer` to track `open_price`. Updated `update_bar` to track the open.
- **Affected Module:** `engine/core/market_data.py`
- **Regression Status:** SAFE. Data layer faithfully tracks open prices without altering existing attributes or ATR mathematics.

### 3. Stabilization Calculation Bug
- **Defect:** `ExecutionPermission` calculated the bar body as `abs(closes[-1] - closes[-2])` (the close-to-close difference).
- **Correction:** Modified the `is_new_bar` branch in `ExecutionPermission.confirm_stabilization` to calculate `abs(opens[-1] - closes[-1])`, yielding the true candle body.
- **Affected Module:** `engine/core/execution_permission.py`
- **Regression Status:** SAFE. Thresholds remain frozen at `< 0.5 * ATR`. Unit tests verify body calculations.

### 4. WAIT-State Participation Bug
- **Defect:** `engine/runtime.py` bypassed the participation check during `WAIT` and hardcoded `LOW_ENTROPY`.
- **Correction:** Replaced the hardcoded `ParticipationState.LOW_ENTROPY` with dynamic re-evaluation: `current_part_state = self.context_interp.evaluate_participation_state(snapshot, True)`.
- **Affected Module:** `engine/runtime.py` (both normal and isolation processing cycles)
- **Regression Status:** SAFE. The wait state correctly honors the participation layer based on actual volume data.
