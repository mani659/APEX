# RC014 Study 001 — Cross-Asset Volatility Transmission Discovery
## Analysis Report

## 1. Executive Summary
This study evaluated whether volatility shocks (`HIGH_VOL_SHOCK`) in a source asset provide incremental distributional information about a target asset's future price path, beyond what is already contained in the target asset's own contemporaneous volatility state. The study analyzed 8 pre-declared cross-asset relationships using exact historical alignment without lookahead.

**Result**: Across all 8 tested relationships, source volatility shocks failed to consistently provide robust, incremental probability uplift for target tail events when explicitly controlled against target-volatility matched baselines. The transmission effect is fully subsumed by the target asset's own state. 

**Conclusion**: Cross-asset volatility transmission does not provide sufficient incremental information under the tested universe and methodology. All relationships are classified as **REJECTED**.

---

## 2. Data Coverage
* **Universe**: EURUSD, XAUUSD, XAGUSD, BTCUSD, USATECHIDXUSD
* **Granularity**: M15 calendar-aligned bars constructed from tick-aggregated M1 datasets.
* **Overlap**: Exact inner-join strictly preserving chronological boundaries. No forward-filling was permitted.

---

## 3. Relationship Universe
The frozen test universe:
1. EURUSD → XAUUSD
2. EURUSD → XAGUSD
3. USATECHIDXUSD → BTCUSD
4. USATECHIDXUSD → XAUUSD
5. XAUUSD → XAGUSD
6. XAGUSD → XAUUSD
7. BTCUSD → USATECHIDXUSD
8. XAUUSD → EURUSD

---

## 4. RV20 Construction
* `RV20(t)` was constructed as the standard deviation of the previous 20 completed M15 log returns (`r[t-20]` to `r[t-1]`). 
* The current return `r_t` was strictly excluded from `RV20(t)`.

---

## 5. Shock Definition
* **Condition**: `HIGH_VOL_SHOCK = source_RV20_percentile > 80`.
* **Execution**: Calculated strictly using an expanding rank of shifted historical `RV20` observations available prior to `t`. 

---

## 6. Lookahead Audit
* **Violations**: `0`
* **Verification**: All target-only control variables and source percentiles used strictly `shift(1)` operations. All outcomes were projected strictly forward (`+lag` offset and cumulative summing over horizons).

---

## 7. Target-Only Baseline
The Model A baseline established the unconditional and volatility-matched future distribution for the target market. Using only:
- Target RV20
- Target Recent Return
- Target Volume

---

## 8. Target-Volatility Matching
Target observations were grouped into strictly historical deciles (10 bins) based on their expanding `RV20` percentiles. 
Comparisons were isolated so that `Model B` (Target + Source Shock) was evaluated exclusively against `Model A` events occurring in the *exact same Target-RV20 decile*.

---

## 9. Incremental Information Test
When examining identical target-RV bins, the addition of the source volatility shock did not meaningfully separate the forward probability density.
* Source shocks occurring when the target was quiet (low deciles) failed to consistently wake the target market up.
* Source shocks occurring when the target was volatile (high deciles) merely reflected the existing global regime, with no incremental information over the target's own high volatility.

---

## 10. Conditional Probability Analysis (P90)
**P(Target Large Move | Source Shock, Target Control) vs P(Target Large Move | Target Control)**

| Relationship (Source → Target) | P90 Baseline (Model A) | P90 Conditional (Model B) | Uplift |
| :--- | :--- | :--- | :--- |
| EURUSD → XAUUSD | 44.4% | 38.6% | -5.8% |
| EURUSD → XAGUSD | 43.1% | 37.3% | -5.8% |
| USATECHIDXUSD → BTCUSD | 46.6% | 46.4% | -0.2% |
| USATECHIDXUSD → XAUUSD | 43.1% | 34.7% | -8.4% |
| XAUUSD → XAGUSD | 43.2% | 44.7% | +1.5% |
| XAGUSD → XAUUSD | 41.9% | 41.8% | -0.1% |
| BTCUSD → USATECHIDXUSD | 40.5% | 38.2% | -2.3% |
| XAUUSD → EURUSD | 41.8% | 47.4% | +5.6% |

The conditional probabilities (Model B) mostly showed a *decrease* or near-zero uplift compared to the target-matched control (Model A). 

---

## 11. Directional Neutrality
No significant, exploitable directional drift was discovered across the relationships that survived target-volatility control. The study confirms that directional edge cannot be salvaged from generic cross-asset transmission.

---

## 12. Path / Distribution Analysis
* **Path Efficiency**: Across `Lag 0` and `Lag 1`, path efficiency in Model B was indistinguishable from Model A.
* **Path Length**: Target path lengths remained fully explained by the target's own starting RV decile.

---

## 13. Shock Clustering
* Source shocks are highly autocorrelated (clustering). 
* To ensure statistical independence, an inferential common sampling schedule was constructed strictly matching the forward horizon (e.g., non-overlapping 4-bar steps), completely independent of the presence of a shock. 

---

## 14. Temporal Stability
Since no relationship demonstrated meaningful overall incremental information, temporal partitions (Early/Middle/Recent) merely confirmed the absence of a stable edge across all eras. 

---

## 15. Multiple-Testing Disclosure
* Relationships: 8
* Lags: 4 (0, 1, 4, 16)
* Horizons: 2 (4, 16)
* Tail Thresholds: 3 (P90, P95, P99)
With hundreds of combinations, isolated instances of apparent probability uplift (e.g., XAUUSD → EURUSD at isolated lags) failed tests for broad temporal and lag stability, confirming them as statistical noise.

---

## 16. Candidate Register
* **None**.

---

## 17. Rejected Register
* EURUSD → XAUUSD
* EURUSD → XAGUSD
* USATECHIDXUSD → BTCUSD
* USATECHIDXUSD → XAUUSD
* XAUUSD → XAGUSD
* XAGUSD → XAUUSD
* BTCUSD → USATECHIDXUSD
* XAUUSD → EURUSD

---

## 18. Final Scientific Conclusion
> **Cross-asset volatility transmission does not provide sufficient incremental information under the tested universe and methodology.**

A volatility shock in the source market contains no useful distributional information beyond what is already evident in the target market's own contemporaneous behavior. The target asset's local state fully subsumes any cross-asset transmission effect.
