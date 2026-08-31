# APEX M12R2 Control Review: Exposure Scarcity Adjudication

## 1. Objective
To adjudicate the `BLOCKED — DATA / OBSERVABILITY` status of M12R2, specifically addressing the extreme exposure sample scarcity (n=8) and determining whether the scientific question remains viable.

## 2. Structural Cause of Scarcity
The n=8 result is not a data-integrity failure but a structural reality exposed by rigorous methodology. It stems from the intersection of two strict, scientifically justified rules:
1. **The Regime-Reset Rule**: This rule correctly prevents pseudo-replication by clustering consecutive bursts of variance into a single continuous volatility episode until a full return to the median occurs. This reduces the total historical episode count to 794 over 4.5 years.
2. **The 2-hour Exposure Window**: `ASIA_TO_LONDON` spans only 1/12th of the trading day. Furthermore, massive variance shocks rarely *originate* in this specific transition compared to the macro-heavy NY session.
The scarcity is therefore both **intrinsic** (major shocks rarely begin here) and **design-induced** (the rigorous reset rule correctly prevents artificially inflating the sample).

## 3. Plausibility of More Historical Data
The current frequency is roughly 1.77 exposure events per year (8 events / 4.5 years). To achieve a minimally robust survival-analysis sample (e.g., n=100 or n=200), the study would require between 50 and 115 years of M15 data. **Conclusion**: More historical data will not solve the problem. The exposure is intrinsically too rare under the rigorous definitions.

## 4. Assessment of the Exposure Definition
The `07:00-09:00 UTC` window successfully isolates the endogenous Asia-to-Europe liquidity transition without macro-event contamination. Widening this window (e.g., 06:00-11:00) would alter the scientific construct just to farm a higher `n`. The definition itself is sound; the problem is that the intersection of this transition with a `HIGH_VOL` onset is fundamentally too rare.

## 5. Assessment of the Regime-Reset Rule
The Regime-Reset rule is a massive methodological upgrade over the arbitrary 12-bar separation limit. It enforces true independence between volatility episodes. Reverting to a fixed-bar limit would artificially inflate `n` at the cost of severe pseudo-replication and scientific invalidity. The rule must be preserved.

## 6. Comparison Against the M10 Backup
The M10 backup hypothesis is: **HIGH_VOL persistence / decay without session conditioning**.
- **Preserves RC012**: Yes.
- **Avoids Rare Intersection**: Yes. It utilizes the full population of 794 robust episodes.
- **Scientifically Novel**: Yes. It characterizes the unconditional survival function of endogenous variance expansion.
- **Observability**: Massive (n=794). 
- **Infrastructure Reuse**: 100% reusable. It uses the exact same 252-day trailing threshold and Regime Reset rule verified in M12R2, simply removing the session-exposure filter.

## 7. Conclusion
The specific intersection of `HIGH_VOL ONSET` and `ASIA_TO_LONDON` is a scientifically valid construct but practically uninformative due to extreme sparsity. We must not manipulate the methodology (e.g., reverting to pseudo-replication or widening windows arbitrarily) just to force the experiment to run. The highest-information-value path is to abandon this specific intersection and activate the M10 backup.
