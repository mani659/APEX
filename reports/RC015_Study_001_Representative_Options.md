# RC015 Study 001 - Representative EUR/USD Option Contracts

## 1. Selection Methodology
- **Selected Expiry**: `2026-08-31`
- **Underlying Futures**: `6EU6` (ID: `10573`)
- **ATM Methodology**: The futures price is not present in the static Definition data. Therefore, the At-The-Money (ATM) strike was estimated purely through strike-grid proximity by taking the median strike of the available strike array for this expiration. Do not rely on this representing the true live ATM.
- **Estimated ATM Strike**: `1.155`

## 2. Why These Six Contracts Are Representative
These six contracts form a perfectly symmetrical micro-chain around the estimated ATM strike. They share a single expiry that is 2-6 weeks away (avoiding short-term expiration noise) and map to a single unified underlying futures contract. By selecting exactly one ITM, one ATM, and one OTM option for both calls and puts, we have a structurally complete minimal dataset. This set is fully sufficient for testing BBO-1s connectivity, data alignment, implied volatility execution, and put-call parity without requiring a massive data download.

## 3. Selected Contracts
|   instrument_id | raw_symbol   | symbol      | asset   | call/put   |   strike_price | expiration                     | underlying   |   underlying_id |   contract_multiplier |   tick_size |
|----------------:|:-------------|:------------|:--------|:-----------|---------------:|:-------------------------------|:-------------|----------------:|----------------------:|------------:|
|        42778548 | MO5Q6 C1142  | MO5Q6 C1142 | MO5     | C          |         1.1425 | 2026-08-31T14:00:00.000000000Z | 6EU6         |           10573 |            2147483647 |         nan |
|        42679028 | MO5Q6 C1155  | MO5Q6 C1155 | MO5     | C          |         1.155  | 2026-08-31T14:00:00.000000000Z | 6EU6         |           10573 |            2147483647 |         nan |
|        42584515 | MO5Q6 C1167  | MO5Q6 C1167 | MO5     | C          |         1.1675 | 2026-08-31T14:00:00.000000000Z | 6EU6         |           10573 |            2147483647 |         nan |
|        42777675 | MO5Q6 P1167  | MO5Q6 P1167 | MO5     | P          |         1.1675 | 2026-08-31T14:00:00.000000000Z | 6EU6         |           10573 |            2147483647 |         nan |
|        42861262 | MO5Q6 P1155  | MO5Q6 P1155 | MO5     | P          |         1.155  | 2026-08-31T14:00:00.000000000Z | 6EU6         |           10573 |            2147483647 |         nan |
|        42367873 | MO5Q6 P1142  | MO5Q6 P1142 | MO5     | P          |         1.1425 | 2026-08-31T14:00:00.000000000Z | 6EU6         |           10573 |            2147483647 |         nan |

## 4. Next Step
The above instrument IDs are to be used for the BBO-1s quote download. Do not assume these contracts are deeply liquid until verified by the actual BBO data.
