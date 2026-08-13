# RC007 Study 005: Permission Layer Attrition & Entry Bottleneck Audit

**Status:** Completed
**Classification:** E - Data / Measurement Problem

## Objective
Study 004 produced a critical negative result: 5,957 behavioral events detected on the canonical EURUSD dataset, with 0 events reaching execution. The objective of this study was to diagnostically determine why behavioral events were eliminated and verify whether the frozen behavioral primitives contained any executable edge.

## Findings
The study found that the zero-execution result was an artifact of the test harness (`research/run_rc007_study004.py`). The simulation runner was hardcoded to pass `volume=1` for every bar. The `ContextInterpretation` logic relies on finding volumes strictly below the 25th percentile. With all volumes being equal, the percentile was identical to the current volume, rendering the `<` condition impossible. Consequently, all 5,957 events were incorrectly classified as `HIGH_ENTROPY` and rejected before even reaching the stabilization permission layer.

Additionally, the audit of the architecture uncovered multiple implementation mismatches:
1. `ExecutionPermission` computes the difference between current and previous close instead of the actual candle body `abs(open-close)`.
2. `runtime.py` bypasses `ContextInterpretation` during the wait period, hardcoding `LOW_ENTROPY`.

## Deliverables
- `reports/RC007_Study_005_Permission_Audit_Report.md`: Full audit results, opportunity conservation matrix, and discrepancies.
- `reports/RC007_Study_005_Attrition_Analysis.csv`: (Empty) No events reached stabilization to undergo attrition.

## Next Steps
Study 004 is methodologically invalid. An engineering fix is required to pass correct volume data and repair the `ExecutionPermission` mathematics before Study 004 can be re-run.
