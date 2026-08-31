# RC015 Study 007 — Minimum-Cost Option BBO Acquisition Plan & Gate

**Status**: READY FOR USER AUTHORIZATION  
**Classification**: `PORTAL ESTIMATE REQUIRED` / `CANDIDATE: EXACT BATCHED IDS`  
**Scope**: 222 Qualifying Events | 699 Unique Option Instrument IDs | 21,312 Predetermined Economic Observation Slots  
**Associated Artifacts**:
- `reports/RC015_Study_007_Minimum_Cost_BBO_Acquisition_Plan.csv`
- `reports/RC015_Study_007_Final_Economic_Observation_Schedule.csv`
- `reports/RC015_Study_007_Final_Moneyness_Revalidation.csv`

---

## 1. Executive Summary & Objective

This document establishes the **smallest scientifically defensible Option BBO-1m data request** required to execute the frozen RC015 Study 007 volatility-pricing analysis across the 222-event historical universe (2022–2026).

By restricting the request to the **exact 699 candidate option instrument IDs** partitioned into **5 annual date-window batches**, the acquisition eliminates gross overfetch of unneeded strikes and expiries, reducing expected data volume from **~80+ GB (broad parent query)** down to **~20–30 MB compressed (~150 MB uncompressed)** and estimating spend at **<$1.50 USD**.

---

## 2. Local Data Audit & Zero-Reuse Confirmation

A thorough audit of the local filesystem (`data/databento/` and extracted temporary directories) was conducted:

| Local Directory / Archive | Content & Product | Covered Date Window (UTC) | Overlap with Frozen Universe (2022-01 → 2026-06) | Usable for Frozen Study 007 |
| :--- | :--- | :--- | :--- | :--- |
| `_tmp_rc015_bbo` | `EUU.OPT` BBO-1m | `2026-08-10` to `2026-08-12` | **0 events (0%)** | Pilot / Qualification only |
| `_tmp_rc015_su2_bbo` | `SU2.OPT` BBO-1m | `2026-08-10` to `2026-08-12` | **0 events (0%)** | Pilot / Qualification only |
| `_tmp_rc015_6e_bbo` / `_s6` | `6E.FUT` BBO-1m | `2026-08-10` to `2026-08-12` | **0 events (0%)** | Pilot / Qualification only |
| `_tmp_rc015_definition` | `6E.FUT` Definition | `2026-05-16` to `2026-08-15` | **0 events (0%)** | Mapping only |
| `_tmp_rc015_options_definition` | Options Definition | `2026-08-13` to `2026-08-15` | **0 events (0%)** | Mapping only |

**Audit Conclusion**:
- **Existing Option BBO Coverage**: **0 rows / 0%** of the 699 frozen option IDs across the 222 events.
- **Remaining Option BBO Requirement**: **699 unique option IDs (100% requires new acquisition)**.
- **Futures BBO Coverage**: Intraday futures midpoints for moneyness validation were extracted live in memory during revalidation; contemporaneous 6E futures BBO for the 222 Wednesday windows (~$0.41) should be acquired alongside options.

---

## 3. Instrument Mapping & Batch Decomposition

From [RC015_Study_007_Final_Moneyness_Revalidation.csv](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/reports/RC015_Study_007_Final_Moneyness_Revalidation.csv):
- **Total Rows**: 700
- **Unique Option Instrument IDs**: 699 (350 Calls, 350 Puts)
- **Recycled IDs**: Exactly 1 option ID (`42313458`) appears in 2 events (`2024-06-12` and `2026-01-28`) due to CME annual contract recycling; 698 IDs appear in exactly 1 event.
- **Operational Batching**:

| Batch Group | Year / Period | Qualifying Events | Total Rows | Unique Option IDs | Unique Futures IDs | Date Span (Wednesdays) |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **`BATCH_2022`** | 2022 Full Year | 50 | 150 | 150 | 4 | 2022-01-05 → 2022-12-28 |
| **`BATCH_2023`** | 2023 Full Year | 50 | 164 | 164 | 4 | 2023-01-04 → 2023-12-27 |
| **`BATCH_2024`** | 2024 Full Year | 49 | 146 | 146 | 4 | 2024-01-03 → 2024-12-18 |
| **`BATCH_2025`** | 2025 Full Year | 50 | 164 | 164 | 4 | 2025-01-08 → 2025-12-24 |
| **`BATCH_2026_H1`** | 2026 H1 | 23 | 76 | 76 | 3 | 2026-01-07 → 2026-06-24 |
| **TOTAL** | **2022–2026 H1** | **222** | **700** | **699** | **19** | **222 Wednesdays** |

---

## 4. True Minimum Quote Window Determination

1. **Economic Observation Timestamps**:
   - The frozen schedule defines 96 M15 observation slots per event: strictly spanning **Wednesday 00:00:00 UTC through Wednesday 23:45:00 UTC**.
   - Option BBO midpoints $O_t$ are required strictly at timestamp $t$ on Wednesday to compute $IV(t)$.
2. **Forward Realized Volatility Path ($RV_{t \to T}$)**:
   - Evaluated strictly on **spot EURUSD M1 data** (already available locally in canonical form) from timestamp $t$ through Friday expiry $T$. Option quotes after Wednesday are **not** needed for RV calculation.
3. **Defensible Quote Windows**:
   - **Strict Scientific Minimum**: `Wednesday 00:00:00Z` to `Wednesday 23:59:00Z` (24 calendar hours per event $\times$ 222 events = **5,328 calendar hours**).
   - **Extended Technical Envelope**: `Wednesday 00:00:00Z` to `Friday 23:59:00Z` (72 hours per event $\times$ 222 events = **15,984 hours**). This includes technical overfetch beyond Wednesday, but ensures CME settlement price alignment if required.

---

## 5. Comparison of Acquisition Strategies

| Strategy | Target Symbols / Query Mode | Target Dates | Estimated Rows | Compressed Volume | Estimated Cost (USD) | Scientific Assessment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Broad Parent Continuous** | `6E.OPT` parent | Continuous 2022–2026 | >500,000,000 | ~80+ GB | >$50.00 | **REJECTED**: Massive overfetch of millions of unused OTM/ITM strikes. |
| **2. Broad Parent Event-Windowed** | `6E.OPT` parent | 222 Wed–Fri Windows | ~60,000,000 | ~8.0–9.3 GB | ~$4.00–$5.00 | **SUBOPTIMAL**: Fetches all strikes in the chain instead of only the $\pm 0.0020$ near-ATM contracts. |
| **3. Exact 699 IDs Continuous** | 699 exact `instrument_id`s | Continuous 2022–2026 | ~5,000,000 | ~100–150 MB | ~$2.00–$3.00 | **INEFFICIENT**: Queries contracts during months when they were inactive / unlisted. |
| **4. Exact IDs Batched by Year / Window (RECOMMENDED)** | Specific `instrument_id`s per batch (76–164 IDs/batch) | 222 Wednesday Windows (24h/event) | **~1,008,000** | **~20–30 MB** | **~$0.45–$1.20** | **OPTIMAL**: Exact scientific scope, minimal volume, zero waste. |

---

## 6. Detailed Request Specification & Volume / Cost Estimate

### Databento Query Parameters
- **Dataset**: `GLBX.MDP3`
- **Schema**: `bbo-1m`
- **SType In**: `instrument_id`
- **SType Out**: `instrument_id`
- **Batch Partitioning**: 5 requests (annual batches `BATCH_2022` through `BATCH_2026_H1`), each passing the exact list of `instrument_id`s active in that year.

### Quantitative Metrics
- **Number of Unique Option Instruments**: 699
- **Number of Unique Futures Instruments**: 19
- **Total Event Windows**: 222
- **Expected BBO-1m Rows**: $\approx 222 \text{ days} \times 1,440 \text{ min/day} \times 3.15 \text{ options/event} \approx 1,007,000 \text{ rows}$.
- **Expected Data Volume**:
  - Compressed (`.csv.zst`): **~20 MB to 30 MB**
  - Uncompressed (`.csv`): **~120 MB to 160 MB**
- **Estimated Cost**:
  - Based on Databento BBO-1m pricing (~$0.01 to $0.05 per MB compressed for historical GLBX): **~$0.45 to $1.20 USD**.
  - Status: `PORTAL ESTIMATE REQUIRED` to verify before live debit.

---

## 7. Security Audit

- **API Key Handling**: Authentication is read exclusively via `os.environ.get("DATABENTO_API_KEY")`.
- **Live Key Verification**: `DATABENTO_API_KEY.md` exists locally (untracked). The key value is never logged, printed, or written into generated reports.
- **Git State**: Untracked working tree clean of accidental secrets.

---

## 8. Answers to Required Report Conclusions

1. **How many of the 699 option IDs require new data?**
   **All 699 IDs (100%)**. Local BBO files cover only the August 2026 pilot.
2. **How many event/date windows require new data?**
   **222 distinct Wednesday observation windows** (and their corresponding Friday expiries).
3. **Can the request be reduced below a broad product-wide purchase?**
   **YES.** Requesting exact `instrument_id` lists reduces the dataset from ~80 GB down to ~25 MB (a >99.9% volume reduction).
4. **What is the smallest exact request?**
   Strategy 4: 5 annual batch requests querying the exact 699 `instrument_id`s and 19 futures `instrument_id`s over their respective Wednesday observation dates.
5. **What unavoidable overfetch exists?**
   Within each Wednesday, BBO quotes are fetched for all 1,440 minutes of the day (since BBO-1m is queried at daily grain), whereas the economic schedule samples 96 M15 points. This is standard technical overhead (<10 MB).
6. **What is the expected data volume?**
   **~20 to 30 MB compressed** (~150 MB uncompressed).
7. **What is the expected cost?**
   **~$0.45 to $1.20 USD** (within the initial signup credit).
8. **Does any additional futures data need to be purchased?**
   **YES**, the contemporaneous BBO-1m for the 19 active 6E futures across the 222 Wednesdays should be acquired in the same batch (~$0.41 total).
9. **Is the planned request sufficient for all 21,312 predetermined economic timestamps?**
   **YES.** Every single scheduled timestamp falls within the acquired Wednesday BBO envelope.
10. **What exact action should be taken in the next session?**
    Submit the 5 batch specifications to the Databento portal/API to confirm the final estimate, and with user authorization, execute the download.

---

## 9. Final Decision & Gate

### **`PORTAL ESTIMATE REQUIRED — READY FOR ACQUISITION AUTHORIZATION`**
- Frozen Events: 222
- Frozen Option IDs: 699
- Required Observation Slots: 21,312
- New Option BBO Required: **YES (100%)**
- Exact Request Strategy: **Exact Instrument IDs Batched Annually**
- Estimated Volume: **~25 MB compressed**
- Estimated Cost: **~$0.45 – $1.20 USD**
- Existing Data Reused: **0% (August 2026 pilot is outside frozen scope)**
- Technical Overfetch: **Intraday 1-minute resolution vs 15-minute sampling grid (<10 MB)**
- Final Recommendation: **PORTAL ESTIMATE REQUIRED -> AUTHORIZE PURCHASE**
