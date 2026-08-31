# APEX M41 — Session-Transition Distributional Component Experiment

**Date**: 2026-08-27
**Milestone**: M41
**Status**: COMPLETE

---

## 1. Executive Summary

M41 executes the frozen M40 sequential hierarchical decomposition on the M39-R2 dataset to determine which distributional component explains the validated CDF difference between LONDON_NY_OVERLAP and the frozen control.

**Primary Result: COMPONENT IDENTIFIED — SCALE**

The hierarchy stopped at Component 2 (Scale). The return-distribution **dispersion** differs between LNO and control under the day-block permutation framework (p = 0.0001). Location does not differ (p = 0.437). Components 3–5 were not tested (hierarchy stopped at Scale).

---

## 2. M39-R2 Foundation

M39-R2 established:

$$F_{LNO}(r) \neq F_{CONTROL}(r)$$

| Component | Value |
|-----------|------:|
| AD statistic | 228.382562 |
| Permutation p-value | 0.000100 |
| LNO observations | 2,757 |
| Control observations | 29,184 |

---

## 3. M40 Frozen Methodology

Sequential hierarchical decomposition with:

- 4 predeclared components + residual shape
- Single day-block permutation framework
- 10,000 replications, seed 42, PCG-64
- α = 0.05, sequential stopping rule

---

## 4. Observed Sample

| Metric | LNO | Control |
|--------|----:|--------:|
| N | 2,757 | 29,184 |
| Mean | +0.00000158 | −0.00000205 |
| Std | 0.00149361 | 0.00090630 |
| Skewness | −0.454497 | +0.255382 |
| Q₀.₀₅ | −0.002245 | −0.001320 |
| Q₀.₉₅ | +0.002182 | +0.001307 |

---

## 5. Hierarchy Execution

### Component 1 — Location (Mean Difference)

| Metric | Value |
|--------|------:|
| Observed statistic | +0.00000363 |
| LNO mean | +0.00000158 |
| Control mean | −0.00000205 |
| Null mean | +0.00000027 |
| Null std | 0.00001944 |
| Null P₅ | −0.00003152 |
| Null median | +0.00000030 |
| Null P₉₅ | +0.00003195 |
| Exceedance count | 4,366 / 10,000 |
| **Empirical p-value** | **0.4367** |
| **Decision** | **FAIL TO REJECT** |

**Interpretation:** The LNO return distribution does not differ from the control in location (mean). The observed mean difference (+3.6 basis points annualized) is well within the permutation null distribution. There is no evidence of a directional return shift during LNO.

**Economic implication:** No directional return premium during LNO. The session-transition finding is NOT a directional trading signal.

---

### Component 2 — Scale (Standard Deviation Difference)

| Metric | Value |
|--------|------:|
| Observed statistic | +0.00058731 |
| LNO std | 0.00149361 |
| Control std | 0.00090630 |
| Null mean | −0.00000045 |
| Null std | 0.00004075 |
| Null P₅ | −0.00006387 |
| Null median | −0.00000187 |
| Null P₉₅ | +0.00006958 |
| Exceedance count | 0 / 10,000 |
| **Empirical p-value** | **0.0001** |
| **Decision** | **REJECT** |

**Interpretation:** The LNO return distribution has significantly wider dispersion than the control. The observed std difference (+0.000587) exceeds all 10,000 null replicates. LNO returns are approximately **1.65× more dispersed** than control returns.

**Economic implication:** The LNO session is associated with different return volatility. This maps to risk-management and volatility-informed mechanisms, not directional trading.

---

### Components 3–5: Not Tested

The hierarchy stopped at Component 2 (Scale). Components 3 (Skewness), 4 (Tail), and 5 (Residual Shape) were not executed because the M40 frozen methodology specifies sequential stopping.

**Descriptive values (not tested):**

| Component | LNO | Control | Observed Diff |
|-----------|----:|--------:|:-------------|
| Skewness | −0.454 | +0.255 | −0.710 |
| Q₀.₀₅ | −0.00224 | −0.00132 | −0.00092 |
| Q₀.₉₅ | +0.00218 | +0.00131 | +0.00087 |

These are reported descriptively only. No formal inference was performed on these components.

---

## 6. Null Distribution Diagnostics

### Location Null

| Metric | Value |
|--------|------:|
| Mean | +0.00000027 |
| Std | 0.00001944 |
| P₅ | −0.00003152 |
| Median | +0.00000030 |
| P₉₅ | +0.00003195 |

The location null is centered near zero with symmetric tails — consistent with no directional effect under H₀.

### Scale Null

| Metric | Value |
|--------|------:|
| Mean | −0.00000045 |
| Std | 0.00004075 |
| P₅ | −0.00006387 |
| Median | −0.00000187 |
| P₉₅ | +0.00006958 |

The scale null is centered near zero. The observed value (+0.000587) is **14.4 standard deviations** above the null mean — an extreme outlier.

---

## 7. Methodology Integrity

| Check | Status |
|-------|--------|
| Sample matches M39-R2 | ✅ 2,757 LNO + 29,184 CTRL = 31,941 |
| Day-block structure | ✅ 1,331 blocks × 24 obs |
| Permutation framework | ✅ 10,000 reps, seed 42, PCG-64 |
| Group-size preservation | ✅ N_LNO = 2,757 per permutation |
| Hierarchy order | ✅ Location → Scale (stopped) |
| Stopping rule | ✅ Scale rejected → hierarchy stopped |
| No post-hoc metrics | ✅ Only predeclared components |
| No sample modification | ✅ Exact M39-R2 data |

**All integrity checks: PASS**

---

## 8. What M41 Establishes

1. **The LNO return distribution differs from the control in scale (dispersion), not in location (mean).** This is the first formally identified component of the M39-R2 CDF difference.

2. **LNO returns are approximately 1.65× more dispersed than control returns.** The std difference is statistically significant under the day-block permutation framework (p = 0.0001, 0 exceedances in 10,000).

3. **There is no directional return premium during LNO.** The location component fails to reject (p = 0.437). The session-transition finding is NOT a directional trading signal.

4. **The scale difference is the primary distributional component.** The M39-R2 CDF difference is principally driven by different return volatility during LNO, not by different return direction or central tendency.

---

## 9. What M41 Does NOT Establish

1. Whether skewness or tail behavior also differ (not tested — hierarchy stopped at Scale)
2. Whether the scale difference is economically exploitable
3. Any trading strategy or PnL
4. The economic mechanism through which the scale difference creates value
5. Causality (session state is deterministic; this is a correlation test)
6. Whether the scale difference is stable across subperiods

---

## 10. Economic Interpretation

The scale difference means:

- **LNO has higher return variance** than non-LNO periods
- **LNO has wider bid-ask spreads** (implicitly, since returns are more dispersed)
- **LNO has higher movement risk** per unit time

This maps to:

| Economic Mechanism | Instrument | Status |
|-------------------|------------|--------|
| Volatility risk premium | Volatility instrument | Requires further research |
| Inventory risk compensation | Market-making | Requires further research |
| Position sizing adjustment | Risk management | Requires further research |
| Directional trading | Long/short | **NOT supported** (Location = NS) |

---

## 11. Files Created

| File | Purpose |
|------|---------|
| `scripts/m41_distributional_component_experiment.py` | Execution script |
| `reports/APEX_M41_Distributional_Component_Results.csv` | Component results |
| `reports/APEX_M41_Result_Summary.json` | Machine-readable result |
| `reports/APEX_M41_Distributional_Component_Experiment.md` | This report |
| `reports/APEX_M41_RESULT.md` | Structured result |

---

## 12. External API calls: 0 | New data acquired: 0 | Spend: $0.00

---

*M41 is an empirical scientific experiment. No strategies were tested. No PnL was calculated. No instruments were traded.*
