# RC012 Study 003 — Research Methodology V2

## 1. Current Methodology Limitations
The previous Apex research framework was overly dependent on fixed-window directional returns, Cohen's d, win rate, and symmetric outcome comparisons. This approach artificially restricted the definition of an "edge" to short-term directional predictions, creating systematic false negatives for strategies that rely on structural carry, variance/volatility forecasting, and asymmetric risk/reward geometries.

## 2. New Definition of Edge
The framework recognizes three distinct categories of trading edge. A candidate can belong to more than one category if justified.

- **Category A — Directional Edge:** The probability or magnitude of future returns is predictably different from baseline (e.g., positive/negative conditional return, continuation/reversal probability). Directional statistics remain valid but are no longer sufficient by themselves.
- **Category B — Distribution / Volatility Edge:** The conditional distribution of future market outcomes differs materially even when the mean return does not. A setup with approximately zero mean return may still contain useful information if it reliably predicts a different outcome distribution (e.g., volatility forecasting, probability of unusually large movement, expected range, variance expansion/contraction, distribution asymmetry).
- **Category C — Payoff / Risk-Geometry Edge:** A trading opportunity may have poor directional accuracy but possess positive expectancy due to its payoff structure.

Future candidate findings should be classified using the type of information they provide:
- **DIRECTIONAL:** Predicts return direction or magnitude.
- **DISTRIBUTIONAL:** Predicts a change in the outcome distribution.
- **PAYOFF:** Creates favorable expectancy through payoff geometry.
- **RISK REDUCTION:** Does not create positive return by itself but materially reduces adverse exposure.
- **NO EDGE:** No economically meaningful conditional difference.

## 3. Directional Framework
Minimum required metrics for analyzing directional edge:
- Mean return
- Median return
- Directional probability
- Continuation probability
- Reversal probability
- Cohen's d or equivalent effect size

## 4. Distribution Framework
Minimum required metrics for analyzing distribution/volatility edge:
- Standard deviation
- Realized volatility
- Percentile movement
- Maximum Favorable Excursion (MFE)
- Maximum Adverse Excursion (MAE)
- Tail probabilities
- Quantile shift
- Distribution distance (where appropriate)

*Future studies may investigate hypotheses such as volatility expansion/contraction, probability of large moves, conditional range, tail-event probability, or volatility persistence.*

## 5. Payoff / Risk Framework
A standard payoff-distribution analysis is required to evaluate expected value and risk of ruin. No single metric (like win rate) should be treated as definitive.

**Expectancy Formula:**
```text
  Win Probability
× Average Win
- Loss Probability
× Average Loss
= Expectancy
```

**Required Payoff Metrics:**
- Expectancy
- Average win
- Average loss
- Payoff ratio
- Profit factor
- Win rate
- Loss rate
- Skewness
- Maximum loss
- Drawdown
- Tail-loss concentration / contribution
- Maximum Adverse Excursion (MAE)
- Maximum Favorable Excursion (MFE)
- Recovery characteristics

## 6. Conditional Probability Framework
Future research must be able to evaluate conditional statements. This is critical for questions that are naturally probabilistic rather than just asking if a mean return is positive. 

**Required Methodology:**
- Conditional probability
- Unconditional probability
- Probability uplift
- Relative risk
- Absolute probability difference

## 7. Outcome-Window Methodology
Future studies must not assume that one arbitrary fixed horizon (e.g., 240 bars) is sufficient. The experiment must choose the horizon appropriate to its specific hypothesis without blindly generating multiple horizons for every study.

**Research protocols must explicitly declare:**
- Event window
- Observation window
- Outcome horizon
- Termination condition

**Where appropriate, the framework should support:**
- Path-dependent outcomes
- Variable-duration outcomes
- Barrier outcomes
- Time-to-event measurements

## 8. Validation Standard
Before a candidate hypothesis can be promoted, the following criteria must be satisfied:
1. It must be defined without future information.
2. Its measurement methodology must be declared before result inspection.
3. The relevant baseline must be established.
4. Sample size must be adequate.
5. Uncertainty must be measured.
6. Temporal stability must be assessed.
7. Multiple-testing effects must be disclosed.
8. The payoff distribution must be evaluated where applicable.
9. The result must survive an independent validation study.

## 9. ML Governance
Machine Learning is NOT to be introduced as part of this methodology reset. ML must not become a replacement for defining what "edge" means. It may only be utilized later if:
- A valid target variable exists.
- The research question is clearly defined.
- The baseline methodology is established.
- The data contains sufficient information.

## 10. Over-Engineering Rules
The new framework must NOT become a giant metric library. 
- **Rule:** Every future experiment should use only the metrics necessary for its hypothesis.
- **Principle:** Broaden the definition of edge, not the number of features.

## 11. Required Minimum Reporting Standards
For all future research reports, the following reporting components are strictly required:
1. Clearly stated hypothesis and its declared Category (Directional, Distributional, Payoff, Risk Reduction).
2. Defined measurement methodology, timeline, and outcome window selected appropriately for the hypothesis.
3. Selected relevant metrics from the Directional, Distributional, and Payoff frameworks.
4. Payoff-distribution analysis (including expectancy, tail risks, and MFE/MAE analysis).
5. Formal validation standard checks as defined above.

---

# Final Principle

Apex's research question is no longer:
> "Can we predict the next move?"

It becomes:
> **"Can we identify a repeatable market condition that changes the probability distribution or payoff distribution enough to create a durable economic edge?"**
