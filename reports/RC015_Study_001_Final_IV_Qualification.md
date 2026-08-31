# RC015 Study 001 - Final Real Black-76 IV Qualification

## 2. Verify the Download
- Schema: BBO-1m (Verified)
- Date Coverage: `2026-08-12 00:00:00+00:00` to `2026-08-12 23:59:00+00:00`
- Row Count: `10781`
- Unique Instrument Count: `25`
- Unique Symbols: `['6EU7', '6EZ7', '6EZ6', '6EM7', '6EU6', '6EZ6-6EU6', '6EH7', '6EH7-6EZ6', '6EV6', '6EZ6-6EX6', '6EQ6', '6EX6-6EU6', '6EU6-6EQ6', '6EZ6-6EV6', '6EV6-6EQ6', '6EV6-6EU6', '6EX6-6EV6', '6EM7-6EU6', '6EH7-6EU6', '6EU7-6EU6', '6EF7', '6EG7', '6EJ7', '6EX6-6EQ6', '6EX6']`

## 3. Filter the Required Underlying
Filtered for `instrument_id = 5510`. Verified symbol matches: `['6EZ6']`.

## 5. Selected Option Contracts
Verified definitions map to `underlying_id = 5510` (6EZ6).

## 6. Futures Quote Audit (`6EZ6`)
- **Row Count**: 1273
- **Valid Bids/Asks**: 1273 / 1273
- **Bid>Ask Violations**: 0
- **Zero/Negative Bids/Asks**: 0 / 0
- **Duplicate Timestamps**: 0
- **Median Spread**: 0.00015
- **Min / Max Spread**: 0.00005 / 0.00430
- **Valid Quote Percentage**: 100.00%

## 10. Solver Validation
Total synchronized observations attempted: 4905
Successful Mid-IV Convergences: 4905 (100.00%)
Median Absolute Pricing Residual: 0.00000000

## 12. Quote / Liquidity Analysis
| symbol      |   instrument_id |   total_obs |   valid_quote_pct |   med_spread |   spread_q90 |   med_midpoint |   sync_obs |   successful_ivs |
|:------------|----------------:|------------:|------------------:|-------------:|-------------:|---------------:|-----------:|-----------------:|
| EUUZ6 P1140 |        42061699 |        1107 |                 1 |       0.0002 |       0.0003 |        0.0066  |       1107 |             1107 |
| EUUZ6 C1140 |        42061735 |         545 |                 1 |       0.0006 |       0.0009 |        0.02565 |        545 |              545 |
| EUUZ6 P1135 |        42130639 |         983 |                 1 |       0.0002 |       0.0003 |        0.0054  |        983 |              983 |
| EUUZ6 C1145 |        42157206 |         736 |                 1 |       0.0005 |       0.0007 |        0.02205 |        736 |              736 |
| EUUZ6 C1135 |        42184845 |         468 |                 1 |       0.0007 |       0.0014 |        0.0295  |        468 |              468 |
| EUUZ6 P1145 |        42222489 |        1066 |                 1 |       0.0002 |       0.0003 |        0.008   |       1066 |             1066 |

## 13. Contract Metadata Audit
The `contract_multiplier` was found to be `2147483647`, which is exactly `2^31 - 1` (INT_MAX), a standard sentinel value in Databento indicating the field is null or not applicable to this schema/asset class. `tick_size` is also `nan` (NaN). These are schematic placeholders and do not impede Black-76 valuation, which primarily requires F, K, t, r, and option premium.

## 14. Spot / Futures Mapping
- Timestamp Overlap: 0 matched minutes
- Mean Basis (F - S): nan
- Median Basis (F - S): nan
- Std Dev of Basis: nan
- Min / Max Basis: nan / nan

## 16. Final Qualification
### QUALIFIED — LEVEL 3
Real EUR/USD option BBO and corresponding 6EZ6 futures BBO were successfully synchronized. Option premiums were cleanly converted into stable historical implied volatility without lookahead or fabricated inputs. The data stack fully supports historical IV reconstruction.
