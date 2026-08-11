"""
=========================================================
APEX Quant Research Framework

indicators.py

Master Feature Pipeline

This module orchestrates all feature engineering.

NO calculations should be implemented here.

=========================================================
"""

from __future__ import annotations

import pandas as pd

# =========================================================
# FEATURE MODULES
# =========================================================

from data.features.price import add_price_features
from data.features.volatility import add_volatility_features
from data.features.trend import add_trend_features


# =========================================================
# PUBLIC API
# =========================================================

def add_indicators(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Master feature engineering pipeline.

    Every feature module is executed
    in dependency order.

    Layer 1 : Price Geometry

    Layer 2 : Volatility

    Layer 3 : Trend

    Layer 4 : Momentum

    Layer 5 : Structure

    Layer 6 : Regime

    Layer 7 : Execution

    Layer 8 : Labels
    """

    print("Adding Price Features...")
    df = add_price_features(df)

    print("Adding Volatility Features...")
    df = add_volatility_features(df)

    print("Adding Trend Features...")
    df = add_trend_features(df)

    # ----------------------------------------------------
    # Future Layers
    # ----------------------------------------------------

    #
    # df = add_momentum_features(df)
    #
    # df = add_structure_features(df)
    #
    # df = add_regime_features(df)
    #
    # df = add_execution_features(df)
    #
    # df = add_labels(df)
    #

    return df


# =========================================================
# STANDALONE TEST
# =========================================================

if __name__ == "__main__":

    from config.settings import DEFAULT_SYMBOL
    from data.loader import load_symbol

    print("=" * 60)
    print("APEX FEATURE PIPELINE")
    print("=" * 60)

    df = load_symbol(DEFAULT_SYMBOL)

    print()

    print(f"Loaded {len(df):,} rows")

    print()

    df = add_indicators(df)

    print()

    print("=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

    print()

    print(f"Total Columns : {len(df.columns)}")

    print()

    print(df.columns.tolist())

    print()

    print(df.head())