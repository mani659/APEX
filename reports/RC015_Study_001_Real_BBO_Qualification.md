# RC015 Study 001 - Real BBO Qualification

## 1. Data Source and ZIP Identification
- ZIP File: `GLBX-20260816-AEWM5PMURM.zip`
- Extracted File: `glbx-mdp3-20260812.bbo-1m.csv.zst`

## 2. Schema Verification
- Dataset matches GLBX.MDP3 BBO-1m schema.
- Columns found: 17
- Required Symbol/Price/Size/TS fields are present.

## 3. Date/Time Coverage
- Row Count: `659775`
- Start TS: `2026-08-12T00:00:00.000000000Z`
- End TS: `2026-08-12T23:59:00.000000000Z`

## 4. Quote-Quality Audit (Aggregate Summary)
- **Total Instruments Analyzed**: 1483
- **Median Valid Quote %**: 99.46%
- **Bid/Ask Violations**: 0
- **Missing Timestamps**: 0
- **Zero/Negative Bids**: 8953
- **Zero/Negative Asks**: 8587

## 5. Option-Universe Audit
- **Instruments present in BBO**: 1483
- **Unique Symbols**: 1483
- **Calls / Puts**: 606 / 578
- **Unique Expiries**: 18
- **Unique Strikes**: 85
- **Raw Option Roots**: EUU

## 6. Definition Mapping
All BBO instruments successfully mapped to the Definition dataset via `instrument_id`.

## 7. Underlying Mapping
- **Option**: `EUUZ6 C1135` (ID: 42184845) -> **Underlying**: `6EZ6` (ID: 5510)
- **Option**: `EUUZ6 C1140` (ID: 42061735) -> **Underlying**: `6EZ6` (ID: 5510)
- **Option**: `EUUZ6 C1145` (ID: 42157206) -> **Underlying**: `6EZ6` (ID: 5510)
- **Option**: `EUUZ6 P1145` (ID: 42222489) -> **Underlying**: `6EZ6` (ID: 5510)
- **Option**: `EUUZ6 P1140` (ID: 42061699) -> **Underlying**: `6EZ6` (ID: 5510)
- **Option**: `EUUZ6 P1135` (ID: 42130639) -> **Underlying**: `6EZ6` (ID: 5510)

## 8. Moneyness Qualification
`UNDERLYING PRICE: NOT PRESENT IN CURRENT SAMPLE`

Because the underlying 6EU6 futures quotes were not included in this BBO options download, true ATM cannot be definitively calculated. Selected strikes are 'near-ATM candidates' based purely on strike grid density.

## 9. Real Black-76 IV Results
Implied Volatility inversion was bypassed because the underlying futures price is missing from the dataset. A contemporaneous futures price is strictly required for valid Black-76 pricing. We will not use spot or prior day settlement as a workaround.

## 10. Selected Contracts & Liquidity Assessment
|   instrument_id | symbol      | instrument_class   |   strike_price |   total_obs |   valid_quote_pct |   med_spread |
|----------------:|:------------|:-------------------|---------------:|------------:|------------------:|-------------:|
|        42184845 | EUUZ6 C1135 | C                  |          1.135 |         470 |          0.995745 |       0.0007 |
|        42061735 | EUUZ6 C1140 | C                  |          1.14  |         547 |          0.996344 |       0.0006 |
|        42157206 | EUUZ6 C1145 | C                  |          1.145 |         738 |          0.99729  |       0.0005 |
|        42222489 | EUUZ6 P1145 | P                  |          1.145 |        1068 |          0.998127 |       0.0002 |
|        42061699 | EUUZ6 P1140 | P                  |          1.14  |        1109 |          0.998197 |       0.0002 |
|        42130639 | EUUZ6 P1135 | P                  |          1.135 |         985 |          0.99797  |       0.0002 |

These contracts exhibit a high density of quote updates. They are classified as `USABLE FOR MICRO-TEST` given the valid quote percentage and continuous bid/ask presence.

## 11. Missing-Data Assessment & Spot/Futures Limitation
The Databento `EUU` / `6E.OPT` options download successfully returns the options chain BBO, but it explicitly does NOT automatically bundle the underlying `6E` futures BBO into the same file unless they share the same parent symbology mapping in the request (which they often do not in BBO extracts). To execute a valid real-market IV conversion, we definitively need the contemporaneous futures price.

## 12. Final Qualification
### CONDITIONALLY QUALIFIED
The real CME EUR/USD option BBO data works exceptionally well. It can be mapped accurately to the Definition dataset, and the quotes are highly dense and valid. However, a clearly defined limitation remains: the missing underlying futures quotes (`6EU6`).

### Next Manual Download Requirement
We need a single additional Databento download to complete the test:
- **Dataset**: `GLBX.MDP3`
- **Schema**: `BBO-1m`
- **Symbol**: `6EU6` (or `6E` parent for futures)
- **Date**: `2026-08-12` (Matching the date of the Options BBO download)

## Local Discovery Failure
The requested 6E BBO-1m dataset could NOT be found in the repository. Exhaustive search revealed only the original three ZIP files. We cannot pair the real EUU option BBO-1m data with the 6EZ6 futures data because the futures data physically does not exist locally.
