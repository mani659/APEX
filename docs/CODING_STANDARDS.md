# APEX Coding Standards

> **One Framework. One Style. One Standard.**

---

# Purpose

This document defines the coding standards for every Python module within APEX.

The objective is not only readability but long-term maintainability and consistency.

Every file in the project should appear as though it was written by the same developer.

The current project is stable, so changes should preserve that consistency rather than introduce stylistic churn.

---

# Guiding Principles

- Readability over cleverness
- Explicit over implicit
- Simplicity over complexity
- Reusable over duplicated
- Deterministic over unpredictable
- Modular over monolithic
- Preserve working structure unless a clear issue is proven

---

# File Header

Every Python file begins with the standard header.

```python
"""
=========================================================
APEX Quant Research Framework

Module      : loader.py
Version     : 1.0

Description :
Loads market data into the framework.

Author      : APEX

=========================================================
"""
```

Every completed version increments the Version field.

---

# Import Order

Always follow this order.

```python
# ==========================================================
# Standard Library
# ==========================================================

from pathlib import Path
import logging

# ==========================================================
# Third Party
# ==========================================================

import numpy as np
import pandas as pd

# ==========================================================
# APEX
# ==========================================================

from config.settings import *
```

Never mix import groups.

---

# Naming Convention

## Files

Use snake_case.

Correct

```
future_returns.py
```

Wrong

```
FutureReturns.py
futureReturns.py
```

---

## Variables

Use descriptive snake_case.

Good

```python
rolling_mean
basket_size
future_return
```

Bad

```python
x
temp
abc
```

---

## Constants

UPPER_CASE.

```python
ATR_PERIOD = 14
MAX_SPREAD = 30
```

Magic numbers are prohibited.

---

## Classes

PascalCase.

```python
MarketStructure
BasketEngine
FeatureRegistry
```

---

## Functions

snake_case

```python
calculate_atr()

build_features()

detect_sweep()
```

---

# Function Design

Functions should do one thing.

Good

```python
calculate_atr()
```

Bad

```python
calculate_everything()
```

Prefer many small functions over one large function.

---

# Function Length

Recommended

< 40 lines

Maximum

100 lines

If a function exceeds this, consider refactoring.

---

# Module Size

Recommended

< 300 lines

Soft limit

400 lines

Hard limit

500 lines

Large modules should be split.

---

# Comments

Explain WHY.

Do not explain obvious code.

Bad

```python
price = close
```

Good

```python
# Prevent division by zero during low volatility periods.
```

---

# Docstrings

Every public function must include a docstring.

Use NumPy style.

Example

```python
def calculate_atr(df):

    """
    Calculate Average True Range.

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    Series
    """
```

---

# Type Hints

Preferred.

```python
def calculate_atr(
    df: pd.DataFrame
) -> pd.Series:
```

---

# Error Handling

Never silently ignore exceptions.

Bad

```python
try:
    ...
except:
    pass
```

Good

```python
try:
    ...
except Exception as e:
    raise RuntimeError(e)
```

---

# Logging

Avoid print() inside framework modules.

Use logging.

```python
logger.info()

logger.warning()

logger.error()
```

print() is acceptable only for standalone experiments or debugging.

---

# Configuration

Never hard-code parameters.

Bad

```python
ema = close.ewm(span=20)
```

Good

```python
ema = close.ewm(span=EMA_FAST)
```

Configuration belongs inside

config/

---

# Feature Modules

Every feature module must:

- Return DataFrame or Series
- Never modify raw data
- Never access future candles
- Be deterministic
- Be independently testable

---

# Label Modules

Labels may use future information.

Features may not.

Never mix labels with features.

---

# Research Modules

Each experiment answers one question.

Never combine unrelated hypotheses.

Every experiment must be reproducible.

---

# Dataset Rules

Raw datasets are immutable.

Intermediate datasets are reproducible.

Master Dataset is the single source of truth.

---

# Code Duplication

Copy-paste is prohibited.

Shared logic belongs in:

```
features/helpers.py
```

or another appropriate shared module.

---

# Versioning

Major rewrite

```
1.0
```

Minor feature

```
1.1
```

Bug fix

```
1.1.1
```

Breaking change

```
2.0
```

---

# TODOs

Always use a consistent format.

```python
# TODO:
# Add rolling VWAP feature.
```

---

# FIXMEs

Use only for known bugs.

```python
# FIXME:
# Incorrect behaviour during missing sessions.
```

---

# Testing Checklist

Before marking a module complete:

- Code executes
- No warnings
- No future leakage
- No duplicated logic
- Documentation updated
- Version updated
- Integrated into pipeline

---

# Pull Request Checklist

Before merging any work:

- Follows coding standards
- No unnecessary complexity
- Modular
- Documented
- Reproducible
- Backward compatible (unless intentional)

---

# The APEX Rule

When in doubt, choose the solution that is:

- Easier to read
- Easier to test
- Easier to reuse
- Easier to maintain

Complexity must always be earned through evidence.

---

# Final Statement

Every line of code added to APEX should make the framework:

- Simpler
- Clearer
- More reusable
- More deterministic
- Better documented

Code quality is a feature.

Maintainability is a competitive advantage.