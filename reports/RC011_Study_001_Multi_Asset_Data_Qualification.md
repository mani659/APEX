# RC011 Study 001 — Multi-Asset Data Qualification

## 1. Executive Summary
This study determines whether the existing historical datasets for multiple asset classes contain sufficient order-flow and microstructure information to proceed with RC011. Every available dataset was independently audited for schema completeness, timestamp precision, volume semantics, and microstructure capability.

**Finding:** None of the existing datasets possess the necessary tick-level resolution, true execution volume, or trade-direction flags required for genuine microstructure research. All markets rely on broker-level indicative quote updates with 1-second timestamp rounding, making true order-flow metrics impossible to calculate reliably.

**Recommendation:** RC011 microstructure research must be paused. We must source an institutional Level-1/Level-2 tick dataset before proceeding.

## 2. Asset Inventory
* **EURUSD**: `other/EURUSD_mt5_ticks_2025.csv` and `EURUSD_mt5_ticks_5_year.csv` (1.2 GB+)
* **XAUUSD**: `XAUUSD/XAUUSD_mt5_ticks_*.csv` (4.4 GB+ across multiple fragments)
* **BTCUSD**: `other/BTCUSD_mt5_ticks.csv` (12.7 GB+)
* **Nasdaq**: `other/USATECHIDXUSD_mt5_ticks_21-23.csv` (10.2 GB+)
* **XAGUSD**: M1 OHLCV only (`data/m1/XAGUSD_M1.parquet`). No tick data exists.
* **Oil**: No data available.

## 3. Schema Audit
All available tick datasets (EURUSD, XAUUSD, BTCUSD, Nasdaq) share a MetaTrader 5 tick export format containing exactly 6 columns:
`[Date, Time, Bid, Ask, Last, Flags]`
*   **Time** is restricted to `HH:MM:SS` format.
*   **Volume/Trade Size** is entirely absent from the schema.
*   **Flags** exist (e.g., indicating quote updates) but do not denote true aggressor direction (BUY/SELL).

## 4. Timestamp Qualification
* **EURUSD**: 1-second precision.
* **XAUUSD**: 1-second precision.
* **BTCUSD**: 1-second precision.
* **Nasdaq**: 1-second precision.
* **XAGUSD**: N/A (1-minute).
* **Oil**: N/A.

**Conclusion:** 1-second precision is completely inadequate for tick ordering. Multiple ticks frequently arrive within the same second, making deterministic trade sequencing impossible.

## 5. Volume Semantics
For all assets, **True Traded Volume is UNAVAILABLE**. MT5 exports in these files either omit the volume column entirely or only report broker tick volume (quote update counts). We cannot measure institutional liquidity consumption. 

## 6. Trade-Direction Capability
* **EURUSD**: IMPOSSIBLE
* **XAUUSD**: IMPOSSIBLE
* **BTCUSD**: IMPOSSIBLE
* **Nasdaq**: IMPOSSIBLE
* **XAGUSD**: IMPOSSIBLE
* **Oil**: IMPOSSIBLE

Without BUY/SELL flags or true trade volume, we can only reconstruct the direction of Bid/Ask quote changes, which does not constitute true aggressor trade direction.

## 7. Spread Capability
For all assets with tick data (EURUSD, XAUUSD, BTCUSD, Nasdaq), **Spread is AVAILABLE DIRECTLY** via the `Ask - Bid` calculation for every quote update.

## 8. Order-Flow Capability
For all markets, calculating order-flow dynamics is impossible because the underlying components (trade direction and trade volume) are missing.
*   **Aggressor Imbalance**: IMPOSSIBLE
*   **Volume Imbalance**: IMPOSSIBLE
*   **Trade Intensity**: IMPOSSIBLE (We can only measure Quote Intensity)
*   **Price Response to Flow**: IMPOSSIBLE

## 9. Data Quality Results
*   **Chronological Order**: Ordered down to the second, but intra-second ticks suffer from ambiguous sequencing.
*   **Missing Fields**: Trade Size and true Trade Price are absent.
*   **Timestamp Anomalies**: Heavy clustering at 00-second marks due to rounding/truncation.

## 10. Cross-Asset Capability Matrix
*Please refer to `reports/RC011_Study_001_Data_Capability_Matrix.csv` for the fully tabularized matrix.*

## 11. Final Market Classification
* **EURUSD**: **D — INSUFFICIENT**
* **XAUUSD**: **D — INSUFFICIENT**
* **BTCUSD**: **D — INSUFFICIENT**
* **Nasdaq**: **D — INSUFFICIENT**
* **XAGUSD**: **D — INSUFFICIENT**
* **Oil**: **D — INSUFFICIENT**

## 12. Recommended Primary Market for Study 002
Because all datasets classified as D, **NO market is recommended for immediate statistical experiments**. 

## 13. Data Limitations
The core issue is that the MT5 tick export format provided is merely an aggregated feed of broker quote updates rounded to the nearest second. It does not reflect a centralized matching engine's Order Book or actual executed institutional trades. 

**Next Steps**: RC011 microstructure research must remain paused until we can source an appropriate high-fidelity (millisecond precision, true volume, and side flags) dataset from a provider such as TrueFX or Dukascopy.
