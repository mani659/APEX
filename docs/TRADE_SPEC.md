# Trade Specification

## 1. Mission

The `Trade` object represents one completed trade lifecycle. It begins the moment a position is successfully opened via execution, and it terminates the moment the position is entirely closed.

- A `Trade` is **NOT** an `Order` (an Order is intent waiting for execution).
- A `Trade` is **NOT** a `Signal` (a Signal is intent before order creation).
- A `Trade` is **NOT** a `Position` (a Position represents current open exposure in the market).

A `Trade` is the permanent, historical record of a completed round-trip transaction.

---

## 2. Trade Lifecycle

1. **Entry:** An `ExecutionReport` is received by the Position Engine, establishing a new open Position. The Trade lifecycle formally begins.
2. **Scaling:** Subsequent ExecutionReports might add to the Position. The Trade tracks the average entry price and cumulative size.
3. **Partial Exits:** As partial closures occur, the Trade logs the realized PnL of those fractions.
4. **Final Exit:** The Position size reaches zero.
5. **Closure:** The `Trade` object is finalized, locked, and emitted to the Portfolio Engine.

---

## 3. Contents

### Suggested Fields
- `trade_id`: Unique cryptographic identifier for the trade lifecycle.
- `position_id`: Reference to the open position that spawned this trade.
- `entry_time`: Timestamp of the first fill.
- `exit_time`: Timestamp of the final fill closing the position.
- `entry_price`: Volume-weighted average price (VWAP) of all entry fills.
- `exit_price`: Volume-weighted average price (VWAP) of all exit fills.
- `direction`: `LONG` or `SHORT`.
- `size`: The maximum volume achieved during the trade.
- `risk`: Initial capital risked (distance to stop loss).
- `reward`: Final realized PnL.
- `R_multiple`: The standardized return relative to initial risk.
- `MFE`: Maximum Favorable Excursion (highest floating profit achieved).
- `MAE`: Maximum Adverse Excursion (deepest floating loss suffered).
- `PnL`: Net profit/loss in account currency.
- `duration`: Total time the position was open.
- `commissions`: Total commissions paid across all legs.
- `swap`: Total overnight financing paid/earned.

---

## 4. Ownership and Immutability

- **Created by:** The Position Engine (manages the open state until closure).
- **Read by:** The Portfolio Engine (to update closed equity and balance).
- **Read by:** Analytics (for strategy evaluation and TCA).
- **Read by:** Research (for walk-forward validation and Monte Carlo).

### Permanent Historical Record
Once a position closes, the resulting `Trade` object becomes completely immutable. It is archived into the simulation ledger as a permanent historical record. It can never be modified, ensuring trade history is a perfect, auditable source of truth.
