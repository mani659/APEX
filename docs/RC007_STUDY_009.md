# RC007 Study 009: Exit Architecture De-conflation

## Scientific Objective
Determine whether the apparent profitability observed in the Apex Version 1 historical engine is a genuine positive-expectancy effect of the exit architecture, or whether the high win rate is primarily the result of accepting negatively-skewed tail risk.

## Methodology
The 410 qualified, isolated entries from Study 007 were evaluated under three independent models:
- **Model 1 — Observation Only**: Fixed 240-bar observation window (No active exit logic).
- **Model 2 — Frozen Apex Exit**: Production exit architecture (Inventory Management).
- **Model 3 — Simple Symmetric Reference**: Pre-declared fixed 1R:1R reference model (to test symmetric predictive accuracy).

## Primary Findings

### The Symmetric Truth (Model 3)
When forced into a symmetric 1R:1R paradigm, the underlying behavioral entry signal yields a **28.5% win rate** and an expectancy of **-0.00012**. This confirms conclusively that the signal possesses negative intrinsic alpha and fails to predict favorable near-term direction. 

### The High-Win-Rate Illusion (Model 2)
The production exit architecture completely warps this underlying distribution. By harvesting winners extremely early (Average Winner: 0.00152) and allowing losers to run extraordinarily deep (Average Loser: -0.00746), the system inflates the win rate to **89.0%** and shifts the mean expectancy positive (+0.00057).

### Tail-Risk Explosion
The cost of this positive expectancy is catastrophic tail risk. 
- The **Worst 5%** of losses account for **88.0%** of the entire loss distribution.
- The **Maximum Loss** (-0.06983) is so severe that it requires **45.9 consecutive average winners** to offset. 
- This negatively-skewed distribution guarantees ruin under infinite exposure time.

## Edge De-conflation Summary
- **Signal Edge:** Negative (28.5% symmetric predictive accuracy).
- **Recovery Edge:** Zero (Grid expansion never executes under frozen rules).
- **Exit Architecture:** Dominant, creating an artificial 89% win rate by packaging the negative expectancy into rare but devastating tail events.

## Scientific Verdict
**Outcome B — High-Win-Rate Illusion:** The architecture produces many small winners but negative or fragile expectancy due to large tail losses. The strategy does not extract an edge through predictive accuracy; it merely hides negative alpha in the tail of the distribution.
