# APEX M45 — Research-Cycle Closure, Evidence Ledger & Restart Conditions

**Date**: 2026-08-27
**Milestone**: M45
**Status**: COMPLETE
**Classification**: Final governance / knowledge-preservation milestone — no empirical work

---

## 1. Executive Summary

M45 closes the current APEX research cycle. It audits what was genuinely established, classifies evidence levels, preserves reusable assets, documents closed paths, and defines restart conditions.

**Decision: A — CURRENT CYCLE CLOSED / PAUSED**

The programme is now formally paused with no automatic future milestone. All validated knowledge is preserved. The repository is usable for future research. Restart requires one of five documented triggers.

---

## 2. Critical Correction to M44

M44 stated:

> "The market already prices volatility information, therefore APEX edge = NONE."

**Classification: ARCHITECTURAL INFERENCE — NOT PROVEN.**

This statement is stronger than the evidence supports. IC7 showed that **one specific long-straddle mechanism failed** on BTC options. It did not prove that every possible instrument already prices every dimension of the APEX information efficiently.

**Corrected statement:**

> "The tested payoff mechanisms (long ATM straddle on BTC options) did not demonstrate incremental economic value. The broader question of whether APEX information has economic value through other instruments or mechanisms remains UNKNOWN."

This distinction matters for future restarts. The programme is paused because no current M3 candidate exists — not because market efficiency has been proven.

---

## 3. Evidence Classification System

Every major conclusion is classified as exactly one:

| Class | Definition |
|-------|-----------|
| **PROVEN** | Directly established by a valid frozen experiment |
| **VALIDATED INFORMATION** | Scientifically established observation; does not itself establish economics |
| **FAILED HYPOTHESIS** | Specific economic/scientific hypothesis tested and rejected |
| **ARCHITECTURAL INFERENCE** | Reasonable interpretation not directly tested |
| **UNKNOWN** | Evidence does not resolve it |

---

## 4. Complete APEX Evidence Ledger

### RC012 — HIGH_VOL Discovery & Translation

| Research Item | What Was Tested | Result | Evidence Level | Economic Status | Reopen? |
|---------------|----------------|--------|----------------|-----------------|---------|
| HIGH_VOL primitive | Distributional feature of EURUSD M15 | Validated (D=0.1927) | **VALIDATED INFO** | No economic mechanism | No (branch closed) |
| HIGH_VOL persistence | Non-memoryless lifecycle | Validated (p<0.0001, n=794) | **VALIDATED INFO** | No economic mechanism | No |
| HIGH_VOL predictability | Onset features → future persistence | Validated (C-index=0.6656) | **VALIDATED INFO** | No economic module | No |
| HIGH_VOL forward RV | Predicted persistence → future RV | Validated (p=0.0032) | **VALIDATED INFO** | No economic module | No |
| HIGH_VOL directional | Predicted persistence → price direction | **REJECTED** (p=0.6418) | **FAILED HYPOTHESIS** | No directional edge | No |
| HIGH_VOL excursion | Predicted persistence → excursion envelope | Validated (p=7.5×10⁻⁵) | **VALIDATED INFO** | No economic module | No |
| HIGH_VOL boundary | Static 1.0×RV20 boundary | **REJECTED** (99.75% saturation) | **FAILED HYPOTHESIS** | Threshold approach failed | No |
| HIGH_VOL dynamic translation | Dynamic boundary methodology | **REJECTED** (methodologically weak) | **FAILED HYPOTHESIS** | Not defensible | No |
| HIGH_VOL standalone branch | Full economic translation | **CLOSED** (M34) | N/A | Economic layer not defensible | No |

### RC013 — Session Transition

| Research Item | What Was Tested | Result | Evidence Level | Economic Status | Reopen? |
|---------------|----------------|--------|----------------|-----------------|---------|
| RC013 raw breakout | Session-transition → directional trade | **REJECTED** (Studies 007-011) | **FAILED HYPOTHESIS** | Monetization failed | No |
| M39-R2 CDF difference | LNO vs control 1h forward returns | Validated (AD=228.38, p=0.0001) | **VALIDATED INFO** | No economic mechanism | No (same finding) |
| M41 scale component | Distributional component decomposition | Validated (p=0.0001, 1.65× ratio) | **VALIDATED INFO** | No economic mechanism | No |
| M41 location component | Mean difference | **REJECTED** (p=0.437) | **FAILED HYPOTHESIS** | No directional premium | No |
| M42 standalone mechanism | LNO scale → economic payoff | **REJECTED** (deterministic, no asymmetry) | **FAILED HYPOTHESIS** | No standalone mechanism | No |
| M42 modular pathway | LNO scale → module combination | **REJECTED** (no validated base) | **FAILED HYPOTHESIS** | No modular pathway | No |

### RC014 — Cross-Asset Transmission

| Research Item | What Was Tested | Result | Evidence Level | Economic Status | Reopen? |
|---------------|----------------|--------|----------------|-----------------|---------|
| RC014 transmission | Cross-asset volatility transmission | **REJECTED** | **FAILED HYPOTHESIS** | Transmission hypothesis rejected | No |

### RC015 — CME Listed Options

| Research Item | What Was Tested | Result | Evidence Level | Economic Status | Reopen? |
|---------------|----------------|--------|----------------|-----------------|---------|
| RC015 observation architecture | CME EUR/USD listed option liquidity | **FAILED** (liquidity infeasible) | **FAILED HYPOTHESIS** | Method infeasible | No |

### BTC Crypto-Options Chain (IC1–IC8)

| Research Item | What Was Tested | Result | Evidence Level | Economic Status | Reopen? |
|---------------|----------------|--------|----------------|-----------------|---------|
| IC3 BTC transferability | EURUSD concept → BTC | Validated (C-index=0.6224) | **VALIDATED INFO** | No economic module | No (same finding) |
| IC3 BTC forward RV | BTC persistence → forward RV | Validated (p=0.000011) | **VALIDATED INFO** | No economic module | No |
| IC7 long straddle | predicted_RV > IV → positive straddle PnL | **REJECTED** (p=0.953, mean PnL=-$130) | **FAILED HYPOTHESIS** | Long straddle mechanism rejected | No |
| IC8 alternative mechanisms | Short vol, term-structure, cross-instrument, non-option vol | **REJECTED** (all scored <35/50) | **FAILED HYPOTHESIS** | No distinct mechanism survives | No |

### M39-R2 / M40 / M41 — Session-Transition Decomposition

| Research Item | What Was Tested | Result | Evidence Level | Economic Status | Reopen? |
|---------------|----------------|--------|----------------|-----------------|---------|
| M39-R2 permutation test | LNO CDF differs from control | Validated (p=0.0001) | **VALIDATED INFO** | No economic mechanism | No |
| M40 decomposition design | Sequential hierarchical framework | Complete (methodology only) | N/A | N/A | N/A |
| M41 scale decomposition | Which component differs | Validated (Scale p=0.0001) | **VALIDATED INFO** | No economic mechanism | No |

### M42 / M43 / M44 — Economic Architecture

| Research Item | What Was Tested | Result | Evidence Level | Economic Status | Reopen? |
|---------------|----------------|--------|----------------|-----------------|---------|
| M42 standalone/module | LNO scale economic mechanism | **REJECTED** (no mechanism) | **FAILED HYPOTHESIS** | No mechanism | No |
| M43 programme continuation | Should APEX continue? | **PAUSED** | N/A | No justified question | N/A |
| M44 M3 candidate discovery | Can any artifact reach M3? | **NO M3 CANDIDATE** | N/A | Programme paused | N/A |

---

## 5. Three Levels of Knowledge

### Scientific Facts (PROVEN / VALIDATED INFO)

1. HIGH_VOL is a structural distributional primitive on EURUSD M15
2. HIGH_VOL persistence is non-memoryless and predictable (C-index 0.6656)
3. Predicted persistence translates to forward RV (p=0.0032) and excursion (p=7.5×10⁻⁵)
4. Predicted persistence does NOT predict direction (p=0.6418)
5. BTC volatility-state transfers from EURUSD (C-index 0.6224)
6. BTC forward RV translation is established (p=0.000011)
7. LNO has a distinct 1h forward-return CDF (p=0.0001)
8. LNO primary component is SCALE (p=0.0001, 1.65× ratio)
9. LNO location (mean) does NOT differ (p=0.437)
10. BTC options exhibit a large VRP (IC7)

### Predictive Information (VALIDATED)

- EURUSD HIGH_VOL persistence predictability (M17-R2)
- BTC volatility-state predictability (IC3)
- BTC forward realized-volatility translation (IC3)
- Walk-forward Cox PH methodology (M17-R2)

### Economic Mechanisms (TESTED AND REJECTED)

- Long ATM straddle on BTC options (IC7)
- Crypto-options alternative mechanisms (IC8)
- LNO scale standalone mechanism (M42)
- LNO scale modular pathway (M42)
- HIGH_VOL boundary monetization (M31)
- HIGH_VOL dynamic translation (M33)
- RC013 raw breakout (Studies 007-011)

---

## 6. Closed Paths — Definitive List

| Path | Closure Point | Evidence Level | Closure Type | What Must NOT Be Repeated |
|------|--------------|----------------|--------------|--------------------------|
| RC012 spot monetization | Studies 007-011 | FAILED HYPOTHESIS | Scientific | All architectures rejected |
| RC014 cross-asset transmission | RC014 | FAILED HYPOTHESIS | Scientific | Transmission hypothesis rejected |
| RC015 CME listed options | M09 | FAILED HYPOTHESIS | Methodological | Liquidity infeasible |
| HIGH_VOL standalone economic branch | M34 | N/A | Methodological | Economic implementation not defensible |
| HIGH_VOL boundary test | M31 | FAILED HYPOTHESIS | Scientific | Static threshold saturated |
| HIGH_VOL dynamic translation | M33 | FAILED HYPOTHESIS | Methodological | Not defensible |
| BTC long straddle | IC7 | FAILED HYPOTHESIS | Scientific | p=0.953, mean PnL=-$130 |
| Crypto-options alternatives | IC8 | FAILED HYPOTHESIS | Scientific | No distinct mechanism survives |
| LNO scale standalone | M42 | FAILED HYPOTHESIS | Scientific | Deterministic, no asymmetry |
| LNO scale modular | M42 | FAILED HYPOTHESIS | Scientific | No validated base component |

**Important:** Closing these paths does NOT imply:
- Volatility research is impossible
- Options trading is impossible
- Session-timing has no economic value
- APEX information has no economic value

It means the **specific tested mechanisms** failed under the **specific tested conditions**.

---

## 7. Reusable Research Assets

### Scientific Primitives

| Asset | Description | Source |
|-------|-------------|--------|
| HIGH_VOL_STATE | Canonical HIGH_VOL episode ledger (794 episodes) | RC012, M34 |
| EURUSD persistence model | Walk-forward Cox PH methodology | M17-R2 |
| BTC persistence model | BTC-native Cox PH with IC3 features | IC3 |
| BTC episode ledger | 1,621 BTC HIGH_VOL episodes | IC3 |
| Session-transition return data | 31,941 hourly returns with LNO/CTRL labels | M39-R2 |

### Predictive Artifacts

| Asset | Description | Source |
|-------|-------------|--------|
| EURUSD OOS predictions | Walk-forward risk scores | M17-R2 |
| BTC OOS predictions | Walk-forward risk scores (1,571 predictions) | IC3 |
| Forward RV mapping coefficients | Walk-forward OLS alpha/beta | IC5, IC3 |

### Data Assets

| Asset | Description | Location |
|-------|-------------|----------|
| EURUSD M1/M15 OHLCV | 5.5 years of hourly data | data/ |
| BTC M1 OHLCV | 5 years of 1-minute data | data/m1/BTCUSD_M1.parquet |
| BTC options trade cache | 827 timestamps of raw trades | data/btc/ic6r3_raw_trade_cache.json |
| M39-R2 transition dataset | 31,941 hourly returns | reports/APEX_M39R2_Session_Transition_Return_Data.csv |
| IC3 transferability data | 1,571 OOS predictions | reports/APEX_IC3_BTC_Transferability_Data.csv |
| IC6-R3 eligibility ledger | 343 eligible BTC options observations | reports/APEX_IC6R3_BTC_Options_Eligibility.csv |
| IC7 economic data | 343-row straddle PnL data | reports/APEX_IC7_BTC_Straddle_Economic_Data.csv |

### Methodology Assets

| Asset | Description | Source |
|-------|-------------|--------|
| Day-block permutation framework | Dependence-aware null construction | M39-R2 |
| Walk-forward Cox PH | Expanding-window survival methodology | M17-R2 |
| Sequential hierarchical decomposition | Component-wise distributional testing | M40/M41 |
| Module qualification framework | M0-M5 lifecycle, qualification checklist | AR1 |
| Bot architecture principles | Architecture A/B, anti-combination-mining | AR1 |

### Negative Knowledge (Failures to Preserve)

| Lesson | Source | What NOT To Repeat |
|--------|--------|--------------------|
| Bootstrap with preserved labels does not simulate H0 | M39-CR | Never preserve group labels in null construction |
| TTE computation requires explicit timestamp binding | IC6-R2-CR | Never reuse loop variable across batch iterations |
| Call/put joint check must search across option types | IC6-R3 | Never check within pre-split groups |
| Static boundaries saturate when continuous relationships exist | M31 | Never expect binary thresholds to capture continuous phenomena |
| F=K in Black-76 overstates premium by ~10-15% | IC7 | Document approximation impact on PnL direction |
| Sequential hierarchical testing controls FWER without Bonferroni | M40 | Use sequential testing for ordered component decomposition |

---

## 8. Module Qualification State

From AR1/M44:

```
M0 (Phenomenon):     many observations
M1 (Scientific):     4 artifacts (HIGH_VOL, LNO scale, session CDF, BTC VRP)
M2 (Predictive):     3 artifacts (HIGH_VOL persistence, BTC transfer, BTC RV translation)
M3 (Economic):       0
M4 (Validated Module): 0
M5 (Production):     0
```

**APEX currently has NO validated economic module.**

Therefore: **no production bot architecture is authorized.**

---

## 9. Bot Architecture Status

### Architecture A — Single Killer Strategy

```
ONE M4/M5 STRATEGY → BOT
```

Status: **NOT AUTHORIZED** — no M4+ artifact exists.

### Architecture B — Validated Module Set

```
REGIME ROUTER (M4) → M4 Module A + M4 Module B + M4 Module C → BOT
```

Status: **NOT AUTHORIZED** — no M4+ modules exist.

### Combination Mining

**FORBIDDEN.** Testing all combinations and selecting best PnL is prohibited under all circumstances.

---

## 10. Rare-Event Policy

Preserved principle:

> Rare events are NOT rejected merely because they occur infrequently.

Future rare-event research must distinguish:
- Event frequency (how often)
- Independent evidence (how many independent observations)
- Confidence (CI width)
- Calendar exposure (forward observation period)
- Execution validation (demo/forward testing)

Forward/demo testing is **execution validation**, not a mechanism for waiting until a favorable result appears.

---

## 11. Restart Conditions

APEX may legitimately restart if ANY ONE of the following occurs:

| Condition | Description | Example |
|-----------|-------------|---------|
| **A. New instrument class** | A new instrument becomes realistically observable with an economically aligned payoff | Liquid BTC volatility futures, DeFi options, prediction markets |
| **B. New validated primitive** | A genuinely new phenomenon is discovered outside closed branches | New market microstructure finding, new cross-asset relationship |
| **C. New predictive model** | A new prediction targets an economically compensated quantity | Funding rate prediction, liquidity provision return prediction |
| **D. External development** | Previously unavailable data/architecture becomes observable | New exchange API, new market structure, new regulatory framework |
| **E. New economic mechanism** | A genuinely distinct mechanism becomes identifiable | Non-options convexity instrument, carry-based vol harvesting |

---

## 12. Forbidden Restart Triggers

The following are explicitly FORBIDDEN as restart triggers:

- Changing a rejected threshold
- Changing a rejected maturity
- Flipping long to short
- Adding filters to rescue a failed strategy
- Brute-force module combinations
- Testing every instrument until one works
- Adding a second predictor solely because it improves PnL
- Reopening a closed branch without a genuinely new hypothesis
- "We feel like testing another strategy"
- "The previous result was close, let's try again with different parameters"

---

## 13. Scientific Pause Definition

**APEX PAUSED** means:

- No active economic experiment
- No automatic next milestone
- Validated knowledge preserved in repository
- Repository remains usable for future research
- Restart requires one of the documented triggers (Section 11)
- All closed paths remain closed (Section 6)
- Bot architecture principles remain in effect (Section 9)

---

## 14. Final Research-Cycle Verdict

**A — CURRENT CYCLE CLOSED / PAUSED**

The programme has produced genuine scientific discoveries across multiple domains. The economic translation layer has proven intractable with the current evidence base. The architecture framework (AR1) is established and ready for future use. The programme is paused, not terminated.

---

## 15. External API calls: 0 | New data acquired: 0 | Spend: $0.00

---

*M45 is a governance/knowledge-preservation milestone. No experiments were run. No data was acquired. No PnL was calculated.*
