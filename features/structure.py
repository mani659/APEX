"""
=========================================================
APEX Quant Research Framework

Module  : structure.py
Version : 2.0
=========================================================
"""

import numpy as np
import pandas as pd

from config.constants import HIGH, LOW


def build_structure_features(df: pd.DataFrame) -> pd.DataFrame:

    feat = pd.DataFrame(index=df.index)

    high = df[HIGH]
    low = df[LOW]

    feat["higher_high"] = (
        high > high.shift(1)
    ).astype(np.int8)

    feat["lower_high"] = (
        high < high.shift(1)
    ).astype(np.int8)

    feat["higher_low"] = (
        low > low.shift(1)
    ).astype(np.int8)

    feat["lower_low"] = (
        low < low.shift(1)
    ).astype(np.int8)

    feat["swing_high"] = (
        (high > high.shift(1)) &
        (high > high.shift(-1))
    ).astype(np.int8)

    feat["swing_low"] = (
        (low < low.shift(1)) &
        (low < low.shift(-1))
    ).astype(np.int8)

    feat["market_structure"] = (
        feat["higher_high"] +
        feat["higher_low"] -
        feat["lower_high"] -
        feat["lower_low"]
    )

    return feat


if __name__ == "__main__":
    print("structure.py v2.0")