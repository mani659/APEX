# APEX Quant Research Framework

# Research State

> **A definitive summary of the current research position within APEX.**

---

## 1. ORIGINAL RESEARCH GOAL

**What problem is APEX trying to solve?**

The objective of APEX is not to build a single trading bot. 

The primary scientific objective is to answer the fundamental question:
**"What characteristics of the market consistently lead to profitable execution?"**

APEX exists to understand markets before attempting to trade them. The goal is to build a statistically validated quantitative research framework that transforms market data into reliable execution models through disciplined engineering, reproducible experimentation, and evidence-based decision making. We aim to discover measurable statistical edges rather than relying on intuition or curve-fitting.

---

## 2. CURRENT STATUS

The APEX framework has successfully completed its foundational engineering phase and transitioned into active research. 

**Data Layer:** COMPLETE and STABLE. 
The system reliably loads broker CSV files, validates schemas, and standardizes data.

**Feature Layer:** COMPLETE and STABLE.
The feature engine pipeline is operational with a dynamic registry. Active feature families include Price, Volume, Volatility, Trend, Momentum, Structure, Smart Money, Regime, and Session. Features strictly describe the present, ensuring no forward-looking data leakage.

**Label Layer:** COMPLETE and STABLE.
Supervised learning targets are successfully generated, including Future Returns, Grid Labels, Survival Labels, and Execution Labels.

**Dataset Builder:** COMPLETE and STABLE.
Features and labels are deterministically merged into the immutable Master Dataset (Parquet format), acting as the single source of truth for all downstream analytics and ML tasks.

**Doctor Framework:** COMPLETE and HEALTHY.
A continuous integrity verification script (`apex_doctor.py`) strictly enforces project structure and engineering quality.

**Analytics Layer:** ACTIVE.
A robust suite of read-only analytics modules (`regime_analysis.py`, `correlation_analysis.py`, `stability_analysis.py`, `hypothesis_discovery.py`) now runs against the Master Dataset to summarize statistics, evaluate stability, and extract preliminary evidence.

**Production Readiness:**
The foundational data pipelines, feature extractors, and dataset architecture are fully production-ready for research consumption. Machine Learning and Simulation execution engines remain planned.

---

## 3. WHAT WE NOW KNOW

Through historical experiments and the initial analytics modules, we have accumulated the following measurable knowledge:

- **Continuation:** Markets exhibit statistically significant continuation after directional movement. Continuation is now treated as a primary regime metric.
- **Persistence:** Directional persistence remains remarkably stable over rolling windows and across multiple years, despite shifting volatility regimes.
- **Transition Stress:** Large drawdowns and execution failures frequently occur during regime transitions rather than during stable trends. 
- **Inventory Management:** Adaptive inventory suppression significantly reduces drawdown while maintaining profitable execution, proving that inventory must be treated as a market state variable.
- **Measurability:** We can now statistically measure feature redundancy, correlation, distributional stability, and regime-based performance directly against outcome labels. 

---

## 4. WHAT WE STILL DO NOT KNOW

The following major research questions remain unanswered and form the core of upcoming experiments:

- **The Grind Regime:** How do we accurately define and detect a "grind" regime (prolonged directional movement with limited reversion) without false positives?
- **Liquidity Sweeps:** Do liquidity sweeps and smart money structure features truly improve mathematical expectancy?
- **Volatility Regimes:** Which volatility regime (expansion, compression, cluster) produces the most robust expectancy?
- **Reversal vs. Continuation:** Under what precise feature states do continuation setups statistically outperform mean-reversion setups?
- **Survival Dynamics:** How long should a position survive based on the entry regime before time-based decay destroys the edge?
- **Label Predictive Power:** Which of the generated labels (Future Returns vs. Grid Labels vs. Survival Labels) contains the strongest predictive power for machine learning models?
- **Failure States:** What exact combination of market conditions mathematically guarantees execution failure?
- **Session Execution:** Does the active trading session significantly influence execution quality?

---

## 5. RESEARCH ROADMAP

The next phases focus strictly on research and statistical validation before advancing to Machine Learning.

**Phase 1: Regime Discovery (Next Active Sprint)**
Classify the market into statistically distinct states (Baseline, Continuation, Persistence, Transition, Adaptive Inventory, Classifier).

**Phase 2: Hypothesis Testing and Analytics Deep-Dive**
Extract statistical knowledge and validate feature importance using the Master Dataset (Ablation studies, Feature comparisons, Parameter sweeps).

**Phase 3: Execution Simulation**
Evaluate trading behavior under realistic conditions (Spread, slippage, flash events, Monte Carlo robustness) using a Market Simulator.

**Phase 4: Machine Learning**
Train predictive models (XGBoost, Random Forest, etc.) using validated datasets.

**Phase 5: MT5 Live Deployment**
Convert validated research into a production Expert Advisor.

---

## 6. SUCCESS CRITERIA

Research is considered complete when:
**"We have statistically demonstrated an edge."**

This is defined by the following measurable criteria:
- A stable, reusable Master Dataset is verified without future leakage.
- The Research Engine outputs reproducible statistical evidence proving the hypothesis.
- The Simulator validates the strategy's profitability under realistic execution costs (spread/slippage).
- The Machine Learning pipeline generates predictive models with measurable out-of-sample robustness.
- Live MT5 execution matches simulated expectations.

---

## 7. RESEARCH PRINCIPLES

These guiding philosophies govern every decision within APEX:

- **Evidence over intuition.** Opinions never override measurable statistics.
- **Research before engineering.** We do not build for hypothetical requirements.
- **No data leakage.** Features describe the present; labels describe the future.
- **No curve fitting.** Optimization never replaces research.
- **Robustness beats peak performance.** Simple, well-tested models are preferable to complex, overfitted systems.
- **Walk-forward before optimization.**
- **Every strategy must be statistically justified.** If a hypothesis cannot be validated statistically, it does not become part of APEX.

---

## 8. CURRENT POSITION

**If a new researcher joined tomorrow, where exactly are we today?**

We have finished building the laboratory and are now running the experiments. 

The APEX framework is fully operational up to the dataset generation and exploratory analytics stages. The data ingestion, feature engineering, and labeling pipelines are robust, strictly modular, and actively outputting a pristine Master Dataset. We have a robust Doctor to ensure engineering health and a set of Analytics V2 modules extracting hypotheses and stability metrics from the data. 

Our immediate focus is purely scientific: discovering statistically significant regimes, testing market hypotheses against our labels, and measuring statistical edges before writing a single line of simulation or machine learning code.

## 9. Research Philosophy Evolution

Earlier versions of the project focused on designing profitable Expert Advisors directly. Through extensive experimentation, we concluded that strategy engineering without understanding market structure leads to curve-fitting and unstable performance. APEX therefore evolved into a market research framework whose first objective is to discover statistically robust market behavior. Trading systems are now considered outputs of research rather than starting points.
