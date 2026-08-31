# RC015 Study 007 — Economic Observation Timestamp Rule Audit & Reconciliation

**Status**: FROZEN & RECONCILED  
**Classification**: `PASS — DISTINCT RULES`  
**Target Manifest**: 222 Qualifying Events | 700 Rows | 699 Unique Option Instrument IDs (350 Calls, 350 Puts)

---

## 1. Authoritative Source Documents

The methodology audit conducted herein relies exclusively on authoritative continuity, charter, specification, and qualified empirical study artifacts, explicitly excluding the superseded discovery script (`scripts/rc015_study_007_volatility_pricing_discovery.py`):

1. **[APEX_SESSION_STATE.json](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/docs/APEX_SESSION_STATE.json)** & **[APEX_SESSION_HANDOFF.md](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/docs/APEX_SESSION_HANDOFF.md)**: Authoritative repository state marking superseded scripts and establishing frozen campaign parameters.
2. **[RC015_CHARTER.md](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/docs/RC015_CHARTER.md)**: Foundational research question comparing implied volatility ($IV_t$) against forward realized volatility ($RV_{t \to T}$) across the remaining option life.
3. **[RC015_Study_007_Final_Purchase_Gate.md](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/reports/RC015_Study_007_Final_Purchase_Gate.md)** & **[RC015_Study_007_Final_Acquisition_Scope.md](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/reports/RC015_Study_007_Final_Acquisition_Scope.md)**: Specifications defining the 222-event universe, Wednesday 00:00 UTC through Friday expiry data windows, outright C/P filtering, and the $\pm 0.0020$ moneyness threshold.
4. **[RC015_Study_006_1DTE_IV_RV_Microtest.md](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/reports/RC015_Study_006_1DTE_IV_RV_Microtest.md)**: Authoritative empirical reference executing real BBO synchronization, Black-76 inversion, and forward realized variance calculation with zero lookahead violations.
5. **[RC015_Study_003_IV_RV_Methodology_Pilot.md](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/reports/RC015_Study_003_IV_RV_Methodology_Pilot.md)** & **[RC015_Study_004_Maturity_Matched_IV_RV_Pilot.md](file:///d:/Gold%20Scripts/MQL5/Ticks%20Data/XAUUSD/grid%20research/apex/reports/RC015_Study_004_Maturity_Matched_IV_RV_Pilot.md)**: Methodological pilots establishing forward rolling return window mechanics and strict non-extrapolation constraints.

---

## 2. Separation of the Two Fundamental Concepts

The methodology explicitly separates the data acquisition boundary from the economic testing engine:

### A. Candidate-Universe Eligibility (Acquisition Scope)
* **Definition**: An option contract is eligible for acquisition if its strike satisfies $\left|\text{Strike} - F_t\right| \le 0.0020$ at **any allowed Wednesday M15 observation boundary** ($t \in [00:00, 23:45]\text{ UTC}$).
* **Rationale**: Because market participants cannot predict the Wednesday futures price path in advance, acquiring BBO quotes for all contracts that enter the near-ATM envelope at any point during Wednesday ensures that all necessary data is acquired without missing-data exceptions during downstream modeling.
* **Property**: This is a pure **data-envelope acquisition rule**.

### B. Economic Observation Timestamp (Valuation & Inversion Point)
* **Definition**: The exact timestamp $t$ at which an option's BBO mid is converted via Black-76 inversion into implied volatility ($IV_t$), and against which forward realized volatility is measured from $t$ strictly through option expiry $T$ ($RV_{t \to T}$).
* **Rationale**: Economic hypothesis testing requires that $t$ be determined either:
  1. Synchronously on a continuous forward grid (e.g. every minute or M15 bar where contemporaneous quotes exist), or
  2. At predetermined event/session timestamps (e.g. 08:00 UTC London Open, 13:30 UTC US Data, or 15:00 UTC Fixing).
* **Property**: This is an **economic valuation rule**. It must **never** be selected by scanning the future intraday path to find an ex-post minimum distance.

---

## 3. Lookahead Analysis & Selection Bias Audit

| Timestamp Rule | Mechanism | Lookahead Status | Valid Use Case |
|---|---|---|---|
| **Any-Wednesday-M15 Superset** | Keep all options where $\min_{t \in \text{Wed}} \left|\text{Strike} - F_t\right| \le 0.0020$ | **ZERO LOOKAHEAD** (Envelope Construction) | **Candidate Acquisition Universe** (Ensures full data availability) |
| **Ex-Post Minimum Distance as Economic $t$** | Set economic observation time $t = \arg\min_{t \in \text{Wed}} \left|\text{Strike} - F_t\right|$ for single event valuation | **CRITICAL LOOKAHEAD VIOLATION** (Scans future path; creates asynchronous timestamps across strikes in the same event) | **FORBIDDEN** for Economic IV/RV Inversion |
| **Forward-Synchronous Grid / Predetermined $t$** | At predetermined timestamp $t$, observe contemporaneous $F_t$ and $O_t$; compute $RV$ strictly over $(t, T]$ | **ZERO LOOKAHEAD** (All returns occur strictly after $t$) | **Authoritative Economic Valuation Rule** |

---

## 4. Study 006 Empirical Timestamp Convention

Study 006 serves as the primary empirical baseline because it passed all execution, synchronization, and lookahead audits with zero violations:

* **Observation Timestamp $t$**: Every synchronized minute bar on the observation date (`2026-08-12`) where valid BBO existed for both the option and futures contract.
* **Quote Selection**: Contemporaneous BBO midpoint at minute $t$ ($O_t = (\text{bid}_t + \text{ask}_t)/2$, $F_t = (\text{bid\_fut}_t + \text{ask\_fut}_t)/2$).
* **Futures Midpoint Synchronization**: Exact inner join on minute timestamp $t$; assertions verified that $\text{ts\_recv} \ge t$ and no future quotes were merged.
* **Realized Volatility Calculation**: $RV_{t \to T} = \sqrt{\frac{\sum_{i=t+1}^{T} r_i^2}{T - t}}$. Cumulative squared returns strictly started after $t$ and terminated at exact expiry $T$.
* **Lookahead Independence**: Observation timestamp $t$ was not chosen using future path metrics. Every point $t$ stood as an independent, forward-looking observation.

---

## 5. Frozen RC015 Research Question Structure

The economic research question in RC015 is:
$$\text{Is } IV_t \text{ systematically mispriced relative to } RV_{t \to T} \text{ conditional on Apex volatility state primitives?}$$

Therefore, timestamp $t$ is:
* **An Event-Level / Intraday Grid Timestamp**: Evaluated either on the predetermined M15 grid or at predetermined session transition points across the Wednesday window.
* **Cross-Sectionally Coherent**: At any chosen timestamp $t$, all evaluated options and underlying futures share the exact same timestamp $t$.
* **Forward-Looking**: For each $t$, $RV_{t \to T}$ integrates returns strictly over the interval $(t, T]$.

---

## 6. Audit of the Current 700 Rows (`RC015_Study_007_Final_Moneyness_Revalidation.csv`)

An audit of `reports/RC015_Study_007_Final_Moneyness_Revalidation.csv` confirms:
* **Total Rows**: 700
* **Unique Option Instrument IDs**: 699
* **Option Breakdown**: 350 Calls (`C`), 350 Puts (`P`)
* **Total Qualifying Events**: 222 (100% resolved)
* **Timestamp Distribution in CSV**:
  * 94 events have a single qualifying timestamp across all strikes.
  * 128 events have multiple qualifying timestamps across different strikes.
* **Role of the Timestamp in the Revalidation CSV**:
  * The `observation_timestamp` recorded in this CSV is **strictly an eligibility proof**. It records the specific M15 bucket that achieved the minimum moneyness distance to prove that the option satisfied $\le 0.0020$ during Wednesday.
  * It is **NOT** the economic observation timestamp for downstream single-point IV/RV inversion.
  * Because it serves solely as an eligibility proof for candidate acquisition, the presence of differing timestamps across strikes does **not** invalidate the 699-instrument acquisition universe.

---

## 7. Critical Decision Classification

### **`PASS — DISTINCT RULES`**

1. **Candidate-Universe Rule**: Any Wednesday M15 observation where $\left|\text{Strike} - F_t\right| \le 0.0020$ qualifies an option for inclusion in the 699-ID acquisition manifest.
2. **Economic Observation Rule**: The actual IV-vs-maturity-matched-RV comparison in Stage 2 is evaluated at predetermined or forward-synchronous timestamps $t$ (such as the full Wednesday M15 grid or predetermined session anchors), where contemporaneous $F_t$ and $O_t$ determine $IV_t$ and forward returns over $(t, T]$ determine $RV_{t \to T}$.
3. **Validity**: The current 699-ID candidate universe is **100% methodologically valid** for Option BBO-1m purchase.

---

## 8. Exact Rule for Stage 2 Execution

When Stage 2 executes the IV/RV volatility-pricing analysis:
1. Load the acquired BBO-1m quotes for the 699 option instruments and contemporaneous 6E futures.
2. For each predetermined observation timestamp $t$ on Wednesday (e.g. every M15 boundary):
   - Extract the contemporaneous futures mid $F_t$.
   - Identify the option contracts satisfying $\left|\text{Strike} - F_t\right| \le 0.0020$ at that exact timestamp $t$.
   - Invert Black-76 to obtain $IV_t$.
   - Compute remaining-life realized volatility $RV_{t \to T} = \sqrt{\frac{\text{cumsum\_r2}(T) - \text{cumsum\_r2}(t)}{\text{TTE\_years}}}$.
   - Compute the Variance Gap $\Delta\sigma^2_t = RV_{t \to T}^2 - IV_t^2$ and evaluate against RC012/RC013 state conditions.
3. This completely eliminates any lookahead or timestamp-selection bias and maintains total alignment with Study 006.
