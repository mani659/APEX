# RC009 Study 001 — Candidate Behavioral Discovery

## Objective
To discover whether the canonical Apex research datasets contain a genuinely different, repeatable market behavior with predictive information independent of the rejected Version 1 formulation.

## Discovery Framework
This exploratory study examined the EURUSD M1 canonical dataset for four explicitly defined behavioral primitives:
1. **C1_Squeeze**: Volatility Compression Breakout
2. **C2_Absorption**: Participation/Price Divergence
3. **C3_Ignition**: Momentum Ignition
4. **C4_Flag**: Low-Participation Pullback

Every candidate occurrence was detected using only backward-looking information, preventing look-ahead bias. Three baselines were generated for comparison (Unconditional, Directional, and Deterministic Control).

## Study Results

### Multiple Testing Disclosure
- **Number of candidate hypotheses tested:** 4
- **Number of outcome metrics examined:** 6+ per candidate
- **Number of candidates showing promising results:** 0
- **Status:** This was an exploratory discovery phase, and all tests yielded negative or insufficient results.

---

### Candidate 1: Volatility Compression Squeeze
- **Hypothesis:** Sustained extreme historical compression followed by a massive displacement signals a structural breakout.
- **Occurrences:** 5 (0.0002% frequency)
- **Result:** **REJECTED** (Insufficient Sample Size). The threshold parameters were so strict that the event practically never occurred in the 2-million bar history.

### Candidate 2: Participation/Price Divergence (Absorption)
- **Hypothesis:** Massive volume ( > 95th percentile) resulting in a tiny price range and body signals absorption, predicting a reversal.
- **Occurrences:** 15,432 (0.75% frequency)
- **Win Rate:** 50.1% (60-bar forward)
- **Effect Size:** 0.019 (vs Unconditional Baseline)
- **Result:** **REJECTED** (No Meaningful Effect Size). The market behaved essentially as a coin flip after this event, identical to the unconditional baseline.

### Candidate 3: Momentum Ignition
- **Hypothesis:** 3 consecutive bars in the same direction, with expanding bodies and expanding volume, signals institutional participation and short-term continuation.
- **Occurrences:** 19,014 (0.93% frequency)
- **Win Rate:** 48.4% (60-bar forward)
- **Effect Size:** -0.009 (vs Unconditional Baseline)
- **Result:** **REJECTED** (No Meaningful Effect Size). The signal possessed zero momentum continuation edge; returns were statistically indistinguishable from noise.

### Candidate 4: Low-Participation Pullback (Flag)
- **Hypothesis:** A massive 60-bar trend followed by a 15-bar low-volume compression predicts trend resumption.
- **Occurrences:** 15,843 (0.77% frequency)
- **Win Rate:** 42.7% (60-bar forward)
- **Effect Size:** -0.056 (vs Unconditional Baseline)
- **Result:** **REJECTED** (No Meaningful Effect Size). Returns were slightly *negative* relative to the baseline, indicating failed continuations rather than successful ones, but not strong enough to exploit.

---

## Verdict: Negative Outcome
The campaign successfully generated a clean empirical map of four distinct market hypotheses across the canonical EURUSD dataset. 

No sufficiently strong new behavioral phenomenon was found. 

All four candidate formulations are formally **REJECTED** and logged in the Rejected Candidate Register. The data demonstrates that standard momentum, absorption, and flag formulations, as strictly defined here, contain no conditional predictive edge on the EURUSD M1 timeframe.
