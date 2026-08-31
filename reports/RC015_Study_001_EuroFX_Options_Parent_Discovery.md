# RC015 Study 001 - Euro FX Options Parent Discovery

## 1. Confirmed 6E Futures Structure
Based on the local Definition audit, the `6E` futures dataset (`GLBX.MDP3`) is highly structured but strictly limited to Futures (`F`) and Spreads (`S`). It successfully maps the standard Euro FX futures contracts with standard contract months (e.g., `6EM6`, `6EU6`, `6EZ6`) but does not contain a single option contract.

## 2. Relevant Definition Fields
Analysis of the existing fields in the `6E` Definition file yielded the following:
- **`asset`**: Unanimously `6E`
- **`group`**: Unanimously `6E`
- **`raw_symbol`**: All symbols start with `6E` (e.g. `6EM6`, `6EZ6`)
- **`underlying`**: Entirely empty / null (`NaN`)
- **`instrument_class`**: Only `F` (Futures) and `S` (Spreads)
- **`security_type`**: Only `FUT`

**Conclusion**: The futures definition dataset contains no `parent`, `underlying`, or any cross-referencing fields pointing to an associated options root. The connection must be derived from Databento's symbology rules rather than the futures dataset itself.

## 3. Databento Options-Parent Convention
According to Databento's parent symbology documentation:
- Options on futures are assigned a `.OPT` suffix appended to the base futures root.
- This creates an aggregate "pseudo-parent" symbol that encompasses all options whose underlying is that futures root.
- For `6E`, the options parent is **`6E.OPT`**.

## 4. Potential Euro FX Options Parent
The exact Databento parent product that exposes the CME Euro FX options chain associated with `6E` is:
**`6E.OPT`**

## 5. CME Alternate-Root Considerations
While `6E.OPT` is the Databento parent, CME actually lists multiple raw option roots for Euro FX, including:
- Standard monthly options (often traded under `O6E` or historically `EUU`).
- Weekly/EOM options (e.g., `E1`, `E2`, `E3`, `E4`, `E5`).
- Volatility-quoted options (`V6E`).

Databento's `.OPT` pseudo-parent (`6E.OPT`) is explicitly designed to abstract this complexity. By requesting `6E.OPT`, Databento automatically resolves all these disparate CME roots into the single request, exposing all standard, weekly, and EOM expirations as long as they are associated with the `6E` futures.

## 6. Manual Portal Feasibility
**Can we manually select the required Euro FX options parent?**
**Yes.** The Databento web portal fully supports parent symbology. You can search for `6E.OPT` directly in the Data Portal's instrument search bar (or select the Euro FX Options product). This avoids the need to select individual child instruments (which would be nearly impossible given the thousands of option strikes).

## 7. API Request Specification
If the manual portal was insufficient, the exact API request parameter for symbology would be:
`symbols="6E.OPT"` with `stype_in="parent"`.
(Note: Do NOT execute this request via API).

## 8. Recommended Next Action
Perform a manual download using the Databento Data Portal to acquire the `6E.OPT` Definition schema for a single recent trading day. This will allow us to audit the exact strikes, expirations, and call/put indicators, as well as the specific raw CME roots (e.g. `O6E`, `E1`-`E5`) that make up the active Euro FX options chain.

---

## Options Definition Download Specification
Please perform the following download manually via the Databento portal:

- **Dataset**: `GLBX.MDP3`
- **Schema**: `Definition`
- **Product**: `6E.OPT` (Euro FX Options)
- **Date**: `2026-08-15` (A single recent trading day)
- **Format**: `CSV`
- **Timestamp**: `ISO 8601`
- **Price format**: `Decimal`
- **Split**: `None`

*Note: Once this ZIP is obtained and placed in `data/databento/`, we will run the next definition audit phase.*
