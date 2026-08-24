Milestone: M34
Status: COMPLETE

Branch: HIGH_VOL Lifecycle / Predictability / Translation

Final branch status: CLOSED — SCIENTIFICALLY INFORMATIVE, ECONOMIC IMPLEMENTATION UNRESOLVED

Validated findings:
1. HIGH_VOL is a structural distributional primitive (RC012)
2. HIGH_VOL persistence is non-memoryless with structured lifecycle (M13/M14: D=0.1927, p<0.0001, n=794)
3. Onset Intensity + Momentum predict future persistence (M17-R2: C-index=0.6656, baseline=0.5000, ΔC=+0.1656)
4. Predicted persistence scales forward RV magnitude (M21: β=-0.014288, p=0.0032)
5. Predicted persistence does NOT predict directional drift (M24: β=-0.000367, p=0.6418)
6. Predicted persistence scales the outer spatial envelope of price excursion (M27: β=-0.001153, p=7.5×10⁻⁵)
7. The expansion is near-symmetric (M27 secondary: upside/downside ratio=0.9218)

Negative findings:
- Session-transition branch infeasible (n=8 after independence rules)
- No linear directional translation detected (M24: p=0.6418)
- Static 1.0×RV20_onset boundary saturated (M31: 395/396=99.75% breach, p=0.2375)
- Spot monetization failed all architectures (RC012 Studies 007–011)

M31 saturation interpretation: The continuous relationship (M27) is real; the arbitrary static threshold (M31) is not. Continuous associations do not automatically translate into useful binary economic thresholds.

Dynamic-translation decision: REJECTED — classified as METHODOLOGICALLY WEAK (M33 score=28/50). Introduces arbitrary constants, depends on calibration to M27 outcomes (circularity), adds little scientific novelty, risks hidden parameter search.

Why branch closed: The HIGH_VOL branch produced substantial validated scientific information. The remaining path from continuous excursion prediction to economically actionable implementation requires additional parameterization that cannot currently be specified with sufficient ex-ante defensibility. The branch is closed for now, not because the phenomenon failed, but because the next economic research layer is not currently sufficiently defensible.

What remains unproven: Profitability, positive expectancy, trading strategy, execution edge, capital efficiency, optimal grid/barrier parameterization, transaction-cost robustness, causal mechanism, cross-instrument generalization.

Reusable knowledge:
- HIGH_VOL_STATE validated market-state primitive
- Canonical HIGH_VOL episode ledger (794 episodes, EURUSD M15)
- M17-R2 walk-forward Cox PH prediction methodology
- M21/M24/M27 frozen translation results

Methodological lessons:
1. Do not relax event definitions to inflate sample size
2. Methodology must be repaired before economic testing
3. Statistical calibration must match data structure
4. Feature count is not scientific value
5. Continuous relationships do not automatically translate into binary thresholds
6. APEX stopping principle: continue only when next question is materially different

Next authorized research direction: M35 — APEX Next-Research Direction Discovery
Authorization status: PLANNED — NOT STARTED

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M34_HIGH_VOL_Final_Closure.md (NEW)
- reports/APEX_M34_FINAL_RESULT.md (NEW)
- docs/APEX_HIGH_VOL_BRANCH_CLOSURE.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
