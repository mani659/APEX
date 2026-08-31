# RC015 Study 008 — Methodology Gate

## 1. Candidate Designs and Structural Rationale

Four strictly defined observation schedules were evaluated:
- **Design A (14:00 UTC)**: Captures the peak of the overlapping European and North American trading sessions.
- **Design B (08:00 & 14:00 UTC)**: Captures the two major institutional entry points (London open and London/NY overlap).
- **Design C (12:00 to 16:00 UTC)**: Covers the entire `LONDON_NY_OVERLAP` session established in RC013.
- **Design D (06:00, 08:00, 12:00, 16:00 UTC)**: Captures exact boundaries of RC013's defined session transitions.

These candidates were defined completely independent of option liquidity empiricals or historical variance outcomes.

## 2. Predeclared Liquidity Gate

To ensure a statistically sound analysis that protects against spurious variance gaps (i.e., artificial gaps caused by matching highly stale options with fresh futures), the following liquidity gate was established *ex ante*:
1. **Minimum Quality Standard**: An observation slot is considered "synchronized" only if the option quote is $\le 15$ minutes old at the predetermined evaluation timestamp.
2. **Event Coverage standard**: At least 80% of the 222 frozen events must retain $\ge 1$ synchronized valid observation slot.
3. **Missing Data Maximum**: No more than 20% of events may be dropped entirely due to total quote sparsity.

## 3. Anti-Selection-Bias Audit

| Criterion | Evaluation |
| :--- | :--- |
| **1. Defined without looking at IV/RV?** | **PASS**. Evaluated strictly on timestamp and age. |
| **2. Based on exchange/market structure?** | **PASS**. Directly anchored to RC013 transitions and known overlap liquidity. |
| **3. Identical across historical events?** | **PASS**. Fixed UTC times applied deterministically to all 222 events. |
| **4. Frozen before economic calculations?** | **PASS**. No IV inversion or RV measurements have occurred yet. |
| **5. Avoids data-mined timestamp selection?**| **PASS**. Schedules reflect mechanics, not backtested highest coverage points. |

## 4. Holiday Policy Options

An explicit rule was formalized for handling early-close or full-closure holidays:
- **Rule**: If a predetermined fixed-anchor timestamp falls *after* the exchange has halted trading for a holiday, the slot is marked as `MISSING` rather than pulling deeply stale quotes forward indefinitely. If an event has no valid slots remaining after holiday exclusions, it is dropped from the sample set (provided the total dropped stays below the 20% maximum).

## 5. Final Design-Space Classification

**`DESIGN SPACE INSUFFICIENT`**

Even when narrowing the study's observation window to the most intensely liquid period of the global FX trading day (the London/NY overlap), the underlying CME EUR/USD listed options market simply does not produce enough consistent quotes to satisfy the minimum liquidity gate. With the best candidate achieving only ~10% chronological slot coverage at a 15-minute tolerance, the study would be starved of data and forced to use unacceptably stale options to calculate IV. 

Because no structurally justified schedule can achieve the required data density, it is impossible to salvage the listed-option framework without resorting to severe ex-post data-mining or compromising the contemporaneous synchronicity required to measure genuine variance gaps.
