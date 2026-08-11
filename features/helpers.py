"""
=========================================================
APEX Quant Research Framework
helpers.py

Reusable mathematical helper functions.

These functions NEVER add columns directly.

They only return Series/DataFrames.

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# --------------------------------------------------------
# True Range
# --------------------------------------------------------

def true_range(df: pd.DataFrame) -> pd.Series:

    prev_close = df["close"].shift(1)

    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    return tr


# --------------------------------------------------------
# Rolling ATR
# --------------------------------------------------------

def atr(
    df: pd.DataFrame,
    period: int = 14,
) -> pd.Series:

    tr = true_range(df)

    return tr.rolling(
        period,
        min_periods=period,
    ).mean()


# --------------------------------------------------------
# Log Return
# --------------------------------------------------------

def log_return(close: pd.Series) -> pd.Series:

    return np.log(close / close.shift(1))


# --------------------------------------------------------
# Simple Return
# --------------------------------------------------------

def pct_return(
    close: pd.Series,
    periods: int = 1,
) -> pd.Series:

    return close.pct_change(periods)


# --------------------------------------------------------
# Rolling Volatility
# --------------------------------------------------------

def rolling_volatility(
    returns: pd.Series,
    period: int,
) -> pd.Series:

    return returns.rolling(
        period,
        min_periods=period,
    ).std()


# --------------------------------------------------------
# Rolling Variance
# --------------------------------------------------------

def rolling_variance(
    returns: pd.Series,
    period: int,
) -> pd.Series:

    return returns.rolling(
        period,
        min_periods=period,
    ).var()


# --------------------------------------------------------
# Rolling Mean
# --------------------------------------------------------

def rolling_mean(
    series: pd.Series,
    period: int,
) -> pd.Series:

    return series.rolling(
        period,
        min_periods=period,
    ).mean()


# --------------------------------------------------------
# Safe Division
# --------------------------------------------------------

def safe_divide(
    numerator,
    denominator,
):

    return np.where(
        denominator != 0,
        numerator / denominator,
        np.nan,
    )