# APEX Engineering Decisions

> **A permanent record of important architectural and engineering decisions.**

---

# Purpose

This document records significant engineering decisions made throughout the life of APEX.

It answers:

- Why was this decision made?
- What alternatives were considered?
- What problem does it solve?
- What impact does it have?

The goal is to preserve engineering knowledge and prevent repeating the same discussions months or years later.

---

# Decision 001

## Date

2026-07

## Title

Research First Architecture

## Decision

APEX will be built as a quantitative research framework rather than a traditional trading system.

## Reason

Most trading systems optimize strategies before understanding market behaviour.

APEX reverses this process.

Research comes first.

Execution comes second.

## Impact

Every module supports research before live trading.

---

# Decision 002

## Date

2026-07

## Title

Modular Architecture

## Decision

Split every major responsibility into independent modules.

## Reason

Large files become difficult to test and maintain.

Smaller modules are easier to improve independently.

## Impact

The framework becomes easier to extend and debug.

---

# Decision 003

## Date

2026-07

## Title

One Responsibility Per Module

## Decision

Each Python file should solve one problem.

## Reason

Single-purpose modules reduce complexity and improve readability.

## Impact

Future maintenance becomes significantly easier.

---

# Decision 004

## Date

2026-07

## Title

Separate Features From Labels

## Decision

Features and labels must live in separate modules.

## Reason

Features describe the present.

Labels describe the future.

Mixing them introduces data leakage.

## Impact

Machine learning experiments remain statistically valid.

---

# Decision 005

## Date

2026-07

## Title

Dataset Builder Belongs In Data Layer

## Decision

dataset_builder.py remains inside the data package.

## Reason

Dataset creation is data engineering.

It is not machine learning.

## Impact

Cleaner architecture.

Simpler dependencies.

---

# Decision 006

## Date

2026-07

## Title

Feature Registry

## Decision

Every feature module is registered through registry.py.

## Reason

Allows automatic feature discovery.

Avoids hard-coded feature lists.

Simplifies future expansion.

---

# Decision 007

## Date

2026-07

## Title

Master Dataset

## Decision

All experiments use the master dataset.

## Reason

One trusted source of truth.

Avoids duplicated preprocessing.

Improves reproducibility.

---

# Decision 008

## Date

2026-07

## Title

No Over Engineering

## Decision

Only introduce complexity after research proves it is valuable.

## Reason

Premature optimization creates technical debt.

Simple systems are easier to understand and validate.

## Impact

Development remains focused on measurable improvements.

---

# Decision 009

## Date

2026-07

## Title

Separate Research From Production

## Decision

Research code never goes directly into MT5.

## Reason

Research explores ideas.

Production requires stability.

## Impact

Every live component is backed by validated research.

---

# Decision 010

## Date

2026-07

## Title

Project Documentation

## Decision

Documentation is treated as part of the codebase.

## Reason

Engineering knowledge is valuable.

Code alone does not explain design choices.

## Impact

Future contributors can understand the project without relying on memory.

---

# Decision 011

## Date

2026-07

## Title

Layered Dependency Architecture

## Decision

Modules may only depend on lower layers.

Example

config

↓

data

↓

features

↓

labels

↓

regimes

↓

simulator

↓

analytics

↓

ml

↓

mt5

## Reason

Avoid circular dependencies.

Keep modules reusable.

Improve maintainability.

---

# Decision 012

## Date

2026-07

## Title

Every Session Starts With Diagnostics

## Decision

Every development session begins with:

1. apex_doctor.py
2. development_status.py

## Reason

Know the project state before writing code.

Avoid duplicate work.

Maintain consistency.

---

# Decision 013

## Date

2026-07

## Title

Feature Modules Remain Independent

## Decision

Every feature module should be independently testable.

## Reason

Features evolve continuously.

Independent modules simplify experimentation.

---

# Decision 014

## Date

2026-07

## Title

Scientific Workflow

## Decision

Every hypothesis follows:

Question

↓

Dataset

↓

Experiment

↓

Validation

↓

Conclusion

↓

Implementation

## Reason

Maintain scientific discipline.

Prevent intuition-driven development.

---

# Decision 015

## Date

2026-07

## Title

Stable Milestone And Structural Hardening

## Decision

The framework should now prioritise structural hardening, schema consistency, and documentation accuracy over redesign.

## Reason

The project has reached a stable milestone and the current objective is to preserve that stability while improving maintainability.

## Impact

Future changes should be incremental and evidence-based.

---

# Decision 016

## Date

2026-08

## Title

Archival of Research Campaign RC002

## Decision

RC002 (Behavioral Mean Reversion) is formally archived. Its core components (Behavioral Response Taxonomy, Participation State context, Absorption Entry policy) are extracted as frozen primitives, but the unified trading strategy built upon them is discarded.

## Reason

Study 013 (Cross-Market Execution Robustness) demonstrated that the exact fixed thresholds (3.0 ATR + Volume Percentile < 0.25) required to capture the "Low Participation + Sudden Shock" edge generated zero trades on four out of five major asset classes (XAUUSD, XAGUSD, BTCUSD, NAS100). The edge is a highly profitable but strictly instrument-specific artifact tied to EURUSD microstructure.

## Impact

APEX will not deploy the RC002 strategy live. Future campaigns will focus on dynamic threshold normalization to ensure behavioral events scale proportionately across different asset classes, rather than relying on absolute rigid parameters.


---

## Decision 017

### Date

2026-08

### Title

Production Implementation in Python

### Decision

Apex Version 1 will not be implemented directly in MQL5. The primary implementation language is Python, connected to the MT5 terminal through the MetaTrader5 Python API.

### Reason

The objective of Apex is scientific iteration, not platform-specific development. Python provides rapid experimentation, deterministic replay, easier debugging, reproducible research, superior testing infrastructure, seamless historical backtesting, and direct integration with scientific libraries. 

### Impact

All research, validation, debugging, replay testing, optimization, and production verification will occur inside the Python execution engine. MQL5 is treated strictly as a deployment language. The Python engine is the canonical reference implementation, and the future MQL5 version must become a literal translation of it.

---

# Decision Template

Use this template for future decisions.

---

## Decision XXX

### Date

YYYY-MM-DD

### Title

Short descriptive title

### Decision

What was decided?

### Reason

Why was it chosen?

### Alternatives Considered

(Optional)

### Impact

How does it affect the framework?

### Notes

(Optional)

---

# Final Principle

Never modify historical decisions.

If a decision changes,

create a new decision explaining why the previous one was replaced.

Engineering history should remain traceable.