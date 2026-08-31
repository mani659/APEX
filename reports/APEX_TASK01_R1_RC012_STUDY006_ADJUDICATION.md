# APEX TASK 01-R1 — RC012 Study-006 Economic Contradiction Adjudication

**Session**: APEX Local Repository Execution Agent — TASK 01-R1 (bounded evidence adjudication)
**Date**: 2026-08-30
**Mode**: Repository-only. No experiment, no re-run of Study-006, no backtest, no PnL recalculation, no assumption change, no cost re-test, no deployability test, no strategy search, no data acquisition, no API call, no code or methodology modification, no RC012 reopen, no rescue, no new module declaration.

---

## 1. Question

> **Does RC012 Study-006 contain a surviving, independently accessible economic mechanism that changes APEX's current M3/M4/M5 = 0 and PAUSED state?**

---

## 2. Evidence Inspected

- `reports/RC012_Study_006_Volatility_Monetization.md` (headline report)
- `reports/RC012_Study_006_results.json` (stored validated results)
- `reports/RC012_Study_006_Volatility_Monetization_Dataset.parquet` (present; source of stored results)
- `scripts/rc012_study_006.py` (exact construction: RV20 percentile states, forward movement, net-edge formula)
- `reports/RC012_Study_007_Volatility_Trading_Architecture.md` (directional hold)
- `reports/RC012_Study_008_Volatility_OCO_Analysis.md` (symmetric OCO)
- `reports/RC012_Study_009_HIGH_VOL_Path_Analysis.md` (path length vs path efficiency)
- `reports/RC012_Study_010_Two_Sided_Path_Analysis.md` (OCO path truncation diagnostic)
- `reports/RC012_Study_011_Bounded_Inventory_Analysis.md` (bounded 2-unit inventory)
- `reports/RC012_Study_012_HIGH_VOL_Monetization_Review.md` (authoritative RC012 monetization review / FREEZE)
- `reports/APEX_M34_HIGH_VOL_Final_Closure.md` (authoritative branch closure)
- `reports/APEX_M45_Research_Cycle_Closure.md`, `reports/APEX_M45_Evidence_Ledger.csv` (authoritative evidence ledger)
- `reports/APEX_AR1_Module_Qualification_Framework.md` (M3/M4/M5 formal definitions)
- `research/SMC_RESEARCH/architecture/SMC_R10_Economic_Qualification_Framework.md` (E[R_net]>0 minimum economic gate)

---

## 3. Study-006 Economic Construction (reconstructed from script + results)

1. **Economic object**: A *stylized synthetic straddle (movement-magnitude / convexity) statistic* on EURUSD M15. It was NOT a real tradeable position, an option, or a futures straddle.
2. **Instrument**: EURUSD M15 OHLCV, 5.5-year sample, out-of-sample validation only `2024-07-01`–`2026-06-30`. No option/futures/options-chain used.
3. **What generated the positive value**: The script computes `net_edge = excess_movement − friction`, where `excess_movement = |realized forward move| − baseline_movement` and `baseline_movement` = the **unconditional mean |forward move| from the Discovery period** (used as a stylized "straddle premium" proxy). So the reported "net edge" is a **mathematical movement-magnitude statistic**, not realized PnL from any position. There is no entry/exit, no direction, no spread/slippage beyond the fixed pip, and no option premium actually paid/collected.
4. **Payoff independently accessible?** **NO.** No executable market position corresponds to `gross_movement − baseline − friction`. Harvesting absolute movement requires an *options-style convexity* instrument, which does not exist in APEX's retail spot evidence and which the later studies (and M34, Study-012) explicitly located outside spot forex.
5. **Real executable market position?** **NO.** Synthetic/stylized only.
6. **Was the 1.0 pip friction empirically justified?** **NO.** It is a **fixed assumption** (with 0.5 and 2.0 pip sensitivities only). At 2.0 pips the headline HIGH_VOL 1h result **breakeven** (mean_net_2.0 ≈ −0.02 pip). No spread/slippage/margin/market-impact model was used. This is not the frozen realistic-cost architecture ultimately required (R10/M15/M36).
7. **Synthetic?** **YES** — explicitly a synthetic directional-neutral representation ("equivalent to a straddle").
8. **Intended as deployable strategy?** **NO.** Study-006 itself states: "This is a monetization proof of concept, not a validated deployable trading strategy. A formal execution architecture would be required for the next phase."

### Critical internal detail from the stored results (not the headline)
The report's headline "+0.98 pips net (mean at 1.0 pip)" is a **mean** that is lifted by the fat upper tail:
- HIGH_VOL, 1h: `mean_net_1.0` = +9.84e-05 (≈ +0.98 pip), but **`median_net_1.0` = −0.000172 (≈ −1.72 pips, negative)** and **`prob_pos_net_1.0` = 0.393** (only ≈39% of observations are net-positive).
- HIGH_VOL, 4h: `mean_net_1.0` = +3.4e-05 (+0.34 pip); median = −5.09 pips (negative); prob_pos = 0.359.
- HIGH_VOL, 16h: `mean_net_1.0` = **−2.35 pips (negative)**. The report's Horizon C "+3.55 pips" was attributed to the **LOW_VOL** state (N=159, median −3.89 pips negative, prob_pos 0.428), not HIGH_VOL.
- Temporal halves (stored `EARLY`/`LATE`): HIGH_VOL 1h `EARLY mean_net_1.0` = +1.87 pip but **`LATE mean_net_1.0` = −0.000039 (≈ −0.39 pip, NEGATIVE)**. The report's §5 claim ("remained economically positive throughout both halves" / late +0.65) is **not supported by the stored results**, which show a negative late-half mean.

These stored figures show the "positive net expectancy" was **not stable across the validation halves and not robust at the median or majority-of-observation level** — additional reasons it cannot satisfy M4's "effect stable across the validation period" and "positive expected value ... with realistic costs" criteria.

---

## 4. Positive-Result Claim (exact)

- Study-006 report header conclusion: **"CANDIDATE ECONOMIC EDGE"** and "the structural, non-directional expectancy ... yields positive net expectancy after ... conservative execution friction (1.0 pips)" and "this is a monetization proof of concept, not a validated deployable trading strategy."
- Authoritative RC012 Study-012 frames Study-006's result as **"CANDIDATE ECONOMIC INFORMATION"** — "measurable absolute movement-value uplift that overcomes **naive** friction assumptions (Study 006)" — i.e., **mathematical convexity potential**, not an accessible, validated, deployable payoff. Study-012 classifies this under the distinction Scientific Value: ACHIEVED / Economic Value: ACHIEVED (as movement-value potential) / **Trading Value: FAILED** (Studies 007–011).

---

## 5. Cost Assumption

- Fixed 1.0 pip round-trip friction (primary); 0.5 and 2.0 pip sensitivities. Not empirically derived; no spread slippage/margin/impact model; not the frozen realistic-cost methodology. **Fails M3/M4 cost-realism test.**

---

## 6. Accessibility / Deployability Assessment

- **Not accessible**: The only way to harvest HIGH_VOL's absolute path length is an options/convexity instrument ("Options pricing arbitrage is the mathematically correct way to harvest this"; Study-012 §6, §9; Study-009 §6). APEX has no such accessible spot vehicle; the options routes were independently closed (CME listed options RC015 liquidity-infeasible; BTC options long straddle IC7 REJECTED; alternatives IC8 REJECTED).
- **Not deployable**: Study-006 self-disclaims deployability; Studies 007–011 then demonstrated every tested risk-constrained spot architecture fails to capture the movement (see §7).

---

## 7. Later RC012 Evidence (Studies 007–011) — What Survived

- **Study-007 (directional hold)**: Combined direction-neutral expectancy rigidly = **−1.0 pip** (structural); both directions negative; REJECTED. Explicitly framed as the separation between "Economic Edge (Study 006)" and "Trading Edge (Study 007)."
- **Study-008 (symmetric OCO)**: Trigger ~93–96%, but TP hit ≈41% ≈ SL hit; expectancy **−0.8 to −1.1 pips**; whipsaw-destroyed; REJECTED.
- **Study-009 (path diagnostic — DECISIVE)**: HIGH_VOL produces **Path Length** (72.1 pips) but **Path Efficiency ~12%**, identical to unconditional baseline. Study-006 "succeeded" **only** because it directly harvested raw absolute path length as a stylized statistic — not because any accessible position-equivalent exists.
- **Study-010 (path-truncation diagnostic)**: OCO exits capture only **21%** of available path (14.7 of 69.3 pips); premature exit abandons ~55 pips; gross +0.12 pip, heavily negative net; REJECTED.
- **Study-011 (bounded 2-unit inventory)**: Expectancy worsened (−1.13 → **−1.46 pips**), drawdown and tail-risk increased (worst-1% 7.7%→9.4%); REJECTED.

**What survived**: The *scientific* finding that HIGH_VOL raises absolute movement magnitude (Studies 004/005) — an M1/M2 validated primitive. **What did NOT survive**: any accessible positive independent payoff. Study-012's monetization-logic audit concluded the spot-architecture space for harvesting chop is structurally barred by the risk constraints (no unlimited inventory, no recovery sizing, finite max loss), and Study-012 made the control decision to **FREEZE HIGH_VOL AS NON-MONETIZABLE INFORMATION** in spot (Option B). M34 closed the HIGH_VOL branch: "Economic implementation unresolved"; "**positive expectancy**" and "**profitability of any HIGH_VOL-based strategy**" listed under **What Remains Unproven**.

---

## 8. M3 Assessment (formal, per AR1)

AR1 M3 (Economic Candidate): "A concrete payoff mechanism exists and can be frozen ex ante. Evidence: Frozen methodology; instrument identified; economic hypothesis stated; falsification criteria defined." APEX's own M3 example is "Long ATM straddle (IC5) — reached M3 but failed at M4."

| Criterion | PASS/FAIL | Evidence |
|---|---|---|
| Independent economic object | **FAIL** | Only a synthetic movement-magnitude statistic; no executable object; Study-012 labels it "CANDIDATE ECONOMIC INFORMATION," not an independent module. |
| Identifiable compensation/mechanism | **PARTIAL / FAIL as M3-module** | Mechanism = convexity harvesting of absolute movement; but the required vehicle (options) is outside spot and independently closed (RC015, IC7, IC8). No accessible compensated mechanism in APEX's evidence. |
| Realistically accessible payoff | **FAIL** | No spot position captures it; Studies 007–011 show spot architectures fail; options route closed. |
| Realistic transaction costs | **FAIL** | Fixed 1.0 pip assumption only; sensitivity to 2.0 pip → breakeven/negative; not frozen realistic-cost method; no spread/slippage/margin/impact. |
| No lookahead | **PASS** | Premium baseline frozen from Discovery period; forward-move metric is realized, not leaked; validation is OOS. |
| Falsifiable | **PASS** | A falsifiable claim was articulated. |
| Survives later research | **FAIL** | Studies 007–011 and Study-012 (FREEZE) and M34 (CLOSE, "economic implementation unresolved") did not preserve an accessible payoff. |

**M3 verdict: FAIL (as a surviving candidate).** Even granting that Study-006 articulated something falsifiable (which is more than study-alone statistics), it does **not** constitute a surviving economic *candidate* because the payoff is synthetic, cost-unrealistic, not restrained-accessible, and its underlying convexity mechanism lacks an accessible, non-closed instrument. Statistical movement-magnitude is not economic profitability (AR1 principle; M34 "What Remains Unproven").

---

## 9. M4 Assessment (formal, per AR1)

AR1 M4 (Validated Economic Module): "positive expectancy under strict OOS validation with realistic costs." Checklist requires: standalone positive expectancy; skeleton **costs included**; OOS chronological validation; **effect stable across the validation period**; no post-hoc parameterization; economically independent. AR1 M4 examples: **None currently.**

| Is it a reproducible economic module? | **NO** — synthetic statistic; no executable payoff; not a self-contained module. |
|---|---|
| Payoff independently accessible? | **NO** — no accessible instrument; options route closed. |
| Deployable under realistic conditions? | **NO** — self-disclaimed; Studies 007–011 reject all tested spot architectures. |
| Positive expectancy robust to required cost realism? | **NO** — fixed 1.0-pip assumption; 2.0-pip → breakeven; median negative; late-half mean negative. |
| Later RC012 preserved or rejected mechanism? | **REJECTED/not preserved** as accessible payoff (Study-012 FREEZE in spot; M34 CLOSE). |
| Explicit non-deployable/proof-of-concept statement? | **YES** — Study-006 §7 note: "monetization proof of concept, not a validated deployable trading strategy." |

**M4 verdict: FAIL.** Study-006 does not qualify as M4. Every required condition fails or is unestablished.

---

## 10. M5 Assessment

**FAIL.** M5 (Production Candidate) is strictly downstream of a validated M4 module. With M4 = 0 and Study-006 non-qualifying, there is no M5 candidate. No forward/demo execution validation exists for Study-006; it was never executable.

---

## 11. Exact Surviving Scientific / Economic Claim

> "Study-006 does not qualify as an APEX economic module because its positive result was produced under a **non-deployable synthetic proof-of-concept architecture** (a stylized movement-magnitude straddle statistic with a fixed, non-empirical 1.0-pip friction) and was **not preserved as a validated, accessible payoff mechanism** — later spot-architecture tests (Studies 007–011) rejected every tested implementation, Study-012 froze HIGH_VOL as non-monetizable in spot, and M34/M45 closed the branch with 'economic implementation unresolved.'"

The **only** surviving *scientific* claim (unchanged, preserved) is: HIGH_VOL is a validated M1/M2 *distributional* primitive — it raises absolute forward movement magnitude (path length) with an unchanged low path efficiency (~12%) and no directional or accessible-payoff translation. That is a scientific fact, not an economic module.

---

## 12. Exact Claim That Must NOT Be Made

Do **NOT** assert: "Study-006 proves synthetic-straddle trading (or volatility convexity harvesting) is impossible."

The repository does **not** establish that in general. Study-012/M34 only establish the narrower claim:
- No **spot** architecture tested could access the payoff under the declared risk constraints (finite max loss, no unlimited inventory, no recovery sizing).
- Options pricing arbitrage is identified as the *mathematically correct* vehicle for harvesting convexity, but that route is separately closed in APEX's evidence (RC015 CME listed-options liquidity-infeasible; IC7 BTC long straddle p=0.953 failed; IC8 alternatives rejected).
- Whether some future, genuinely new instrument/mechanism could access this is **UNKNOWN / not established** — and would be a restart-gate avenue (M45 restart conditions A/D/E), not the Study-006 result itself.

So the correct claim is the one in §11 (narrow, evidence-supported), NOT a blanket "volatility trading is impossible."

---

## 13. Restart Impact

| Item | Changed? | Reason |
|---|---|---|
| M3 count | **NO** | Study-006 does not qualify as a surviving M3 candidate (synthetic, cost-unrealistic, inaccessible, not preserved). |
| M4 count | **NO** | Fails every M4 condition (AR1); explicitly non-deployable proof-of-concept. |
| M5 count | **NO** | No M4 base; downstream of M4. |
| Closed-path inventory | **NO** | RC012 spot monetization (C01) and HIGH_VOL branches (C02–C04) remain closed per M45/M34/Study-012. |
| Restart eligibility | **NO** | No new accessible economic object or independent payoff is established. |
| Need for a new economic mechanism | **NO** | Still required. |

**Explicit statement**: *Study-006 is an evidence-classification clarification and does not change the APEX restart state.*

---

## 14. Evidence Citations / Paths

- `reports/RC012_Study_006_Volatility_Monetization.md` (§3 tables; §5 "remained positive both halves"; §6 "CANDIDATE ECONOMIC EDGE"; §7 "proof of concept, not a validated deployable trading strategy")
- `reports/RC012_Study_006_results.json` (stored VALIDATION_INFERENTIAL/EARLY/LATE metrics; median negative; prob_pos ~0.39; LATE mean negative)
- `scripts/rc012_study_006.py` (net_edge = excess_movement − friction; synthetic straddle premium = discovery baseline mean |move|)
- `reports/RC012_Study_007_Volatility_Trading_Architecture.md` (direction-neutral expectancy = −1.0 pip; Economic Edge vs Trading Edge)
- `reports/RC012_Study_008_Volatility_OCO_Analysis.md` (OCO REJECTED; whipsaw)
- `reports/RC012_Study_009_HIGH_VOL_Path_Analysis.md` (path length 72.1 vs path efficiency 12% identical)
- `reports/RC012_Study_010_Two_Sided_Path_Analysis.md` (OCO truncates ~80%; REJECTED)
- `reports/RC012_Study_011_Bounded_Inventory_Analysis.md` (expectancy −1.46; tail risk up; REJECTED)
- `reports/RC012_Study_012_HIGH_VOL_Monetization_Review.md` (CANDIDATE ECONOMIC INFORMATION; "naive friction assumptions"; options = correct vehicle; FREEZE HIGH_VOL as non-monetizable in spot)
- `reports/APEX_M34_HIGH_VOL_Final_Closure.md` (branch CLOSED; "positive expectancy" & "profitability" = What Remains Unproven; spot monetization failure 007–011)
- `reports/APEX_M45_Research_Cycle_Closure.md`, `reports/APEX_M45_Evidence_Ledger.csv` (RC012 spot monetization = FAILED HYPOTHESIS / Monetization failed; M4=0)
- `reports/APEX_AR1_Module_Qualification_Framework.md` (M3/M4/M5 definitions; M4 examples None)
- `research/SMC_RESEARCH/architecture/SMC_R10_Economic_Qualification_Framework.md` (E[R_net]>0; realistic costs)

---

## 15. Conclusion

**NO.** RC012 Study-006 does **not** contain a surviving, independently accessible economic mechanism. It is a *non-deployable synthetic proof-of-concept* (movement-magnitude statistic with a fixed, non-empirical 1.0-pip friction); its mean-positive result is not stable (negative median, only ~39% net-positive observations, negative late-half mean), and its underlying convexity-payoff vehicle (options) is outside spot and independently closed in APEX's evidence. Later RC012 work (007–011) rejected every tested spot architecture; Study-012 froze HIGH_VOL as non-monetizable in spot; M34 closed the branch ("economic implementation unresolved"); M45 records RC012 spot monetization as FAILED HYPOTHESIS.

**APEX state unchanged: M3 = 0, M4 = 0, M5 = 0, PAUSED.** Study-006 is an evidence-classification clarification only and does not change the APEX restart state. No M51, no strategy, no new economic mechanism is authorized by this finding.

*Final control answer: **NO.***
