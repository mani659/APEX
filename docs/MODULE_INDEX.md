# APEX Module Index

> Complete reference of every module within the APEX Quant Research Framework.

---

# Purpose

This document explains the purpose, inputs, outputs, and dependencies of every module.

Unlike the folder structure, this document explains what each module actually does.

Unlike development_status.py, this document is maintained manually.

---

# Current Status Summary

The framework has now reached a stable milestone. The core data, feature, label, and dataset layers are operational, and the documentation below reflects that current state.

---

# Layer Overview

```
Configuration
      │
      ▼
Data Loading
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
Dataset Builder
      │
      ▼
Regime Engine
      │
      ▼
Simulator
      │
      ▼
Analytics
      │
      ▼
Machine Learning
      │
      ▼
MT5 Deployment
```

---

# CONFIG

---

## settings.py

Purpose

Global configuration and filesystem paths.

Inputs

None.

Outputs

Configuration values and project paths.

Dependencies

constants.py

Status

Stable

---

## constants.py

Purpose

Framework-wide constants for data columns, windows, and labels.

Status

Stable

---

## experiment_profiles.py

Purpose

Stores reusable experiment configurations.

Status

Planned

---

# DATA

---

## loader.py

Purpose

Load and standardise market data from broker CSV files.

Input

CSV files.

Output

Standardised DataFrame.

Status

Stable

---

## validator.py

Purpose

Validate datasets and input quality.

Checks

- Missing values
- Duplicates
- Time ordering
- Data quality

Status

Stable

---

## preprocessing.py

Purpose

Clean and standardise market data before feature generation.

Status

Stable

---

## feature_builder.py

Purpose

Assemble all registered feature modules into a single feature dataset.

Status

Stable

---

## dataset_builder.py

Purpose

Create the Master Dataset from raw data, features, and labels.

Status

Stable

---

# LABELS

---

## labels.py

Purpose

Master label interface.

Status

Stable

---

## future_returns.py

Purpose

Generate future return labels.

Status

Stable

---

## grid_labels.py

Purpose

Generate grid and future-range outcome labels.

Status

Stable

---

## survival_labels.py

Purpose

Estimate survival and adverse excursion labels.

Status

Stable

---

## execution_labels.py

Purpose

Create execution-quality labels.

Status

Stable

---

# FEATURES

---

## helpers.py

Shared feature utilities.

Status

Stable

---

## registry.py

Registers every feature module and exposes the feature builder mapping.

Status

Stable

---

## price.py

Price-based features.

Status

Stable

---

## volume.py

Volume features.

Status

Stable

---

## session.py

Trading session features.

Status

Stable

---

## volatility.py

ATR and volatility metrics.

Status

Stable

---

## trend.py

Trend features.

Status

Stable

---

## momentum.py

Momentum features.

Status

Stable

---

## structure.py

Market structure features.

Status

Stable

---

## smart_money.py

Liquidity and Smart Money concepts.

Status

Stable

---

## regime.py

Market regime features.

Status

Stable

---

# REGIMES

Baseline

Continuation

Persistence

Transition

Adaptive Inventory

Classifier

Purpose

Convert raw features into statistically meaningful market regimes.

Status

Planned

---

# SIMULATOR

Purpose

Research execution engine.

Modules

Basket

Grid

Execution

Inventory

Flash Events

Monte Carlo

Status

Planned

---

# ANALYTICS

Purpose

Research analysis.

Modules

Statistics

Feature Importance

Tail Analysis

Reporting

Status

Planned

---

# MACHINE LEARNING

Purpose

Train predictive models.

Modules

Training

Validation

Inference

Status

Planned

---

# MT5

Purpose

Production deployment.

Modules

Signal Generator

Order Manager

Bridge

Live Monitor

Status

Planned

---

# Dependency Rules

Allowed

Config

↓

Data

↓

Features

↓

Labels

↓

Dataset Builder

↓

Regimes

↓

Simulator

↓

Analytics

↓

ML

↓

MT5

Higher layers may depend on lower layers.

Lower layers must never depend on higher layers.

---

# Module Status

Draft

In Progress

Stable

Deprecated

Every module should always have one of these states.

---

# Version Policy

Every module should include

- Version
- Description
- Revision History

Major architectural changes belong in CHANGELOG.md.

Engineering reasoning belongs in DECISIONS.md.

---

# Final Principle

The purpose of every module should be understandable in less than two minutes.

If a module cannot be easily explained, it is probably trying to do too much.