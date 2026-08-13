# RC008 Study 001: Conditional Context Exploration

## Objective
To determine whether the negative standalone Apex entry contains conditional predictive information across different market environments (Volatility, Trend, Liquidity, Path, Temporal) before the execution decision.

## Methodology
The 410 valid, isolated EURUSD behavioral events from RC007 were enriched with contemporaneous market context calculated from the pre-event bar. Events were classified as Favorable (PnL > 0) or Unfavorable (PnL <= 0) based on the isolated 240-bar baseline. 

The contextual variables were compared between Favorable and Unfavorable outcomes using Cohen's d effect size, and conditional expectancies were calculated across quartiles.

## Findings Summary

The analysis tested 6 broad contextual categories. The results were universally negative. 

### Volatility Context (1-Week ATR Percentile)
- **Effect Size:** 0.12 (No Evidence)
- **Observation:** Whether volatility was historically compressed or extremely expanded, the event win rate remained bound between 33% and 38%, with a persistently negative mean PnL across all quartiles.

### Trend Context (Distance from 24h Mean & 240-bar Return)
- **Effect Size:** 0.03 and -0.14 (No Evidence)
- **Observation:** Trading into a prevailing 24-hour trend or against it made virtually no difference. The mean return was negative across every trend quartile.

### Liquidity Context (240-bar Volume Z-Score)
- **Effect Size:** -0.07 (No Evidence)
- **Observation:** While RC002 established that *low absolute participation* was required to form a valid event, attempting to further condition the event based on relative volume standard deviations yielded no additional information gain. 

### Path Context (60-bar Pre-Event Momentum)
- **Effect Size:** 0.11 (No Evidence)
- **Observation:** The speed/velocity at which the 3.0 ATR displacement occurred did not separate winners from losers. Sudden crashes performed identically to gradual bleed-outs.

### Temporal Context (Hour of Day)
- **Effect Size:** -0.08 (No Evidence)
- **Observation:** No specific time of day significantly improved the expectancy of the signal.

## Winner / Loser Profile
There is no measurable difference between the market environments of Favorable and Unfavorable events. The distributions for winners and losers are virtually identical across all tested dimensions. 

## Scientific Verdict
**No Evidence.** 
The data conclusively demonstrates that the negative alpha of the underlying V1 behavioural event is **unconditional**. 

It is not merely a good signal suffering in the wrong regime; it is a fundamentally zero/negative-information signal. No combination of these standard contextual filters can reliably partition the distribution to extract a durable edge. 

Future research must reconsider the definition of the behavioural event itself, rather than attempting to filter it.
