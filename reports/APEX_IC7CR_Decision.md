# APEX IC7-CR — Decision Classification

**Date**: 2026-08-26
**Milestone**: IC7-CR

---

## Decision: A — IC7 VALID — LONG-STRADDLE MECHANISM REJECTED

### Requirements Met

| Requirement | Status |
|-------------|--------|
| Sample lineage | **PASS** — 343 IC7 observations map 1:1 to 343 IC6-R3 approved observations |
| Entry methodology | **PASS** — Black-76 from IV (MINOR IMPLEMENTATION LIMITATION, not deviation) |
| PnL scaling | **PASS** — internally consistent, matches IC5 |
| Conditional rule | **PASS** — pre-registered in IC5 Section 8 |
| Statistical test | **PASS** — HAC t-test, one-sided, α=0.05, correctly implemented |
| No material methodology deviation | **PASS** — one approximation (F=K) is conservative |

### Classification

| Component | Classification | Impact |
|-----------|---------------|--------|
| Sample lineage | EQUIVALENT IMPLEMENTATION | None — 343 is the correct count |
| Entry premium | MINOR IMPLEMENTATION LIMITATION | Conservative — overstates premium, makes PnL more negative |
| TTE [12h,24h] | OBSERVATION-PROCESS CHANGE (approved by IC6-R2-CR) | Conservative — option covers longer than forecast |
| IV from trade data | OPERATIONAL (approved by IC6-R3-CR) | None — same Black-76 model |
| Freshness ≤1h | OBSERVATION-PROCESS (approved by IC6-R3) | None — 91.8% under 15 min |
| Conditional sample | FROZEN IN IC5 | None — 267/343 satisfy predicted_RV > IV |
| Cost model | EQUIVALENT | None — 0.04% × 4 legs exactly as IC5 |

### What IC7 Establishes

1. **BTC volatility risk premium is real and large** — IV > RV on average
2. **APEX signal has predictive content** — r = 0.18 OOS, partially identifies when VRP is smaller
3. **Signal is not strong enough for positive straddle expectancy** — conditional mean PnL = −$130
4. **Long straddle is not the right instrument** — model predicts elevated vol, but options market already prices it (or more)

### What IC7 Does NOT Establish

- Short straddle works
- Volatility spread works
- BTC volatility prediction has no economic value
- IC3 is invalid
- Any alternative instrument is profitable

### Long-Straddle Mechanism Status

> **CLOSED.** The mechanism (predicted_RV > IV → positive expected long-straddle PnL) is falsified by IC7.

### Report Corrections Required

| Correction | Type |
|-----------|------|
| Remove "robust to maturity limitation" claim | Language — no sensitivity tested |
| Reclassify "35% better" as descriptive only | Language — no formal comparison frozen |
| State: "IC7 failed under [12h,24h]; robustness not tested" | Required interpretation |

### Crypto-Options Path Status

> **OPEN BUT FROZEN.** The long-straddle path is closed. An alternative mechanism may be proposed if it passes the IC7-CR Stop Rule (scientifically distinct, economically coherent, independently falsifiable, ex-ante freezable).

### IC8 Status

> **BLOCKED.** No alternative mechanism has been proposed or validated. IC8 requires:
> 1. A scientifically distinct mechanism (not the opposite side of the same relationship)
> 2. An independently falsifiable hypothesis
> 3. A frozen methodology before any execution

### Next Authorized Milestone

> **None.** The control session must decide whether the crypto-options path closes entirely or whether a new mechanism is justified.
