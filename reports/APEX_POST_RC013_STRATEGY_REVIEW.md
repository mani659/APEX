# Project-Level Strategy Review — Post-RC013 Data Constraint Decision

## 1. Current Apex State
The Apex research programme has evolved through rigorous hypothesis testing and systematic rejection of false edges:
- **RC007:** Original V1 entry/exit formulation rejected (asymmetric exits masked negative expectancy).
- **RC008:** Conventional context rescue rejected (context cannot manufacture an edge).
- **RC009:** Behavioral discovery rejected (short-term M1 directional prediction is an illusion).
- **RC010:** Behavioral discovery methodology paused (exhausted current feature space).
- **RC011:** Microstructure research paused (existing tick data lacks true aggressor/trade-level information).
- **RC012:** Methodology V2 successfully discovered and validated a distributional volatility primitive (HIGH_VOL), but tested spot monetization architectures failed due to path truncation, low directional efficiency, and tail-risk inventory compounding.
- **RC013:** Structural carry/funding research paused because the required historical financing data (swap rates, funding histories) is currently unavailable in the repository.

## 2. RC013 Data Constraint vs Hypothesis Rejection
It is critical to distinguish between hypothesis rejection and data constraints. RC013 represents a **DATA CONSTRAINT**. The hypothesis—that structural carry or funding premiums provide a persistent baseline expectancy—was *not* tested and failed. It simply could not be tested because the required historical financing data does not exist in the current Apex data architecture. Therefore, carry/funding remains a theoretically valid source of edge, but it is currently placed in a holding pattern. Do not record carry/funding as negative knowledge.

## 3. Decision Question
> **Is acquiring new financing/funding data justified by its expected information value, or should Apex continue using the data it already has and search for another structural edge?**

## 4. Carry/Funding Acquisition Assessment (Option A)
Acquiring historical FX swap/financing data or crypto perpetual funding rates would answer the specific question of whether a structural financing premium exists. However:
- **What specific unanswered question would it answer?** Whether a financing premium provides a baseline positive expectancy.
- **Could it produce information current data cannot?** Yes.
- **Is the expected value greater than the acquisition and engineering cost?** **NO.** 
Historical MT5 broker swap rates are notoriously opaque, unstandardized, and difficult to reconstruct accurately across years, introducing severe data reliability issues. While crypto funding rates are more accessible, integrating an entirely new asset class structure (perpetual futures) requires massive engineering overhead. Acquiring this data simply because we "ran out of spot hypotheses" violates the core project principles.

## 5. Existing-Data Opportunity Audit (Option B)
The existing canonical datasets (EURUSD, XAUUSD, XAGUSD, BTCUSD, USATECHIDXUSD) contain high-quality M1 OHLCV data. This data can still support fundamentally different structural hypotheses without requiring external acquisition:
- **Distributional Structure:** Exploring the LOW_VOL compression breakout identified in RC012 Study 006, which showed +3.55 pips of net expectancy over a 16-hour horizon.
- **Cross-Asset Relative Structure:** Evaluating cross-sectional momentum or relative value ranking among the 5 assets as a portfolio-level edge, independent of localized prediction.
- **Session / Calendar Mechanics:** Investigating whether structural, deterministic liquidity cycles (e.g., Asian session compression vs. London/NY overlap expansion) create a persistent distributional asymmetry.
- **Volatility Relationships:** Analyzing volatility contagion (e.g., does an RV20 spike in USATECHIDXUSD structurally precede a volatility expansion in BTCUSD or XAUUSD?).

## 6. Research Domain Scorecard

| Domain | Data Availability | Data Quality | Scientific Testability | Execution Realism | Information Value | Economic Potential | Complexity | Cost | Overfit Risk |
|---|---|---|---|---|---|---|---|---|---|
| **Carry / Funding (Option A)** | LOW | LOW (FX Swaps) | MED | HIGH | HIGH | HIGH | HIGH | HIGH | LOW |
| **Session / Calendar Mechanics** | HIGH | HIGH | HIGH | HIGH | HIGH | MED | LOW | LOW | MED |
| **Cross-Asset Volatility** | HIGH | HIGH | HIGH | MED | HIGH | MED | MED | LOW | HIGH |
| **Cross-Sectional Ranking** | HIGH | HIGH | HIGH | MED | MED | MED | MED | LOW | HIGH |

## 7. Over-Engineering Assessment
Pursuing Option A (Data Acquisition) risks over-engineering by drastically expanding the data pipeline and execution assumptions (e.g., perpetual futures hedging) before exhausting the structural opportunities present in the existing high-quality OHLCV data. 
Conversely, testing another variation of M1 directional behavior would also be over-engineering. The optimal path avoids both traps by asking a *structurally new question* using the *existing reliable data*.

## 8. Strategic Options

- **OPTION A:** Acquire high-quality carry/funding data and continue RC013. (Rejected due to high cost and low data reliability for historical broker swaps).
- **OPTION B:** Keep RC013 paused and select one new structural research direction using existing data. (Optimal. Maximizes information gained per unit of cost and complexity).
- **OPTION C:** Pause research entirely. (Premature. Existing data still holds untested, highly credible structural hypotheses).

## 9. Final Decision

**OPTION B** — Keep RC013 paused and select one new structural research direction using existing data.

## 10. Single Next Research Question

> **Do deterministic, structural liquidity cycles (Session/Calendar Mechanics) create a persistent distributional asymmetry (e.g., reliable mean-reversion during low-liquidity windows vs. reliable path-expansion during high-liquidity transitions) that can be monetized without requiring localized behavioral prediction?**

**Why it is superior:** 
This question leverages the existing high-quality M1 data and perfectly aligns with the lessons of RC012 (focusing on distribution and payoff geometry rather than directional prediction). Session mechanics are driven by the physical realities of global banking hours and algorithmic liquidity provision, making them a true structural market property. Unlike volatility (which requires complex dynamic scaling), time-of-day liquidity is deterministic and highly testable, offering a credible path to a robust, non-predictive baseline expectancy at zero additional data cost.
