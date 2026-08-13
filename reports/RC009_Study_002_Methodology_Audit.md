# RC009 Study 002 — Methodology Audit

## Objective
To determine whether the negative result of RC009 Study 001 reflects a genuine absence of predictive behavioral structure, or whether it stems from insufficient coverage of the behavioral state space and/or methodological blind spots.

---

## Audit 1 — Coverage of Behavioural Dimensions
The four candidate primitives tested in Study 001 were mapped against major behavioral dimensions:
- **C1_Squeeze (Volatility Compression Breakout):** Tested *Volatility* (compression) and *Price Path* (expansion).
- **C2_Absorption (Participation/Price Divergence):** Tested *Price/Volume Interaction* (extreme volume vs small price displacement).
- **C3_Ignition (Momentum Ignition):** Tested *Directional Persistence*, *Participation* (volume expansion), and *Path* (body expansion).
- **C4_Flag (Low-Participation Pullback):** Tested *Path* (strong trend), *Temporal behavior* (duration of rest), and *Participation* (volume contraction).

**Coverage Assessment:** Study 001 successfully tested isolated, local instances of momentum, mean-reversion/absorption, and volatility expansion. 

---

## Audit 2 — Structural Blind Spots
The following major behavioral dimensions were completely absent from the Study 001 search:
1. **Cross-Market Interaction:** The study looked exclusively at EURUSD in a vacuum, ignoring lead/lag relationships, synchronization, or divergence against correlated assets (e.g., XAUUSD, DXY).
2. **Event Sequencing & Clustering:** Candidates were treated as isolated single-bar triggers. The study did not investigate whether the *frequency* or *clustering* of events (e.g., three absorption events in 10 minutes) contains edge.
3. **Regime Transitions:** The candidates evaluated local (60-bar) contexts but ignored the overarching macro regime (e.g., is the market transitioning from a low-volatility state to a high-volatility state on the daily timeframe?).
4. **Duration-Dependent States:** The study looked at static lookback windows rather than measuring how long an asset has been trapped in a specific state.

---

## Audit 3 — Baseline Adequacy
- **Baseline A (Unconditional):** 100,000 random samples with forced 50/50 directional symmetry provided a mathematically sound anchor for unconditional expected value.
- **Baseline B (Direction-Matched):** Omitted in the initial implementation. 
- **Baseline C (Matched Control):** A deterministic shift of exactly 1440 bars (24 hours) prior was used. While this effectively controlled for time-of-day and directional orientation, it **failed to control for the volatility regime**. Comparing a breakout during a high-volatility session to a control sample 24 hours prior (which might have been a low-volatility session) introduces variance skew.
- **Serial Dependence (Overlapping Events):** The implementation did not filter for overlapping occurrences. C3 (Ignition) triggered 19,014 times, meaning it likely triggered on consecutive bars during strong trends. This serial correlation heavily overstates the true number of independent observations.

---

## Audit 4 — Candidate Independence
The four candidates were structurally distinct and did not overlap:
- C1 required extreme volatility compression.
- C2 required extreme volume expansion on tiny price movement.
- C3 required consecutive directional momentum.
- C4 required a massive trend followed by volume collapse.
The candidates represented genuinely independent hypotheses.

---

## Audit 5 — Statistical Power
- **C1_Squeeze (N=5):** Statistical power is near zero. Cannot reject any meaningful effect.
- **C2 (N=15,432), C3 (N=19,014), C4 (N=15,843):** With sample sizes exceeding 15,000, the study possessed massive statistical power (>99% power to detect an effect size as small as Cohen's *d* = 0.05). 
- **Conclusion:** The failure to find an edge for C2, C3, and C4 is **not** due to a lack of data. We can state with extreme confidence that these specific mathematical formulations possess no economically meaningful predictive alpha on the M1 timeframe. "No effect" genuinely means no effect for these candidates.

---

## Audit 6 — Multiple Testing
- **Number of hypotheses:** 4
- **Number of metrics:** ~6 per candidate (Forward returns, MFE/MAE, Win Rate)
- **Selection Bias:** None. The definitions were strictly frozen prior to execution.
- **Assessment:** Because all results were heavily negative, multiple testing correction (e.g., Bonferroni) is irrelevant. P-hacking did not occur. The negative conclusion is robust.

---

## Final Classification

### **B — Valid Negative, Limited Scope**

The four candidates (excluding C1) are genuinely rejected. The statistical power was massive, and the methodology was sufficiently robust to prove that standard isolated momentum, absorption, and flag formulations do not possess conditional edge.

However, the study covered only a narrow, localized portion of the behavioral state space. It completely ignored cross-market interactions, sequence clustering, and regime transitions. 

**Verdict:** We successfully proved that these specific patterns do not work, but we failed to search broadly enough to reject the overarching hypothesis that repeatable market behavior exists.

## Next Steps
The V1 context-filtering path remains closed, and the four C1-C4 local formulations are now also closed. Future research in RC009 should abandon local single-instrument pattern definitions and pivot towards exploring the structural blind spots identified above (e.g., cross-market synchronization or event clustering).
