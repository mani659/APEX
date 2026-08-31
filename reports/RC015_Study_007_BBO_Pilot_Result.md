# RC015 Study 007 — BBO Validation Pilot Results

**Total Data Cost:** $0.0015
**Final Decision Gate**: FAIL

## Executive Summary
## Event Analysis
### Event: 2022-01-05_2022-01-07
- **Futures ID**: 28727 (28727)
- **Futures Target Timestamp**: 2022-01-05T15:00:00 UTC
- **Futures Actual Timestamp**: 2022-01-05 15:00:00+00:00 UTC (diff: 0s)
- **Futures BBO Midpoint**: 1.135075

#### Option: 585890 (585890) - Type C
**Definition Cross-Check**
- `symbol`: 585890
- `raw_symbol`: EUUF2 C1132
- `asset`: EUU
- `expiration`: 2022-01-07 15:00:00+00:00
- `strike`: 1.1325
- `instrument_class`: C
- `underlying_id`: 28727 (Matches Futures ID 28727? YES)

**Moneyness Validation**
- Strike: 1.1325
- Futures Mid: 1.135075
- Absolute Distance: 0.00257
- PASS: False

**Option Quote Audit**
- Total BBO observations: 115
- First quote: 2022-01-05 14:00:00+00:00
- Last quote: 2022-01-05 15:59:00+00:00
- Valid Bid count: 114
- Valid Ask count: 115
- Bid > Ask violations: 0
- Zero/Negative Bid count: 0
- Zero/Negative Ask count: 0
- Median spread: 0.00039999999999999975
- P90 spread: 0.0004000000000000002
- Target timestamp covered: True

#### Option: 573458 (573458) - Type P
**Definition Cross-Check**
- `symbol`: 573458
- `raw_symbol`: EUUF2 P1132
- `asset`: EUU
- `expiration`: 2022-01-07 15:00:00+00:00
- `strike`: 1.1325
- `instrument_class`: P
- `underlying_id`: 28727 (Matches Futures ID 28727? YES)

**Moneyness Validation**
- Strike: 1.1325
- Futures Mid: 1.135075
- Absolute Distance: 0.00257
- PASS: False

**Option Quote Audit**
- Total BBO observations: 120
- First quote: 2022-01-05 14:00:00+00:00
- Last quote: 2022-01-05 15:59:00+00:00
- Valid Bid count: 120
- Valid Ask count: 120
- Bid > Ask violations: 0
- Zero/Negative Bid count: 0
- Zero/Negative Ask count: 0
- Median spread: 0.0002000000000000001
- P90 spread: 0.00030000000000000014
- Target timestamp covered: True

### Event: 2024-03-20_2024-03-22
- **Futures ID**: 131197 (131197)
- **Futures Target Timestamp**: 2024-03-20T15:00:00 UTC
- **Futures Actual Timestamp**: 2024-03-20 15:00:00+00:00 UTC (diff: 0s)
- **Futures BBO Midpoint**: 1.0889250000000001

#### Option: 42032233 (42032233) - Type C
**Definition Cross-Check**
- `symbol`: 42032233
- `raw_symbol`: 4EUH4 C1097
- `asset`: 4EU
- `expiration`: 2024-03-22 14:00:00+00:00
- `strike`: 1.0975
- `instrument_class`: C
- `underlying_id`: 131197 (Matches Futures ID 131197? YES)

**Moneyness Validation**
- Strike: 1.0975
- Futures Mid: 1.0889250000000001
- Absolute Distance: 0.00857
- PASS: False

**Option Quote Audit**
- Total BBO observations: 89
- First quote: 2024-03-20 14:00:00+00:00
- Last quote: 2024-03-20 15:59:00+00:00
- Valid Bid count: 89
- Valid Ask count: 89
- Bid > Ask violations: 0
- Zero/Negative Bid count: 0
- Zero/Negative Ask count: 0
- Median spread: 0.00019999999999999993
- P90 spread: 0.00024999999999999995
- Target timestamp covered: True

#### Option: 42252599 (42252599) - Type P
**Definition Cross-Check**
- `symbol`: 42252599
- `raw_symbol`: 4EUH4 P1097
- `asset`: 4EU
- `expiration`: 2024-03-22 14:00:00+00:00
- `strike`: 1.0975
- `instrument_class`: P
- `underlying_id`: 131197 (Matches Futures ID 131197? YES)

**Moneyness Validation**
- Strike: 1.0975
- Futures Mid: 1.0889250000000001
- Absolute Distance: 0.00857
- PASS: False

**Option Quote Audit**
- Total BBO observations: 104
- First quote: 2024-03-20 14:00:00+00:00
- Last quote: 2024-03-20 15:59:00+00:00
- Valid Bid count: 104
- Valid Ask count: 104
- Bid > Ask violations: 0
- Zero/Negative Bid count: 0
- Zero/Negative Ask count: 0
- Median spread: 0.00040000000000000105
- P90 spread: 0.0005000000000000004
- Target timestamp covered: True

### Event: 2026-06-24_2026-06-26
- **Futures ID**: 10573 (10573)
- **Futures Target Timestamp**: 2026-06-24T15:00:00 UTC
- **Futures Actual Timestamp**: 2026-06-24 15:00:00+00:00 UTC (diff: 0s)
- **Futures BBO Midpoint**: 1.138075

#### Option: 42213640 (42213640) - Type C
**Definition Cross-Check**
- `symbol`: 42213640
- `raw_symbol`: 4EUM6 C1140
- `asset`: 4EU
- `expiration`: 2026-06-26 14:00:00+00:00
- `strike`: 1.14
- `instrument_class`: C
- `underlying_id`: 10573 (Matches Futures ID 10573? YES)

**Moneyness Validation**
- Strike: 1.14
- Futures Mid: 1.138075
- Absolute Distance: 0.00192
- PASS: True

**Option Quote Audit**
- Total BBO observations: 120
- First quote: 2026-06-24 14:00:00+00:00
- Last quote: 2026-06-24 15:59:00+00:00
- Valid Bid count: 120
- Valid Ask count: 120
- Bid > Ask violations: 0
- Zero/Negative Bid count: 0
- Zero/Negative Ask count: 0
- Median spread: 0.0002000000000000001
- P90 spread: 0.0002999999999999999
- Target timestamp covered: True

#### Option: 42127757 (42127757) - Type P
**Definition Cross-Check**
- `symbol`: 42127757
- `raw_symbol`: 4EUM6 P1137
- `asset`: 4EU
- `expiration`: 2026-06-26 14:00:00+00:00
- `strike`: 1.1375
- `instrument_class`: P
- `underlying_id`: 10573 (Matches Futures ID 10573? YES)

**Moneyness Validation**
- Strike: 1.1375
- Futures Mid: 1.138075
- Absolute Distance: 0.00057
- PASS: True

**Option Quote Audit**
- Total BBO observations: 120
- First quote: 2026-06-24 14:00:00+00:00
- Last quote: 2026-06-24 15:59:00+00:00
- Valid Bid count: 120
- Valid Ask count: 120
- Bid > Ask violations: 0
- Zero/Negative Bid count: 0
- Zero/Negative Ask count: 0
- Median spread: 0.0002000000000000001
- P90 spread: 0.0002999999999999999
- Target timestamp covered: True

