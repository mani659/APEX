# RC015 Study 007 — Final Economic Observation Schedule Freeze

**Status**: FROZEN & DETERMINISTIC  
**Classification**: `PASS — ECONOMIC OBSERVATION SCHEDULE FROZEN`  
**Scope**: 222 Qualifying Events | 96 M15 Timestamps per Event | 21,312 Total Predetermined Observation Slots  
**Associated Artifacts**:
- `reports/RC015_Study_007_Final_Economic_Observation_Schedule.csv`
- `reports/RC015_Study_007_Final_Moneyness_Revalidation.csv` (699 Unique Option Instrument IDs)

---

## 1. Executive Summary

This specification deterministically freezes the **single exact economic observation schedule** for RC015 Study 007.

The 699-option / 700-row instrument universe is accepted as the **acquisition superset** (capturing all options that enter within $\pm 0.0020$ moneyness of 6E futures during Wednesday). The schedule defined herein provides the exact, predetermined timestamp grid used for the final $IV_t$ versus maturity-matched $RV_{t \to T}$ economic pricing test, guaranteeing **zero lookahead bias, zero ex-post optimization, and strict compatibility with RC012 / RC013 primitives**.

---

## 2. Evaluation of Candidate Observation Designs

| Design Candidate | Specification | Alignment with Repository Evidence | Verdict |
| :--- | :--- | :--- | :--- |
| **Candidate A: Full Wednesday M15 Grid** | Every 15-minute boundary ($00:00, 00:15, \dots, 23:45\text{ UTC}$, 96 slots/event) | **EXACT MATCH**: Matches RC012 `HIGH_VOL` native 15-minute resolution, full Wednesday data window in Purchase Gate, and Study 006 continuous evaluation pipeline. | **SELECTED (FROZEN)** |
| **Candidate B: Single Fixed Timestamp** | One arbitrary fixed hour per Wednesday (e.g. 15:00 UTC) | **UNSUPPORTED**: No charter or specification document freezes a single fixed hour. An arbitrary single minute creates fragility to temporary quote gaps or intraday spread spikes. | **REJECTED** |
| **Candidate C: Predefined Multiple Anchors** | Only specific session boundaries (e.g. 06:00, 12:00 UTC) | **SUBSET ONLY**: Session boundaries are properties of the continuous grid rather than disjoint sampling points. Restricting to anchors discards valid RC012 state transitions. | **REJECTED** |
| **Candidate D: Ex-Post Path-Dependent Selection** | Min-distance or highest-liquidity timestamp chosen after observing data | **METHODOLOGICALLY FATAL**: Scans future path; introduces lookahead and selection bias. | **STRICTLY FORBIDDEN** |

---

## 3. Study 006 Empirical Evidence Check

Study 006 (`scripts/rc015_study_006_1dte_iv_rv.py` & `reports/RC015_Study_006_1DTE_IV_RV_Microtest.md`) provides the empirical benchmark for how timestamps are handled:
1. **Timestamp Population**: Evaluated quotes across the entire observation day (`2026-08-12 00:00` to `23:59 UTC`) resampled to standard minute bars (`dt.floor('Min')`).
2. **Ex-Ante Predetermination**: Every valid quote timestamp was an independent observation slot; no timestamp was selected or discarded based on subsequent price movement or moneyness outcomes.
3. **Synchronization**: Synchronized contemporaneous option and futures quotes at $t$ ($\text{ts\_recv} \ge t$).
4. **Forward Realized Volatility**: Measured strictly forward over the interval $(t, T]$:
   $$RV_{t \to T} = \sqrt{\frac{\sum_{i=t+1}^{T} r_i^2}{T - t}}$$
5. **Zero Lookahead**: Lookahead violations = 0 confirmed by formal assertions.

Study 007 adopts this exact continuous evaluation logic, standardized to the 15-minute (`M15`) frequency to match the RC012 state machine.

---

## 4. RC012 and RC013 Compatibility

The frozen observation schedule natively integrates both upstream primitives:

### A. RC012 HIGH_VOL Primitive
- **Definition**: Distributional state defined on spot EURUSD M15 bars:
  $$\text{rv20}_t = \text{std}\left(r_{t-20}, \dots, r_{t-1}\right)$$
  $$\text{HIGH\_VOL}_t = \left(\text{PercentileRank}(\text{rv20}_t) > 80.0\right)$$
- **Schedule Attachment**: Because the schedule evaluates every 15-minute timestamp $t \in \{00:00, 00:15, \dots, 23:45\}$, $\text{HIGH\_VOL}_t$ is evaluated synchronously at each M15 boundary using strictly prior returns $(t-20 \to t-1)$, preserving zero lookahead.

### B. RC013 Session State Annotations
- **Definition**: Fixed time-of-day market regime intervals:
  - `ASIA_TO_LONDON`: $06:00 \le \text{Hour}(t) < 08:00\text{ UTC}$
  - `LONDON_NY_OVERLAP`: $12:00 \le \text{Hour}(t) < 16:00\text{ UTC}$
  - `OTHER`: All other Wednesday hours
- **Schedule Attachment**: Session labels attach deterministically as an ex-ante time-of-day attribute to each scheduled M15 slot. They are observational category labels, not downsampling filters.

---

## 5. Statistical Observation Unit & Dependence Handling

To ensure scientific integrity and prevent false sample-size inflation:

1. **Intraday Observation Unit**: The basic measurement point is $(e, t)$, where $e \in \{1, \dots, 222\}$ is the event and $t \in \{1, \dots, 96\}$ is the M15 timestamp.
2. **Clustering & Autocorrelation**: Consecutive M15 observations within the same Wednesday share overlapping forward realization paths $(t, T]$. Therefore, individual M15 rows must **never** be treated as 21,312 independent degrees of freedom in hypothesis testing.
3. **Formal Statistical Protocol**:
   - **Primary Unit of Independence**: The **222 distinct weekly events** ($N = 222$).
   - **Inference Methods**: Cluster-robust standard errors (clustered by `event_id`) or event-level time-weighted aggregations ($\overline{\Delta\sigma^2}_e$).
   - **Intraday Profiling**: M15-level resolution is utilized to assess the dynamic trajectory of variance gaps across session transitions and during active $\text{HIGH\_VOL}$ regimes.

---

## 6. Relationship to the 699-Instrument Universe

- **Acquisition Superset**: The 699 unique option IDs (700 rows across 222 events) represent the complete universe acquired from Databento.
- **Intraday Selection Mechanism**: At each predetermined timestamp $t$ in the schedule:
  1. Measure contemporaneous 6E futures midpoint $F_t$.
  2. Filter the acquired options for that event to those satisfying:
     $$\left|\text{Strike} - F_t\right| \le 0.0020$$
  3. Extract contemporaneous option BBO midpoint $O_t$.
  4. Invert Black-76 IV ($IV_t$) and compute remaining-life $RV_{t \to T}$.
  5. If multiple strikes satisfy the threshold at timestamp $t$, average their implied variance or evaluate them as a cross-sectional near-ATM straddle/pair.

---

## 7. Deterministic Schedule Summary

- **Total Events**: 222
- **Timestamps per Event**: 96 M15 intervals (`00:00:00Z` to `23:45:00Z`)
- **Total Predetermined Observation Slots**: **21,312**
- **Schedule CSV**: `reports/RC015_Study_007_Final_Economic_Observation_Schedule.csv`
- **Reproducibility**: 100% deterministic; contains no stochastic or data-dependent elements.

---

## 8. Final Decision Classification

### **`PASS — ECONOMIC OBSERVATION SCHEDULE FROZEN`**

The economic observation schedule is strictly predetermined, fully documented, and frozen in repository artifacts. Study 007 is methodologically ready for the next acquisition gate.
