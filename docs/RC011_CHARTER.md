# RC011 Study 000 — Order-Flow & Microstructure Research Charter

## Campaign
**RC011 — Order-Flow & Execution Microstructure Research**

## Status
**PLANNED**

---

## 1. Scientific Objective

Define the next research direction for Apex after the behavioral discovery pause established by RC010.

RC007–RC010 demonstrated that the tested price/volatility/state-based behavioral formulations did not produce a validated trading edge on EURUSD M1.

Therefore, RC011 will investigate a fundamentally different information source:

> **Order-flow and execution microstructure.**

The objective is to determine whether information contained in trading activity itself provides predictive information that cannot be extracted from conventional OHLCV price-state representations.

This is a research campaign.
It is NOT a redesign of the Apex production engine.

---

## 2. Primary Research Question

> **Does order-flow / microstructure information contain measurable incremental predictive information about short-term future market behavior beyond conventional price and volume data?**

The campaign must first establish whether such information exists before attempting to turn it into a trading strategy.

---

## 3. Why This Direction

The previous campaigns primarily analyzed:
- price;
- volatility;
- volume;
- market states;
- sequences;
- cross-market states;
- higher-timeframe regimes.

These approaches did not produce a validated edge. RC011 therefore changes the information domain rather than adding more filters to the same domain.

The research focus becomes:
- trade flow;
- aggressor direction;
- imbalance;
- bid/ask interaction;
- liquidity response;
- execution friction.

---

## 4. Research Boundaries

RC011 must NOT begin by building:
- a BUY/SELL predictor;
- a neural network;
- a portfolio model;
- a scalping strategy;
- an order-book trading system;
- a latency arbitrage system.

First determine whether microstructure variables contain useful information at all.

---

## 5. Initial Market

Use **one market only** for the first experiment.

**Preferred initial market:**
EURUSD

**Reason:**
- extensive existing Apex research history;
- canonical historical data already available;
- previous price-based research provides a strong baseline;
- the objective is to determine whether microstructure adds information to a well-understood research environment.

Do not expand to Gold, BTC, NQ, or other assets until the first microstructure experiment justifies it.

---

## 6. Required Data

RC011 requires data beyond ordinary M1 OHLCV.

Potential required information includes:
- timestamped trades;
- trade price;
- trade size;
- aggressor direction where available;
- bid;
- ask;
- spread;
- tick direction;
- execution count;
- short-term order-flow imbalance.

If the available dataset cannot support exact reconstruction of a proposed microstructure variable, the report must explicitly state that limitation. Do not substitute an approximate variable without labeling it as approximate.

---

## 7. Candidate Microstructure Variables

The initial discovery experiment should remain deliberately small. Investigate only:

### 1. Aggressor Imbalance
Difference between buy-initiated and sell-initiated activity.

### 2. Volume Imbalance
Relative buying versus selling volume.

### 3. Trade Intensity
Number of trades per unit time.

### 4. Spread State
Current spread relative to recent spread distribution.

### 5. Price Response to Flow
Price movement relative to the amount of observed directional flow.

These are research variables only. They are not trading rules.

---

## 8. Primary Baseline

Every microstructure variable must be compared against the existing conventional-information baseline:
- price return;
- ATR;
- volume;
- current volatility state.

The question is:
> Does microstructure add information beyond what price/volume already tells us?

---

## 9. Experimental Unit

Use a fixed, pre-declared observation interval.

**Initial proposal:**
1-minute observation blocks

Do not search different intervals until the first experiment is complete.

---

## 10. Outcome Variables

For each observation calculate:
- Forward 5-minute return
- Forward 15-minute return
- Forward 60-minute return
- MFE
- MAE
- continuation probability
- reversal probability

These horizons are deliberately short because microstructure information should primarily affect near-term behavior.

---

## 11. Statistical Analysis

For each microstructure variable:
- sample size;
- distribution;
- conditional forward return;
- conditional MFE;
- conditional MAE;
- effect size;
- confidence interval;
- temporal stability.

Use pre-declared quantile bins where appropriate. Do not search hundreds of thresholds.

---

## 12. Incremental Information Test

The critical comparison is:

### Model A
Price + Volume information only.

### Model B
Price + Volume + one microstructure variable.

The objective is to determine whether Model B provides meaningful incremental information.
Do NOT compare only against an unconditional market baseline.

---

## 13. Multiple-Testing Protection

The report must disclose:
- variables tested;
- outcome horizons;
- number of comparisons;
- sample sizes;
- exploratory nature of the study.

A variable is not considered successful merely because it produces the largest effect.

---

## 14. Candidate Classification

### REJECTED
No meaningful incremental information.

### EXPLORATORY
Some evidence exists but is weak or unstable.

### CANDIDATE
Meaningful incremental information survives sample-size and temporal-stability checks.

### SUPPORTED
Not permitted in Study 001. Any supported microstructure effect requires independent validation.

---

## 15. Data Integrity Requirements

Before any statistical experiment:
1. Validate chronological ordering.
2. Validate duplicate timestamps.
3. Validate missing data.
4. Validate bid/ask consistency where available.
5. Validate trade-direction classification.
6. Validate spread calculations.
7. Confirm timezone conventions.
8. Confirm that no future information enters the microstructure variables.

If the data cannot support reliable order-flow reconstruction, stop the study rather than using a questionable proxy.

---

## 16. Governance

RC001–RC010 remain frozen.

Do NOT:
- modify the Apex production engine;
- modify RC007;
- modify RC008;
- modify RC009;
- introduce ML;
- introduce new behavioral filters;
- optimize parameters;
- optimize timeframes;
- create execution rules;
- create portfolio rules.

RC011 is strictly an information-discovery campaign.

---

## 17. Success Definition

RC011 Study 001 will be considered informative if it can answer:

> **Does microstructure contain incremental short-horizon predictive information that conventional OHLCV cannot explain?**

### Positive result
A microstructure variable demonstrates meaningful, stable incremental information.
→ Candidate for independent validation.

### Negative result
Microstructure variables provide no meaningful information beyond price/volume.
→ Another major information domain is eliminated.
