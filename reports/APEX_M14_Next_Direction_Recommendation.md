# APEX M14: Next Research Direction Recommendation

## Primary Research Direction
**Conditional Predictability of HIGH_VOL Persistence**

### Objective
Determine whether the duration of a `HIGH_VOL` episode is conditionally predictable from market-state information available strictly before or exactly at the episode's onset bar. 

### Rationale
M13 proved that `HIGH_VOL` possesses structural memory, meaning it does not decay randomly. The empirical distribution exhibits heterogeneity (a mixture of very short bursts and massive, persistent runs). If this heterogeneity is not entirely random, it may be forecastable. Identifying which episodes will be short-lived versus which will be highly persistent transforms a descriptive structural finding into a powerful predictive primitive.

### Requirements for the Next Methodology
- **Target**: Persistence duration (or binary classification of long vs short episodes).
- **Information Boundary**: Predictors MUST be strictly calculated using data available at $t \le t_{onset}$.
- **Null Hypothesis**: The predictors provide no information regarding the subsequent duration beyond the unconditional baseline distribution.
- **Feasibility**: Can be executed on the existing 794-episode EURUSD M15 ledger.

---

## Backup Research Direction
**Empirical Hazard-Function Decomposition**

### Objective
Determine the shape of the empirical hazard function of the `HIGH_VOL` state to formally decompose its lifecycle into distinct phases (e.g., initial lock-in momentum, steady state, and accelerating decay).

### Rationale
If conditional predictability fails or proves too complex, the next highest-value scientific step is to purely describe the internal mechanics of the memory proved in M13. By mapping the hazard rate, APEX can determine exactly *when* an episode is most likely to die, providing foundational logic for any future trade-exit heuristics.
