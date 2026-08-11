"""
=========================================================
APEX Quant Research Framework
momentum.py

Momentum State Engine

Public API

    df = add_momentum_features(df)

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .helpers import safe_divide


# ==========================================================
# INTERNAL FUNCTIONS
# ==========================================================

def rsi(close: pd.Series, period: int = 14) -> pd.Series:

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    rs = safe_divide(avg_gain, avg_loss)

    return 100 - (100 / (1 + rs))


def ema(series, period):
    return series.ewm(
        span=period,
        adjust=False
    ).mean()


def macd(close):

    ema12 = ema(close, 12)
    ema26 = ema(close, 26)

    macd_line = ema12 - ema26

    signal = ema(macd_line, 9)

    hist = macd_line - signal

    return macd_line, signal, hist


def roc(close, period):

    return (
        close / close.shift(period) - 1
    ) * 100


# ==========================================================
# PUBLIC API
# ==========================================================

def add_momentum_features(
    df: pd.DataFrame
):

    features = pd.DataFrame(index=df.index)

    # ------------------------------------------------------
    # RSI
    # ------------------------------------------------------

    for p in [7, 14, 21]:

        features[f"rsi_{p}"] = rsi(
            df["close"],
            p
        )

    # ------------------------------------------------------
    # RSI Momentum
    # ------------------------------------------------------

    features["rsi_velocity"] = (
        features["rsi_14"]
        - features["rsi_14"].shift(1)
    )

    features["rsi_acceleration"] = (
        features["rsi_velocity"]
        - features["rsi_velocity"].shift(1)
    )

    # ------------------------------------------------------
    # ROC
    # ------------------------------------------------------

    for p in [5, 10, 20]:

        features[f"roc_{p}"] = roc(
            df["close"],
            p
        )

    # ------------------------------------------------------
    # Momentum
    # ------------------------------------------------------

    for p in [5, 10, 20]:

        features[f"momentum_{p}"] = (
            df["close"]
            - df["close"].shift(p)
        )

    # ------------------------------------------------------
    # MACD
    # ------------------------------------------------------

    macd_line, signal, hist = macd(
        df["close"]
    )

    features["macd"] = macd_line

    features["macd_signal"] = signal

    features["macd_hist"] = hist

    # ------------------------------------------------------
    # Histogram Expansion
    # ------------------------------------------------------

    features["macd_hist_delta"] = (
        hist
        - hist.shift(1)
    )

    # ------------------------------------------------------
    # Consecutive Up Bars
    # ------------------------------------------------------

    up = (
        df["close"] >
        df["close"].shift(1)
    ).astype(int)

    down = (
        df["close"] <
        df["close"].shift(1)
    ).astype(int)

    features["up_streak"] = (
        up.groupby(
            (up == 0).cumsum()
        ).cumsum()
    )

    features["down_streak"] = (
        down.groupby(
            (down == 0).cumsum()
        ).cumsum()
    )

    # ------------------------------------------------------
    # Acceleration
    # ------------------------------------------------------

    features["price_velocity"] = (
        df["close"]
        - df["close"].shift(1)
    )

    features["price_acceleration"] = (
        features["price_velocity"]
        - features["price_velocity"].shift(1)
    )

    # ------------------------------------------------------
    # Exhaustion
    # ------------------------------------------------------

    features["bull_exhaustion"] = (
        (features["rsi_14"] > 75)
        &
        (features["macd_hist_delta"] < 0)
    ).astype(np.int8)

    features["bear_exhaustion"] = (
        (features["rsi_14"] < 25)
        &
        (features["macd_hist_delta"] > 0)
    ).astype(np.int8)

    # ------------------------------------------------------
    # Momentum Strength
    # ------------------------------------------------------

    score = 0

    score += (
        features["rsi_14"] > 50
    ).astype(int)

    score += (
        features["macd"] > 0
    ).astype(int)

    score += (
        features["macd_hist"] > 0
    ).astype(int)

    score += (
        features["roc_10"] > 0
    ).astype(int)

    score += (
        features["price_velocity"] > 0
    ).astype(int)

    features["momentum_strength"] = score

    return features

# ==========================================================
# Compatibility Wrapper
# ==========================================================

def build_momentum_features(df):
    """
    Compatibility wrapper for the APEX Feature Registry.
    """
    return add_momentum_features(df)

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
    from data.features.price import add_price_features
    from data.features.volatility import add_volatility_features
    from data.features.trend import add_trend_features

    df = load_symbol(DEFAULT_SYMBOL)

    df = add_price_features(df)
    df = add_volatility_features(df)
    df = add_trend_features(df)
    df = add_momentum_features(df)

    print("=" * 60)
    print("MOMENTUM FEATURES")
    print("=" * 60)

    print(df.tail())

    cols = [
        c for c in df.columns
        if (
            "rsi" in c
            or "roc" in c
            or "macd" in c
            or "momentum" in c
            or "velocity" in c
            or "acceleration" in c
            or "streak" in c
            or "exhaustion" in c
        )
    ]

    print()
    print(f"Momentum Features : {len(cols)}")
    print(cols)