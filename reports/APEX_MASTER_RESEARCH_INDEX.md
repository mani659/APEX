# APEX MASTER RESEARCH INDEX

> **APEX = PAUSED / DORMANT.** This document is the canonical, read-only master index of every research stream, milestone, artifact, finding, and reusable asset produced under the APEX programme and its integrated SMC workstream. It is updated only by a control-authorised milestone (APEX-M51). It does NOT itself authorize any experiment.

| Field | Value |
|---|---|
| Milestone | **APEX-M51** (RESEARCH_KNOWLEDGEBASE_AUDIT) |
| Programme status | **APEX = PAUSED / DORMANT** |
| M3 validated modules | **0** |
| M4 validated modules | **0** |
| M5 candidates | **0** |
| Economic research authorization | **NONE** |
| Canonical evidence ledger | `reports/APEX_RESEARCH_EVIDENCE_LEDGER.csv` |
| Last authoritative update | APEX-M51 |
| Next milestone | **NONE (STOP after M51)** |

---

## Section 1 — Current State (Authoritative; do NOT modify)

- Programme: **APEX = PAUSED / DORMANT** (per POST-M50 CONTROL adjudication; Task 01-03 governance; M43/M45 closure).
- M3 = **0**, M4 = **0**, M5 = **0**. No validated economic module exists.
- Economic research authorization: **NONE**. No experiments, backtests, PnL, or market-data acquisition authorized.
- `current_milestone`: `APEX-TASK03` (moving to `APEX-M51` after commit), then **STOP**.
- The single binding constraint (core bottleneck): an **M3 → M4 validated economic base does not exist**; every M50/M47 candidate was found to be an *overlay* of a nonexistent M4 base.

## Section 2 — Evidence Classification Rules

Classes (from the canonical ledger `evidence_class` column):

| Class | Meaning | Example |
|---|---|---|
| VALIDATED | Replicated scientific finding (M1/M2) | HIGH_VOL distribution; session-transition LNO scale |
| OBSERVED | User-supplied / environment observation, NOT independently validated | Custom-bot Week-6 observations |
| HYPOTHESIS | Not yet tested; candidate direction | C5 funding prediction (pre-M48) |
| ARCHITECTURAL_INFERENCE | Structural reason, not an empirical result | SMC module/architecture; R10/R11 governance |
| FAILED | Tested and rejected | BOS+OB M4; CHOCH M3; raw breakout |
| CLOSED | Path closed/archived (may combine rejection + class) | HIGH_VOL branch closure |
| UNKNOWN | Not classifiable from available evidence | (reserved) |

Promotion rule: **OBSERVED → VALIDATED only via a replicated, auditable extraction; never by assertion.** No custom-bot observation has been promoted.

## Section 3 — APEX Core Research (RC12–RC15; M17-R2 → M50)

| Stream | Milestone | Conclusion | Status |
|---|---|---|---|
| HIGH_VOL distributional primitive | RC012 | Validated M1/M2 scientific primitive; NOT economical | CLOSED |
| HIGH_VOL monetization | RC012·006/007–011 | Spot/synthetic-straddle PoC non-deployable; rejected | CLOSED |
| Session-transition primitive | RC013 | LNO distributional difference validated (M39-R2: p=0.0001); scale component (M41) | CLOSED |
| Session raw breakout | RC013·004 | Raw breakout not economically exploitable | CLOSED |
| Cross-asset transmission | RC014 | Transmission hypothesis rejected for tested pairs | CLOSED |
| CME listed options | RC015 | Method infeasible (liquidity / scarce synchronized slots); 222 events; 699 options; spend ~$1.2570 | CLOSED |
| HIGH_VOL episode duration prediction | M17-R2 | OOS duration predictability validated (M2) | CLOSED |
| Predicted-persistence → forward RV | M21 | Translation established (M2) | CLOSED |
| Predicted-persistence → direction | M24 | Directional translation rejected | CLOSED |
| Predicted-persistence → extremes | M27 | Extremum translation established (M2) | CLOSED |
| Dispersion boundary | M31 | No independent economic payoff | CLOSED |
| HIGH_VOL branch adjudication | M32 | Saturation → early branch stop | CLOSED |
| HIGH_VOL branch scientific closure | M34 | Final closure; evidence archived | CLOSED |
| Session-transition asymmetry | M39 → M39-CR → M39-R2 | M39 invalidated (null error); M39-R2 re-established p=0.0001 | CLOSED |
| Distributional decomposition | M40 | Methodology designed | COMPLETE |
| Session-transition scale component | M41 | Scale = LNO 1.65x more dispersed; p=0.0001 | CLOSED |
| Session-transition economy | M42 | NO economic mechanism justified | CLOSED |
| Programme continuation | M43 | Programme paused | PAUSED |
| M3 candidate discovery (AR1) | M44 | NO M3 candidate | PAUSED |
| Research cycle closure | M45 | Cycle closed; 5 restart conditions; 10 closed paths | CLOSED |
| SMC integration | M46 | SMC-R1..R11 integrated; no competing state | COMPLETE |
| Integrated direction discovery | M47 | C5 funding/carry prediction selected (design only) | PAUSED |
| Funding methodology | M48 → M48-CR | M48 BLOCKED (sign/circularity/formula errors; mechanism not established) | CLOSED |
| Funding mechanism rediscovery | M49 | Funding mechanism NOT established; path closed (costs 5–12bp > funding 1–3bp) | CLOSED |
| Integrated bot-evidence hypothesis discovery | M50 | 6 candidates /60; none earned design cycle; all were overlays of nonexistent M4 base | COMPLETE |
| Post-M50 restart control | POST-M50 CONTROL | **KEEP APEX PAUSED**; no candidate satisfies R1–R10 | CLOSED |

## Section 4 — SMC-Derived Research (R1–R11 integrated)

| # | Milestone | Purpose | Key outcome |
|---|---|---|---|
| R1 | SMC-R1 | Module/signal architecture + POI trigger compatibility | Architecture spec |
| R2 | SMC-R2 | Event extraction validation | Extraction validated |
| R3 | SMC-R3 (+CR/CR2) | BOS+OB economic methodology | Methodology frozen |
| R4 | SMC-R4 (+CR) | BOS+OB descriptive/gross experiment | Gross ~+1.01 bps/event |
| R5 | SMC-R5 (+CR/CR2) | BOS+OB M4 qualification methodology | Methodology frozen |
| R6 | SMC-R6 (+CR) | BOS+OB M4 qualification | **M4 FAILED**: net **-1347.31** bp/day; OOS **-751.34**; p=0.500; t=-67.20 |
| R7 | SMC-R7 | Frequency-compression rescue | Not viable; path closed |
| R8 | SMC-R8 (+CR) | CHOCH economic methodology | Methodology frozen |
| R9 | SMC-R9 (+CR) | CHOCH standalone economics | **M3 FAILED**: net **-17.0286** bps; OOS **-9.6414**; gross +0.8936 |
| R10 | SMC-R10 | R10 economic qualification framework (APEX-wide) | Governance integrated |
| R11 | SMC-R11 | Rare-event / module framework (rare != weak) | Governance integrated |

**SMC headline:** Both tested economic expressions of the SMC primitive set (BOS+OB, standalone CHOCH) failed economics under the tested M1 XAUUSD cost architecture. The SMC geometry/gross effects remain valid **empirical (non-economic)** findings.

## Section 5 — Custom-Bot Operational Evidence

- Classification: **B — USER-SUPPLIED / OBSERVED** (not validated).
- The original Week-6 statistical analysis document was **NOT FOUND** in the forensic search of `D:\Gold Scripts\MQL5` (§ Audit A–D). The only located artifacts are bot **source** scripts (`D:\Gold Scripts\MQL5\Ticks Data\XAUUSD\CAB.py`, `ghost_grid.py`, `SMC.py`) — these are backtest/operational code, not the statistical analysis.
- Recorded observations (from user supply): R-Velocity / early-trade deterioration; ATR; ADX; volume; sessions; stale cache; execution quality; correlated positions; **regime UNKNOWN**; NY Overlap; 19.5 conv.
- **Status: NOT FOUND** on disk → evidence class stays **OBSERVED**, auditability = **UNAUDITED**. A future repository audit is REQUIRED before any promotion; no promotion has occurred.

## Section 6 — Validated Scientific Findings (M1/M2)

1. **HIGH_VOL** is a distributional primitive of EURUSD/XAUUSD volatility (RC012; D=0.193, C=0.666). [VALIDATED]
2. **HIGH_VOL episode duration** is predicted out-of-sample (M17-R2). [VALIDATED]
3. Predicted persistence **translates to forward RV** (M21). [VALIDATED]
4. Predicted persistence **translates to price-extremum boundaries** (M27). [VALIDATED]
5. **Session-transition LNO distributional difference** validated (M39-R2, p=0.0001). [VALIDATED]
6. The difference is driven by a **scale (dispersion)** component, LNO **1.65x** more dispersed (M41, p=0.0001). [VALIDATED]

## Section 7 — Validated Predictive Findings

- HIGH_VOL **episode duration** (OOS survival; M17-R2) and **predicted-persistence → forward RV** (M21). Both are **non-directional**; no validated directional edge exists (M24 rejected direction).

## Section 8 — Economic Candidates (not validated; watchlist/hypothesis only)

- **C5 / W1:** Commodity **convenience yield / inventory term structure** (Task02 G1/G2) — blocked on *no futures-curve dataset* + not authorized (trigger **T1**).
- **W2:** New liquid **venue/instrument** carrying validated vol info with **independent** payoff — no such venue observable today (RC015; IC8 s4D) (trigger **T2**).

## Section 9 — Failed Economic Mechanisms

- **HIGH_VOL spot/synthetic-straddle** monetization (RC012/006–011) — FAILED.
- **Session raw breakout** (RC013/004) — FAILED.
- **Predicted-persistence → direction** (M24) — FAILED.
- **BOS+OB M4** (SMC-R6) — M4_FAILED.
- **CHOCH M3** (SMC-R9) — M3_FAILED.
- **Perpetual-swap funding/carry prediction** (M49) — CLOSED.

## Section 10 — Closed Paths (complete list)

| # | Path | Closed at | Reason |
|---|---|---|---|
| 1 | HIGH_VOL monetization | M34 | Saturation; no expression |
| 2 | Session raw breakout | RC013 | Not economical |
| 3 | Cross-asset transmission | RC014 | Rejected |
| 4 | CME listed options | RC015 | Method infeasible |
| 5 | Session-transition economy | M42 | No mechanism justified |
| 6 | Direction translation | M24 | No directional edge |
| 7 | Dispersion boundary | M31 | No payoff |
| 8 | BOS+OB economics | SMC-R6/R7 | M4 FAILED |
| 9 | CHOCH economics | SMC-R9 | M3 FAILED |
| 10 | Perpetual funding/carry | M49 | Not established |
| 11 | Funding prediction methodology | M48-CR | BLOCKED |

## Section 11 — M3–M5 Status

- M3 validated modules: **0** (SMC BOS+OB & CHOCH both failed M3/M4 economics; no M3 candidate cleared M44 gate).
- M4 validated modules: **0** (global count = 0).
- M5 candidates: **0**.

## Section 12 — Reusable Assets (science/machinery only; not economic)

- Cancelable: DATA/002-EURUSD tick transit; XAUUSD M1 extraction/OHLC; forward RV; realized vol; distribution decomposition; session segmentation; SMC event extraction (R2 machinery + scripts); bootstrap/day-block permutation; Black-76 IV inversion machinery; Databento BBO acquisition.
- SMC R10/R11 governance frameworks (APEX-wide).

## Section 13 — Reusable Negative Knowledge

- Predicted HIGH_VOL persistence → **no** directional/breakout edge (M24, RC013).
- SMC primitives' **gross** +1.01 (BOS+OB) / +0.89 (CHOCH) bps are swamped by tested M1 costs (net strongly negative).
- Funding/carry: 1–3bp funding ≪ 5–12bp costs → **no** standalone route.
- Existing listed-option IV already prices the validated vol info (W2 blocker).

## Section 14 — Current Bottleneck

**No validated M3/M4 economic module exists on which candidates can be overlaid.** Every candidate that emerged in M47/M50 was an overlay of a nonexistent M4 base. Any restart must first establish a validated, independent economic payoff.

## Section 15 — Restart Conditions (from M45 + POST-M50)

1. R1–R10 restart gates must be satisfied (per `APEX_POST_M50_CONTROL_ADJUDICATION` + M45 restart conditions); **none currently satisfied**.
2. A **new economic mechanism/dataset** (e.g., W1 convenience yield needing a futures-curve dataset; W2 requiring a new instrument/venue) must arise, backed by authorization.
3. Control authorization is required before any data acquisition or experiment (economic research authorization remains **NONE**).
4. Any custom-bot evidence promotion requires a **repository audit** of the missing analysis document (currently NOT FOUND; class B/OBSERVED).

## Section 16 — Canonical Evidence Ledger

- **File:** `reports/APEX_RESEARCH_EVIDENCE_LEDGER.csv`
- **Schema:** 24 columns (record_id … notes) as specified.
- **Coverage:** RC012/013/014/015; M17-R2, M21, M24, M27, M31, M32, M34, M39, M39-CR, M39-R2, M40, M41, M42, M43, M44, M45, M46, M47, M48, M48-CR, M49, M50, POST-M50 CONTROL; SMC-R1..R11; Task01–03 governance; custom-bot (B/OBSERVED).
- **Integrity note:** every `source_path` verified to exist on disk (§ Audit B); M4 global module count = **0**.

## Section 17 — Source Directory Map

| Directory | Content |
|---|---|
| `reports/` | All APEX milestone reports, results, ledger, index, audit |
| `docs/` | `APEX_SESSION_HANDOFF.md`, `APEX_SESSION_STATE.json` (authoritative state) |
| `research/SMC_RESEARCH/` | Integrated SMC workstream (R1–R11 tree) |
| `reports/APEX_TASK0[1-3]_*` | Task 01–03 governance records (watchlist, economic mechanism discovery) |
| External (read-only): `D:\Gold Scripts\MQL5\Ticks Data\XAUUSD\` | Bot sources (CAB.py, ghost_grid.py, SMC.py), strategy result CSVs |
| External (read-only): `D:\Gold Scripts\MQL5\SMC\`; `...\Strategies\` | SMC EA reports; GOLD-sniper strategy PDFs (NOT the custom-bot analysis) |

## Section 18 — Research Relationship Graph

```
             ┌────────────────────────────── PRESENT (DORMANT) ──────────────────────────────┐
             │                                                                               │
   APEX CYCLE (RC012..RC015, M17R2..M42)                                                     │
      │  HIGH_VOL primitive (VALIDATED, non-econ) ──► predictions (M17R2/M21/M27)            │
      │  Session-transition LNO (M39R2/M41, VALIDATED, non-econ) ──► M42 economy: NONE       │
      ▼                                                                                       │
   M43 pause ─► M44 no-M3-candidate ─► M45 CYCLE CLOSED (5 restart conditions)                │
      │                                                                                       │
      ├──► M46: SMC-R1..R11 INTEGRATED ──► R6 BOS+OB M4 FAILED / R9 CHOCH M3 FAILED           │
      │         └─ R10/R11 governance (APEX-wide)                                             │
      ├──► M47 C5 funding (design only) ─► M48 BLOCKED ─► M49 funding CLOSED                  │
      └──► M50: bot evidence (B/OBSERVED) ─► POST-M50 CONTROL = KEEP PAUSED (R1–R10 unmet)    │
                                                                                              │
   BOT EVIDENCE (B/OBSERVED, NOT FOUND on disk): CAB / Ghost Sniper / Unified Runner /        │
   R-Velocity / stale cache / regime UNKNOWN ──► feeds M50 only; needs repository audit       │
                                                                                              │
   WATCHLIST (Task03 W1/W2): convenience yield (T1), new instrument/venue (T2)  ──► triggers │
                                                                                             ┘
```

---

*This index and the canonical evidence ledger were produced under APEX-M51 as a knowledge-integration and version-control backup milestone. Compliance: External API calls = 0; new data acquired = 0; spend = $0.00. APEX remains PAUSED.*
