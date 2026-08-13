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

### Apex RC007: De-conflation of Entry and Exit Alpha
- **Studies 001-010**: Investigated whether the Apex behavioural entry signal possesses statistically significant alpha independent of grid-based recovery mechanics.
- **Conclusion**: The hypothesis was totally rejected. De-conflation proved the signal possesses negative expectancy. The grid recovery never triggered under frozen rules (max depth 1). The historical profitability is entirely a statistical illusion created by an asymmetric exit architecture harvesting tiny wins while hiding massive, negatively-skewed tail risks.

### Apex RC008: Conditional Market Context Research
- **Studies 001-002**: Investigated whether the rejected V1 Behavioral Event could be rescued by filtering it using standard market context (Volatility, Trend, Liquidity, Pre-event Path, Temporal).
- **Conclusion**: The V1 Context-Rescue path is permanently closed. No context category produced a meaningful effect size. The negative alpha of the V1 event is unconditional.



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

### RC007: Apex V1 Alpha Validation
- **Research Question**: Does the Apex behavioural entry signal possess statistically significant alpha independent of grid-based recovery mechanics?
- **Evidence**: RC007 Studies 007-009 (Dual and Triple Mode De-conflation).
- **Outcome**: Rejected
- **Knowledge Gained**: High historical win rates were a statistical illusion created by asymmetric payoffs. Grid recovery was a phantom component that never fired. The underlying signal possesses negative predictive edge.
- **Knowledge Removed**: The belief that the frozen V1 rules contained validated standalone alpha.
- **Reason For Next Study**: The campaign was closed. The next research campaign must start from the empirical fact that the V1 formulation is rejected.
- **Frozen?**: Campaign CLOSED - HYPOTHESIS REJECTED.

### RC008: V1 Context-Rescue Investigation
- **Research Question**: Are there measurable market-context conditions under which the V1 behavioural event's subsequent outcome distribution becomes materially better than its unconditional baseline?
- **Evidence**: RC008 Study 001 (Context Dataset extraction & Comparison Report).
- **Outcome**: Rejected (Not Supported)
- **Knowledge Gained**: Standard volatility, trend, liquidity, path, and temporal contexts fail to extract conditional edge from the V1 event. The event's negative expectancy is unconditional.
- **Knowledge Removed**: The belief that the V1 event could be rescued by adding conventional filters.
- **Reason For Next Study**: The V1 rescue path is closed. Future research must search for a genuinely different behavioral formulation.
- **Frozen?**: Campaign CLOSED - NOT SUPPORTED.

### RC009: Behavioral Discovery Campaign
- **Research Question**: Does isolated EURUSD M1 behavior possess structural predictability via local sequences, participation behaviors, cross-market synchronization, or higher-timeframe regime conditioning?
- **Evidence**: RC009 Studies 001-006.
- **Outcome**: Rejected (Negative Discovery Campaign)
- **Knowledge Gained**: The tested RC009 behavioral formulations did not demonstrate robust predictive alpha on EURUSD M1.
- **Knowledge Removed**: The belief that basic local M1 patterns, M1 state sequences, contemporaneous cross-market state synchronization, or H4 regime conditioning contain robust, scalable predictive edge on EURUSD M1.
- **Reason For Next Study**: The behavioral discovery campaign is permanently closed.
- **Frozen?**: Campaign CLOSED - FROZEN NEGATIVE.

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
| **R008** | The frozen Apex Version 1 behavioral entry provides a standalone positive expectancy edge. | RC007 Study 007, 009 | Confirmed | Standalone entry expectancy is negative and win rate is low (35.1%). |
| **R009** | The historical profitability of V1 is driven by adaptive grid expansion recovering losers. | RC007 Study 008 | Confirmed | Grid expansion never triggers under the frozen rules (max depth 1). |
| **R010** | A high win rate generated by asymmetric payoff structures implies a viable trading edge. | RC007 Study 009 | Confirmed | Masks extreme negatively-skewed tail risk (worst 5% holds 88% of loss footprint); guarantees ruin under infinite time. |
| **R011** | Standard Volatility Context (ATR percentiles) rescues the V1 event. | RC008 Study 001 | Confirmed | Effect size too weak (Cohen's d = 0.12). |
| **R012** | Standard Trend Context (Distance to Mean, Return Slope) rescues the V1 event. | RC008 Study 001 | Confirmed | Effect sizes too weak (Cohen's d < 0.15). |
| **R013** | Standard Liquidity/Temporal/Path contexts rescue the V1 event. | RC008 Study 001 | Confirmed | Effect sizes too weak (Cohen's d < 0.15). |
| **R014** | Local M1 behavioral patterns (momentum, absorption, flag) predict directional returns. | RC009 Study 001 | Confirmed | Effect sizes near zero with massive statistical power. |
| **R015** | M1 state sequences (N=3, N=5) add meaningful information beyond the terminal state. | RC009 Study 003 | Confirmed | Sequences converged back to terminal state baselines. |
| **R016** | Cross-market synchronization (XAUUSD, BTCUSD, etc.) provides incremental M1 edge. | RC009 Study 004 | Confirmed | No contemporaneous or short-lag relationships met criteria. |
| **R017** | H4 volatility/direction regimes materially alter expected M1 state outcomes. | RC009 Study 006 | Confirmed | H4 regime provided no meaningful incremental structure. |
| **R018** | Deterministic session transitions (e.g. ASIA_TO_LONDON, LONDON_NY_OVERLAP) materially alter EURUSD future movement distributions independent of prediction. | RC013 Study 001, 002 | Confirmed | Validated structural primitives, survived chronological OOS. |
| **R019** | Session expansion exhibits higher movement with directionally efficient path geometry relative to the HIGH_VOL chop regime. | RC013 Study 003 | Confirmed | Classified as TYPE A Directionally Efficient Expansion. |
| **R020** | The raw immediate pre-session-range breakout architecture generates positive expectancy. | RC013 Study 004 | Rejected | Architecture produced negative expectancy and severe tail-losses. |
| **R021** | Transaction-cost reduction alone rescues the raw breakout architecture. | RC013 Study 004 | Rejected | Expectancy remained negative even at 0.5 pip transaction costs. |

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
- **A strong-looking win rate can be manufactured by payoff asymmetry.**
- **Entry quality must be measured independently of recovery and exits.**
- **A grid that never activates cannot be credited for historical profitability.**
- **MAE/MFE distribution is more informative than win rate alone.**
- **Negative results are valuable because they eliminate false explanations.**
- **Apex must not mistake a successful payoff distribution for predictive alpha.**
- **A fundamentally negative-expectancy event cannot be rescued purely by conventional context filtering.**

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
| RC007 | 007 | Isolated Entry Expectancy | Rejected | Confirmed |
| RC007 | 008 | Recovery Architecture De-conflation | Rejected (No Grid Expansion) | Confirmed |
| RC007 | 009 | Exit Architecture De-conflation | High-Win-Rate Illusion | Confirmed |
| RC007 | 010 | Campaign Closure | Hypothesis Rejected | Confirmed (Campaign Closed) |
| RC008 | 001 | Conditional Context Exploration | Rejected (No Evidence) | Confirmed |
| RC008 | 002 | V1 Context-Rescue Closure | Path Closed | Confirmed |
| RC009 | 001 | Local Behavioral Discovery | Rejected | Confirmed |
| RC009 | 003 | State Sequences | Rejected | Confirmed |
| RC009 | 004 | Cross-Market Synchronization | Rejected | Confirmed |
| RC009 | 005 | Discovery Review & Closure Assessment | Supported (Decision to close) | Confirmed |
| RC009 | 006 | H4 Regime Conditioning | Rejected | Confirmed (Campaign Closed) |
| RC013 | 001 | Session / Calendar Structural Mechanics Discovery | Candidate Structural Edge | Confirmed |
| RC013 | 002 | Independent Validation | Validated Structural Primitive | Confirmed |
| RC013 | 003 | Session Transition Path Geometry | TYPE A Directionally Efficient | Confirmed |
| RC013 | 004 | Session Transition Breakout Monetization | Architecture Rejected | Confirmed (Campaign Closed) |

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
