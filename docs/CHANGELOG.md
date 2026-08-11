# APEX Change Log

> **Chronological record of major changes made to the APEX Quant Research Framework.**

---

# Version 1.0

## Project Created

### Added

- Initial project architecture
- Modular folder structure
- Documentation framework
- Project Charter

---

# Version 1.1

## Data Layer

### Added

- loader.py
- validator.py

### Improvements

- Automatic path handling
- Root-relative loading
- Dataset validation

---

# Version 1.2

## Feature Engineering

### Added

Feature modules

- price.py
- trend.py
- momentum.py
- volatility.py
- structure.py
- smart_money.py
- regime.py
- helpers.py

### Improvements

Feature engineering moved from a monolithic indicators.py to independent modules.

---

# Version 1.3

## Documentation

### Added

- README.md
- DESIGN_PRINCIPLES.md
- CODING_STANDARDS.md
- DECISIONS.md
- RESEARCH_INDEX.md
- ROADMAP.md
- CHANGELOG.md

---

# Version 1.4

## Development Tools

### Added

- apex_doctor.py
- development_status.py

### Improvements

Automated project auditing and development progress reporting.

---

# Version 2.0

## Stable Milestone

### Completed

- Configuration layer stabilised through settings.py and constants.py
- Feature registry completed
- Feature pipeline operational
- Volume and session features integrated
- Label modules completed
- Dataset builder operational
- Doctor checks healthy

### Improvements

- Structural consistency improved across the feature and label layers
- Documentation aligned with the current operational state
- The framework moved from early implementation to a stable research-ready state

---

# Version 2.1 (Phase 2 Core Complete)

## Phase 2 Research Infrastructure

### Completed & Frozen
- Research Feature Library
- Feature Pipeline
- Feature Store
- Research Labeling Engine
- Dataset Builder
- Dataset Validation Engine
- Feature Analysis Engine
- Dataset Split Engine
- Experiment Engine
- Experiment Repository

---

# Planned Version 3.0

## Regime Engine

- Baseline
- Continuation
- Persistence
- Transition
- Adaptive Inventory
- Classifier

---

# Planned Version 4.0

## Simulation Engine

- Basket Engine
- Execution Engine
- Inventory Engine
- Flash Events
- Monte Carlo

---

# Planned Version 5.0

## Machine Learning

- Master Dataset
- Training Pipeline
- Validation
- Inference

---

# Planned Version 6.0

## Live Trading

- MT5 Bridge
- Signal Generator
- Order Manager
- Live Monitor

---

# Versioning Policy

Major Version

Architectural changes.

Example

1.0 → 2.0

Minor Version

New functionality.

Example

1.0 → 1.1

Patch Version

Bug fixes.

Example

1.1.0 → 1.1.1

---

# Notes

This changelog records major architectural milestones.

Minor experimental changes should be documented inside the relevant experiment or module rather than here.