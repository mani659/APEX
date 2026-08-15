# RC014 Study 001 — Cross-Asset Volatility Discovery

## Campaign Context
**RC014 — Cross-Asset Volatility Transmission**

## Status
**PENDING EXECUTION** (Awaiting project-level review of RC014_CHARTER.md)

---

## 1. Objective
Investigate whether a measurable volatility shock in one market (Source) changes the future movement distribution of another market (Target) in a way that the target market's own current information cannot explain.

---

## 2. Experimental Setup
* **Unit**: Canonical M15 bars (time-aligned, valid overlap only).
* **Source Variable**: RV20 (Standard deviation of previous 20 completed M15 log returns).
* **Shock Threshold**: Source RV20 > 80th percentile.
* **Lag Structure**: Contemporaneous, +1 M15, +4 M15, +16 M15.

## 3. Approved Test Relationships
1. EURUSD → XAUUSD
2. EURUSD → XAGUSD
3. USATECHIDXUSD → BTCUSD
4. USATECHIDXUSD → XAUUSD
5. XAUUSD → XAGUSD
6. XAGUSD → XAUUSD
7. BTCUSD → USATECHIDXUSD
8. XAUUSD → EURUSD

---

## 4. Execution Plan (Future)

### Phase 1: Data Alignment & Preprocessing
* Time-align source and target M15 data streams.
* Compute RV20 for all source and target pairs.
* Define `HIGH_VOL_SHOCK` condition using the 80th percentile threshold on source RV20.

### Phase 2: Baselines & Target State Analysis
* Establish Model A (Baseline): Target unconditional distribution and target volatility-matched distribution.

### Phase 3: Incremental Information Testing (Model B)
* Measure conditional target outcome metrics (absolute return, realized volatility, tail probabilities, path metrics) following a source `HIGH_VOL_SHOCK`.
* Compare Model B (Target Information + Source Shock) to Model A (Target Information).

### Phase 4: Temporal Stability & Dependence Treatment
* Test findings across Early, Middle, and Recent historical eras.
* Correct for overlapping observations and shock clustering using standardized sampling rules.

---

## 5. Result Log (To be completed post-execution)

### 5.1. Baseline vs Conditional Probability Analysis
*(Insert analysis comparing P(Target Large Move | Source Shock) vs P(Target Large Move | Baseline) and Target-matched state)*

### 5.2. Directional Neutrality Audit
*(Insert summary of signed return drift to ensure outcomes are not driven purely by trend effects)*

### 5.3. Incremental Distributional Information Test
*(Insert results detailing if source shocks provide information beyond target state)*

### 5.4. Temporal Stability Assessment
*(Insert breakdown of stability across historical eras)*

---

## 6. Conclusions

### REJECTED RELATIONSHIPS
*(To be populated)*

### EXPLORATORY RELATIONSHIPS
*(To be populated)*

### CANDIDATE STRUCTURAL EDGES
*(To be populated)*

---

## 7. Next Steps
*(To be populated based on candidate discoveries)*
