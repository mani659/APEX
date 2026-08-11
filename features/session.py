"""
=========================================================
APEX Quant Research Framework

Module      : session.py
Description : Session Features
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ==========================================================
# PUBLIC API
# ==========================================================

def add_session_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Build session-based features.

    Supports either:
        - datetime column
        - timestamp column
        - DatetimeIndex
    """

    feat = pd.DataFrame(index=df.index)

    # ------------------------------------------------------
    # Locate datetime source
    # ------------------------------------------------------

    if "datetime" in df.columns:

        ts = pd.to_datetime(df["datetime"])

    elif "timestamp" in df.columns:

        ts = pd.to_datetime(df["timestamp"])

    elif isinstance(df.index, pd.DatetimeIndex):

        ts = pd.Series(df.index, index=df.index)

    else:

        raise ValueError(
            "Session features require a 'datetime' column, "
            "'timestamp' column, or DatetimeIndex."
        )

    # ------------------------------------------------------
    # Calendar Features
    # ------------------------------------------------------

    hour = ts.dt.hour.astype(np.int8)

    feat["hour"] = hour
    feat["weekday"] = ts.dt.weekday.astype(np.int8)
    feat["month"] = ts.dt.month.astype(np.int8)

    # ------------------------------------------------------
    # Trading Sessions (UTC)
    # ------------------------------------------------------

    feat["asian"] = (
        (hour >= 0) &
        (hour < 8)
    ).astype(np.int8)

    feat["london"] = (
        (hour >= 8) &
        (hour < 16)
    ).astype(np.int8)

    feat["newyork"] = (
        (hour >= 13) &
        (hour < 21)
    ).astype(np.int8)

    feat["overlap"] = (
        (hour >= 13) &
        (hour < 16)
    ).astype(np.int8)

    return feat


# ==========================================================
# Compatibility Wrapper
# ==========================================================

def build_session_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    return add_session_features(df)