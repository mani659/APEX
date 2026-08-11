# Research Campaign RC001 — Final Archive & Closure

## 1. Campaign Overview
- **Research Objective**: Investigate institutional liquidity sweeps as a primary signal for predictive continuation in the XAUUSD market.
- **Hypothesis**: Price pushing beyond a significant structural liquidity level and subsequently rejecting implies an accumulation/distribution event that predicts a directional continuation.
- **Methodology**: Systematic statistical analysis of historical tick data (aggregated to M1) over a 5-year period. Features were built using Smart Money concepts and conditioned with various market context parameters. 20-bar forward returns were used as the primary label. Strict QA rules required the 95% Confidence Interval to exclude zero, an effect size $\ge 0.05$, a win rate $\ge 50\%$, and temporal stability.
- **Dataset**: XAUUSD M1 (April 2021 - April 2026), ~1.7 million rows.
- **Validation Process**: Two-step validation involving automated statistical generation followed by an independent QA robustness verification pass checking for sample adequacy, directional consistency, and temporal stability.

---

## 2. Timeline

- **Study 001**: Liquidity Sweep
  - *Objective*: Test the base predictive power of a liquidity sweep.
  - *Hypothesis*: Sweeps predict continuation.
  - *Outcome*: INCONCLUSIVE. Highly noisy, weak effect size.
  
- **Study 002**: Liquidity Sweep + Market Regime
  - *Objective*: Condition sweeps by trend alignment.
  - *Hypothesis*: Sweeps in direction of the trend perform better.
  - *Outcome*: CANDIDATE. Displayed promising preliminary statistics.

- **Study 003 (QA)**: Robustness Verification
  - *Objective*: Independently verify Study 002.
  - *Outcome*: REJECTED (FRAGILE). Bearish sweeps inside bear trends produced confidence intervals crossing zero.

- **Study 004**: Liquidity Sweep + Expansion
  - *Objective*: Condition sweeps by immediate volatility expansion (momentum).
  - *Hypothesis*: Sweeps followed by $>1$ ATR expansion confirm the move.
  - *Outcome*: REJECTED (NOT SUPPORTED).

- **Study 005**: Liquidity Sweep + Session
  - *Objective*: Condition sweeps by market session (time of day).
  - *Hypothesis*: Sweeps during specific sessions are more institutional.
  - *Outcome*: SUPPORTED (Initially). "Other" session showed strong metrics.

- **Study 005 QA**: Session Robustness Verification
  - *Objective*: Independently verify Study 005.
  - *Outcome*: REJECTED (FRAGILE). The "Other" session edge was temporally unstable and failed directional logic for short setups (bearish sweeps produced positive mean returns).

- **Study 006**: Liquidity Sweep Taxonomy
  - *Objective*: Classify sweeps by structural rejection strength.
  - *Hypothesis*: "Strong Rejection" sweeps isolate the edge.
  - *Outcome*: REJECTED (NOT SUPPORTED). Failed to isolate a statistically valid directional edge.

---

## 3. Verified Findings

### Confirmed
- *(None)*. No hypothesis survived the strict QA validation process across both bullish and bearish directions.

### Rejected
- Liquidity Sweep + Trend Regime alignment (Failed QA - CI crossing zero).
- Liquidity Sweep + Post-Sweep Expansion (Failed statistical significance).
- Liquidity Sweep + Session Conditioning (Failed QA - Temporal instability and directional failure).
- Liquidity Sweep Rejection Taxonomy (Failed statistical significance).

### Inconclusive
- The base liquidity sweep without any conditioning filters remains a noisy event indistinguishable from random market behavior over a 20-bar horizon.

---

## 4. Statistical Summary
- **Datasets**: 1 main XAUUSD dataset (~100,000 recent samples used per pipeline run).
- **Experiments Executed**: 6 core experiments archived in the repository.
- **Validation**: Independent QA verification correctly invalidated two seemingly profitable candidate edges due to underlying structural fragility (directional inconsistencies and temporal instability).
- **Confidence Verification**: Across all attempts, the bearish continuation scenario repeatedly failed to produce a 95% Confidence Interval that cleanly excluded zero on the negative side.
- **Robustness Testing**: Sample starvation and temporal concentration were successfully identified and mitigated through QA.

---

## 5. Research Lessons
- **Liquidity Sweep alone is insufficient**: The base event is too common and noisy to predict directional continuation.
- **Regime improved conditional averages but failed robustness**: Aligning with the trend improved the mean, but variance remained too high to form a reliable edge.
- **Expansion after sweep degraded execution**: Waiting for a $>1$ ATR confirmation move destroyed the risk/reward profile and failed to improve win rates.
- **Session conditioning failed temporal stability**: While some sessions looked profitable in aggregate, year-by-year analysis revealed they were driven by isolated periods and failed to perform directionally for short trades.
- **Sweep taxonomy failed to isolate a robust class**: Structurally classifying the sweep by closing rejection strength did not effectively separate a predictive signal from the noise.

---

## 6. Final Scientific Conclusion
**Did RC001 demonstrate a robust predictive edge?**
No. Research Campaign RC001 conclusively demonstrated that the specific definition of an institutional liquidity sweep used in this study does **not** possess a robust, statistically significant, and directionally consistent predictive edge for a 20-bar continuation, regardless of how aggressively the signal is filtered by trend, momentum, time of day, or structural taxonomy.

---

## 7. Future Recommendations
- **New Hypotheses**: Shift focus away from standard liquidity sweeps. The current definition captures too much noise.
- **Alternative Market Behaviors**: Investigate Mean Reversion rather than Continuation. A sweep might be better modeled as an exhaustion event leading to a reversal back into the range rather than a continuation beyond it.
- **Different Event Definitions**: Explore volume-delta clusters or order-flow imbalances instead of purely price-based swing high/low sweeps.

---

## 8. Archive Manifest
- **Experiments**: `experiment_000001` through `experiment_000006`
- **Reports**: 
  - `Study_001_Report.md` through `Study_006_Report.md`
- **QA Reports**:
  - `Study_003_QA_Report.md`
  - `Study_005_QA_Report.md`
- **Repository Location**: `research/RC001_Continuation/repository`
- **Completion Date**: 2026-08-02
