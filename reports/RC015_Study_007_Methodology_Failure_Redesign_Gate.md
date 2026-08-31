# RC015 Study 007 — Methodology Failure & Redesign Gate

## 1. Proven Successful Components
The following components of the study have been proven successful and validated by the evidence:
- **Historical option/futures mapping**: Successfully mapped 100% of the 222 frozen events, resulting in 707 unique option candidates (Stage-1 + Stage-2 Recovery).
- **Contemporaneous futures midpoint reconstruction**: Successfully processed 222/222 events, extracting midpoints for validation.
- **Exact moneyness rule**: `abs(strike - futures_mid) <= 0.0020` correctly identified the frozen 699-option / 700-row instrument universe.
- **BBO acquisition**: Acquired 100% of the required data (997,986 rows originally, correctly recovered the missing datasets for 2022-04-27, 2025-12-24, and 2025-12-31).
- **Zero-lookahead timestamp construction**: Study 006 microtest verified 0 lookahead violations using `ts_event <= t` logic.
- **Black-76 IV pipeline**: Successfully demonstrated in earlier pilots.

## 2. Proven Failed Component
The evidence definitively supports the following conclusion:
> The continuous 24-hour Wednesday M15 option-observation design is not economically observable at sufficient quote freshness across the 222-event universe.

This is fundamentally proven by the quote-age diagnostic. With a target of 21,312 predetermined M15 slots across 222 events, only 91 slots (0.4%) contained freshly synchronized option and futures quotes.

## 3. Quantification of Failure
- **Total scheduled slots**: 21,312
- **Genuinely synchronized fresh slots**: 91 (0.4%)
- **≤ 5-minute coverage**: 1,240 slots (1.8%)
- **≤ 15-minute coverage**: 2,963 slots (4.4%)
- **≤ 30-minute coverage**: 5,127 slots (7.6%)
- **≤ 60-minute coverage**: 8,665 slots (12.9%)
- **Number of events reaching 25% coverage**: 2 (at 5m), 2 (at 15m), 4 (at 30m), 25 (at 60m)
- **Number of events reaching 50% coverage**: 0 (at 5/15/30m), 1 (at 60m)
- **Number of events reaching 75% coverage**: 0
- **Number of events reaching 100% coverage**: 0
- **Median option quote age**: ~9 hours (549.7 minutes across events)
- **Normal-day quote age**: 410.7 minutes (median)
- **Holiday quote age**: 425.8 minutes (median), maxing up to 22 hours due to early closes

These figures are fundamentally inconsistent with reliable full-grid IV/RV evaluation. Without fresh quotes, the pipeline would match deeply stale options with fresh futures, generating spurious variance gaps that do not represent tradeable reality.

## 4. Nature of the Failure
This failure is unequivocally classified as a combination of:
- **C. Market-structure limitation**: The required market observations simply do not exist frequently enough in the underlying listed EUR/USD option market.
- **D. Methodology-design limitation**: The methodology demands observation density (a strict 24-hour chronological grid at M15 frequency) that the instrument cannot support.

It is **not** an Acquisition Failure (the BBO data was fully acquired and successfully recovered) nor a Processing Failure (the diagnostic explicitly proved zero forward-filling and maintained strict timestamp integrity).

## 5. Testing the Freshness Rule Repair
> Can the existing methodology be repaired merely by specifying an as-of quote-age tolerance?

**No.**
Using the already completed predeclared policies (≤5, ≤15, ≤30, ≤60 minutes), not a single one provides sufficient cross-event coverage.
Even with a 60-minute freshness policy, only 1 event out of 222 reaches a 50% slot coverage rate. The existing 21,312-slot design cannot be salvaged by relaxing the quote age because the quote gaps naturally stretch for several hours.

## 6. Theoretical Redesign Viability
An alternative observation design could theoretically be frozen **ex ante**. 
The failure lies in demanding a continuous 24-hour evaluation on a sparse asset. However, if an observation schedule were designed to sample at fixed liquid-session windows or predetermined daily anchors, it could still meet the strict scientific governance constraints. 

## 7. Final Classification
**`INCONCLUSIVE — REDESIGN REQUIRED`**

The economic hypothesis remains meaningful and the analytical pipeline functions perfectly, but the frozen observation design is unusable due to fundamental market structure sparsity. A new methodology can and must be specified ex ante.

## 8. Redesign Requirements Specification (For Future Study)
Any future redesign opening a new study MUST satisfy the following requirements:
- **What must be frozen ex ante**: The specific observation timestamps or session windows must be perfectly defined prior to evaluating any IV/RV or PnL outcomes.
- **What cannot be optimized**: The observation schedule cannot be chosen by maximizing variance gaps or scanning the current dataset for hours that produce profitable results.
- **What data-density requirement must be met**: A quote-availability pre-check must verify that the vast majority of requested observation slots have option quotes within a strict freshness tolerance (e.g., 5 or 15 minutes) before proceeding to volatility calculations.
- **What evidence must be collected before opening the new study**: A structural liquidity analysis proving that the selected schedule corresponds to actual exchange activity (e.g., European/US overlap hours), preventing data-mining.
- **What would distinguish a scientifically valid redesign from data-mining**: The redesign must apply deterministically to all historical and future events, maintain the definition of HIGH_VOL, preserve maturity-matched RV, and rely on external market mechanics (like session overlaps) rather than empirical coverage maximization.
