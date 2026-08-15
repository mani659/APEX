# RC015 Study 000 — Options Data Sourcing & Qualification

## 1. Strategic Rationale
To safely monetize the pure volatility expansion primitives discovered in RC012 (`HIGH_VOL`) and RC013 (Session transitions), Apex requires historical options data. This report evaluates the technical feasibility, cost, and completeness of primary data venues (CME DataMine and Databento) to determine the safest and most economical acquisition path.

## 2. CME Qualification (DataMine)
CME DataMine is the official self-service platform for historical CME data. It provides authoritative End-of-Day (EOD) options settlements and the CVOL index.
- **Access**: Direct via CME Group portal.
- **Use Case**: Best for daily settlement extraction, closing implied volatilities, and daily baseline risk assessments.
- **Drawback**: Intraday tick data from DataMine can be prohibitively expensive and cumbersome for rapid programmatic research compared to modern APIs.

## 3. Databento Qualification
Databento is a licensed distributor of CME Globex MDP 3.0 data.
- **Dataset ID**: `GLBX.ALL`
- **Coverage**: Includes CME Euro FX futures (6E) and all associated options on futures.
- **Earliest History**: June 2010 (covering the required 2021–Present window).
- **Format**: Available as Market-By-Order (MBO), Top-Of-Book (TBBO), OHLCV, and Trades. APIs in Python/Rust/C++.
- **Pricing**: Pay-as-you-go per gigabyte. A small sample test (e.g., one day of TBBO) costs cents, making qualification testing extremely cheap.
- **Drawback**: Databento provides *raw market data* (prices and volumes). It does **not** provide pre-calculated implied volatility or Greeks. These must be reconstructed using a pricing model.

## 4. CVOL Qualification
The **CME EUR/USD CVOL Index** is a 30-day forward implied volatility benchmark derived from options on Euro FX futures.
- **Availability**: Historical EOD data available via CME DataMine.
- **Utility**: Highly useful as a low-complexity, macro "Level 1" gauge of whether the broad options market underprices/overprices overall variance around certain regimes.
- **Limitation**: As a 30-day aggregated benchmark, it cannot reconstruct exact intraday option execution for an M15 session transition.

## 5. Option-Chain Qualification
Through Databento's symbology and instrument definitions, the complete Euro FX option chain (calls and puts across all strikes and expirations for a given date) can be reconstructed programmatically. This ensures exact strike selection (ATM vs OTM) and expiry matching.

## 6. Historical Coverage
- **Requirement**: `2021-01-01 → present`.
- **Result**: Fully satisfied by both CME DataMine and Databento (which stores CME data back to 2010).

## 7. Schema Availability
### Level 1 (CVOL)
Available via CME. Schema: Date, Index Value.
### Level 2 (Settlements)
Available via CME. Schema: Date, Contract, Settlement Price, Volume, Open Interest.
### Level 3 (Intraday)
Available via Databento (TBBO/Trades). Schema: Timestamp, Bid, Ask, Trade Price, Size, Instrument ID. *Missing: Implied Volatility and Greeks.*

## 8. Timestamp Quality
CME Globex timestamps via Databento are PTP hardware-stamped at the matching engine (nanosecond precision). Chronological order and timezone (UTC) are guaranteed. This perfectly satisfies the `lookahead violations = 0` mandate.

## 9. Spot/Futures Basis Assessment
The validated Apex primitives operate on spot EUR/USD. CME options are written on Euro FX futures (6E).
- **The Basis**: The difference between spot and futures is driven by the interest rate differential (Carry) between the USD and EUR. 
- **Volatility**: Intraday basis volatility is statistically negligible. Around London/NY session transitions (RC013) or `HIGH_VOL` clusters (RC012), the future tracks the spot tick-for-tick. 
- **Conclusion**: CME Euro FX options are a perfectly valid proxy for trading spot EUR/USD volatility.

## 10. Cost Assessment
- **Small Test (Databento)**: Submitting a limited historical API query for 1 week of Euro FX options TBBO data will cost less than $10, establishing full technical schema validation.
- **Full Acquisition (Databento)**: 5 years of full intraday TBBO for Euro FX options requires processing terabytes of raw CME data. Through Databento's targeted parent-symbol filtering, this is estimated to cost low hundreds of dollars.
- **CME DataMine**: Pricing is enterprise/quote-based. CVOL and EOD settlements may incur flat licensing fees.

## 11. Licensing / Reproducibility
Databento manages CME licensing automatically. Internal research and strategy development are generally covered under non-display or internal usage, avoiding heavy commercial redistribution fees. Reproducibility is high due to the Python API.

## 12. Engineering Complexity
**High.** 
Because Level 3 intraday data (Databento) does not supply pre-calculated IV, Apex must build a strict Black-76 options pricer to back out implied volatility from the bid/ask midpoints, requiring accurate alignment of the underlying futures price and a risk-free rate proxy.

## 13. Data-Quality Risks
- Options on futures can suffer from wide bid/ask spreads during illiquid overnight sessions (Asian session).
- Reconstructing IV requires exact synchronization between the option timestamp and the underlying future timestamp.

## 14. Recommended Acquisition Level
**Acquire Intraday Option Quotes/Trades (LEVEL 3) via Databento — CONDITIONALLY QUALIFIED.**
While CVOL (Level 1) is easier, it fails to answer the core RC015 question: *Does an RC012/RC013 event create actionable mispricing for a specific M15 options structure?* Only Level 3 TBBO (Top of Book) data can reconstruct the actual bid/ask execution premium and back out the intraday implied volatility surface.

## 15. Final Decision
**Option C — Acquire Intraday Option Quotes/Trades (conditionally).**
Because Level 3 requires building a custom Black-76 pricer, we must run a minimal viability test first.

**Next Action**: Run a highly restricted, low-cost API request to Databento for a single week of Euro FX options (TBBO + underlying futures) to prove that Apex can successfully reconstruct implied volatility before committing to the full 2021–present acquisition.
