# RC011 Study 001 — Microstructure Data Qualification

## 1. Data Inventory
An audit of the Apex research repository was conducted on the existing data sources for EURUSD.
- **Available Datasets**: `data/m1/EURUSD_M1.parquet`, `data/m1/EURUSD_M1.csv`, and monthly CSV fragments in `data/m1/EUR`.
- **File Formats**: `.parquet` and `.csv`.
- **Timestamp Precision**: 1-minute boundaries (`YYYY-MM-DD HH:MM:00`).
- **Available Fields**: `timestamp`, `open`, `high`, `low`, `close`, `volume`.

## 2. Provenance
The data is derived from MetaTrader 5 historical archives (indicated by the `MQL5\Ticks Data` path structure). It consists of broker-provided M1 OHLCV bars, typical of retail CFD/FX data, rather than raw exchange-level matching engine data (such as EBS or Reuters matching for FX).

## 3. Field Availability
Based on the required information for an order-flow study:
- **timestamped trades**: UNAVAILABLE
- **trade price**: UNAVAILABLE (only minute-level boundaries)
- **trade size / volume**: UNAVAILABLE (true traded volume is missing)
- **bid**: UNAVAILABLE
- **ask**: UNAVAILABLE
- **tick direction**: UNAVAILABLE
- **aggressor side / trade side**: UNAVAILABLE
- **spread**: UNAVAILABLE
- **sufficient timestamp precision**: UNAVAILABLE (1-minute resolution cannot support microstructure)
- **continuous chronological coverage**: AVAILABLE DIRECTLY (continuous at the 1-minute scale, excluding weekends).

## 4. Volume Semantics
**LIMITATION**: The `volume` field represents **broker tick volume** (the number of price quote updates received by the MT5 terminal during that minute). It does **NOT** represent actual traded volume, institutional order flow, or true market liquidity. There is no reliable mechanism to map broker tick volume to executed sizes. 

## 5. Trade-Direction Capability
**Aggressor direction cannot be obtained directly.** 
Furthermore, it **cannot be deterministically reconstructed** because we lack intra-minute tick prices and bid/ask quote updates. Any attempt to derive direction (e.g., using `close - open` to signify buy/sell dominance) would merely be a mathematical restatement of the price candle itself, explicitly violating the requirement for true order-flow isolation. Therefore, deriving trade-direction from this dataset is **impossible**.

## 6. Exact Requirement Capabilities (RC011 Variables)
- **Aggressor Imbalance**: Impossible.
- **Volume Imbalance**: Impossible.
- **Trade Intensity**: Approximate (tick volume acts as a poor proxy for quote intensity, not trade intensity).
- **Spread State**: Impossible.
- **Price Response to Flow**: Impossible.

## 7. Data Quality Tests (Coverage Analysis)
- **Study Period**: 2021-01-04 00:00:00 to 2026-06-30 23:59:00
- **Total Records**: 2,041,613 M1 bars
- **Records per day**: ~1020 (consistent with active 24/5 trading)
- **Duplicate Records**: 0
- **Missing Periods**: 844,147 missing minutes, completely attributable to expected FX weekend gaps and holidays.
- **Invalid Prices**: 0 (all Open/Close remain within High/Low bounds).
- **Negative/Zero Volume**: 10 records found with <= 0 volume.
- **Impossible Spreads**: N/A (no spread data).

## 8. Research Suitability
The currently available EURUSD M1 dataset is perfectly suitable for the macroscopic, state-based, and structural behavioral discovery tested in RC001–RC010. However, it completely lacks the resolution, depth, and semantics necessary to calculate true order-flow metrics. 

Attempting to run a microstructure study using 1-minute OHLCV tick-volume data would violate the scientific integrity of the campaign.

## 9. Final Classification
**D — INSUFFICIENT**
The data cannot support a scientifically credible microstructure experiment.

## 10. Recommendation for RC011 Study 002
**DO NOT PROCEED with statistical experiments.**

**What is missing:** 
True Level 1 (Top of Book) tick data including Bid, Ask, Traded Price, Traded Size, and exact timestamping (millisecond/microsecond).

**Why it matters:** 
Without top-of-book dynamics, we cannot determine aggressor side (imbalance) or calculate spread dynamics. Without true volume, we cannot gauge liquidity consumption.

**Minimum Dataset Required:** 
A Level 1 historical tick dataset for EURUSD from a reputable institutional aggregator (e.g., TrueFX, Dukascopy tick data, or a primary ECN like EBS/Reuters) containing:
`[Timestamp (ms), Bid, Ask, DealPrice, DealVolume, DealDirection]`

**Next Step:**
RC011 Study 002 should focus exclusively on sourcing, acquiring, and parsing an appropriate institutional tick-level dataset for EURUSD before attempting to generate any features or run any predictive baselines. Do not attempt to synthesize order-flow from the existing M1 Parquet files.
