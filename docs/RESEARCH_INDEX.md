# APEX Quant Research Framework

# Research Index

> **A permanent record of every research topic, experiment, discovery, and conclusion made during the development of APEX.**

---

# Purpose

The purpose of this document is to preserve research knowledge.

Unlike ROADMAP.md, this document does not track development progress.

Instead, it records:

- Research questions
- Hypotheses
- Experiments
- Results
- Conclusions
- Future research

This document should grow throughout the life of the project.

---

# Current Research Status

The framework has reached a stable milestone. The core research pipeline is operational, and the record below reflects both completed work and the next areas of structural refinement.

---

# Research Philosophy

APEX follows a research-first methodology.

Every feature inside the framework must originate from statistical research rather than intuition.

Every experiment should answer one specific question.

Research must always be reproducible.

---

# Research Lifecycle

Every research topic follows the same lifecycle.

```
Question

↓

Hypothesis

↓

Dataset

↓

Experiment

↓

Statistical Validation

↓

Conclusion

↓

Implementation

↓

Production
```

No research should skip any stage.

---

# Completed Research

---

# R001

## Title

Continuation Behaviour

## Objective

Determine whether markets exhibit statistically significant continuation after directional movement.

## Metrics

- Continuation Probability
- Expansion
- Continuation Length
- Continuation Strength

## Result

Positive.

Continuation exists and became one of the primary regime metrics.

## Status

Implemented

---

# R002

## Title

Persistence Analysis

## Objective

Measure directional persistence over rolling windows.

## Metrics

- Persistence
- Oscillation
- Drift Strength
- Reversion Efficiency

## Findings

Persistence remained remarkably stable across multiple years despite changing volatility regimes.

## Status

Implemented

---

# R003

## Title

Grind Regime Detection

## Objective

Detect prolonged directional movement with limited reversion.

## Findings

Current definition produced zero grind regimes.

Conclusion:

Definition requires revision.

## Status

Needs Further Research

---

# R004

## Title

Transition Stress Analysis

## Objective

Measure execution quality during regime transitions.

## Findings

Large drawdowns frequently occurred during transitions rather than stable trends.

## Conclusion

Transition detection should become part of the regime engine.

## Status

Implemented

---

# R005

## Title

Adaptive Inventory Control

## Objective

Reduce drawdown through inventory-aware suppression.

## Findings

Adaptive suppression significantly reduced drawdown while maintaining profitable execution.

Inventory should be treated as a market state variable.

## Status

Implemented

---

# R006

## Title

Execution Realism

## Objective

Introduce realistic spread, slippage, and execution assumptions.

## Findings

Strategies remained profitable under realistic execution costs.

## Status

Completed

---

# R007

## Title

Monte Carlo Robustness

## Objective

Measure robustness under randomized execution conditions.

## Findings

Framework demonstrated resilience across randomized simulations.

## Status

Completed

---

# R008

## Title

Master Dataset Architecture

## Objective

Create a reusable dataset for research and machine learning.

## Components

- Loader
- Validation
- Preprocessing
- Features
- Labels
- Dataset Builder

## Status

Completed

---

# Current Research

---

## Dataset Pipeline

Current focus.

Objective

Produce a high-quality Master Dataset for all future research.

Current Stage

Feature Engineering

---

# Future Research

---

## Multi-Timeframe Features

Status

Planned

---

## Cross-Market Correlation

Status

Planned

---

## Market Microstructure

Status

Planned

---

## Liquidity Dynamics

Status

Planned

---

## Order Flow Approximation

Status

Planned

---

## Volatility Clustering

Status

Planned

---

## Dynamic Position Sizing

Status

Planned

---

## Execution Quality Prediction

Status

Planned

---

## Reinforcement Learning

Status

Future

---

## Portfolio Optimisation

Status

Future

---

# Research Datasets

Primary datasets currently available:

- XAUUSD
- XAGUSD
- BTCUSD
- EURUSD
- NAS100

Resolution

M1

Historical Coverage

Approximately five years.

The Master Dataset will become the primary source for all future research.

---

# Research Principles

Every experiment must satisfy the following:

- Reproducible
- Versioned
- Independent
- Statistically validated
- Properly documented

Research without documentation is considered incomplete.

---

# Lessons Learned

Throughout the development of APEX several important lessons have emerged.

## Lesson 1

Market behaviour is more important than indicator combinations.

---

## Lesson 2

Inventory management contributes more to long-term survival than entry precision alone.

---

## Lesson 3

Market regimes explain execution quality better than individual indicators.

---

## Lesson 4

Adaptive systems consistently outperform static parameter sets.

---

## Lesson 5

Research must precede optimisation.

Optimising an incorrect hypothesis only produces misleading results.

---

## Lesson 6

Simple, well-tested models are preferable to highly complex systems without statistical justification.

---

# Research Milestones

✓ Continuation research

✓ Persistence research

✓ Transition research

✓ Adaptive inventory research

✓ Simulation framework

✓ Master dataset

⬜ Regime classifier

⬜ Machine learning

⬜ MT5 live deployment

---

# Research Backlog

Potential future investigations include:

- Dynamic volatility regimes
- Session-specific execution behaviour
- Multi-symbol synchronisation
- Cross-asset regime transfer
- Feature importance ranking
- Bayesian parameter estimation
- Probabilistic stop-loss placement
- Adaptive basket management
- Regime confidence scoring
- Online learning

---

# Final Statement

Research is the foundation of APEX.

Every module, experiment, model, and execution engine should originate from validated statistical evidence rather than assumptions.

The quality of future trading systems will depend directly on the quality of the research preserved in this document.