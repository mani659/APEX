# RC015 Study 000 — Options / Implied Volatility Data Qualification

## 1. Strategic Rationale
Apex has exhausted the M1/M15 OHLCV informational domain for single-instrument retail spot trading. While we successfully validated non-directional volatility expansion via RC012 (`HIGH_VOL`) and RC013 (Session primitives), monetizing these edges in spot architectures exposes the system to unmanageable directional tail risk and cost friction. 
Options (derivatives) naturally isolate and monetize pure volatility expansion (via straddles/strangles) while strictly capping adverse directional excursions to the premium paid. Therefore, acquiring and qualifying options data is the mandatory next step to safely extract the value of our validated OHLCV primitives.

## 2. Options Research Question
> **Does a validated Apex condition (RC012 HIGH_VOL or RC013 Session Transition) predict that realized volatility will differ materially from the implied volatility already priced into options?**

## 3. Required Data Schema
To successfully execute this research on the primary candidate (**EURUSD Options**), the historical dataset must provide:
- `timestamp` (aligned or alignable to M15 boundaries)
- `underlying_price` (reference spot)
- `option_expiry`
- `strike`
- `call_put_flag`
- `bid`, `ask`, `mid` prices
- `option_volume` and `open_interest`
- `implied_volatility` (IV)
- `greeks` (Delta, Gamma, Theta, Vega) where available.

At minimum, the research must be able to securely reconstruct:
- Implied volatility
- Option premium
- Time to expiry
- Moneyness
- Historical option price

## 4. Data-Quality Requirements
Any candidate dataset must undergo strict auditing for:
- **Timestamp Quality**: Timezone, precision, chronological ordering, duplicates, and missing observation density.
- **Contract Identity**: Accurate mapping of strike, expiry, call/put, and underlying.
- **Price Quality**: Bid/ask spreads (detecting crossed markets, stale quotes, or zero/invalid prices).
- **Volatility Quality**: Explicit determination of whether supplied IV is vendor-calculated, exchange-published, broker-derived, or model-derived. Different sources cannot be treated as equivalent.

## 5. Historical Surface Requirements
The data must support querying the historical volatility surface across three dimensions (strike, expiry, time). It must specifically allow reliable extraction of:
- ATM implied volatility
- 25-delta call / 25-delta put
- Short-dated implied volatility
- Term structure
- Volatility skew

*Note: The goal is to verify the raw data can support these queries, not to build a full surface model in Study 000.*

## 6. RC012 Mapping
**Question**: When the `HIGH_VOL` primitive is triggered in the spot market, is future realized volatility systematically above the implied volatility that existed just before the event?

## 7. RC013 Mapping
**Question**: Before major session transitions (e.g., London Open), does the options market's implied volatility systematically understate or overstate the true realized movement that follows?

## 8. Realized-vs-Implied Framework
The core comparison evaluates:
**Realized Volatility** (What actually happened) vs. **Implied Volatility** (What the options market priced).
All comparisons must be rigorously normalized for horizon, annualization convention, and option expiry. Existing RC012 definitions for realized movement remain canonical.

## 9. VRP Framework
**Volatility Risk Premium (VRP)** = `Implied Volatility - Expected/Realized Volatility`
The study must measure the mean, median, distribution, persistence, and temporal stability of the VRP. The ultimate test is whether RC012/RC013 conditions systematically shift the VRP in a predictable manner.

## 10. Cost Framework
Directly comparing realized volatility to mid-price premium is fundamentally invalid. All future options research must incorporate:
- Bid/ask spread and Slippage
- Commission
- Option premium level
- Time decay (Theta)
- Expiry horizon
- Hedging costs (if delta-hedging)
- Underlying transaction costs

## 11. Long-vs-Short Risk Clarification
- **Long Options**: Maximum loss is absolutely bounded by the premium paid. This directly solves the RC012/RC013 spot friction problem.
- **Short Options**: Loss may be very large or theoretically unbounded. Study 000 explicitly forbids assuming that "options = bounded risk" when writing premium.

If a candidate indicates `Expected Realized Vol > Implied Vol + Costs`, then a long-volatility structure (straddle/strangle) becomes the primary candidate.

## 12. Data Acquisition Assessment
Before initiating Study 001, the data acquisition must be classified into one of three states:
- **QUALIFIED**: Reliable historical data exists and is affordable/usable.
- **CONDITIONALLY QUALIFIED**: Data exists but important limitations remain.
- **INSUFFICIENT**: Historical data cannot support rigorous analysis.

## 13. Alternative-Domain Comparison
Options research represents a significantly higher expected probability of actionable knowledge than continuing OHLCV spot research (which has reached terminal diminishing returns). It is also theoretically superior to acquiring carry/funding data (which misaligns with short-term behavioral primitives) or microstructure data (which carries extreme engineering complexity and poor retail execution realism). 

While options data adds engineering complexity and cost, it is the only domain mathematically structured to explicitly price and monetize the exact volatility expansions Apex has already proven it can predict.

## 14. Final Recommendation
**Nominate options / implied volatility as the sole candidate for RC015.**
Halt all spot directional research. The immediate priority is to locate and audit a historical EURUSD options dataset to determine if it meets the **QUALIFIED** status. Only upon successful qualification will RC015 Study 001 commence.
