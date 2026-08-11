"""
=========================================================
APEX
loader.py

Purpose
-------
Load broker M1 CSV files into a standardized DataFrame.

Responsibilities
----------------
✓ Read CSV
✓ Standardize column names
✓ Convert datetime
✓ Convert numeric columns
✓ Sort chronologically
✓ Remove duplicate timestamps

Output Columns
--------------
datetime
open
high
low
close
volume

Nothing else.

Cleaning, validation and feature engineering belong to
validator.py and indicators.py.
=========================================================
"""

from pathlib import Path
import sys
import pandas as pd

# =========================================================
# Locate project root
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (
    SYMBOL_FILES,
    DEFAULT_SYMBOL,
)

# =========================================================
# Column aliases
# =========================================================

COLUMN_ALIASES = {

    # datetime
    "Datetime": "datetime",
    "datetime": "datetime",
    "DATE": "datetime",
    "date": "datetime",
    "Time": "datetime",
    "time": "datetime",
    
    "timestamp": "datetime",
    "Timestamp": "datetime",
    "TIMESTAMP": "datetime",
    
    "DateTime": "datetime",
    "DATE_TIME": "datetime",

    # OHLC
    "Open": "open",
    "OPEN": "open",
    "open": "open",

    "High": "high",
    "HIGH": "high",
    "high": "high",

    "Low": "low",
    "LOW": "low",
    "low": "low",

    "Close": "close",
    "CLOSE": "close",
    "close": "close",

    # Volume
    "Volume": "volume",
    "TickVolume": "volume",
    "tick_volume": "volume",
    "volume": "volume"
}

# =========================================================
# Required columns
# =========================================================

REQUIRED_COLUMNS = [
    "datetime",
    "open",
    "high",
    "low",
    "close",
    "volume"
]

# =========================================================
# Loader
# =========================================================

def load_csv(csv_path):
    """
    Load a broker CSV and return a standardized DataFrame.

    Parameters
    ----------
    csv_path : str | Path

    Returns
    -------
    pandas.DataFrame
    """

    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found:\n{csv_path}")

    print("=" * 60)
    print("APEX DATA LOADER")
    print("=" * 60)
    print(f"Loading : {csv_path.name}")

    df = pd.read_csv(csv_path)

    # -----------------------------------------------------
    # Rename columns
    # -----------------------------------------------------

    df.rename(columns=COLUMN_ALIASES, inplace=True)

    # -----------------------------------------------------
    # Verify required columns
    # -----------------------------------------------------

    missing = [
        c for c in REQUIRED_COLUMNS
        if c not in df.columns
    ]

    if missing:

        raise Exception(
            "\n"
            "Missing required columns\n\n"
            f"Missing : {missing}\n\n"
            f"Available :\n{list(df.columns)}"
        )

    # -----------------------------------------------------
    # Datetime
    # -----------------------------------------------------

    df["datetime"] = pd.to_datetime(
        df["datetime"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # Numeric
    # -----------------------------------------------------

    numeric_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # -----------------------------------------------------
    # Remove rows that failed parsing
    # -----------------------------------------------------

    df.dropna(
        subset=REQUIRED_COLUMNS,
        inplace=True
    )

    # -----------------------------------------------------
    # Sort
    # -----------------------------------------------------

    df.sort_values(
        "datetime",
        inplace=True
    )

    # -----------------------------------------------------
    # Remove duplicate timestamps
    # -----------------------------------------------------

    before = len(df)

    df.drop_duplicates(
        subset="datetime",
        keep="last",
        inplace=True
    )

    duplicates_removed = before - len(df)

    # -----------------------------------------------------
    # Reset index
    # -----------------------------------------------------

    df.reset_index(
        drop=True,
        inplace=True
    )

    print(f"Rows Loaded        : {len(df):,}")
    print(f"Duplicates Removed : {duplicates_removed:,}")
    print(f"Start Date         : {df.datetime.iloc[0]}")
    print(f"End Date           : {df.datetime.iloc[-1]}")

    return df

# =========================================================
# Convenience loader
# =========================================================

def load_data(symbol=DEFAULT_SYMBOL):
    """
    Load a symbol defined in config.py.

    Example
    -------
    df = load_symbol("XAUUSD")
    """

    symbol = symbol.upper()

    if symbol not in SYMBOL_FILES:
        raise ValueError(
            f"Unknown symbol: {symbol}\n"
            f"Available: {list(SYMBOL_FILES.keys())}"
        )

    return load_csv(SYMBOL_FILES[symbol])

# ==========================================================
# Compatibility API
# ==========================================================

def load_symbol(symbol=DEFAULT_SYMBOL):
    """
    Backward compatibility wrapper.

    Legacy modules call:

        load_symbol()

    New framework uses:

        load_data()

    Both resolve to the same implementation.
    """

    return load_data(symbol)