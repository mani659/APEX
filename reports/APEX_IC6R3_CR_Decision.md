# APEX IC6-R3-CR — Decision Classification

**Date**: 2026-08-26
**Milestone**: IC6-R3-CR

---

## Decision: **B — APPROVE IC7 WITH EXPLICIT LIMITATION**

---

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| A | Eligible observations correct | ✅ PASS — 343 verified |
| B | IV represents intended contemporaneous quantity | ✅ PASS — trade-derived IV within 1h |
| C | Call/put timestamps economically coherent | ✅ PASS — mean diff 9.3 min |
| D | Maturity defensible relative to future-RV horizon | ✅ PASS — [12h,24h] conservative |
| E | No lookahead | ✅ PASS |
| F | Methodology executable without further choices | ✅ PASS |

---

## Documented Limitation

**Maturity width:** TTE ∈ [12h, 24h] (mean ~16.6h) covers a longer period than IC3's 12h forward-RV prediction horizon. The economic test therefore compares a 12h RV prediction against a ~16.6h IV expectation.

**Impact:** Conservative — strengthens the economic test by requiring the 12h prediction to be informative enough for a longer-dated straddle.

**Documentation required in IC7:** State that the comparison is between 12h predicted RV and ~16.6h ATM IV, and that this represents a conservative interpretation of the IC5 economic quantity.

---

## Amendment Classification Summary

| Component | Classification | Decision |
|-----------|---------------|----------|
| Trade-level IV | OBSERVATION-PROCESS | ACCEPTED |
| TTE [12h,24h] | OBSERVATION-PROCESS (conservative) | ACCEPTED with limitation |
| 1h freshness | OBSERVATION-PROCESS (restored) | ACCEPTED |
| Timestamp matching | OPERATIONAL | ACCEPTED |
| Call/put pairing | OPERATIONAL | ACCEPTED |
| Strike selection | OPERATIONAL | ACCEPTED |
| Cost model | OPERATIONAL | ACCEPTED (no change) |

**No methodology amendment required.**

---

## IC7 Authorization

IC7 is **AUTHORIZED** pending control-session review of IC6-R3-CR.

IC7 must:
1. Execute the frozen IC5 economic methodology
2. Document the maturity-width limitation in the result interpretation
3. Use the IC6-R3 eligibility ledger (343 observations)
4. Apply the frozen cost model (0.04% × 4 legs)
5. Apply the frozen statistical framework (HAC t-test, α=0.05 one-sided)
6. Compare conditional straddle PnL against unconditional baseline

---

*End of decision.*
