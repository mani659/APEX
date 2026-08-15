# RC014 Study 001 — Cross-Asset Volatility Transmission Discovery
## Final Execution Protocol

## Objective

Determine whether a volatility shock in one market provides incremental information about the future movement distribution of another market beyond the target market's own contemporaneous information.

This is a structural-discovery study.

It is NOT a trading-strategy study.

---

## 1. Frozen Universe

Use only these eight source → target relationships:

1. EURUSD → XAUUSD
2. EURUSD → XAGUSD
3. USATECHIDXUSD → BTCUSD
4. USATECHIDXUSD → XAUUSD
5. XAUUSD → XAGUSD
6. XAGUSD → XAUUSD
7. BTCUSD → USATECHIDXUSD
8. XAUUSD → EURUSD

Do not add or remove relationships after inspecting results.

---

## 2. Data

Use the canonical M1 datasets already present in Apex.

Convert each asset to standard calendar-aligned M15 bars.

For every source → target relationship:

- inner-align timestamps;
- retain only genuine overlapping observations;
- do not forward-fill;
- do not interpolate;
- report overlap coverage.

---

## 3. Source Volatility Predictor

For every asset calculate:

`RV20(t) = std(r[t-20], ..., r[t-1])`

where:

`r[t] = log(C_t / C_{t-1})`

The current return must NOT enter its own RV20.

---

## 4. Source Volatility Shock

Define:

`HIGH_VOL_SHOCK = source_RV20_percentile > 80`

The historical percentile must be calculated only from source RV20 observations available before the current timestamp.

Do not optimize the 80th percentile.

Do not test alternative thresholds.

Also record continuous:

`source_shock_magnitude`

as the source RV20 percentile or standardized distance from its historical distribution.

---

## 5. Target Information Baseline

At each observation calculate target information available at or before the observation:

- target RV20;
- target recent return;
- target M15 tick volume / relative volume.

The target state is the primary control.

Do not use future target information.

---

## 6. Outcome Timing

For a source shock observed at time `t`, evaluate target outcomes beginning after `t`.

Use exactly:

### Lag 0
Target response from `t` forward over the declared outcome horizon.

### Lag 1
Target response beginning at `t + 1 M15`.

### Lag 4
Target response beginning at `t + 4 M15`.

### Lag 16
Target response beginning at `t + 16 M15`.

Do not introduce additional lags.

For every lag, the target outcome must be strictly forward of the measurement point.

---

## 7. Outcome Horizons

Use the same fixed response horizons:

- 4 M15 bars;
- 16 M15 bars.

Do not add further horizons.

Thus each source shock produces a small, pre-declared response matrix.

---

## 8. Primary Distributional Outcomes

For the target calculate:

- absolute forward return;
- signed forward return;
- future realized volatility;
- maximum absolute excursion;
- total path length;
- net displacement;
- path efficiency.

Also evaluate:

- 90th percentile tail event;
- 95th percentile tail event;
- 99th percentile tail event.

Use the same tail-event definitions established under Apex Methodology V2.

---

## 9. Baseline Construction

For each source → target → lag → horizon combination construct:

### Baseline A — Unconditional Target
All eligible target observations.

### Baseline B — Target-Volatility Matched
Compare the shock population against target observations with comparable target RV20.

Use a pre-declared target-volatility matching method.

Do not optimize the matching rule after viewing results.

### Baseline C — Target-Information-Controlled
Evaluate:

`Target information only`

versus:

`Target information + Source HIGH_VOL_SHOCK`

The purpose is to determine whether the source actually adds information.

---

## 10. Incremental Information Test

The key comparison is:

### Model A
Target-only information:

- target RV20;
- target recent return;
- target volume.

### Model B
Target-only information + source volatility shock.

For every outcome calculate the incremental change in:

- tail probability;
- future volatility;
- absolute return;
- path length;
- path efficiency.

Do NOT treat a source-only difference as sufficient evidence.

---

## 11. Conditional Probability

For each source shock calculate:

`P(target_large_move | source_shock, target_control)`

Compare against the appropriate target-controlled baseline.

Report:

- conditional probability;
- baseline probability;
- absolute probability uplift;
- relative risk.

Do this separately for:

- P90;
- P95;
- P99.

---

## 12. Directional Neutrality

For every relationship report:

- signed mean return;
- median signed return;
- positive-return probability;
- negative-return probability.

The primary candidate is volatility transmission, not directional transmission.

A directional result may be reported, but it must not be promoted as the primary finding.

---

## 13. Dependence Treatment

Source volatility shocks may cluster and target outcomes may overlap.

Therefore:

### Descriptive Population
Retain all valid observations.

### Inferential Population
Use one identical non-overlapping anchor schedule for every relationship and comparison.

The sampling rule must not depend on whether a source shock occurred.

Do not selectively thin strong relationships.

Report:

- raw N;
- inferential N;
- shock frequency;
- average shock-cluster duration.

---

## 14. Temporal Stability

Split the historical sample into:

- Early;
- Middle;
- Recent.

For each relationship that appears promising, report:

- tail probability uplift;
- relative risk;
- target future volatility;
- path length;
- path efficiency.

Do not change the historical partitions after seeing results.

---

## 15. Multiple-Testing Disclosure

Report the full multiplicity:

- 8 source → target relationships;
- 4 lags;
- 2 outcome horizons;
- 3 tail thresholds;
- all primary distributional metrics.

Do not promote a relationship merely because it has the largest statistic.

A candidate must demonstrate:

- economic relevance;
- stability;
- adequate sample size;
- incremental information beyond target state.

---

## 16. Candidate Classification

### REJECTED
No meaningful incremental information beyond target-only controls.

### EXPLORATORY
Source shock shows incremental distributional information but is weak, unstable, or economically small.

### CANDIDATE STRUCTURAL EDGE
Source volatility shock demonstrates:

- meaningful incremental distributional information;
- stable temporal behavior;
- adequate sample size;
- economically relevant uplift;
- robustness to target-volatility control.

### VALIDATED STRUCTURAL PRIMITIVE
Not permitted in Study 001.

Any candidate must undergo independent validation.

---

## 17. Governance

Do NOT:

- create trading signals;
- create entries/exits;
- combine with HIGH_VOL;
- combine with session transitions;
- optimize lags;
- optimize thresholds;
- optimize matching;
- introduce ML;
- add new assets;
- modify the production engine.

This is transmission discovery only.

---

## 18. Data Integrity Audits

Automate checks for:

- chronological ordering;
- duplicate timestamps;
- missing observations;
- exact overlap;
- source predictor lookahead;
- target outcome lookahead;
- invalid M15 bars;
- insufficient forward horizon;
- timezone consistency.

The report must explicitly state the number of lookahead violations.

Required result:

`0`

---

## 19. Deliverables

Create:

`reports/RC014_Study_001_Cross_Asset_Volatility_Dataset.parquet`

`reports/RC014_Study_001_Cross_Asset_Volatility_Analysis.md`

The report must include:

1. Data coverage
2. Relationship universe
3. RV20 construction
4. Shock definition
5. Lookahead audit
6. Target-information baselines
7. Conditional probabilities
8. Incremental-information analysis
9. Directional neutrality
10. Path/distribution analysis
11. Dependence treatment
12. Temporal stability
13. Multiple-testing disclosure
14. Candidate register
15. Rejected register
16. Final scientific conclusion

---

## 20. Final Scientific Question

> **Does a volatility shock in one asset provide incremental information about another asset's future movement distribution beyond the target asset's own current volatility, return, and volume information?**

If YES:

→ Candidate cross-asset structural primitive.

If NO:

→ Cross-asset volatility transmission is not a sufficiently useful research direction under the tested universe.

---

## Final Principle

Do not ask:

> "Which market leads which?"

Ask:

> **"Does source-market volatility contain incremental information that the target market itself does not already reveal?"**

That is the test that makes RC014 materially different from the earlier cross-market research.
