# RC015 Study 007 — Stage-2 BBO Recovery Report

## 1. Scope & Execution
- **Original Row Count**: 997,986
- **Recovery Row Count**: 3,306
- **Merged Row Count**: 1,001,292
- **Recovered Timestamp Intervals**: 2022-04-27 (Full), 2025-12-24 (18:45-Close), 2025-12-31 (21:59-Close)

## 2. Integrity Revalidation
### Instrument Completeness
- Option IDs: 699 / 699
- Futures IDs: 19 / 19
- Missing IDs: 0

### Event Completeness
- Events: 222 / 222
- Fully covered Wednesday windows: 222 / 222
- Completely missing windows: 0
- Partial windows: 0

### Contamination
- Unexpected options: 0
- Unexpected futures: 0
- MLEG/spreads: 0

### Observation Slots
21,312 / 21,312 observation slots technically covered

### Quote Integrity
- valid bid count: 988,382
- valid ask count: 994,413
- zero/negative sizes: 12,910 bids, 6,879 asks
- bid > ask: 295
- duplicate timestamps: 696,113
- timestamp ordering: 0
- structurally malformed rows: 0

## 3. Final Classification
### PASS — ACQUISITION FULLY RECOVERED
699/699 option IDs present, 19/19 futures IDs present, and 222/222 event windows fully covered.
