# APEX Economic Knowledge Map

**Applies to**: APEX Control Session authorized task — TASK 01 (Economic Knowledge & Closed-Path Map)
**Date**: 2026-08-30
**Session type**: Repository-only audit & knowledge mapping. No experiment, backtest, statistical test, data download, external API call, spend, or bot/strategy modification.
**Authoritative state carried forward (unchanged, not challenged here)**: `APEX = PAUSED`; M1/M2 (scientific) preserved; M3 = 0; M4 = 0; M5 = 0; no M51 authorized; restart remains gated on a genuinely new economic object with repository-audited, independently-payoff evidence.

---

## 1. Evidence Classification Legend

This map applies the same four-class scheme already used across the APEX/SMC governance:

| Class | Meaning |
|-------|---------|
| **A — VALIDATED APEX SCIENTIFIC** | Repository-audited, controlled experiments. Scientifically established **but NOT automatically economic**. Includes M1 (scientific) and M2 (predictive) artifacts. |
| **B — OBSERVED / OPERATIONAL** | Observed operational behavior, incl. custom-bot observations (R-Velocity, ATR/ADX/volume/session, stale-cache, portfolio clustering). **Repository-audited: NO** for the Week-6 document. |
| **C — HYPOTHESIS** | Plausible explanation / direction, not established by evidence. |
| **D — ARCHITECTURAL INFERENCE** | Structural design interpretations (signal→risk→allocation, execution-state, trade-path, portfolio-risk overlays), not directly tested. |

Milestone/maturity ladder preserved APEX-wide:
- **M1 (Scientific)** — pattern is deterministic and reproducible.
- **M2 (Predictive)** — pattern contains predictive information.
- **M3 (Economic Candidate)** — `E[R_net] > 0` after realistic frozen costs (minimum economic gate; R10 Level 2).
- **M4 (Validated Economic Module)** — positive net expectancy survives stronger validation (R10 Level 3).
- **M5 (Deployment Candidate)** — suitable for bot inclusion (R10 Level 4).

---

## 2. Validated Scientific Inventory (Evidence Class A — M1/M2)

Scientifically established findings from controlled, frozen-methodology (M15/M36) experiments. **None is an economic module.**

| ID | Name | Class | Milestone | Target / Instrument | Result | Economic test | Economic result | M4 status |
|----|------|-------|-----------|----------------------|--------|----------------|-----------------|-----------|
| V01 | HIGH_VOL distributional primitive | A (M1) | RC012/M34 | EURUSD M15 | Cramér–von Mises D=0.1927, distinct distribution | None | N/A | M4=0 |
| V02 | HIGH_VOL persistence lifecycle | A (M1) | RC012/M34 | EURUSD M15 | Non-memoryless, p<0.0001, n=794 | None | N/A | M4=0 |
| V03 | HIGH_VOL onset predictability | A (M2) | M17-R2 | EURUSD M15 | C-index 0.6656 | None | N/A | M4=0 |
| V04 | HIGH_VOL → forward RV | A (M2) | M17-R2 | EURUSD M15 | p=0.0032 | None | N/A | M4=0 |
| V05 | HIGH_VOL → excursion envelope | A (M2) | M17-R2 | EURUSD M15 | p=7.5e-05 | None | N/A | M4=0 |
| V06 | HIGH_VOL → direction | REJECTED | M17-R2 | EURUSD M15 | p=0.6418 (no directional edge) | Rejected | Negative | M4=0 |
| V07 | Session-transition CDF difference (LNO) | A (M1) | M39-R2 | EURUSD 1h returns | AD=228.38, p=0.0001 | None | N/A | M4=0 |
| V08 | LNO scale component | A (M1) | M41 | EURUSD 1h returns | p=0.0001, 1.65× ratio | None | N/A | M4=0 |
| V09 | LNO location (mean) component | REJECTED | M41 | EURUSD 1h returns | p=0.437 (no location premium) | Rejected | Negative | M4=0 |
| V10 | BTC HIGH_VOL transferability | A (M2) | IC3 | BTC (from EURUSD) | C-index 0.6224 | None | N/A | M4=0 |
| V11 | BTC forward-RV translation | A (M2) | IC3 | BTC | p=0.000011 | None | N/A | M4=0 |
| V12 | BTC large volatility risk premium (VRP) | A (M1) | IC7 | BTC options | Large observed VRP | Long straddle REJECTED | Negative | M4=0 |
| V13 | SMC structural M1 primitives | A (M1) | SMC-R1..R9 | XAUUSD M1 | BOS/OB/FVG/CHOCH/sweep/swing(N=5)/freshness deterministic & reproducible | BOS+OB/CHOCH tests | Negative (below cost) | M4=0 |

**Ethical / economic note**: A scientifically validated primitive is NOT an economic module. Every validated finding above lacks a demonstrated independent `E[R_net] > 0` payoff with realistic frozen costs.

---

## 3. Closed-Path Inventory (Definitive — 13 paths) + Collision Test

Per M45 (§6), M50/M49, and SMC closures. **These must not be silently reopened.** Collision test (economic cores): each closed path is checked to confirm NO distinct, un-tested economic compensation stream survives; none does.

| # | Closed Path | Closure Point | Evidence Class | Closure Type | What must NOT be repeated | Economic core collision result |
|---|-------------|----------------|----------------|--------------|---------------------------|--------------------------------|
| C01 | HIGH_VOL spot monetization | RC012 S007-011 | FAILED HYPOTHESIS | Scientific | All spot architectures rejected | None survives |
| C02 | HIGH_VOL static boundary | M31 | FAILED HYPOTHESIS | Scientific | Static threshold saturated (99.75%) | None |
| C03 | HIGH_VOL dynamic translation | M33 | FAILED HYPOTHESIS | Methodological | Not defensible | None |
| C04 | HIGH_VOL standalone economic branch | M34 | CLOSED | Methodological | Economic layer not defensible in spot | None |
| C05 | Session raw breakout | RC013 S007-011 | FAILED HYPOTHESIS | Scientific | Monetization failed | None |
| C06 | Session-transition standalone (LNO scale) | M42 | FAILED HYPOTHESIS | Scientific | Deterministic, no asymmetry | None |
| C07 | Session-transition modular pathway | M42 | FAILED HYPOTHESIS | Scientific | No validated base module | None |
| C08 | CME listed options (EUR/USD) | RC015 (M09) | FAILED HYPOTHESIS | Methodological | Liquidity infeasible | None |
| C09 | BTC long straddle | IC7 | FAILED HYPOTHESIS | Scientific | p=0.953, mean PnL=-$130 | None |
| C10 | Crypto-options alternatives | IC8 | FAILED HYPOTHESIS | Scientific | All scored <35/50; no distinct mechanism | None |
| C11 | Cross-asset transmission | RC014 | FAILED HYPOTHESIS | Scientific | Transmission hypothesis rejected | None |
| C12 | SMC BOS+OB | SMC-R7 | FAILED HYPOTHESIS | Scientific | Gross +1.01 bp, net −1,347 bp/day; M4 FAIL | None |
| C13 | SMC CHOCH | SMC-R9-CR | FAILED HYPOTHESIS | Scientific | Gross +0.89 bp, net −17.03 bp; M3 FAIL | None |
| C14 | Funding / carry | M49 | CLOSED | Methodological (mechanism discovery) | No validated predictor of funding; sign/formula/unit errors | None |

Collision-test conclusion: **No closed path conceals a distinct, independently-payoff economic compensation stream.** Reopening any requires a genuinely NEW mechanism/hypothesis, not parameter/architecture retries (forbidden under M45 §12).

---

## 4. Predictive-but-Not-Economic Inventory (Evidence Class A-B, M2)

Prediction capability is established but does **not** translate into validated economics:

| ID | Predictive finding | Evidence | Economic translation | Status |
|----|--------------------|----------|----------------------|--------|
| P01 | HIGH_VOL persistence predictability (EURUSD) | C-index 0.6656 | No direction/mechanism | NOT economic |
| P02 | BTC volatility-state predictability | C-index 0.6224 | No direction/mechanism | NOT economic |
| P03 | BTC forward-RV translation | p=0.000011 | Long straddle failed | NOT economic |
| P04 | Session-transition scale (LNO) | p=0.0001, 1.65× | Standalone & modular rejected | NOT economic |
| P05 | R-Velocity early-deterioration association | B (OBSERVED, unaudited) | Path-dependent; HYPOTHESIS only | NOT validated |

---

## 5. Hypothesis / Architectural Inference Inventory (Evidence Class B-C-D)

| ID | Candidate | Evidence class | Assessment | Status |
|----|-----------|----------------|------------|--------|
| H01 | Execution-State economics | D (ARCHITECTURAL) | Largely mandatory frozen-cost layer; no base; no independent payoff | REJECTED (future layer, requires M4) |
| H02 | Trade-Path economics (entry+path+exit) | B/C (R-Velocity unaudited) | Most conceptually novel; exit/decision optimization on nonexistent base; no validated compensation chain | REJECTED (needs M1→M3 programme) |
| H03 | Signal→risk→allocation overlay | D (ARCHITECTURAL) | Distinct architectural role, not an economic module | Rejected as economic candidate |
| H04 | Portfolio-risk correlation module | D (ARCHITECTURAL) | Risk engineering only; no portfolio of M4 modules; no independent E[R_net]>0 | Rejected as economic candidate |
| H05 | Regime / combined filter (CAB+Ghost+ADX+...) | B/C | Combination-mining / reuse; M4=0 forbids | Rejected (anti-combination-mining) |
| H06 | Transition-aware regime | C | Re-opens M42-closed session-transition without new hypothesis | Rejected |
| H07 | Cross-stream / raw breakout reuse | C | Repackaged closed path | Rejected |

---

## 6. M4 Audit (Evidence-Class-A drill-down)

**M4 validated economic modules = 0.** Verified by inspecting underlying reports, not merely filenames.

Subject of special scrutiny: **RC012 Study 006 — Volatility Monetization** (`reports/RC012_Study_006_Volatility_Monetization.md`) headline: "CANDIDATE ECONOMIC EDGE" and "+0.98 pips net at 1.0 pip friction" / "positive net expectancy."

Audit result — **does NOT qualify as M4**:
1. It is explicitly a **monetization proof-of-concept, not a validated deployable trading strategy** (Study 006 §7 note).
2. Payoff is a **synthetic directional-neutral straddle** with premium deducted as unconditional mean forward movement (not a real traded instrument).
3. Friction is a **fixed 1.0 pip assumption with 0.5/2.0 pip sensitivity**; at 2.0 pips HIGH_VOL A breakeven (−0.02) and is not the frozen realistic-cost architecture later enforced (R10/M15).
4. It was **superseded**: RC012 Studies 007-011 showed every tested spot execution architecture failed to capture the movement (path length high, path efficiency ~12%, rigid exits capture only ~21% of travel, bounded adverse inventory worsens expectancy and adds drawdown). M34/M45 therefore record RC012 spot monetization as FAILED HYPOTHESIS.
No independent-tradeable-payoff M4 chain exists. **All M4=0 declarations confirmed.**

## 7. M5 Audit

**M5 deployment candidates = 0.** No M4 exists, and R10 Level 4 (M5) is strictly downstream of a validated M4 module. Bot architectures A (single killer strategy) and B (validated-module set) both remain **NOT AUTHORIZED**. Combination mining remains forbidden.

---

## 8. Data / Instrument Inventory

| Asset / instrument | Coverage | Source / location | Usable for economic test? |
|--------------------|----------|-------------------|---------------------------|
| EURUSD M1/M15 OHLCV | ~5.5 yr hourly | `data/` | Yes (scientific; no validated economics) |
| BTC M1 OHLCV | ~5 yr 1-min | `data/m1/BTCUSD_M1.parquet` | Yes (scientific; straddle failed) |
| BTC options trades cache | 827 timestamps | `data/btc/ic6r3_raw_trade_cache.json` | IC7/IC8 tested/rejected |
| M39-R2 transition dataset | 31,941 hourly returns | `reports/APEX_M39R2_Session_Transition_Return_Data.csv` | Scientific; economics rejected |
| IC3 transferability data | 1,571 OOS predictions | `reports/APEX_IC3_BTC_Transferability_Data.csv` | Scientific only |
| IC6-R3 eligibility ledger | 343 BTC option obs | `reports/APEX_IC6R3_BTC_Options_Eligibility.csv` | IC7 base |
| IC7 economic data | 343-row straddle PnL | `reports/APEX_IC7_BTC_Straddle_Economic_Data.csv` | Long straddle rejected |
| HIGH_VOL episode ledger | 794 episodes | RC012/M34 | Scientific only |
| BTC episode ledger | 1,621 episodes | IC3 | Scientific only |
| XAUUSD M1 | SMC structural events | SMC_RESEARCH | BOS+OB/CHOCH net < 0 |

## 9. Evidence-Gap Inventory

| Gap | Why it matters | Class | Required to close |
|-----|----------------|-------|-------------------|
| No validated predictor of funding/carry (M49) | Funding path closed at discovery | A/M2 | New validated predictor of funding state |
| R-Velocity predictive power not validated | Trade-Path depends on it; unaudited | B→A needed | Controlled M0→M1→M2 validation programme |
| Execution friction not directly measured | Execution-State economics depends on it | B/D | Direct execution/friction measurement |
| CME EUR/USD listed-option liquidity infeasible | Options convexity harvest blocked | — | New liquid instrument/venue (restart trigger D) |
| No portfolio of M4 modules | Portfolio-risk allocation untestable | D | Prior M4 modules |
| Absent custom-bot Week-6 document | Observations cannot be repository-audited | B (unaudited) | Original document; still B even if located |

---

## 10. Custom-Bot Evidence Search Result

Searched (filename + content) across the `apex` tree and the broader `grid research` tree for: r-velocity/R-Velocity, Ghost Sniper, ghost/sniper, CAB, Unified Runner, unified, Week-6/week 6, custom bot, ATR, ADX, cache/stale-cache, portfolio clustering.

**Result: original custom-bot Week-6 analysis document NOT found on disk.** Only internal references within APEX governance/report files match (HANDOFF, STATE, M50, POST-M50 CONTROL, Control Review). Consistent with the prior 2026-08-30 Control Review finding.
- Must remain: **B — USER-SUPPLIED / OBSERVED**, `Repository-audited: NO`.
- Not reconstructed, not fabricated.
- Even if located later, classification stays B (observations remain non-repository-audited unless re-validated).

---

## 11. Contradiction / Nuance Flag (for Control Session adjudication)

**CONTRADICTION FOUND (evidence nuance, not silently resolved):**

- **Source A**: `reports/RC012_Study_006_Volatility_Monetization.md` — headline "CANDIDATE ECONOMIC EDGE", "+0.98 pips net (1.0 pip)", "positive net expectancy", "early/late validation stable."
- **Source B**: `docs/APEX_HIGH_VOL_BRANCH_CLOSURE.md` / M34 / `APEX_M45_Evidence_Ledger.csv` — "RC012 spot monetization = FAILED HYPOTHESIS / Monetization failed", "APEX currently has NO validated economic module."
- **Nature**: Study 006 reports positive net on a *synthetic straddle* with *fixed 1.0 pip friction* and explicitly disclaims deployability; Studies 007-011 then reject every real spot architecture; reconciliation is documented in `RC012_Study_012_HIGH_VOL_Monetization_Review.md` (freeze HIGH_VOL as non-monetizable except via options).
- **Materiality**: LOW-to-MEDIUM. Not a hidden M4 — Study 006 is a proof-of-concept, not a deployable strategy, and does not satisfy frozen realistic-cost / independent-payoff criteria. No restart is implied.
- **Recommended Control Review**: Confirm closure of RC012 spot monetization stands; no action required unless a genuinely new options-based instrument arrives (restart trigger A/D).

---

## 12. Data / API / Spend Compliance

- External API calls: **0**
- New data acquired: **0**
- Spend: **$0.00**

---

*End of Task 01 Economic Knowledge Map. Programme remains PAUSED pending Control Session decision.*
