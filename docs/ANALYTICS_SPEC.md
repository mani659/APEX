# APEX Quant Research Framework  
# Analytics Specification

Version: 1.0  
Status: Draft for implementation

---

# 1. Purpose

The Analytics layer transforms the master dataset into research evidence.

It does not load raw market data.
It does not create features.
It does not create labels.
It does not modify the dataset.

Its role is to answer research questions such as:

- What does the dataset look like?
- Which features are informative?
- Which distributions have heavy tails?
- Which parameters are stable?
- What evidence should be included in reports?

Analytics is a read-only consumer of the master dataset.

---

# 2. Core Principle

Doctor validates engineering.  
Analytics validates hypotheses.

Doctor asks: “Does the framework work correctly?”  
Analytics asks: “What does the data tell us?”

---

# 3. Scope

The Analytics layer covers:

- dataset description
- feature statistics
- tail behavior
- feature importance
- parameter surfaces
- report assembly

The Analytics layer does not cover:

- data loading
- preprocessing
- feature generation
- label generation
- model training
- live trading
- execution logic

---

# 4. Folder Contract

The analytics package contains the following modules:

- `statistics.py`
- `tail_statistics.py`
- `feature_importance.py`
- `parameter_surface.py`
- `reporting.py`

Optional support files:

- `utils.py`
- `analytics.py` or `apex_analytics.py` as a runner

---

# 5. Shared Interface Contract

Every analytics module should follow the same public interface:

```python
def analyze(df, output_dir, verbose=True) -> AnalyticsResult:
    ...