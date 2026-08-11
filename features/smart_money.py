"""
=========================================================
APEX Quant Research Framework

Module  : smart_money.py
Version : 2.0
=========================================================
"""

import numpy as np
import pandas as pd

from config.constants import OPEN, HIGH, LOW, CLOSE


def build_smart_money_features(df):

    feat = pd.DataFrame(index=df.index)

    feat["bull_fvg"] = (
        df[LOW] >
        df[HIGH].shift(2)
    ).astype(np.int8)

    feat["bear_fvg"] = (
        df[HIGH] <
        df[LOW].shift(2)
    ).astype(np.int8)

    feat["bull_displacement"] = (
        (df[CLOSE]-df[OPEN]) >
        (
            df[HIGH]-df[LOW]
        )*0.70
    ).astype(np.int8)

    feat["bear_displacement"] = (
        (df[OPEN]-df[CLOSE]) >
        (
            df[HIGH]-df[LOW]
        )*0.70
    ).astype(np.int8)

    feat["liquidity_sweep_high"] = (
        (df[HIGH] > df[HIGH].shift(1)) &
        (df[CLOSE] < df[HIGH].shift(1))
    ).astype(np.int8)

    feat["liquidity_sweep_low"] = (
        (df[LOW] < df[LOW].shift(1)) &
        (df[CLOSE] > df[LOW].shift(1))
    ).astype(np.int8)

    return feat


if __name__ == "__main__":
    print("smart_money.py v2.0")