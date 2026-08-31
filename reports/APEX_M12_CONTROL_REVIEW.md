# APEX M12 Control Review

## 1. Objective
To adjudicate the M12 `BLOCKED — DATA / OBSERVABILITY` status, audit the methodology for logical coherence and lookahead, and determine if M13 (Economic Experiment) can be authorized.

## 2. Macro-Event Exclusion Adjudication
- **Finding**: The methodology requires excluding macro events (NFP, FOMC), but local timestamps are unavailable. 
- **Assessment**: Major US macro releases (NFP, CPI, FOMC) systematically occur during the `LONDON_NY_OVERLAP` window (typically 12:30 or 18:00 UTC). If these are not excluded, the exposure cohort will be heavily contaminated by exogenous macro shocks rather than pure endogenous session-transition liquidity. Comparing this to the off-peak control cohort would materially compromise interpretation—any observed difference in persistence/decay could simply be "macro shocks decay differently than off-peak random shocks." 
- **Decision**: Resolution C. Macro confounding materially compromises interpretation. A methodology revision or external data acquisition is required.

## 3. DST Alignment Review
- **Finding**: Session boundaries are implemented using fixed UTC hours, meaning they drift by 1 hour relative to local market time during non-aligned DST periods (a few weeks in March and October/November).
- **Assessment**: The core institutional transition mechanism is driven by local time (London/NY open). Fixed UTC proxies will slightly blur the exposure classification boundaries during these mismatched weeks, introducing noise. However, over a 5.5-year sample, this only affects a small subset of the data. 
- **Decision**: `DST SAFE WITH DOCUMENTED LIMITATION`. The noise is acceptable, provided it is formally acknowledged.

## 4. Exposure Definition Audit
- **Definition**: "HIGH_VOL episode whose onset bar occurs entirely inside the specified session-transition condition."
- **Assessment**: The implementation checked if `t` (onset bar) was inside the transition window. This perfectly partitions the eligible population cleanly into exposure and control. The 12-bar separation applies globally before classification.
- **Decision**: The definition is methodologically sound and internally coherent.

## 5. HIGH_VOL Threshold Audit (Lookahead Risk)
- **Finding**: M12 reported the 80th-percentile threshold was dynamically calculated as `0.000563` across the *full* 5.5-year sample (136k rows). 
- **Assessment**: This is a severe lookahead violation. Calculating a global percentile uses future information (`t+1` to end of sample) to classify an event at bar `t`. The RC012 methodology intended for thresholds to be defined ex-ante (e.g., via a trailing multi-month rolling window or a frozen pre-sample training period).
- **Decision**: **METHODOLOGY ISSUE**. The M11 methodology must be revised to explicitly define a lookahead-free rolling or historical reference period for the RV20 80th percentile.

## 6. 2-Bar Falsification Rule Audit
- **Finding**: M11 froze a falsification rule requiring `p < 0.05` AND a median persistence difference `≥ 2 bars`.
- **Assessment**: There is no defensible ex-ante rationale in the repository documentation establishing why 2 bars (30 minutes) is the exact threshold for economic meaning. This is an arbitrary researcher degree of freedom injected without domain justification.
- **Decision**: `METHODOLOGY DESIGN QUESTION — REQUIRES CONTROL REVIEW`. The methodology must be revised to either mathematically justify the 2-bar threshold or replace it with a structurally defined boundary.

## 7. Conclusion
M13 cannot be authorized. The M11 methodology contains a material lookahead flaw (global RV20 threshold), an arbitrary falsification rule (2-bar threshold), and a fatal data blocker (systematic macro confounding during the NY overlap). A substantive methodological redesign is required.
