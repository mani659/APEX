# RC015 Study 007 - Corrected Data Acquisition Manifest

## 1. Scope & Definitions
- **Historical Range**: 2022-01-01 through 2026-06-30
- **Observation**: Wednesday (~2 DTE)
- **Expiry**: Friday
- **Option Roots**: Friday weekly (1EU, 2EU, 3EU, 4EU, 5EU) and Monthly (EUU)
- **Futures**: CME Euro FX (6E)
- **Schema**: BBO-1m
- **Spot RV**: Canonical data/m1/EURUSD_M1.parquet (No new spot data required)

## 2. Near-ATM Rule
bs(strike - futures_mid) <= 0.0020 applied at contemporaneous observation.

## 3. Sample Size Statistics
- **Total Calendar Fridays**: 234
- **Holiday/Missing Exclusions**: 12
- **Final Qualifying Observation Events**: 222

## 4. Cost & Volume Estimate
- **Qualifying Event Count**: 222
- **Option Data Days**: ~3 days per event (Wed-Fri)
- **Futures Data Days**: ~3 days per event (Wed-Fri)
- **Expected Parent Requests**: 6E.OPT for Options, 6E for Futures.
- **Approximate Data Volume**: ~9.3 GB compressed total
- **Approximate Cost**: PORTAL-ESTIMATED COST: PENDING MANUAL REQUEST

*See RC015_Study_007_Final_Acquisition_Scope.md for the exact mapped schedule.*