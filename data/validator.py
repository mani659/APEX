"""
=========================================================
APEX
validator.py

Purpose
-------
Validate standardized market data.

This module DOES NOT calculate indicators.
This module DOES NOT modify prices.

It reports data quality before research begins.
=========================================================
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.loader import load_symbol

# =====================================================
# Validator
# =====================================================

def validate(df, timeframe="1min"):

    print("=" * 60)
    print("APEX DATA VALIDATOR")
    print("=" * 60)

    report = {}

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    report["rows"] = len(df)

    if len(df) == 0:
        raise Exception("Dataset is empty.")

    # -------------------------------------------------
    # NaN
    # -------------------------------------------------

    report["nan"] = int(df.isna().sum().sum())

    # -------------------------------------------------
    # Infinite
    # -------------------------------------------------

    numeric = df.select_dtypes(include=np.number)

    report["inf"] = int(np.isinf(numeric).sum().sum())

    # -------------------------------------------------
    # Duplicate timestamps
    # -------------------------------------------------

    report["duplicate_time"] = int(
        df["datetime"].duplicated().sum()
    )

    # -------------------------------------------------
    # Sorted
    # -------------------------------------------------

    report["sorted"] = bool(
        df["datetime"].is_monotonic_increasing
    )

    # -------------------------------------------------
    # Missing candles
    # -------------------------------------------------

    expected = pd.date_range(
        df.datetime.iloc[0],
        df.datetime.iloc[-1],
        freq=timeframe
    )

    report["missing_bars"] = len(expected) - len(df)

    # -------------------------------------------------
    # Weekend bars
    # -------------------------------------------------

    report["weekend"] = int(
        (df.datetime.dt.dayofweek >= 5).sum()
    )

    # -------------------------------------------------
    # OHLC integrity
    # -------------------------------------------------

    bad = (

        (df.high < df.open)

        | (df.high < df.close)

        | (df.low > df.open)

        | (df.low > df.close)

        | (df.high < df.low)

    )

    report["bad_ohlc"] = int(bad.sum())

    # -------------------------------------------------
    # Negative prices
    # -------------------------------------------------

    report["negative"] = int(

        (df[["open", "high", "low", "close"]] <= 0)

        .sum()

        .sum()

    )

    # -------------------------------------------------
    # Date range
    # -------------------------------------------------

    report["start"] = df.datetime.iloc[0]

    report["end"] = df.datetime.iloc[-1]

    # -------------------------------------------------
    # Print summary
    # -------------------------------------------------

    print(f"Rows               : {report['rows']:,}")
    print(f"Start              : {report['start']}")
    print(f"End                : {report['end']}")
    print(f"NaN                : {report['nan']}")
    print(f"Infinite           : {report['inf']}")
    print(f"Duplicate Bars     : {report['duplicate_time']}")
    print(f"Missing Bars       : {report['missing_bars']}")
    print(f"Weekend Bars       : {report['weekend']}")
    print(f"Bad OHLC           : {report['bad_ohlc']}")
    print(f"Negative Prices    : {report['negative']}")
    print(f"Sorted             : {report['sorted']}")

    # -------------------------------------------------
    # Hard failures
    # -------------------------------------------------

    if report["bad_ohlc"] > 0:
        raise Exception("Dataset contains invalid OHLC candles.")

    if report["inf"] > 0:
        raise Exception("Dataset contains infinite values.")

    if not report["sorted"]:
        raise Exception("Dataset is not time sorted.")

    return report


# =====================================================
# Standalone test
# =====================================================

if __name__ == "__main__":

    df = load_symbol()

    validate(df)