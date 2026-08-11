# APEX Quant Research Framework

> **Adaptive Probabilistic Execution Framework**
>
> *Research First. Statistics First. Execution Second.*

---

# Overview

APEX is a modular quantitative research framework for studying financial market behaviour and developing statistically robust execution models.

The framework has now reached a stable milestone. Doctor checks are healthy, the feature registry is complete, the feature pipeline is operational, duplicate feature names are not present, and the architecture is stable enough to support disciplined structural improvements.

The project remains focused on the same core objectives:

- Research-driven analysis
- Data-centric experimentation
- Modular architecture
- Reproducible datasets
- Broker-independent research logic
- Machine learning readiness
- MT5 deployment readiness

---

# Current Operational Status

**Completed**
- Simulation Core
- Research Layer
- Presentation Layer
- Deployment Layer
  - Data Loader

**Current Sprint:**
- Sprint 13: Data Exporter

These conditions define the project’s current state. New work should strictly consume the frozen APIs and improve structure, documentation, and reporting rather than redesign the framework.

---

# Project Goals

The primary objective of APEX is not to build another trading robot.

The objective is to answer a more important question:

> **What characteristics of the market consistently lead to profitable execution?**

Once those characteristics are understood, strategy development becomes an engineering task rather than guesswork.

---

# Core Philosophy

APEX follows several guiding principles:

- Data before opinion
- Statistics before optimization
- Simplicity before complexity
- Research before implementation
- Evidence before intuition
- One module, one responsibility
- Preserve stability unless evidence justifies change

---

# Architecture

```
Raw Market Data
        │
        ▼
Loader
        │
        ▼
Preprocessing
        │
        ▼
Feature Engineering
        │
        ▼
Label Generation
        │
        ▼
Master Dataset
        │
        ▼
Research Engine
        │
        ▼
Simulator
        │
        ▼
Machine Learning
        │
        ▼
MT5 Live Execution
```

---

# Project Structure

```
apex/

config/
data/
features/
labels/
regimes/
simulator/
analytics/
ml/
mt5/
experiments/
datasets/
reports/
docs/
```

Each folder has a single responsibility and should remain independent wherever possible.

---

# Development Workflow

Every development session follows the same process.

```
Run Project Doctor

↓

Review Current Status

↓

Inspect Structural Risks

↓

Implement Only If Necessary

↓

Validate

↓

Document

↓

Commit
```

This workflow preserves the current architecture and avoids unnecessary churn.

---

# Research Workflow

Every research experiment follows the same lifecycle.

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
```

If a hypothesis cannot be validated statistically, it does not become part of APEX.

---

# Dataset Pipeline

```
Raw M1 Data

↓

Cleaning and Standardisation

↓

Feature Engineering

↓

Label Generation

↓

Master Dataset

↓

Research and ML Workflows
```

The Master Dataset is now treated as the primary source of truth for research and machine learning experiments.

---

# Module Categories

## Data

Responsible for loading, validating, preprocessing, and assembling datasets.

---

## Features

Describe the current market state.

Examples:

- Price
- Trend
- Volatility
- Momentum
- Market Structure
- Smart Money
- Regime
- Session

---

## Labels

Describe future outcomes.

Examples:

- Future Returns
- Grid Survival
- Execution Quality
- Basket Success

Features must never use future information.

---

# Documentation

The current documentation set is maintained alongside the codebase.

Relevant references:

- [CHARTER.md](CHARTER.md)
- [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md)
- [CODING_STANDARDS.md](CODING_STANDARDS.md)
- [MODULE_INDEX.md](MODULE_INDEX.md)
- [RESEARCH_INDEX.md](RESEARCH_INDEX.md)
- [DECISIONS.md](DECISIONS.md)
- [CHANGELOG.md](CHANGELOG.md)
- [ROADMAP.md](ROADMAP.md)

---

## Regimes

Classify the market into statistically meaningful behavioural states.

Examples:

- Baseline
- Continuation
- Persistence
- Transition
- Adaptive Inventory
- Classifier

---

## Simulator

Tests execution models under realistic trading conditions.

Examples:

- Basket Engine
- Execution Engine
- Inventory Engine
- Monte Carlo
- Flash Events

---

## Machine Learning

Consumes the Master Dataset to train predictive models for execution and risk management.

---

## MT5

Deploys validated research into a live trading environment.

---

# Documentation

The project documentation is located in:

```
docs/
```

Important documents include:

- README.md
- DESIGN_PRINCIPLES.md
- CODING_STANDARDS.md
- DECISIONS.md
- RESEARCH_INDEX.md
- ROADMAP.md
- CHANGELOG.md

These documents should always be kept up to date.

---

# Versioning

Every completed module contains:

- Module Name
- Version Number
- Description
- Revision History

Major architectural changes should also be recorded in:

```
docs/CHANGELOG.md
```

---

# Current Development Phase

At the time of writing, APEX is focused on building the foundational research framework, including:

- Modular feature engineering
- Dataset generation
- Regime classification
- Research engine
- Simulation engine

Machine Learning and MT5 deployment will be built on top of this foundation.

---

# Long-Term Vision

The long-term goal of APEX is to become a complete quantitative research platform capable of:

- Multi-asset analysis
- Market regime classification
- Inventory-aware execution
- Statistical strategy validation
- Machine learning prediction
- Live MT5 execution
- Continuous research and experimentation

---

# Guiding Principle

> **"Research builds understanding. Understanding builds confidence. Confidence builds execution."**

APEX exists to transform market research into statistically validated execution models through disciplined engineering, reproducible experimentation, and continuous learning.