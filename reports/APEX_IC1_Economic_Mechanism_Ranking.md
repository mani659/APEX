# APEX IC1 — Economic Mechanism Ranking

**Date**: 2026-08-25
**Milestone**: IC1

---

## Final Ranking

| Rank | Candidate | Score / 50 | Class | Main Reason |
|------|-----------|-----------:|-------|-------------|
| 1 | A: Crypto Options Vol Monetization | 42 | HIGH PRIORITY | Strongest payoff alignment; instrument accessible; data available; mechanism intelligible |
| 2 | D: Directional Instrument | 36 | REJECT | M24 conclusively eliminates directional translation; RC012 spot monetization failed |
| 3 | E: EURUSD Options (Fallback) | 28 | LOW PRIORITY | Signal IS validated on EURUSD but instrument data is inaccessible (RC015) |
| 4 | B: Barrier/Range Products | 25 | REJECT | M31 boundary saturation; exotic barriers illiquid |
| 5 | C: Relative-Value Volatility | 24 | REJECT | Requires two predictive legs; APEX has one; RC014 cross-asset rejected |

---

## Detailed Ranking Rationale

### Rank 1: Candidate A — Crypto Options Vol Monetization (42/50, HIGH PRIORITY)

**Score Breakdown:**
- Economic Payoff Alignment: 5/5 — Convex payoff directly rewards the quantity APEX predicts (movement magnitude)
- Market Accessibility: 4/5 — Deribit is retail-accessible; requires KYC but no institutional gate
- Liquidity: 4/5 — Deribit has ~85% BTC options market share; ~$4.2B daily volume
- Historical Data: 5/5 — Available since March 2019 via Tardis, CryptoDataDownload, Deribit API
- Data Cost: 4/5 — Free historical data via API; no subscription required
- Execution Realism: 3/5 — Options execution during vol events may have wider spreads; slippage risk during onset
- OOS Feasibility: 4/5 — Chronological split possible with 5+ years of BTC options data
- Structural Simplicity: 4/5 — Buy straddle when risk score exceeds threshold; well-defined
- Scientific Novelty: 5/5 — Genuinely new; NOT RC015; different asset class, different exchange
- Strategy Potential: 4/5 — Simple falsifiable trade: "Does predicted RV exceed IV on BTC during HIGH_VOL onset?"

**Why Rank 1:**
This is the only candidate that satisfies all three critical requirements simultaneously:
1. The instrument payoff matches APEX's non-directional prediction (convex payoff)
2. The instrument is accessible with historical data available
3. The economic mechanism is intelligible and testable

The primary risk is the unvalidated cross-asset transfer assumption (HIGH_VOL trained on EURUSD, applied to BTC). This is a significant assumption but is explicitly testable as a prerequisite to IC2.

**Reuse from APEX history:**
- Builds on: M17-R2 prediction methodology (adapted), M21 RV translation, M27 excursion translation
- Does NOT reopen: HIGH_VOL (uses it as background), RC013, RC014, RC015
- Genuinely new: Yes — first time APEX evaluates crypto options as an instrument class

---

### Rank 2: Candidate D — Directional Instrument (36/50, REJECT)

**Score Breakdown:**
- Economic Payoff Alignment: 1/5 — Payoff requires direction; APEX has none (M24 p=0.6418)
- Market Accessibility: 5/5 — EURUSD spot/CFD/futures universally accessible
- Liquidity: 5/5 — EURUSD is the most liquid financial instrument
- Historical Data: 5/5 — Complete, high-quality, multi-year
- Data Cost: 5/5 — Existing canonical dataset
- Execution Realism: 4/5 — Spot execution is straightforward
- OOS Feasibility: 4/5 — Chronological split easy
- Structural Simplicity: 5/5 — Simplest possible instrument
- Scientific Novelty: 1/5 — RC012 Studies 007–011 already rejected spot monetization
- Strategy Potential: 1/5 — No directional prediction exists

**Why Ranked 2 but REJECTED:**
Despite excellent accessibility and data scores, this candidate is eliminated by the fundamental mismatch between APEX's non-directional signal and spot's directional requirement. M24 (p=0.6418) conclusively established no directional translation exists. RC012 Studies 007–011 empirically failed at spot monetization. No amount of instrument accessibility compensates for a signal that does not align with the payoff structure.

**Reuse from APEX history:**
- Reopens: RC012 spot monetization (already rejected)
- Verdict: ELIMINATED — payloff mismatch is structural

---

### Rank 3: Candidate E — EURUSD Options Fallback (28/50, LOW PRIORITY)

**Score Breakdown:**
- Economic Payoff Alignment: 5/5 — Perfect match (same as Candidate A)
- Market Accessibility: 2/5 — CME listed options require institutional access; RC015 demonstrated infeasibility
- Liquidity: 2/5 — RC015 found insufficient liquidity for observation design
- Historical Data: 2/5 — RC015 found data problematic (CME listed-option data constraints)
- Data Cost: 2/5 — Historical options data requires paid sources; quality uncertain
- Execution Realism: 2/5 — Listed option execution architecture infeasible per RC015
- OOS Feasibility: 3/5 — Would be feasible IF data were available
- Structural Simplicity: 4/5 — Same as Candidate A
- Scientific Novelty: 3/5 — Mechanism is new; instrument is problematic
- Strategy Potential: 3/5 — Highest potential IF instrument constraints resolved

**Why Rank 3 and LOW PRIORITY:**
EURUSD options are the ideal instrument from a signal-validation perspective (the signal IS validated on EURUSD). But RC015 conclusively demonstrated that CME listed-option data and liquidity are insufficient for the required observation design. This candidate can only re-enter if:
1. A new EURUSD options data source with sufficient liquidity is identified
2. The observation design requirements are relaxed to match available liquidity
3. An alternative EURUSD options venue (e.g., Saxo, IG, Interactive Brokers) provides sufficient historical data

This is a data-constrained path, not a hypothesis-rejected path.

**Reuse from APEX history:**
- Reopens: RC015 mechanism (not the implementation)
- Status: DATA-CONSTRAINED — may re-enter if data becomes available

---

### Rank 4: Candidate B — Barrier/Range Products (25/50, REJECT)

**Score Breakdown:**
- Economic Payoff Alignment: 3/5 — Movement-magnitude payoff matches prediction
- Market Accessibility: 3/5 — Exotic barriers available on some platforms
- Liquidity: 2/5 — Exotic barrier products have wide spreads
- Historical Data: 4/5 — Reconstructable from spot data
- Data Cost: 4/5 — Uses existing data
- Execution Realism: 2/5 — Exotic execution is complex
- OOS Feasibility: 3/5 — Feasible if products exist
- Structural Simplicity: 2/5 — Barrier level selection, expiry matching, path dependency
- Scientific Novelty: 1/5 — M31 boundary saturation already failed (99.75%)
- Strategy Potential: 1/5 — M31 demonstrated the signal cannot discriminate breach vs non-breach

**Why REJECTED:**
M31 already demonstrated the core problem: at reasonable boundary levels, the breach probability is ~100%, providing zero discriminative power. Lowering the boundary increases the premium cost. Raising it reduces the probability further. The signal's excursion prediction is continuous, but barrier products are binary — and M31 proved the continuous-to-binary translation fails.

**Reuse from APEX history:**
- Reopens: M31 boundary testing (already failed)
- Verdict: ELIMINATED — M31 saturation is structural

---

### Rank 5: Candidate C — Relative-Value Volatility (24/50, REJECT)

**Score Breakdown:**
- Economic Payoff Alignment: 2/5 — Requires two predictive legs; APEX has one
- Market Accessibility: 3/5 — Depends on specific structure
- Liquidity: 3/5 — Depends on specific structure
- Historical Data: 3/5 — One leg available, second leg requires assumptions
- Data Cost: 3/5 — Partial data availability
- Execution Realism: 2/5 — Multi-leg execution is complex
- OOS Feasibility: 2/5 — Requires two validated predictions
- Structural Simplicity: 2/5 — Multi-leg structures are inherently complex
- Scientific Novelty: 2/5 — Novel concept but insufficient data
- Strategy Potential: 2/5 — Cannot proceed without second predictive leg

**Why REJECTED:**
Relative-value strategies require predicting the relationship between two quantities. APEX predicts one (EURUSD forward RV) but has no second predictive leg. RC014 conclusively rejected cross-asset transmission — there is no validated second leg. Without two validated predictions, relative-value is a design exercise, not a testable hypothesis.

**Reuse from APEX history:**
- Reopens: Nothing — this is a new concept
- Verdict: INSUFFICIENT DATA — no second validated predictive leg

---

## Decision: CONTINUE

A credible economic mechanism and instrument exist (Candidate A: Crypto Options Vol Monetization).

The next authorized milestone is:

> **IC2 — Economic Mechanism Methodology Design**

IC2 must:
1. Determine whether HIGH_VOL onset dynamics transfer to BTC (cross-asset validation)
2. Design the frozen methodology for the IV-RV divergence test
3. Freeze all parameters before execution
4. NOT begin IC3

---

## STOP / CONTINUE Gate

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Is there a realistic instrument? | ✅ YES | BTC options on Deribit |
| Is there a credible economic mechanism? | ✅ YES | Predicted RV > IV → profit from convexity |
| Is the instrument accessible? | ✅ YES | Deribit retail-accessible |
| Is historical data available? | ✅ YES | Since 2019 via Tardis/CryptoDataDownload |
| Can the hypothesis be frozen? | ✅ YES | Pre-definable score threshold + IV-RV comparison |
| Does it reopen a rejected branch? | ❌ NO | Genuinely new instrument class |

**Decision: CONTINUE to IC2.**
