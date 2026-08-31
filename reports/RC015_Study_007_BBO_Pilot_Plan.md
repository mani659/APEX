# RC015 Study 007 — BBO Pilot Plan & Local Coverage Audit

**Date**: 2026-08-18
**Status**: PLAN ONLY — no data acquisition executed. Mandatory STOP applied (section 12).
**Authorization**: LOCAL AUDIT + MINIMUM-COST PILOT PLANNING ONLY.

This plan determines the **smallest scientifically defensible next data request** to validate the repaired RC015 instrument mapping and contemporaneous futures-based moneyness before any meaningful Databento credit is spent on the full study.

---

## 1. Current Local BBO Inventory

All locally available data lives in `data/databento/` (5 ZIPs + extraction dirs). Source of truth = extracted `*.csv.zst` payloads; verified direct, not from metadata.json alone.

| Payload | Schema | Date coverage (UTC) | Product | Unique instr. | Rows | In frozen 222-universe dates? |
|---|---|---|---|---|---|---|
| `_tmp_rc015_6e_bbo` (= `_tmp_rc015_6e_bbo_s6` identical) | bbo-1m | 2026-08-10 16:23 → 2026-08-12 23:58 | 6E futures (25 instr incl. 6EU6) | 25 | 10,781 | **NO** |
| `_tmp_rc015_bbo` | bbo-1m | 2026-08-10 00:15 → 2026-08-12 20:49 | EUU.OPT (1,483 instr) | 1,483 | 659,775 | **NO** |
| `_tmp_rc015_su2_bbo` | bbo-1m | 2026-08-10 07:54 → 2026-08-12 19:05 | SU2.OPT (77 instr) | 77 | 26,015 | **NO** |
| `_tmp_rc015_definition` | definition | 2026-05-16 → 2026-08-15 | 6E.FUT | 141 | 13,282 | **NO** (mapping only) |
| `_tmp_rc015_options_definition` | definition | 2026-08-13 → 2026-08-15 | Options (18 assets incl. EUU/1EU-5EU) | 9,357 rows | 9,357 | **NO** (mapping only) |

**Conclusion**: Every local BBO/definition file covers 2026-08-10..15 **pilot & mapping windows only**. The frozen 222-event universe spans observation dates **2022-01-05 → 2026-06-24**. Verified date-overlap = **zero**; no local BBO is genuine coverage of any frozen event.

---

## 2. Repaired Manifest Coverage

Verified (recomputed from `reports/RC015_Study_007_Repaired_Exact_Option_Instrument_Manifest.csv`):

- 708 rows ✓
- 707 unique option IDs ✓ (one ID appears in 2 rows)
- 354 Calls / 354 Puts ✓
- 222 events ✓ (every observation date is a Wednesday; every expiry a Friday)
- 19 unique futures IDs ✓
- All rows `moneyness_pass=True` (vs reconstructed midpoint: daily ohlcv-1d **close**, not BBO mid)
- Per-event structure: 132 events × 4 rows (2 strikes), 90 events × 2 rows (1 strike)

### Local-BBO cross-check (per frozen event)

| Metric | Result |
|---|---|
| Repaired option IDs present in local option BBO (any date) | **1** (`42169141`) — and it is a **coincidental instrument-ID reuse**, not real overlap (see Conflict below) |
| Repaired futures IDs present in local futures BBO (any date) | **1** (`10573` = 6EU6), on pilot dates 2026-08-10..12 only |
| Events with ANY local option BBO on the event's observation date | **0 / 222** |
| Events with local futures BBO on the event's observation date | **0 / 222** |
| Events validating any repaired instrument locally | **0 / 222** |
| % frozen events covered by genuine existing BBO | **0%** |

**Conflict — instrument-ID reuse**: `instrument_id 42169141` = `EUUX5 P1152` (repaired manifest, event `2025-11-05_2025-11-07`), but the SAME ID = `EUUQ7 C1320` in local 2026-08 option data and in `_tmp_rc015_options_definition`. **Databento instrument IDs are not unique across time.** This is exactly why the pilot MUST request exact instrument IDs **within exact date windows** and verify the returned symbol — and why a bare ID cross-check is insufficient evidence of coverage.

**Community of practice** (full frozen universe, for reference only — NOT authorized to purchase):
- 707 options × 3 days ≈ 2,121 option-instrument-days; 19 futures × 3 days = 57 futures-instrument-days.

---

## 3. Minimum Futures Validation Requirement

The frozen moneyness rule `abs(strike − futures_mid) <= 0.0020` requires a **contemporaneous futures midpoint**. The reconstruction satisfied this approximately with the Wednesday `ohlcv-1d` **close**; the pilot must replace that with a true **BBO-1m mid**.

- **Observation date** (per frozen schedule): the event's **Wednesday** (`observation_date`).
- **Required window**: the full Wednesday UTC calendar day (`00:00:00Z → 24:00:00Z`), which contains the Wednesday close bar — the BBO-1m analog of the reconstruction's close, and the frozen window start.
- **Instrument scope**: the exact `futures_instrument_id` listed per event in the repaired manifest (quarterly-cycle contract, e.g. 6EH2 not front-month 6EG2). **No parent query**, no broad `6E` history, no cross-2022→2026 sweep.

Narrowest window per instrument = **1 market day (Wednesday)**. This is the minimum that captures the moneyness reference point.

---

## 4. Pilot Selection Rule (procedural — NOT result-driven)

Fixed, pre-declared rule, applied to the 222-event universe sorted by observation date, with the 3 degraded-date events excluded:

> **Rule**: select the earliest eligible event, the median-position eligible event, and the most recent eligible event. Within each, use the **first complete Call/Put pair** (lowest strike having both C and P present).

Excluded degraded observation dates (from reconstruction logs): `2024-09-18` (event 2024-09-18_2024-09-20), `2025-09-17`, `2025-09-24`.

No pilot event was chosen for outcome, moneyness favorability, HIGH_VOL, session state, or profitability.

---

## 5. Exact Pilot Events & Instruments

### Event 1 — earliest eligible (2022-01-05_2022-01-07)
| Field | Value |
|---|---|
| Observation date (request window) | **2022-01-05 00:00:00Z → 2022-01-06 00:00:00Z** |
| Futures instrument ID | **28727** (`6EH2`) |
| Option instrument IDs | **585890** (`EUUF2 C1132`, K=1.1325) · **573458** (`EUUF2 P1132`, K=1.1325) |
| Parent | EUU.OPT |
| Reconstructed futures mid (ohlcv close) | 1.13260 |

### Event 2 — median eligible (2024-03-06_2024-03-08)
| Field | Value |
|---|---|
| Observation date (request window) | **2024-03-06 00:00:00Z → 2024-03-07 00:00:00Z** |
| Futures instrument ID | **156627** (`6EH4`) |
| Option instrument IDs | **262121** (`EUUH4 C1090`, K=1.0900) · **333729** (`EUUH4 P1090`, K=1.0900) |
| Parent | EUU.OPT (mapping class RESOLVED_ALTERNATE_OPTION_ROOT — good procedural variety) |
| Reconstructed futures mid (ohlcv close) | 1.09030 |

### Event 3 — most recent eligible (2026-06-24_2026-06-26)
| Field | Value |
|---|---|
| Observation date (request window) | **2026-06-24 00:00:00Z → 2026-06-25 00:00:00Z** |
| Futures instrument ID | **10573** (`6EU6`) |
| Option instrument IDs | **42769619** (`4EUM6 C1137`, K=1.1375) · **42127757** (`4EUM6 P1137`, K=1.1375) |
| Parent | 4EU.OPT |
| Reconstructed futures mid (ohlcv close) | 1.13915 |

Diversity achieved procedurally: three distinct periods (2022 / 2024 / 2026), two option parents (EUU.OPT, 4EU.OPT), three distinct futures (6EH2, 6EH4, 6EU6), three distinct option classes as mapped (QUARTERLY, ALTERNATE_ROOT, QUARTERLY).

**Total pilot instrument-days: 6 option × 1 day + 3 futures × 1 day = 9 instrument-days.**

---

## 6. Exact Request Specification (if live request is approved)

| Parameter | Value |
|---|---|
| Dataset | `GLBX.MDP3` |
| Schema | `bbo-1m` |
| stype_in | `instrument_id` (exact IDs only) |
| stype_out | `instrument_id` (MapSymbols for symbol verification) |
| Symbols | 6 options: 585890, 573458, 262121, 333729, 42769619, 42127757; 3 futures: 28727, 156627, 10573 |
| Time ranges | 3 × single Wednesday UTC day (see section 5) |
| Compression / encoding | csv + zstd (reuse existing pipeline) |

No parent symbols. No definition schema re-request (local defs confirm the 2026 set is a different ID epoch). No 6E history sweep.

---

## 7. Estimated Data Volume

Grounded empirically from downloaded files (zstd-compressed bytes per instrument-day):

| Anchor | bytes / instrument-day (zstd) |
|---|---|
| EUU.OPT bbo-1m | 2,143 |
| SU2.OPT bbo-1m | 1,243 |
| 6E futures bbo-1m | 2,235 |

Pilot estimate (using the larger option rate for conservatism):
- 6 option-instrument-days × ~2,143 B ≈ **12.9 KB**
- 3 futures-instrument-days × ~2,235 B ≈ **6.7 KB**
- **Total ≈ 20 KB compressed (~0.02 MB)**.

---

## 8. Estimated Databento Cost

Local cost anchors:
- Stage-1 artifact rate: $0.45 / 26.5 MB ≈ **$0.01698 / MB**
- Final scope rate: $5.00 / 9.3 GB ≈ **$0.00054 / MB**

Pilot at ~0.02 MB:
- At stage-1 rate: ≈ **$0.0003**
- At scope rate: ≈ **$0.00001**

**Expected cost ≈ $0.00 – $0.01** (negligible; subject to Databento's per-request billing floor, to be confirmed via the portal's request-estimate endpoint BEFORE executing). This is far below any meaningful credit spend and satisfies "minimum useful validation per unit of signup credit."

---

## 9. Expected Validation Checks (TWO tests only)

**A. Instrument validity** — for each pilot event, does the exact option `instrument_id` return genuine `bbo-1m` bars on its Wednesday window? Criteria:
- non-empty result set;
- returned `symbol` matches the manifest symbol (e.g. `EUUF2 C1132`) — guards against instrument-ID epoch reuse;
- `bid_px_00` / `ask_px_00` populated for at least one bar.

**B. Moneyness validation** — for each pilot event, does the actual futures BBO mid at the observation reference point satisfy?
```
abs(K − futures_mid_bbo) <= 0.0020
```
where `futures_mid_bbo` = (bid_px_00 + ask_px_00)/2 of the futures instrument on the last BBO-1m bar of Wednesday (the analog of the ohlcv-1d close used in the reconstruction). A PASS for all 3 events (including the ALTERNATE_ROOT and 4EU cases) validates the repaired mapping's moneyness at maximum scientific scope.

**Do NOT**: calculate IV, calculate RV, inspect subsequent option performance, apply HIGH_VOL, apply RC013 sessions, or compute variance gaps.

---

## 10. Security

- API key used only from existing local file `DATABENTO_API_KEY.md` / env `DATABENTO_API_KEY`.
- Key is **NOT** printed, embedded in source, written to reports, committed, or exposed in logs.
- Verification before any commit: `git check-ignore -v DATABENTO_API_KEY.md`.
- Current state: `git check-ignore` on `DATABENTO_API_KEY.md` returns **exit 1 (NOT ignored)**. Per task section 10: this is reported and NOT silently modified. No `.gitignore` change made in this task; escalation required before any commit/push.

---

## 11. Explicit Limitation Statement

**No full Option BBO acquisition is authorized or performed.** This plan does not:

- download Option BBO for all 707 instruments;
- run the 222-event study;
- calculate Black-76 IV;
- calculate maturity-matched RV;
- calculate variance gaps;
- apply HIGH_VOL or RC013 session states;
- modify the candidate universe;
- choose between 707 / 530 / 191 based on outcomes;
- change the frozen moneyness rule, the 222-event universe, or the canonical EURUSD M1 RV source.

---

## 12. Mandatory STOP

**STOP.**
- No live Databento request has been executed.
- No pilot data has been downloaded.
- Cost estimate is available (section 8); request specification is available (section 6); execution awaits explicit user approval.
- Return to the user: local coverage (0%), pilot events & exact IDs, estimated volume (~20 KB) and cost (~$0.00–$0.01), and whether existing data can eliminate part of the request (answer: it cannot — 0% coverage; the pilot is irreducible).