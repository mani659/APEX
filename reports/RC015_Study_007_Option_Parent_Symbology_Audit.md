# RC015 Study 007 - Option Parent Symbology Audit

## 1. Objective
Identify the correct Databento parent symbol mapping (`[asset].OPT`) for the historical EUR/USD outright options roots required for RC015 Study 007. This corrects the false assumption that `6E.OPT` could resolve the option universe, recognizing that CME defines the `asset` for EUR/USD standard and weekly options differently from the underlying futures root.

## 2. Methodology
Using the `GLBX.MDP3` schema `definition` endpoint, parent symbol combinations were requested against historical timeframes to confirm the raw `asset` field returned by Databento. The mapping strictly adheres to the rule: if `asset = X`, the valid parent symbol is `X.OPT`. 

*No Option BBO-1m data was downloaded. No IV or RV calculations were run.*

## 3. Results

| raw_root | asset | group | example_raw_symbol | instrument_class | security_type | inferred_parent_symbol | confidence | evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EUU** | EUU | XE | `EUUZ4 P1045` | P | OOF | `EUU.OPT` | **CONFIRMED** | Definition endpoint returned asset=EUU and security_type=OOF for EUU.OPT |
| **1EU** | 1EU | XE | `1EUG4 P1122` | P | OOF | `1EU.OPT` | **CONFIRMED** | Definition endpoint returned asset=1EU and security_type=OOF for 1EU.OPT |
| **2EU** | 2EU | XE | `2EUF4 C1070` | C | OOF | `2EU.OPT` | **CONFIRMED** | Definition endpoint returned asset=2EU and security_type=OOF for 2EU.OPT |
| **3EU** | 3EU | XE | `3EUF4 C1065` | C | OOF | `3EU.OPT` | **CONFIRMED** | Definition endpoint returned asset=3EU and security_type=OOF for 3EU.OPT |
| **4EU** | 4EU | XE | `4EUF4 P1085` | P | OOF | `4EU.OPT` | **CONFIRMED** | Definition endpoint returned asset=4EU and security_type=OOF for 4EU.OPT |
| **5EU** | 5EU | XE | `5EUK4 C1115` | C | OOF | `5EU.OPT` | **CONFIRMED** | Definition endpoint returned asset=5EU and security_type=OOF for 5EU.OPT |

## 4. Analysis
The assumption that `6E.OPT` serves as the universal parent for EUR/USD options on `GLBX.MDP3` is invalid. CME designates the standard monthly options with `asset = EUU` and the weekly expiries with `asset = [1-5]EU`. Databento's parent symbology accurately mirrors this exact hierarchy.

Therefore, `6E.OPT` was legitimately rejected as `symbology_invalid_request` because the options are grouped under `EUU.OPT` and `[1-5]EU.OPT`, not `6E.OPT`.

## 5. Conclusion
To correctly acquire the historical EUR/USD outright options universe for Study 007, the Stage 1 Definition pipeline must request `EUU.OPT` for standard expirations and `1EU.OPT`, `2EU.OPT`, `3EU.OPT`, `4EU.OPT`, `5EU.OPT` for weeklies.
