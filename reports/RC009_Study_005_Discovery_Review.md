# RC009 Study 005 — Discovery Campaign Review & Closure Assessment

## 1. Evidence Summary

| Study | Research Dimension | Result | Strongest Finding | Final Status |
|---|---|---|---|---|
| 001 | Local behavioral patterns | Negative | Massive statistical power proved specific local formulations have no conditional edge. | Rejected |
| 002 | Methodology coverage | Mixed | Identified that local pattern definitions are exhausted; pivot to structural blind spots required. | Valid Negative / Limited Scope |
| 003 | State sequences | Negative | Sequences up to N=5 converge back to the baseline of the final state. | Rejected |
| 004 | Cross-market interaction | Negative | No contemporaneous or lagged context market states provided robust incremental information. | Rejected |

## 2. Research Space Coverage

- **Local price behavior:** Tested
- **Volatility behavior:** Tested
- **Participation behavior:** Tested
- **Price/volume interaction:** Tested
- **State transitions:** Tested
- **Sequence behavior:** Tested
- **Event clustering:** Partially Tested (Contiguous sequences tested, but non-contiguous event frequency not tested)
- **Temporal behavior:** Partially Tested (Resting periods tested, but state-duration not tested)
- **Cross-market synchronization:** Tested
- **Lead/lag behavior:** Tested
- **Regime transitions:** Untested (Higher-timeframe macro regimes completely ignored)

## 3. Negative Knowledge Register

1. **Hypothesis:** Local momentum, absorption, and flag structures predict directional returns.
   - **Study:** 001
   - **Evidence:** N > 15,000 samples for each candidate yielded effect sizes near zero with massive statistical power.
   - **Scope of rejection:** The pre-declared local formulations for Momentum Ignition, Absorption, Volatility Compression Breakout, and Low-Participation Pullback tested in RC009 Study 001 did not demonstrate meaningful predictive structure on EURUSD M1.

2. **Hypothesis:** The sequence of states leading to a final state contains more information than the final state itself.
   - **Study:** 003
   - **Evidence:** 22,853 unique sequences of length 5 evaluated; none demonstrated meaningful stable edge compared to the baseline of their final state.
   - **Scope of rejection:** The sequence of M1 Volatility/Direction states (up to length 5) tested in RC009 Study 003 does not contain meaningful predictive information beyond the final state itself on EURUSD M1.

3. **Hypothesis:** Contemporaneous or lagged state information from correlated markets predicts EURUSD better than EURUSD alone.
   - **Study:** 004
   - **Evidence:** 972 cross-market state combinations evaluated at t, t-15, and t-30; no combination met the threshold for a candidate (|d| >= 0.2 and N >= 500) with temporal stability.
   - **Scope of rejection:** The contemporaneous and short-lagged (t-15m, t-30m) 9-state representations of XAUUSD, XAGUSD, BTCUSD, and USATECHIDXUSD tested in RC009 Study 004 do not provide meaningful incremental predictive information for EURUSD M1 beyond its own current state.

## 4. Candidate Evidence Register

- **Study 003 — `NORMAL_VOL_BULL -> NORMAL_VOL_BULL -> NORMAL_VOL_BULL`**
  - **Context:** N=3 Sequence
  - **Sample Size:** 1111
  - **Effect Size:** -0.1010
  - **Temporal Stability:** Not formally evaluated.
  - **Reason NOT Promoted:** Effect size was too weak to justify elevation to CANDIDATE; remained EXPLORATORY (Weak Edge).

- **Study 004 — `USATECHIDXUSD t-30 (HIGH_VOL_BEAR -> LOW_VOL_BULL)`**
  - **Context:** EURUSD `HIGH_VOL_BEAR` + Context `LOW_VOL_BULL` at t-30 lag.
  - **Sample Size:** 184
  - **Effect Size:** 0.212
  - **Temporal Stability:** Not evaluated (N < 500).
  - **Reason NOT Promoted:** Insufficient sample size to trust the observed effect size (N < 500 threshold).

## 5. Research Methodology Assessment

### **Status: SOUND**
The current RC009 discovery framework remains highly disciplined and scientifically useful for one additional limited discovery study.
- **Candidate pre-definition:** Excellent. Prevented p-hacking.
- **Look-ahead protection:** Excellent. Strict bar and sequence alignment.
- **Baseline construction:** Excellent. The Model A matching in Study 004 isolated incremental information cleanly.
- **Multiple-testing discipline:** Excellent. Formal disclosures prevented reporting bias.
- **Sample-size handling:** Excellent. Minimum-N thresholds successfully protected against small-sample mirages.

## 6. Remaining Material Blind Spots

1. **Higher-Timeframe Regime Conditioning**
   - **What remains unknown:** Does EURUSD M1 behavior change conditionally based on the overarching macro regime (e.g., Daily or H4 volatility/trend states)?
   - **Why it matters:** Microstructure is generally subservient to macro regimes. A local momentum ignition in a Daily high-volatility trend regime often behaves fundamentally differently than one in a Daily tight-ranging regime.
   - **Why existing studies missed it:** Studies 001-004 evaluated M1 purely in a local vacuum (maximum 60-bar or 1-week rolling windows on M1), completely ignoring Higher Timeframes.
   - **Would it change our understanding?** Yes. If M1 behavior remains random even when partitioned by HTF regimes, we can definitively prove that no structural M1 alpha exists.

2. **Event Clustering / Frequency**
   - **What remains unknown:** Does the frequency of non-contiguous events (e.g., three absorption events within a 2-hour window) hold predictive edge?
   - **Why it matters:** Institutional accumulation often manifests as clustered, rather than contiguous, anomalies over time.
   - **Why existing studies missed it:** Study 003 tested only contiguous sequences without gaps.
   - **Would it change our understanding?** Yes, but arguably less impactful than HTF conditioning.

3. **Duration-Dependent States**
   - **What remains unknown:** Does the time spent trapped in a specific state alter its exit probability distribution?
   - **Why it matters:** Mean-reversion probabilities often scale directly with the duration of the extremity (rubber-band effect).
   - **Why existing studies missed it:** State definitions were static snapshots (e.g., 15-bar rolling), not duration trackers.
   - **Would it change our understanding?** Yes, but it is a secondary derivative of state transitions.

## 7. Cost-of-Research Assessment

**Potential Direction: Higher-Timeframe Regime Conditioning**
- **Expected information value:** High
- **Complexity:** Low
- **Risk of overfitting:** Low (using standard HTF state primitives)
- **Required data:** Low (EURUSD D1 or H4 already exists or can be generated)
- **Required engineering:** Low (re-use Study 004 framework but map HTF states instead of cross-market states)
- **Probability of producing actionable knowledge:** Medium (highly likely to produce definitive negative knowledge if it fails, closing the campaign permanently).

## 8. Final Decision

### **Option B — ONE FINAL LIMITED STUDY**

The existing discovery framework is inadequate only because evaluating M1 in a vacuum without Higher-Timeframe Regime awareness is a massive material blind spot. We have one clearly defined blind spot that remains sufficiently important to justify exactly one additional study.

## 9. Proposed Research Study (Option B)

**Proposed Research Question:**
Does conditioning EURUSD M1 state behavior on the overarching Higher-Timeframe (e.g., Daily or H4) Volatility and Directional Regime reveal predictive structure that is obscured when analyzing M1 in isolation?

**Why it is uniquely valuable:**
It maps the missing structural link. If M1 behavior is truly random across all macro regimes, we can definitively close behavioral state research and pivot to execution/latency arbitrage or other entirely different families of strategies.

**Minimal dataset required:**
- EURUSD M1 dataset
- EURUSD D1 or H4 dataset

**Minimal experiment required:**
- Construct a 9-state (Vol/Dir) representation on the HTF.
- Evaluate the M1 9-state representation conditioned on the HTF 9-state representation (similar to Model B in Study 004, but intra-market cross-timeframe).

**Strict stop condition:**
If no M1 state + HTF state combination yields an effect size `|d| >= 0.2` with `N >= 500` and temporal stability, RC009 will be permanently closed.

---

## 10. Final Question

> **Have we learned enough from RC009 to know whether continuing this style of behavioral discovery is worth the research cost, or are we now searching simply because we have not yet found a profitable pattern?**

**Answer:** We are on the precipice of searching out of desperation. The immense statistical power of Studies 001-004 proves definitively that local, single-timeframe, or simply-correlated M1 structural edges do not exist in the defined formulations. Continuing to test random M1 indicator combinations would be a waste of research cost. 

However, ignoring the Higher-Timeframe Regime is a known, massive structural flaw in M1 quantitative research. Testing this one final, well-defined blind spot using the proven, robust methodology is worth the minimal research cost because it provides the definitive structural closure required to shut down RC009 without lingering doubt.
