# APEX IC6-R2-CR — Methodology Amendment Decision

**Date**: 2026-08-26
**Milestone**: IC6-R2-CR
**Classification**: CONTROL REVIEW — Amendment Adjudication

---

## 1. Amendment A — Maturity Window

| Dimension | Detail |
|-----------|--------|
| IC5 frozen | TTE ∈ [6h, 18h] |
| IC6-R2 proposed | TTE ∈ [6h, 72h] |
| Classification | **ESTIMAND CHANGED** |
| Scientific equivalence | NO |
| Decision | **NOT APPROVED** |

### Rationale

The IC5 economic quantity compares a 12h forward RV forecast against option IV. Expanding maturity to 68h mixes fundamentally different term exposures. However, the nearest daily expiry (T+1, ~16-20h TTE) IS a defensible approximation for the 12h horizon.

A scientifically defensible maturity rule would be:

> **TTE ∈ [12h, 24h]** — captures the nearest daily expiry at 08:00 UTC

This would reduce N but preserve the economic quantity. The [6h, 72h] window mixes T+1, T+2, and T+3 expiries, which are not economically equivalent.

### Counter-Argument

IC6-R2 argued that [6h, 18h] captures zero BTC expiries. This is correct — BTC's nearest daily expiry has TTE ~16-20h. But the solution is [12h, 24h], not [6h, 72h].

---

## 2. Amendment B — IV Source

| Dimension | Detail |
|-----------|--------|
| IC5 frozen | Black-76 from midpoint of bid/ask |
| IC6-R2 proposed | Pre-computed Black-76 from trade data |
| Classification | **OPERATIONAL** |
| Scientific equivalence | YES |
| Decision | **APPROVED** (pending corrected data) |

### Rationale

The mathematical pricing model is identical (Black-76). Using trade price as midpoint proxy is a standard approximation for liquid ATM options. The Deribit `iv` field is computed by the exchange using the same model IC5 specifies.

This amendment changes the observation process (trade vs quote) but not the economic estimand.

---

## 3. Amendment C — Freshness

| Dimension | Detail |
|-----------|--------|
| IC5 frozen | Quote age ≤ 1 hour |
| IC6-R2 proposed | Trade within 24h query window |
| IC6-R2 actual | No freshness check (all pass) |
| Classification | **OBSERVATION-PROCESS CHANGE** |
| Scientific equivalence | WEAKLY YES with ≤1h; NO with unbounded |
| Decision | **NOT APPROVED as implemented** |

### Rationale

The IC6-R2 code sets `freshness_ok = True` unconditionally, with an incorrect comment ("we queried within 1h"). The actual query window is 24h. No trade-level freshness is computed.

A scientifically defensible freshness rule would be:

> **Trade timestamp within 1 hour of prediction timestamp**

This is achievable for Deribit's active BTC ATM options market. A24h freshness rule is interpretable but substantially weaker than IC5's specification.

---

## 4. TTE Computation Bug

| Dimension | Detail |
|-----------|--------|
| Type | **FATAL IMPLEMENTATION BUG** |
| Root cause | Python loop variable scoping in batch processing |
| Impact | 57.3% of observations have TTE error ≥ 100h |
| Mean error | 307.4 hours |
| Decision | **INVALIDATES IC6-R2 ELIGIBILITY RESULTS** |

### Rationale

The bug causes maturity selection to use the wrong reference timestamp. Most "eligible" observations have IV from options expiring weeks/months after the prediction timestamp. The selected instruments are not the ones IC5 intended.

This is not an amendment question — it is a data-integrity failure.

---

## 5. Aggregate Decision

### **REJECT IC6-R2 — REQUIRES IC6-R3**

The three amendments are adjudicated as follows:

| Amendment | Verdict |
|-----------|---------|
| Maturity [6h, 72h] | NOT APPROVED — use [12h, 24h] |
| IV from trade data | APPROVED — equivalent methodology |
| Freshness (unbounded) | NOT APPROVED — require ≤ 1h trade freshness |
| TTE bug | FATAL — invalidates all results |

IC6-R3 must:
1. Fix the TTE bug
2. Apply maturity rule [12h, 24h]
3. Apply freshness rule: trade timestamp within 1h of prediction timestamp
4. Re-evaluate eligibility count
5. If eligible observations ≥ 100, authorize IC7
6. If eligible observations < 100, STOP the crypto-options path

---

## 6. No Methodology Amendment V2 Created

No `APEX_IC5_OPTIONS_METHODOLOGY_AMENDMENT_V2.md` is created because:
- No amendment was approved on its merits (all were superseded by the TTE bug)
- The control review must be repeated on corrected data
- The original IC5 methodology remains frozen

---

*End of amendment decision.*
