# RC013 Study 000 — Structural Carry / Funding Research Charter

## Campaign
**RC013 — Structural Carry / Funding Research**

## Status
**PLANNED**

## 1. Strategic Objective
Begin a new research programme focused on structural sources of expectancy that do not require short-term directional prediction. 
This campaign follows the RC012 project-level strategy review. The strategic decision is to move away from short-term directional behavioral prediction, HIGH_VOL spot monetization, microstructure requiring unavailable data, and increasingly complex payoff engineering.
The new research focus is: **Structural carry / funding / financing effects.**

## 2. Primary Research Question
> **Can persistent financing, carry, or funding differences create a measurable positive baseline expectancy that can be harvested without requiring short-term directional prediction?**

The initial research must determine whether such a structural return source exists in the markets and instruments available to Apex.
This is NOT a strategy-development study.

## 3. Why Carry / Funding
RC012 demonstrated that validated information can exist without a tradable spot payoff, non-directional volatility can be real but difficult to monetize safely in spot, and directional prediction is not the only possible source of edge.
Carry/funding is attractive because the source of return may be embedded in the market structure itself rather than requiring prediction of the next price movement. The hypothesis is therefore fundamentally different from RC007–RC012 behavioral prediction.

## 4. Candidate Carry Domains
Evaluate only the following initially:

### A — FX Carry / Swap
Potential sources: long/short financing differences, interest-rate differential effects, broker swap structures.

### B — Crypto Funding
Potential sources: perpetual-futures funding payments, persistent funding-rate imbalances, market-neutral funding capture.

### C — Cross-Asset Financing Differences
Only if the existing datasets contain sufficiently reliable information to support the analysis.
Do not expand beyond these categories during the charter phase.

## 5. Data Qualification Comes First
Before any profitability experiment, determine what historical carry/funding information is actually available.
For each candidate domain identify whether we have:
- historical swap rates;
- historical funding rates;
- financing costs;
- contract specifications;
- trading-session rules;
- rollover timing;
- leverage/margin assumptions;
- historical prices needed to construct the hedge.

Do NOT assume that current broker swap/funding data can be used as historical data.

## 6. Existing Apex Data Audit
Inspect the repository for: symbol metadata, swap rates, contract specifications, funding-rate histories, broker-specific financing files, existing account statements or historical financing records.
Do not modify the production engine. Do not acquire external data yet.

## 7. Economic Definition
Separate:
- **Carry Yield**: The financing/carry received or paid for holding a position.
- **Price Return**: Movement in the underlying asset.
- **Total Return**: Carry + price return + transaction costs.

The research must NOT confuse a positive carry rate with positive total strategy expectancy.

## 8. Market-Neutral Requirement
Where the hypothesis is intended to be market-neutral, explicitly define: long exposure, offsetting short exposure, hedge ratio, financing received, financing paid, transaction costs, residual directional exposure.
Do NOT assume that "market neutral" means zero directional exposure unless it is mathematically demonstrated.

## 9. Carry Persistence
For any available carry/funding series, measure: mean, median, standard deviation, positive/negative frequency, persistence, duration, regime changes, extreme observations. Do NOT yet optimize entry or exit.

## 10. Total-Cost Framework
Any future carry experiment must include: financing/carry, spread, commission, slippage, rollover effects, hedge costs, funding-payment timing.
The goal is **net economic expectancy**, not headline carry yield.

## 11. Candidate Qualification
A structural carry hypothesis may become a candidate only if: the historical financing source is measurable, the data is trustworthy, the carry persists sufficiently, transaction and hedge costs are identifiable, the total-return mechanism is economically plausible, and the result can eventually be executed through a realistic trading architecture.

## 12. Governance
Do NOT: build a trading strategy, optimize leverage, optimize holding period, introduce ML, create a portfolio optimizer, add dozens of assets, assume current funding data represents historical funding, purchase data automatically, modify RC012, modify RC007–RC011.
This first study is strictly research qualification.

## 13. Deliverables
Create: `docs/RC013_CHARTER.md` and `reports/RC013_Study_000_Data_Qualification.md`.

## 14. Decision Rule
If a carry/funding domain has: trustworthy historical data, clear economic mechanics, realistic execution, and measurable net-return potential → nominate it as the sole candidate for RC013 Study 001.
If no domain meets those requirements → pause RC013 and return to strategic review. Do not force the research to continue simply because carry/funding was selected in the strategic review.

## Final Principle
Apex is no longer asking: "Can we predict the next move?" Nor: "Can we force a volatile spot market to pay us?"
The question is now: **"Does the market contain a persistent structural source of return that exists before we predict direction?"**
That is the next hypothesis worth testing.
