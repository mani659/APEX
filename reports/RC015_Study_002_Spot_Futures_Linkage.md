# RC015 Study 002 - Spot / CME Futures Temporal Linkage Audit

## 2. Determine Why Overlap Was Zero
- Apex EURUSD timestamp datatype: `datetime64[us]`
- Apex EURUSD timezone localization: `Naive (assumed UTC)`
- CME 6EZ6 timestamp datatype: `str` parsed to `datetime64[ns, UTC]`
- CME 6EZ6 timezone localization: `UTC`

Example timestamps:
```text
Apex EURUSD:
2026-06-30 23:59:00

CME 6EZ6:
2026-08-12T00:00:00.000000000Z
```

**Date Range Diagnosis:**
- Apex EURUSD coverage: `2021-01-04 00:00:00+00:00` to `2026-06-30 23:59:00+00:00`
- CME 6EZ6 coverage: `2026-08-12 00:00:00+00:00` to `2026-08-12 23:56:00+00:00`

The apparent zero overlap is **NOT** caused by a datatype or formatting mismatch. It is a **genuine temporal separation**. The Apex historical dataset does not share any date overlap with the sampled CME real market data.

## 3. Normalize to UTC
Apex timestamps were explicitly localized to UTC using `.dt.tz_localize('UTC')`. CME timestamps were parsed and converted to `UTC`.

## 4. Normalize to M1 Boundaries
Both datasets were normalized to exact minute boundaries using `.dt.floor('1Min')` to create a common `m1_key`.

## 5. Actual Overlap
- Exact timestamp intersection count: `0`
- Overlap percentage of Apex observations: `0.0000%`
- Overlap percentage of CME observations: `0.0000%`

**CRITICAL HALT**: Overlap remains identically zero due to disjoint date ranges. Cannot proceed with Basis Analysis (Step 6-10).

## 12. Final Classification
### NOT LINKED
A reliable temporal/basis mapping cannot be established because the datasets physically do not overlap in time. The Apex data ends on 2026-06-30, whereas the CME sample is from 2026-08-12.
