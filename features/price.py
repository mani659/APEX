"""
=========================================================
APEX Quant Research Framework

Module  : price.py
Version : 2.0
=========================================================
"""

import numpy as np
import pandas as pd

from config.constants import OPEN, HIGH, LOW, CLOSE


def build_price_features(df: pd.DataFrame) -> pd.DataFrame:

    feat = pd.DataFrame(index=df.index)

    feat["price"] = df[CLOSE]

    feat["hl2"] = (
        df[HIGH] + df[LOW]
    ) / 2

    feat["hlc3"] = (
        df[HIGH] +
        df[LOW] +
        df[CLOSE]
    ) / 3

    feat["ohlc4"] = (
        df[OPEN] +
        df[HIGH] +
        df[LOW] +
        df[CLOSE]
    ) / 4

    feat["body"] = (
        df[CLOSE] - df[OPEN]
    )

    feat["body_abs"] = (
        feat["body"]
        .abs()
    )

    feat["upper_wick"] = (
        df[HIGH] -
        np.maximum(df[OPEN], df[CLOSE])
    )

    feat["lower_wick"] = (
        np.minimum(df[OPEN], df[CLOSE]) -
        df[LOW]
    )

    feat["range"] = (
        df[HIGH] -
        df[LOW]
    )

    feat["body_pct"] = (
        feat["body"] /
        feat["range"].replace(0, np.nan)
    )

    return feat


if __name__ == "__main__":
    print("price.py v2.0")