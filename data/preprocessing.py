"""
=========================================================
APEX Quant Research Framework

Module      : preprocessing.py
Version     : 1.0

Description :
Market data preprocessing.

Responsible for cleaning and standardising raw OHLCV
data before feature engineering.

Author      : APEX
=========================================================
"""

# ==========================================================
# Imports
# ==========================================================

import numpy as np
import pandas as pd

from config.constants import (
    OPEN,
    HIGH,
    LOW,
    CLOSE,
    VOLUME,
)

# ==========================================================
# Helper Functions
# ==========================================================

def sort_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort dataframe by datetime index.
    """
    return df.sort_index()


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicated timestamps.
    """
    return df.loc[~df.index.duplicated(keep="first")]


def remove_missing_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with missing OHLC values.
    """
    required = [OPEN, HIGH, LOW, CLOSE]

    return df.dropna(subset=required)


def enforce_numeric_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert market columns to numeric.
    """

    columns = [OPEN, HIGH, LOW, CLOSE]

    if VOLUME in df.columns:
        columns.append(VOLUME)

    for col in columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df


def fill_volume(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing volume with zero.
    """

    if VOLUME in df.columns:

        df[VOLUME] = (
            df[VOLUME]
            .fillna(0)
        )

    return df


# ==========================================================
# Main Pipeline
# ==========================================================

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Complete preprocessing pipeline.
    """

    df = sort_data(df)

    df = remove_duplicates(df)

    df = enforce_numeric_types(df)

    df = remove_missing_rows(df)

    df = fill_volume(df)

    df = df.reset_index(drop=False)

    df = df.set_index(df.columns[0])

    return df


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("APEX Preprocessing v1.0")