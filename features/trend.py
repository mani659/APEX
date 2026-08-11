"""
=========================================================
APEX Quant Research Framework
trend.py

Trend State Engine

Public API

    df = add_trend_features(df)

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .helpers import safe_divide


# ==========================================================
# INTERNAL FUNCTIONS
# ==========================================================

def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(
        span=period,
        adjust=False,
    ).mean()


def rolling_zscore(series: pd.Series, window: int):

    mean = series.rolling(window).mean()

    std = series.rolling(window).std()

    return safe_divide(
        series - mean,
        std,
    )


def rolling_slope(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Fast rolling linear regression slope.

    Uses numpy.polyfit with raw=True to avoid creating
    pandas Series objects for every rolling window.

    Returns
    -------
    pd.Series
    """

    x = np.arange(window, dtype=np.float64)

    def slope(values):

        if np.isnan(values).any():
            return np.nan

        return np.polyfit(x, values, 1)[0]

    return series.rolling(
        window=window,
        min_periods=window,
    ).apply(
        slope,
        raw=True,          # <-- IMPORTANT
    )


# ==========================================================
# PUBLIC API
# ==========================================================

def add_trend_features(df: pd.DataFrame):

    features = pd.DataFrame(index=df.index)

    EMA_PERIODS = [10, 20, 50, 100, 200]

    # ------------------------------------------------------
    # EMA
    # ------------------------------------------------------

    for p in EMA_PERIODS:

        features[f"ema_{p}"] = ema(
            df["close"],
            p,
        )

    # ------------------------------------------------------
    # EMA Distance
    # ------------------------------------------------------

    for p in EMA_PERIODS:

        features[f"ema_dist_{p}"] = safe_divide(
            df["close"] - features[f"ema_{p}"],
            features[f"ema_{p}"],
        )

    # ------------------------------------------------------
    # EMA Slope
    # ------------------------------------------------------

    for p in EMA_PERIODS:

        features[f"ema_slope_{p}"] = (
            features[f"ema_{p}"]
            - features[f"ema_{p}"].shift(1)
        )

    # ------------------------------------------------------
    # EMA Stack
    # ------------------------------------------------------

    features["ema_stack_bull"] = (
        (features["ema_10"] > features["ema_20"])
        &
        (features["ema_20"] > features["ema_50"])
        &
        (features["ema_50"] > features["ema_100"])
        &
        (features["ema_100"] > features["ema_200"])
    ).astype(np.int8)

    features["ema_stack_bear"] = (
        (features["ema_10"] < features["ema_20"])
        &
        (features["ema_20"] < features["ema_50"])
        &
        (features["ema_50"] < features["ema_100"])
        &
        (features["ema_100"] < features["ema_200"])
    ).astype(np.int8)

    # ------------------------------------------------------
    # VWAP
    # ------------------------------------------------------

    tp = (
        df["high"]
        + df["low"]
        + df["close"]
    ) / 3

    cumulative_volume = df["volume"].cumsum()

    cumulative_tp = (
        tp * df["volume"]
    ).cumsum()

    features["vwap"] = safe_divide(
        cumulative_tp,
        cumulative_volume,
    )

    # ------------------------------------------------------
    # VWAP Distance
    # ------------------------------------------------------

    features["vwap_distance"] = safe_divide(
        df["close"] - features["vwap"],
        features["vwap"],
    )

    # ------------------------------------------------------
    # Rolling ZScore
    # ------------------------------------------------------

    for p in [20, 50, 100]:

        features[f"zscore_{p}"] = rolling_zscore(
            df["close"],
            p,
        )

    # ------------------------------------------------------
    # Linear Regression Slope
    # ------------------------------------------------------

    for p in [20, 50, 100]:

        features[f"trend_slope_{p}"] = rolling_slope(
            df["close"],
            p,
        )

    # ------------------------------------------------------
    # Trend Strength Score
    # ------------------------------------------------------

    score = 0

    score += (
        df["close"] > features["ema_20"]
    ).astype(int)

    score += (
        features["ema_20"] > features["ema_50"]
    ).astype(int)

    score += (
        features["ema_50"] > features["ema_200"]
    ).astype(int)

    score += (
        features["ema_slope_20"] > 0
    ).astype(int)

    score += (
        features["ema_slope_50"] > 0
    ).astype(int)

    score += (
        features["vwap_distance"] > 0
    ).astype(int)

    features["trend_strength"] = score

    return features

# ==========================================================
# Compatibility Wrapper
# ==========================================================

def build_trend_features(df):
    """
    Compatibility wrapper for the APEX Feature Registry.
    """
    print("[Trend] EMA...")
    # EMA code

    print("[Trend] VWAP...")
    # VWAP code

    print("[Trend] Z-Score...")
    # Z-score code

    print("[Trend] Trend Strength...")
    # Trend strength code

    print("[Trend] Done")
    
    return add_trend_features(df)
    
# ==========================================================
# STANDALONE TEST
# ==========================================================

if __name__ == "__main__":

    from pathlib import Path
    import sys

    ROOT = Path(__file__).resolve().parents[2]

    sys.path.insert(0, str(ROOT))

    from config.settings import DEFAULT_SYMBOL
    from data.loader import load_symbol

    from data.features.price import (
        add_price_features,
    )

    from data.features.volatility import (
        add_volatility_features,
    )

    df = load_symbol(DEFAULT_SYMBOL)

    df = add_price_features(df)

    df = add_volatility_features(df)

    df = add_trend_features(df)

    print("=" * 60)
    print("TREND FEATURES")
    print("=" * 60)

    print(df.head())

    print()

    print("Trend Features Added")

    cols = [
        c
        for c in df.columns
        if
        c.startswith("ema")
        or
        c.startswith("trend")
        or
        c.startswith("zscore")
        or
        c == "vwap"
        or
        c == "vwap_distance"
    ]

    print(cols)

    print()

    print(
        "Trend Feature Count:",
        len(cols),
    )