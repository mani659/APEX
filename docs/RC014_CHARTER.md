# RC014 Study 000 — Cross-Asset Volatility Transmission Research Charter

## Campaign
**RC014 — Cross-Asset Volatility Transmission**

## Status
**PLANNED**

---

## 1. Strategic Objective

Begin a new research campaign investigating whether volatility shocks propagate systematically between related markets.

This campaign follows the closure of:
* RC007 — V1 directional formulation;
* RC008 — conventional context rescue;
* RC009 — behavioral/state discovery;
* RC010 — behavioral/ML regime discovery;
* RC011 — microstructure research;
* RC012 — volatility distribution and payoff research;
* RC013 — session structural mechanics.

The objective is to investigate a **different structural mechanism**:
> **Does a measurable volatility shock in one market change the future movement distribution of another market?**

This is not a directional prediction study.

---

## 2. Why This Is Different

RC009 Study 004 tested cross-market **state combinations and short lags**.
RC014 must NOT repeat that framework.

Instead, RC014 will study:
* continuous realized-volatility changes;
* volatility shocks;
* shock magnitude;
* persistence;
* cross-asset transmission;
* future distributional response.

The research question is therefore:
> **Does volatility information propagate across assets even when directional information does not?**

---

## 3. Primary Asset Universe

Use only the canonical datasets already available:
* EURUSD
* XAUUSD
* XAGUSD
* BTCUSD
* USATECHIDXUSD

*Note: Do not acquire new data. Do not add Oil because the canonical dataset is not currently available.*

---

## 4. Candidate Transmission Relationships

Investigate the following directional relationships:
* **EURUSD → XAUUSD**
* **EURUSD → XAGUSD**
* **USATECHIDXUSD → BTCUSD**
* **USATECHIDXUSD → XAUUSD**
* **XAUUSD → XAGUSD**
* **XAGUSD → XAUUSD**
* **BTCUSD → USATECHIDXUSD**
* **XAUUSD → EURUSD**

*Note: Additional relationships may be listed descriptively, but do not expand the formal test universe after seeing results.*

---

## 5. Experimental Unit

Use standard M15 observations.
Construct the same canonical M15 bars used in RC012 and RC013.

* All timestamps must be aligned exactly.
* Do not forward-fill missing market observations.
* Only use timestamps where the required source and target observations are valid.

---

## 6. Source Volatility Variable

For every asset calculate:
### RV20
Standard deviation of the previous 20 completed M15 log returns.
Do not include the current return. This keeps the predictor strictly causal.

---

## 7. Volatility Shock Definition

Define a volatility shock using the source asset's historical RV20 distribution.

### HIGH_VOL_SHOCK
Source RV20 above its frozen 80th percentile.

### SHOCK_MAGNITUDE
Current source RV20 relative to its historical RV distribution.

*Note: Do NOT optimize the percentile. Do NOT search alternative thresholds.*

---

## 8. Lag Structure

Evaluate only three pre-declared lags:
* contemporaneous;
* +1 M15;
* +4 M15;
* +16 M15.

Interpretation:
If source shock occurs at time `t`, measure target response beginning at:
* `t`;
* `t + 15m`;
* `t + 1h`;
* `t + 4h`.

*Note: Do not add additional lags after inspecting results.*

---

## 9. Primary Outcome

The target asset's future **movement distribution** is the primary outcome.

For every source shock calculate:
* absolute return;
* realized future volatility;
* 90th percentile tail-event probability;
* 95th percentile tail-event probability;
* 99th percentile tail-event probability;
* total path length;
* net displacement;
* path efficiency;
* maximum absolute excursion.

*Direction remains secondary.*

---

## 10. Directional Neutrality

For every source-target relationship report:
* signed mean return;
* median signed return;
* positive-return probability;
* negative-return probability.

The primary hypothesis is volatility transmission, not directional transmission. A relationship should not be promoted merely because it happens to contain directional drift.

---

## 11. Baselines

For every source-target relationship calculate:

### Baseline A
Unconditional target outcome distribution.

### Baseline B
Target volatility matched baseline.

This is important because a source volatility shock may coincide with periods when the target is already volatile.

The question is therefore:
> **Does the source volatility shock add information beyond the target's own current volatility state?**

---

## 12. Incremental Information Test

For each source-target pair and lag compare:

### Model A
Target's own current information:
* target RV20;
* target recent return;
* target volume.

### Model B
Target information + source volatility shock.

The central test is:
> **Does the source asset add incremental distributional information beyond the target's own state?**

*Note: Do not evaluate source-only effects as sufficient evidence.*

---

## 13. Conditional Probability

For large movement events calculate:
`P(Target Large Move | Source Volatility Shock)`

versus:
`P(Target Large Move | Baseline)`

Report:
* conditional probability;
* unconditional probability;
* absolute probability uplift;
* relative risk.

Also calculate the same metrics after conditioning on the target's own volatility state.

---

## 14. Temporal Stability

Split the historical sample into:
* Early
* Middle
* Recent

For every promising transmission relationship report:
* tail probability uplift;
* relative risk;
* target future volatility;
* path length;
* path efficiency.

A relationship that exists only in one historical era is exploratory.

---

## 15. Dependence Treatment

Source volatility shocks may cluster. Target outcomes may overlap. Therefore:
* retain full-resolution descriptive observations;
* use a common non-overlapping observation schedule for primary inferential comparisons;
* apply identical sampling rules to all source-target combinations.

*Note: Do not selectively thin the strongest relationships.*

---

## 16. Multiple-Testing Protection

Disclose:
* assets;
* directional relationships;
* lag count;
* tail thresholds;
* total comparisons.

Do not rank relationships by the strongest p-value or largest effect alone.
A candidate must show:
* economic relevance;
* temporal stability;
* adequate sample size;
* incremental information.

---

## 17. Candidate Classification

### REJECTED
No incremental information beyond the target's own state.

### EXPLORATORY
Source volatility appears related to future target distribution but is weak or unstable.

### CANDIDATE STRUCTURAL EDGE
A source volatility shock provides:
* meaningful incremental distributional information;
* stable temporal behavior;
* adequate sample size;
* economically relevant uplift.

### VALIDATED STRUCTURAL PRIMITIVE
Not permitted in Study 000. Independent validation would be required.

---

## 18. Governance

Do NOT:
* create trading signals;
* create entries/exits;
* combine with HIGH_VOL;
* combine with session transitions;
* introduce ML;
* optimize lags;
* optimize volatility thresholds;
* add dozens of cross-asset relationships;
* modify the production engine.

This is structural discovery only.

---

## 19. Success Definition

The campaign is informative if it can answer:
> **Does a volatility shock in one market provide incremental information about the future movement distribution of another market beyond that target market's own current volatility state?**

Possible outcomes:
### Positive
A persistent cross-asset volatility transmission mechanism exists.

### Negative
The existing cross-asset data does not reveal a robust incremental volatility transmission effect.

Either outcome is valuable.

---

## Final Principle

Do not ask:
> "Does Gold predict EURUSD?"

Ask:
> **"Does a measurable volatility shock in one market change another market's future distribution in a way that the target market's own information cannot explain?"**

That is the structural question RC014 should test.
