# APEX M12 Pre-Economic Data Validation

## 1. Objective
To determine whether the M11 frozen methodology can be implemented perfectly on the existing APEX canonical dataset without new external data, lookahead, or methodological modifications.

## 2. Canonical Data Verification
- **Source**: `data/m1/EUR/EURUSD_*.csv` (67 historical monthly files).
- **Processing**: Successfully parsed 2,246,730 M1 rows and deterministically resampled to 136,787 M15 rows.
- **Result**: Core historical OHLCV data is strictly available and complete.

## 3. HIGH_VOL Observability
- **Metric**: RV20 (20-period standard deviation of log returns).
- **Threshold**: The 80th percentile calculates deterministically (0.000563) on the full sample.
- **Result**: The frozen RC012 HIGH_VOL definition is perfectly reproducible without ambiguity.

## 4. Session & DST Observability
- **Metric**: `ASIA_TO_LONDON` and `LONDON_NY_OVERLAP` windows.
- **Finding**: Static hour boundaries (07:00-09:00 and 12:00-16:00 UTC) can be applied. However, without a dedicated historical Daylight Saving Time (DST) mapping for NY and London in the repository, the precise session boundaries will drift by 1 hour during non-aligned DST periods.
- **Result**: Timezone boundaries are conditionally observable but contain a structural limitation regarding precise historical DST edges.

## 5. Event Construction & Independence
- **Rule**: Minimum 12-bar separation between episodes.
- **Result**: Deterministic and fully implementable. 
- **Total Count**: 1,182 discrete HIGH_VOL episodes successfully extracted from the 5.5-year history.

## 6. Exposure & Control Classification
- **Rule**: Onset bar falls inside (Exposure) vs outside (Control) the transition windows.
- **Result**: Both populations are unambiguous to classify.

## 7. Sample Adequacy
The M11 requirement of ≥200 episodes in both cohorts is easily satisfied:
- **Exposure (Session-Transition) Episodes**: 336
- **Control (Off-Peak) Episodes**: 846

## 8. Macro-Event Exclusion (FATAL BLOCKER)
- **Requirement**: M11 requires excluding NFP/FOMC events to prevent macro-shock confounding.
- **Finding**: No historical economic calendar or macro-event timestamp data exists natively within the APEX repository.
- **Result**: UNAVAILABLE / BLOCKED. We cannot exclude these events without acquiring new external data.

## 9. Lookahead Audit
- The logic strictly defines `HIGH_VOL` at bar `t` using RV20 from `[t-19, t]`.
- Session mapping depends solely on the known timestamp of `t`.
- Forward 12-bar measurements do not leak backward into the classification step.
- **Result**: PASS. No lookahead violations detected.

## 10. Gate Decision
**BLOCKED — DATA / OBSERVABILITY**

**Reason**: The methodology requires NFP/FOMC exclusions to preserve the validity of the structural comparison (separating endogenous session mechanics from exogenous macro shocks). The timestamps for these macro events do not exist in the local repository. 

**Control Session Action Required**: The control session must either authorize the external acquisition of an NFP/FOMC historical calendar or explicitly amend the frozen M11 methodology to accept macro-event confounding as a known limitation. M13 is blocked until this is resolved.
