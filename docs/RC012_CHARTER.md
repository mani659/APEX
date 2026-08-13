# RC012 Study 000 — Alternative Edge Research Charter

## Campaign
**RC012 — Alternative Edge Research**

## Status
**PLANNED**

---

## 1. Executive Summary
RC012 represents a fundamental pivot in Apex's research philosophy. Having definitively exhausted local directional price patterns (RC007–RC010) and paused microstructure research due to data limitations (RC011), RC012 changes the research question entirely. Rather than attempting to predict the absolute direction of a single asset, this campaign seeks to identify a non-directional structural edge that is scientifically testable using our existing high-quality M1 datasets. 

Based on a rigorous evaluation of data availability, complexity, and information value, **Statistical Relative Value (Pairs/Cointegration)** has been selected as the primary research domain.

## 2. Current Apex Research State
- **Platform**: Validated and stable.
- **V1 Strategy**: Rejected.
- **Behavioral Discovery**: Paused (exhausted without success).
- **Microstructure**: Paused (data insufficient).
- **Production Bot**: Not yet validated because no durable trading edge has been identified.

## 3. Candidate Research Domains
**A — Statistical Relative Value:** Pair relationships, spread behavior, cointegration, synthetic instruments, relative-value mean reversion.
**B — Cross-Asset Relative-Value Structures:** Divergence between economically related assets (e.g., Gold vs. Silver).
**C — Carry / Funding / Yield Structures:** Persistent structural return sources from interest-rate differentials or funding rates.
**D — Structural Session / Calendar Effects:** Recurring behavioral structures associated with market-session mechanics or calendar events.

## 4. Evaluation Criteria
Each domain is scored as HIGH, MEDIUM, or LOW against:
- Data Availability
- Data Quality
- Scientific Testability
- Execution Realism
- Complexity
- Overfitting Risk
- Information Value
- Profitability Relevance

## 5. Comparative Scoring

| Domain | Data Availability | Testability | Execution Realism | Complexity | Overfit Risk | Information Value | Profitability Relevance |
|---|---|---|---|---|---|---|---|
| **A: Statistical Relative Value** | HIGH | HIGH | HIGH | MEDIUM | MEDIUM | HIGH | HIGH |
| **B: Cross-Asset Structures** | HIGH | HIGH | HIGH | MEDIUM | MEDIUM | HIGH | HIGH |
| **C: Carry / Yield Structures** | LOW | HIGH | MEDIUM | HIGH | LOW | HIGH | MEDIUM |
| **D: Session / Calendar Effects** | HIGH | HIGH | HIGH | LOW | HIGH | MEDIUM | MEDIUM |

## 6. Over-Engineering Assessment
RC012 must explicitly guard against feature accumulation, arbitrary parameter sweeps, and the premature introduction of Machine Learning. The selected domain must be tested using the **smallest experiment capable of falsifying the hypothesis**. To prevent over-engineering, we will rely on classical statistical models (e.g., Augmented Dickey-Fuller tests for cointegration) before any advanced modeling is considered. We will strictly utilize our existing datasets rather than building expensive infrastructure.

## 7. Primary Research Direction
**PRIMARY: Domain A — Statistical Relative Value**
*Justification:* Apex currently holds multi-year M1 OHLCV datasets for multiple highly related assets (e.g., XAUUSD and XAGUSD). This data is perfectly sufficient to test statistical cointegration and spread mean-reversion. The hypothesis is objectively testable, fundamentally different from single-asset directional prediction, and can realistically be executed in MT5 by managing opposing positions. The expected information value is high, as relative-value strategies are a proven institutional paradigm.

## 8. Secondary Directions
**SECONDARY: Domain B — Cross-Asset Relative-Value Structures**
*Justification:* Highly correlated to Domain A, focusing on macroeconomic divergences rather than purely statistical spread mean-reversion.

**SECONDARY: Domain D — Structural Session / Calendar Effects**
*Justification:* Data is readily available and complexity is low, but overfitting risk is severe. It remains a backup option if relative value fails.

## 9. Deferred / Rejected Directions
**DEFERRED: Domain C — Carry / Funding / Yield Structures**
*Justification:* While scientifically valid, Apex currently lacks historical swap rates, yield curves, and crypto funding rates. Sourcing this data violates the RC012 mandate to prioritize existing datasets and avoid acquiring complexity prematurely.

## 10. RC012 Governance Rules
1. Do not download new data.
2. Do not modify the production engine.
3. Do not run historical experiments or parameter optimizations during the charter phase.
4. Do not introduce ML.
5. Do not create trading signals or execution logic yet.

## 11. Final Recommendation
**Domain A (Statistical Relative Value)** is selected as the sole focus of RC012 Study 001. 

> **What type of market structure gives us the best remaining opportunity to discover a real edge using data we can actually trust and eventually trade?**
*Answer: The statistical relationship between two correlated instruments, analyzed for stationarity and spread mean-reversion, independent of broader market direction.*

The RC012 research pipeline will now pivot exclusively to establishing a statistical relative-value testing framework.
