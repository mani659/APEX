Milestone: M12 Control Review
Status: COMPLETE

M12 Blocker Adjudication: Resolution C (Pause and require methodology revision). Macro confounding systematically taints the exposure window (NY Open) and materially compromises interpretation.
DST Decision: DST SAFE WITH DOCUMENTED LIMITATION. The noise from fixed UTC boundaries during mismatched daylight-saving weeks is acceptable over a 5.5-year sample.
Macro-Event Decision: BLOCKED. NFP/CPI systematically occur during LONDON_NY_OVERLAP. Exclusion is a mandatory scientific condition, not a minor limitation.

HIGH_VOL Threshold Audit: METHODOLOGY ISSUE (Lookahead). M12 dynamically computing the 80th percentile over the entire dataset leaks future volatility information to historical event classification. A rolling or trailing reference period is required.
2-Bar Falsification Rule Audit: METHODOLOGY DESIGN QUESTION — REQUIRES CONTROL REVIEW. The 2-bar threshold is an arbitrary researcher degree of freedom with no prior justification.

Final Control-Session Decision: M13 BLOCKED — METHODOLOGY REVISION REQUIRED.
M13 Authorized: NO.
Required Methodology Amendment: None attached. A full methodology revision milestone is required instead of a quiet patch.

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M12_CONTROL_REVIEW.md (NEW)
- reports/APEX_M12_CONTROL_REVIEW_DECISION.md (NEW)
- reports/APEX_M12_CONTROL_REVIEW_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
