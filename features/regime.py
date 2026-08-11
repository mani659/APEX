"""
=========================================================
APEX Quant Research Framework

Module  : regime.py
Version : 2.0
=========================================================
"""

import numpy as np
import pandas as pd

from config.constants import CLOSE


def build_regime_features(df):

    feat = pd.DataFrame(index=df.index)

    ret = df[CLOSE].pct_change()

    feat["return"] = ret

    feat["rolling_mean20"] = (
        ret.rolling(
            20,
            min_periods=1
        ).mean()
    )

    feat["regime_std20"] = (
        ret.rolling(
            20,
            min_periods=1
        ).std()
    )

    feat["regime_strength"] = (
        feat["rolling_mean20"] /
        feat["regime_std20"]
    )

    feat["high_volatility"] = (
        feat["regime_std20"] >
        feat["regime_std20"].rolling(
            100,
            min_periods=1
        ).median()
    ).astype(np.int8)

    return feat


if __name__ == "__main__":
    print("regime.py v2.0")