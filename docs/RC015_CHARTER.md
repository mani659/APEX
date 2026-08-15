# RC015 Study 000 — Options / Implied Volatility Data Qualification Charter

## Campaign
**RC015 — Options / Implied Volatility Research**

## Status
**PLANNED**

---

## 1. Strategic Objective
Apex has reached a project-level conclusion that the remaining high-value research frontier is the relationship between:
* validated volatility information; and
* the market price of volatility itself.

RC012 demonstrated that `HIGH_VOL` reliably predicts increased future movement magnitude (direction-neutral), but spot monetization architectures cannot safely capture the movement.
RC013 demonstrated that deterministic session transitions create persistent distributional expansion (direction-neutral), but the raw breakout monetization architecture failed.

The strategic question is now:
> **Does the market's options-implied volatility adequately price the future volatility/distributional expansion that Apex can predict?**

This is a research qualification campaign. It is NOT an options trading strategy.

---

## 2. Primary Research Question
> **Can the validated RC012 HIGH_VOL and/or RC013 session-transition information explain future realized volatility in excess of the volatility already priced into options?**

The relevant comparison is:
```
Predicted / realized future volatility
        versus
Implied volatility / option premium
        versus
All trading and carry costs
```
Do NOT begin by assuming a straddle is profitable.

---

## 3. Critical Instrument Definition
The initial research target should be:
### EURUSD options

Reason:
* RC012 was discovered on EURUSD;
* RC013 was validated on EURUSD;
* the historical spot dataset already exists;
* this preserves continuity with the validated primitives.

Do NOT immediately expand to equities, indices, commodities, or crypto options. A second asset class may only be considered after EURUSD option research is proven feasible.

---

## 4. Required RC012 / RC013 Mapping
Determine exactly how the validated spot primitives could map onto option-volatility observations.

### RC012 HIGH_VOL
Question: When HIGH_VOL is present, is future realized volatility systematically above the implied volatility that existed before the event?

### RC013 Session Transition
Question: Before major session transitions, does implied volatility systematically understate or overstate the realized movement that follows?

Do NOT assume the answer is positive.

---

## 5. Economic Question
The first economic question is NOT "Would a straddle make money?" 
It is:
> **"Does a validated Apex condition predict that realized volatility will differ materially from the implied volatility already priced into options?"**

Only if the answer is positive should option-payoff monetization be considered.

---

## 6. Important Risk Boundary
Explicitly distinguish:
* **Long Options**: Maximum loss can be bounded by premium paid.
* **Short Options**: Loss may be very large or theoretically unbounded depending on structure.

Study 000 must not assume that "options = bounded risk." No short-vol strategy may be proposed as automatically safe.

---

## 7. Governance
Do NOT:
* create an options strategy;
* backtest straddles;
* optimize strikes;
* optimize expiries;
* optimize delta;
* optimize premium thresholds;
* introduce ML;
* acquire data automatically;
* modify RC012;
* modify RC013;
* modify the production engine.

This is data qualification and research scoping only.

---

## Final Principle
Apex has already demonstrated that:
> **Predicting movement is not enough.**

The next question is:
> **Can Apex predict when the market will realize more or less volatility than the market itself is pricing?**

That is the core research question behind the options pivot.
