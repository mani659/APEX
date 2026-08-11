# Apex Knowledge Base

This document serves as the permanent historical record for all pre-Apex and Apex research. It preserves the complete evolution of the system, capturing major discoveries, failures, and frozen primitives. 

---

## 1. Historical Timeline

### Pre-Apex Mean Reversion Research
- **Phase 1-3 (Grid Survival)**: Investigated basic grid survival. Discovered that simple filtering is insufficient against catastrophic continuation regimes. Walk-forward testing revealed major regime shifts in 2024-2026.
- **Phase 4-6 (Regime Modeling)**: Transitioned to statistical regime classification (continuation analysis, failure pressure, baseline modeling). Proven that traditional fixed-grid systems are structurally incompatible with modern volatility.
- **Phase 7-10 (Inventory & Payoff)**: Discovered that payoff architecture (R-Multiples) and inventory decay systems dramatically improved survivability over entry precision. System evolved into statistical inventory management.
- **Phase 11-13 (Robustness)**: Validated via Monte Carlo, flash-event stress testing, and parameter surface analysis.

### QuantForge Behavioral Research
- **Phase 1-5 (Signal Discovery)**: Investigated short-term panic displacement. Found that deep z-score extremes, volatility expansion, and panic momentum created an asymmetric edge.
- **Phase 6-11 (Recoil & Persistence)**: Discovered that the strongest edges exhibited immediate recoil and post-panic stabilization (persistence). Validated across multiple assets (EURUSD) and Monte Carlo testing.
- **Phase 12-13 (Execution Robustness)**: Edge survived spread friction, latency degradation, and showed strong temporal stability.

### Apex RC001: Institutional Liquidity Sweep
- **Studies 001-006**: Investigated whether price pushing beyond a structural liquidity level and rejecting predicts a directional continuation. Tested conditioning with trend regimes, post-sweep expansion, market sessions, and structural taxonomy.
- **Conclusion**: All hypotheses failed strict QA validation (directional inconsistencies, temporal instability, confidence intervals crossing zero). The base liquidity sweep was deemed too common and noisy to predict directional continuation.

### Apex RC002: Behavioral Mean Reversion
- **Studies 001-004**: Pivoted to mean reversion. Defined the Behavioral Event (3.0x ATR displacement) and validated the Behavioral Response Taxonomy (Immediate Recoil, Delayed Recoil, Volatility Absorption, Momentum Continuation).
- **Studies 005-006**: Investigated whether Spatial Context (Mean Distance) or Volatility State reduced the entropy of the Response Taxonomy. Both were rejected.
- **Study 007**: Investigated Participation State (Volume Density). Successfully discovered that low-participation environments (volume vacuums) significantly reduce behavioral entropy. Validated and frozen.
- **Studies 008-009**: Investigated Structural Context (Range Position) and Behavioral Archetypes (Momentum). Both failed to reduce entropy and were permanently rejected.

### Apex RC003: Decision Primitive Decomposition
- **Study 001**
  - **Status:** FROZEN
  - **Artifact:** Primitive Catalog
  - **Purpose:** Defines the canonical vocabulary used by the Decision Engine.
  - **Governance:** All future campaigns must reference this catalog before introducing new concepts.

### Apex RC004: Implementation Validation
- **Studies 001-004**
  - **Status:** FROZEN
  - **Purpose:** Finalized the software architecture, traceability matrix, runtime execution cycle, and module interfaces for the canonical Python Reference Engine.
  - **Governance:** The Python architecture is now constitutionally frozen. RC005 is strictly limited to faithful implementation without architectural redesign.



---

## 1.5 Research Decision Log

### Pre-Apex: Evolution to Inventory Architecture
- **Research Question**: Can robust filtering and regime awareness fully solve inventory stress and payoff asymmetry?
- **Initial Hypothesis**: Filtering entries is enough to survive production conditions.
- **Motivation**: Hybrid models showed good survivability but still suffered unacceptable inventory stress.
- **Evidence**: Pre-Apex Phase 6-9 (Production Validation & Payoff Discovery)
- **Outcome**: Fragile
- **Knowledge Gained**: Inventory management is more important than entry precision. Payoff engineering (R-Multiples) and Inventory Decay dramatically improve survivability.
- **Knowledge Removed**: The belief that entry precision alone determines grid survival.
- **Reason For Next Study**: System evolved into statistical inventory management, progressing to production realism and flash-event testing.
- **Frozen?**: Yes

### Quant Research: Behavioral Mean Reversion Discovery
- **Research Question**: Do statistically significant behavioral mean reversion patterns exist that survive volatility regime shifts?
- **Initial Hypothesis**: Deep z-score displacements combined with panic momentum during elevated volatility produce asymmetric mean reversion behavior.
- **Motivation**: Seeking alternative structural edges beyond classic indicator filtering.
- **Evidence**: QuantForge Phase 1-6 (Factor Isolation & Recoil Discovery)
- **Outcome**: Supported
- **Knowledge Gained**: Strongest edges exhibit immediate recoil and post-panic stabilization (persistence).
- **Knowledge Removed**: Not supported by archived research.
- **Reason For Next Study**: Proceeded to test if the edge survives expansion, temporal stress, and cross-market transfer.
- **Frozen?**: Yes

### RC001: Institutional Liquidity Sweeps
- **Research Question**: Do institutional liquidity sweeps predict directional continuation?
- **Initial Hypothesis**: Price pushing beyond a structural liquidity level and rejecting implies an accumulation/distribution event that predicts a directional continuation.
- **Motivation**: Not supported by archived research.
- **Evidence**: RC001 Studies 001-006.
- **Outcome**: Rejected
- **Knowledge Gained**: The base liquidity sweep is highly noisy. Aligning with trend or session fails robustness and temporal stability.
- **Knowledge Removed**: The belief that standard structural liquidity sweeps provide a tradable continuation edge.
- **Reason For Next Study**: RC001 completely failed. Focus shifted to Mean Reversion (RC002) since sweeps might be better modeled as exhaustion events rather than continuations.
- **Frozen?**: No

### RC002: Behavioral Entropy Reduction
- **Research Question**: Does a single contextual variable significantly reduce Behavioral Response entropy? Can it be executed profitably across diverse markets?
- **Initial Hypothesis**: Contextual variables explain response fragmentation, and translated execution policies can exploit this across markets.
- **Evidence**: RC002 Studies 005-013.
- **Outcome**: Partially Supported (Participation State & Gradual Expansion reduce entropy). Execution discovery supported (Absorption Entry). Universality Rejected (Instrument-specific artifact).
- **Knowledge Gained**: Low market participation reduces behavioral entropy. Waiting for price stabilization (Absorption Entry) materially improves expectancy.
- **Knowledge Removed**: The belief that strict, rigid ATR and Volume thresholds can generalize universally across asset classes without dynamic normalization.
- **Reason For Next Study**: The campaign failed Cross-Market Validation (Study 013), generating zero trades outside of EURUSD. Edge is deemed an instrument-specific artifact.
- **Frozen?**: Campaign ARCHIVED. Primitives (Response Taxonomy, Participation State, Absorption Entry) extracted.

### RC003: Decision Primitive Decomposition
- **Research Question**: How should validated knowledge be organized for future decision-engine research?
- **Outcome**: SUPPORTED
- **Knowledge Gained**: 
  - Canonical behavioral vocabulary established.
  - Signal, Decision and Execution primitives formally separated.
  - Primitive dependency graph established.
  - Future research now constrained to build upon frozen knowledge rather than rediscover it.
- **Frozen**: YES


---

## 2. Confirmed Knowledge

| Knowledge ID | Statement | Supporting Studies | Confidence | Current Status |
| :--- | :--- | :--- | :--- | :--- |
| **K001** | Filtering entries alone is insufficient to protect against modern volatility continuation regimes. | Pre-Apex Phase 1, 6 | High | Confirmed |
| **K002** | Inventory decay and R-Multiple payoff architecture provide vastly superior survivability compared to entry engineering. | Pre-Apex Phase 7, 9 | High | Confirmed |
| **K003** | Extreme short-term behavioral displacement followed by immediate recoil stabilization is a persistent cross-market phenomenon. | Quant Research Phase 6, 11 | High | Confirmed |
| **K004** | Behavioral Exhaustion Events (3.0x ATR) do not have a universal outcome; they naturally fragment into a predictable Taxonomy of responses. | RC002 Study 004 | High | Confirmed |
| **K005** | Low market participation (volume vacuums) provides structural information that reduces Behavioral Response entropy. | RC002 Study 007 | High | Confirmed |

---

## 3. Rejected Ideas

| ID | Hypothesis | Rejected by | QA Status | Reason |
| :--- | :--- | :--- | :--- | :--- |
| **R001** | Institutional Liquidity Sweeps alone predict directional continuation. | RC001 Study 001-006 | Confirmed | Too noisy; confidence intervals consistently crossed zero. |
| **R002** | Conditioning sweeps by Trend, Expansion, or Session isolates a continuation edge. | RC001 QA Studies | Confirmed | Edges were fragile, temporally unstable, or suffered directional failures. |
| **R003** | Spatial Context (Mean Distance) reduces Behavioral Response entropy. | RC002 Study 005 | Confirmed | Provided negligible information gain. |
| **R004** | Pre-event Volatility State reduces Behavioral Response entropy. | RC002 Study 006 | Confirmed | Provided negligible information gain. |
| **R005** | Structural Context (Range Position) reduces Behavioral Response entropy. | RC002 Study 008 | Confirmed | Information gain was <3% even under sensitivity perturbations. |
| **R006** | Pre-event Behavioral Archetypes (Momentum) reduce Behavioral Response entropy. | RC002 Study 009 | Confirmed | Completely orthogonal to edge; no information gain. |
| **R007** | A rigid set of static behavioral and contextual thresholds (e.g., 3.0x ATR + Vol Pct < 0.25) generalizes universally across major asset classes. | RC002 Study 013 | Confirmed | Over a 5-year sample, 4 out of 5 markets starved completely. Instrument-specific artifact. |

---

## 4. Frozen Knowledge

The following concepts have survived rigorous QA and are considered stable research primitives:
- **Regime-Aware Inventory Control**
- **R-Multiple Payoff Architecture**
- **Inventory Decay System**
- **Behavioral Event (3.0x ATR Displacement)**
- **Behavioral Response Taxonomy**
- **Participation State (Contextual Primitive)**
- **Absorption Entry (Policy C: Wait for price stabilization < 0.5 ATR)**

---

## 5. Open Questions

- Can Behavioral Events and Participation vacuums be dynamically normalized per asset to discover equivalent panics in diverse markets?
- Does the isolated EURUSD edge survive transaction costs, slippage, and Monte Carlo stress in a live simulation environment?
- Can adaptive inventory management algorithms be successfully integrated with the Behavioral Response Taxonomy?

---

## 6. Research Lessons

- **Filtering alone does not create an edge.** Inventory management and payoff engineering mathematically dominate entry precision.
- **The market regime must be modeled.** Traditional grid systems are structurally incompatible with modern volatility expansions.
- **Liquidity sweeps are too common.** The standard institutional sweep is heavily noisy and ineffective as a standalone continuation signal.
- **Behavioral responses fragment.** A single massive exhaustion event does not guarantee a single type of recoil; the taxonomy of outcomes must be respected.
- **Participation carries information.** Neither structural position, distance to the mean, nor volatility state explain behavioral fragmentation—but the volume participation density does.

---

## 7. Duplicate Prevention

| Campaign | Study | Topic | Final Verdict | QA Status |
| :--- | :--- | :--- | :--- | :--- |
| RC001 | 001 | Base Liquidity Sweep Continuation | Inconclusive | N/A |
| RC001 | 002 | Liquidity Sweep + Trend Regime | Candidate | Rejected (Fragile) |
| RC001 | 004 | Liquidity Sweep + Post-Sweep Expansion | Rejected | N/A |
| RC001 | 005 | Liquidity Sweep + Market Session | Candidate | Rejected (Fragile) |
| RC001 | 006 | Liquidity Sweep Rejection Taxonomy | Rejected | N/A |
| RC002 | 001 | Behavioral Event Definition | Supported | Confirmed |
| RC002 | 002 | Behavioral Recoil | Not Supported | N/A |
| RC002 | 003 | Cross-Market Reproducibility | Partially Supported | N/A |
| RC002 | 004 | Behavioral Response Classification | Supported | Confirmed |
| RC002 | 005 | Entropy Reduction (Spatial Context) | Rejected | Confirmed |
| RC002 | 006 | Entropy Reduction (Volatility State) | Rejected | Confirmed |
| RC002 | 007 | Entropy Reduction (Participation State)| Supported | Confirmed (Frozen) |
| RC002 | 008 | Entropy Reduction (Structural Context)| Rejected | Confirmed |
| RC002 | 009 | Behavioral Archetype Discovery | Rejected | Confirmed |
| RC002 | 010 | Path Dependency (Gradual Expansion) | Supported | N/A |
| RC002 | 011 | Contextual Interaction | Supported | N/A |
| RC002 | 012 | Execution Policy Evaluation | Supported (Absorption Entry) | N/A |
| RC002 | 013 | Cross-Market Execution Robustness | Rejected | Confirmed (Campaign Archived) |

---

## 8. Governance

### Primitive Governance Rule

Before any future study is approved, it must answer:

- Does this study use an existing frozen primitive?
- If introducing a new primitive:
  - Why can the existing primitives not explain the phenomenon?
  - Does this primitive duplicate an existing concept?

If duplication exists:

The study must be rejected before implementation.


## 9. Development Pipeline

The permanent development pipeline for Apex transitions sequentially through the following phases. No phase may be skipped.

1. **Research** (Completed via RC001 - RC002)
2. **Architecture** (Completed via RC003 - RC004)
3. **Python Reference Engine** (Canonical behavioral specification)
4. **Historical Validation** (Independent testing on historical datasets)
5. **Forward Validation (MT5)** (Live execution via MetaTrader5 API)
6. **Production Freeze** 
7. **MQL5 Translation** (Literal translation of the frozen Python engine)
8. **Deployment**
