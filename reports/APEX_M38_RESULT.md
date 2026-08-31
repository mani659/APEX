# APEX M38 RESULT

## Gate: PASS — All non-fatal limitations resolved

## Date: 2026-08-24

---

## 1. M38 Objective

Resolve the four non-fatal limitations identified in M37's pre-execution data validation, reconcile RC013 count discrepancies, and amend the frozen methodology to ensure M39 can execute the session-transition distributional asymmetry experiment without post-hoc methodological choices.

## 2. Resolutions

| Issue | M37 Finding | M38 Resolution | Status |
|---|---|---|---|
| A: Overlap exclusion | Position-based shifting may not handle DST | Time-based interval logic with strict inequality endpoint rule | ✅ FROZEN |
| B: Calendar exclusions | Good Friday/Thanksgiving/FOMC/ECB require external lists | Good Friday + Thanksgiving computable; FOMC/ECB downgraded to robustness check | ✅ RESOLVED |
| C: Bootstrap seed | Not frozen — results non-reproducible | Seed = 42 frozen; RNG = PCG-64 | ✅ FROZEN |
| D: Bootstrap purpose | Not stated — procedure ambiguous | Calibrate AD statistic uncertainty under H0; joint resampling | ✅ FROZEN |

## 3. Additional Findings

| Finding | Classification | Impact |
|---|---|---|
| AD test: `scipy.stats.anderson_ksamp` | COMPATIBLE | Smoke test passed; statistic + significance_level available |
| Decision rule: reject if significance_level < 0.05 | FROZEN | Consistent with M36 α=0.05 two-sided |
| Block bootstrap: 24, day-boundary, 10K, joint resampling | FROZEN | Purpose and seed now frozen; M36 spec confirmed |
| RC013 hourly count: 34,197 (M15) vs 34,199 (M1→1H) | NON-FATAL | +2 bars from edge effects; structure preserved |
| RC013 LNO count: 5,192 (M15) vs 2,950 (M1→1H) | NON-FATAL | Classification method difference; test valid regardless |
| FOMC/ECB exclusion | DOWNGRADED | Primary test proceeds without; ~7.4% of trading days; random distribution across treatment/control |

## 4. Degrees of Freedom — M38 Additions

| Decision | M36 Status | M38 Resolution |
|---|---|---|
| Bootstrap seed | NOT FROZEN | FROZEN: seed = 42 |
| Bootstrap purpose | NOT FROZEN | FROZEN: Calibrate AD uncertainty under H0 |
| Overlap exclusion method | NOT FROZEN | FROZEN: Time-based interval; strict inequality |
| FOMC/ECB exclusion | FROZEN (required) | AMENDED: Downgraded to robustness check |

## 5. Risks — M38 Additions

| Risk | Severity | Blocker |
|---|---|---|
| R13: Bootstrap seed non-reproducibility | Low | No |
| R14: Bootstrap purpose ambiguity | Low | No |
| R15: RC013 count discrepancy | Low | No |
| R16: FOMC/ECB date absence | Medium | No |

## 6. M39 Authorization

M39 is authorized to execute the frozen methodology as amended by M38. The following procedures are permitted:
- Compute session states using pytz (RC013 definitions)
- Construct forward returns (1H horizon)
- Exclude Sat/Sun, Dec 25–Jan 1, Good Friday, Thanksgiving, NFP (first Friday)
- Exclude hours whose forward window overlaps LNO intervals (time-based logic)
- Compute two-sample Anderson-Darling test (`scipy.stats.anderson_ksamp`)
- Run block bootstrap (length=24, 10K reps, seed=42, day-boundary, joint resampling)
- Compute secondary descriptors and robustness checks (KS+HAC, Cohen's d, CDF plot)
- Report results

**M39 must NOT:**
- Run the real experiment or inspect real economic results before submission to APEX control
- Amend any frozen parameter or methodological choice
- Compute real bootstrap p-values as part of the validation methodology
- Overwrite M36 methodology or M38 amendment files

---

## 7. Session State

**M38: COMPLETE — M39 PLANNED/AUTHORIZED**

- Blocking: None
- Forward pointers: M39 PRIMARY (execute frozen methodology)
- Back pointers: M37 (validation), M36 (methodology), M35 (direction), M34 (HIGH_VOL closure)
