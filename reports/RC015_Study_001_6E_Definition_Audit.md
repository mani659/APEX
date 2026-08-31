# RC015 Study 001 - Local 6E Definition Audit & Euro FX Options Discovery

## Dataset Identification
- **ZIP filename**: `GLBX-20260816-RMS9TQEJU8.zip`
- **Source**: Databento (GLBX.MDP3)
- **Date Range**: 2026-05-16 to 2026-08-15 (inferred from filename)
- **File count (extracted)**: 4
- **Row count (raw dataset)**: 13282
- **Unique Instrument count**: 141
- **Schema columns**: 74

## Schema
```text
ts_recv
ts_event
rtype
publisher_id
instrument_id
raw_symbol
security_update_action
instrument_class
min_price_increment
display_factor
expiration
activation
high_limit_price
low_limit_price
max_price_variation
unit_of_measure_qty
min_price_increment_amount
price_ratio
inst_attrib_value
underlying_id
raw_instrument_id
market_depth_implied
market_depth
market_segment_id
max_trade_vol
min_lot_size
min_lot_size_block
min_lot_size_round_lot
min_trade_vol
contract_multiplier
decay_quantity
original_contract_size
appl_id
maturity_year
decay_start_date
channel_id
currency
settl_currency
secsubtype
group
exchange
asset
cfi
security_type
unit_of_measure
underlying
strike_price_currency
strike_price
match_algorithm
main_fraction
price_display_format
sub_fraction
underlying_product
maturity_month
maturity_day
maturity_week
user_defined_instrument
contract_multiplier_unit
flow_schedule_type
tick_rule
leg_count
leg_index
leg_instrument_id
leg_raw_symbol
leg_instrument_class
leg_side
leg_price
leg_delta
leg_ratio_price_numerator
leg_ratio_price_denominator
leg_ratio_qty_numerator
leg_ratio_qty_denominator
leg_underlying_id
symbol
```

## Field Status (Important Fields)
- **instrument_id**: `PRESENT`
- **symbol**: `PRESENT`
- **raw_symbol**: `PRESENT`
- **asset**: `PRESENT`
- **instrument_class**: `PRESENT`
- **security_type**: `PRESENT`
- **expiration**: `PRESENT`
- **strike_price**: `PRESENT`
- **underlying**: `PRESENT`
- **underlying_id**: `PRESENT`
- **parent**: `FIELD NOT PRESENT`
- **parent_id**: `FIELD NOT PRESENT`
- **currency**: `PRESENT`
- **put_or_call**: `FIELD NOT PRESENT`
- **contract_multiplier**: `PRESENT`
- **min_price_increment**: `PRESENT`
- **maturity_year**: `PRESENT`
- **maturity_month**: `PRESENT`
- **option type (via security_type/cfi)**: `PRESENT (indirect)`
- **tick size**: `PRESENT (as min_price_increment)`
- **maturity**: `PRESENT (as maturity_year/month/day/week)`

## Dataset Characterization
### By Asset
- `6E`: 141 unique instruments
### By Instrument Class
- `S`: 101 unique instruments
- `F`: 40 unique instruments
### By Security Type
- `FUT`: 141 unique instruments

**Contains Option Instruments?**: `No`

## Euro FX Futures Summary
|   Instrument ID | Raw Symbol   | Expiry                         | Contract Month   | Instrument Class   | Security Type   |   Tick Size |   Contract Multiplier | Parent/Root   |
|----------------:|:-------------|:-------------------------------|:-----------------|:-------------------|:----------------|------------:|----------------------:|:--------------|
|        42012835 | 6EK6         | 2026-05-18T14:16:00.000000000Z | 2026-05          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|           20048 | 6EM6         | 2026-06-15T14:16:00.000000000Z | 2026-06          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42004841 | 6EN6         | 2026-07-13T14:16:00.000000000Z | 2026-07          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42003651 | 6EQ6         | 2026-08-17T14:16:00.000000000Z | 2026-08          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|           10573 | 6EU6         | 2026-09-14T14:16:00.000000000Z | 2026-09          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42001229 | 6EV6         | 2026-10-19T14:16:00.000000000Z | 2026-10          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823529 | 6EX6         | 2026-11-16T15:16:00.000000000Z | 2026-11          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|            5510 | 6EZ6         | 2026-12-14T15:16:00.000000000Z | 2026-12          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823817 | 6EF7         | 2027-01-15T15:16:00.000000000Z | 2027-01          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823836 | 6EG7         | 2027-02-12T15:16:00.000000000Z | 2027-02          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|           19927 | 6EH7         | 2027-03-15T14:16:00.000000000Z | 2027-03          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823846 | 6EJ7         | 2027-04-19T14:16:00.000000000Z | 2027-04          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823530 | 6EK7         | 2027-05-17T14:16:00.000000000Z | 2027-05          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|            8915 | 6EM7         | 2027-06-14T14:16:00.000000000Z | 2027-06          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823837 | 6EN7         | 2027-07-19T14:16:00.000000000Z | 2027-07          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823873 | 6EQ7         | 2027-08-16T14:16:00.000000000Z | 2027-08          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|            3505 | 6EU7         | 2027-09-13T14:16:00.000000000Z | 2027-09          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823847 | 6EV7         | 2027-10-18T14:16:00.000000000Z | 2027-10          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42824172 | 6EX7         | 2027-11-15T15:16:00.000000000Z | 2027-11          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|            5344 | 6EZ7         | 2027-12-13T15:16:00.000000000Z | 2027-12          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42824229 | 6EF8         | 2028-01-14T15:16:00.000000000Z | 2028-01          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42824252 | 6EG8         | 2028-02-14T15:16:00.000000000Z | 2028-02          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|           36964 | 6EH8         | 2028-03-13T14:16:00.000000000Z | 2028-03          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823538 | 6EJ8         | 2028-04-17T14:16:00.000000000Z | 2028-04          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42823938 | 6EK8         | 2028-05-15T14:16:00.000000000Z | 2028-05          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|           11313 | 6EM8         | 2028-06-16T14:16:00.000000000Z | 2028-06          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42006050 | 6EN8         | 2028-07-17T14:16:00.000000000Z | 2028-07          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42056338 | 6EQ8         | 2028-08-14T14:16:00.000000000Z | 2028-08          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42005041 | 6EU8         | 2028-09-18T14:16:00.000000000Z | 2028-09          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42007492 | 6EZ8         | 2028-12-18T15:16:00.000000000Z | 2028-12          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42009961 | 6EH9         | 2029-03-19T14:16:00.000000000Z | 2029-03          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42445105 | 6EM9         | 2029-06-15T14:16:00.000000000Z | 2029-06          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42193598 | 6EU9         | 2029-09-17T14:16:00.000000000Z | 2029-09          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42053216 | 6EZ9         | 2029-12-17T15:16:00.000000000Z | 2029-12          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42093712 | 6EH0         | 2030-03-18T14:16:00.000000000Z | 2030-03          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42654425 | 6EM0         | 2030-06-17T14:16:00.000000000Z | 2030-06          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42658580 | 6EU0         | 2030-09-16T14:16:00.000000000Z | 2030-09          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42042861 | 6EZ0         | 2030-12-16T15:16:00.000000000Z | 2030-12          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42014023 | 6EH1         | 2031-03-17T14:16:00.000000000Z | 2031-03          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |
|        42112983 | 6EM1         | 2031-06-16T14:16:00.000000000Z | 2031-06          | F                  | FUT             |       5e-05 |            2147483647 | 6E            |

## Options Discovery
The current 6E definition file contains **no options data** and **no references** pointing from futures to associated options. Fields such as `strike_price` exist but are entirely null. There are no fields like `put_or_call`, and no symbols contain `.OPT`.

Because the definition file does not contain cross-references from the underlying futures to the options, we cannot extract the exact options symbols from this file alone. However, based on Databento's documented options-on-futures symbology conventions, the parent product for options on a future is designated by appending `.OPT` to the futures root. Therefore, the exact Databento symbology required to query options on `6E` futures is `6E.OPT`.

## Missing Information
- Option symbols and specific option roots.
- Call/Put indicators (`put_or_call` field is absent).
- Strike prices (present in schema but no data populated).
- Direct linkage from Futures to Options (no `parent` or `associated_options` field).

---

## Options Query Specification

### Dataset
`GLBX.MDP3`

### Schema
`Definition`

### Product / Parent
`6E.OPT`

### Date Range
`2026-08-15` (A single day is sufficient to discover the active options contracts and their definitions. Using the last day of the futures download range ensures we see current active options.)

### Expected Records
We expect to see Definition records where:
- `instrument_class` = `O` (Option)
- `security_type` = `OPT`
- `strike_price` is populated with valid strike values.
- The CFI code or a similar field indicates Call/Put (e.g., `OC` for Call, `OP` for Put).
- `underlying` or `group` references `6E`.
- `expiration` represents the option expiry date.
- `instrument_id` gives the unique integer ID for each specific option contract.
