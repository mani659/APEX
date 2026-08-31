Milestone: M11-R2
Status: COMPLETE

Original M11 methodology rejected due to lookahead (global threshold), macro-confounding, and arbitrary parameters. 

Revised Scientific Question: Does HIGH_VOL triggered by the ASIA_TO_LONDON transition (endogenous liquidity) persist differently than off-peak HIGH_VOL?

Revised HIGH_VOL Methodology: Option C. Rolling 252-day trailing historical reference for the 80th percentile threshold. Eliminates lookahead.

Session/DST Treatment: Fixed UTC proxy. Explicitly documented as an acceptable limitation.

Macro-Event Treatment: Bypassed. By selecting ASIA_TO_LONDON as the primary exposure, we avoid the US macro-shock overlap (NFP/CPI) completely. No external data needed.

Primary Endpoint: Persistence (number of contiguous M15 bars).
Control Design: Episodes with onset during structurally quiet off-peak hours (20:00-06:00 UTC).

Dependence/Overlap Treatment: Regime Reset Rule. A new episode cannot trigger until the previous one fully mean-reverts below the trailing 50th percentile. Replaces arbitrary 12-bar limit.

Falsification Framework: Log-rank p < 0.05 AND 95% Confidence Interval for median duration difference excludes zero. Arbitrary 2-bar threshold removed.

Unresolved Items: None.
M12R2 Prerequisites: Verify the 252-day rolling computation and confirm sample sizes under the new Regime Reset separation rule.

Freeze Status: FROZEN. (M11R2_FROZEN_METHODOLOGY.md generated).

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M11R2_Methodology_Reconstruction.md (NEW)
- reports/APEX_M11R2_Research_Degrees_of_Freedom.csv (NEW)
- reports/APEX_M11R2_Methodology_Risk_Register.csv (NEW)
- reports/APEX_M11R2_RESULT.md (NEW)
- docs/APEX_M11R2_FROZEN_METHODOLOGY.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
