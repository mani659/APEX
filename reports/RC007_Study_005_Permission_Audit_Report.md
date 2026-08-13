# RC007 Study 005: Permission Layer Attrition & Entry Bottleneck Audit

## Executive Summary

Study 004 produced a critical negative result: 5,957 behavioral events were detected, but 0 reached execution. 

This Study 005 diagnostic audit has determined that the 0-execution result is **not** a genuine scientific finding about the frozen behavioral phenomenon, nor is it an overly restrictive permission rule. 

Instead, it is caused by a **Data / Measurement Problem (Category E)** combined with an **Implementation Mismatch (Category C)**.

Specifically:
1. **The Measurement Problem:** The test harness used for Study 004 (`research/run_rc007_study004.py`) hardcodes `volume=1` for all historical bars. 
2. **The Bottleneck:** Because all bars have identical volume (1.0), the 25th percentile of the volume lookback window is always exactly 1.0. The `ContextInterpretation` logic requires `current_volume < percentile`. Since `1.0 < 1.0` is False, 100% of events are classified as `HIGH_ENTROPY`.
3. **The Attrition:** The `runtime.py` engine correctly rejects all `HIGH_ENTROPY` events before they ever reach the `ExecutionPermission` stabilization layer. 

Therefore, 100% of the 5,957 events were rejected at the Interpretation layer (Entropy filter), and exactly 0 events reached Stabilization.

Furthermore, several critical Implementation Mismatches were found in the `ExecutionPermission` layer itself, meaning even if events had reached it, the stabilization mathematics do not conform to the expected logic (using close-to-close difference instead of candle body).

---

## Study 004 Baseline & Opportunity Conservation Table

For all 5,957 behavioral events detected in the canonical dataset run via `run_rc007_study004.py`, the exact accounting chain is as follows:

| State | Count | % of Events |
|-------|------:|------------:|
| EVENT_DETECTED | 5,957 | 100.00% |
| LOW_ENTROPY | 0 | 0.00% |
| HIGH_ENTROPY | 5,957 | 100.00% |
| WAIT | 0 | 0.00% |
| REJECT_HIGH_ENTROPY | 5,957 | 100.00% |
| REJECT_TIMEOUT | 0 | 0.00% |
| REJECT_PERMISSION | 0 | 0.00% |
| EXECUTE | 0 | 0.00% |

**Reconciliation:** The counts perfectly reconcile. 5,957 events were detected, and exactly 5,957 were rejected as `REJECT_HIGH_ENTROPY`. 0 opportunities proceeded.

---

## Permission Attrition & Stabilization Analysis

Because 100% of events were rejected prior to Stabilization, exactly 0 events entered `WAIT`.

Consequently:
- **Stabilization Attrition:** Empty dataset (0 candidates).
- **Distance-to-Threshold Analysis:** Empty dataset (0 candidates).
- **Temporal Analysis:** Median bars until rejection is exactly 0 bars (immediate rejection upon detection).

The 240-bar `MODEL_D_OBSERVE` window had absolutely no impact on the zero-execution result. The events never reached the execution engine.

---

## Implementation Conformance Audit

The audit of the frozen `ExecutionPermission` and `ContextInterpretation` logic against the expected architecture revealed several critical discrepancies:

### 1. Hardcoded Volume in Measurement Harness
The `run_rc007_study004.py` harness uses a hardcoded `volume=1`. This completely breaks the participation classification which relies on a 25th percentile volume threshold.

### 2. Stabilization Mathematics Discrepancy (Major)
In `ExecutionPermission.confirm_stabilization`, the calculation for the current bar body is implemented as:
`current_bar_body = abs(snapshot.closes[-1] - snapshot.closes[-2])`
This measures the absolute return (delta between current close and previous close), **not** the candle body size (`abs(open - close)`). This fundamentally violates standard stabilization mathematics. 

### 3. State Transition Flaw during WAIT
In `runtime.py`, when an event enters `WAIT` (setting `self.is_waiting_stabilization = True`), subsequent bars bypass step 1 and 2, jumping straight to:
`perm_state = self.exec_perm.confirm_stabilization(snapshot, ParticipationState.LOW_ENTROPY)`
It hardcodes `ParticipationState.LOW_ENTROPY`, meaning the engine completely ignores whether volume expands heavily (high entropy) during the waiting period. The participation layer is bypassed for all wait bars.

---

## Isolation-Mode Conformance Audit

The `ENTRY_ISOLATION` mode in `runtime.py` successfully removes grid/basket expansion as requested. It correctly halts after 1 active position and utilizes `ExperimentalExitManager`.

However, the architecture intends for `ENTRY_ISOLATION` to not modify upstream behavior. It largely succeeds, but because it copies the buggy sequence from NORMAL mode, the signal observation and permission calculations share the same flawed transitions (such as skipping participation re-evaluation during `WAIT`).

---

## Scientific Interpretation & Decision Tree

### **Decision Classification:** E — Data / Measurement Problem (and C — Implementation Mismatch)

The zero-execution result of Study 004 is fundamentally invalid. It is not a genuine negative scientific result (A), nor is it an over-constraint of the permission logic (B). 

It is directly caused by a **Data/Measurement Problem (E)**—the simulation runner failed to feed volume data into the engine. Because of this, the entropy filter mechanically rejected 100% of candidates. 

Additionally, the audit uncovered **Implementation Mismatches (C)** in how the `ExecutionPermission` calculates bar bodies and handles state transitions during the wait phase.

---

## Recommended Next Study

Before proceeding with parameter modifications or further scientific analysis, the engineering foundation must be repaired.

**Recommendation: Authorize an Engineering Sprint to address the following:**
1. Fix `run_rc007_study004.py` to extract and pass actual `volume` values from the Parquet dataset rather than hardcoding `1`.
2. Correct `ExecutionPermission` to use standard candle body calculation (`abs(open - close)`), which requires `MarketSnapshot` to store opens, not just closes.
3. Fix the state machine in `runtime.py` so that wait-state bars correctly re-evaluate the participation state rather than hardcoding `LOW_ENTROPY`.

After these fixes, Study 004 must be re-run to establish a valid baseline.
