"""
=========================================================
APEX Quant Research Framework

Module  : volatility.py
Version : 2.0
=========================================================
"""

import pandas as pd

from config.constants import (
    HIGH,
    LOW,
    CLOSE,
    ATR_PERIOD,
)


def build_volatility_features(df: pd.DataFrame) -> pd.DataFrame:

    feat = pd.DataFrame(index=df.index)

    prev_close = df[CLOSE].shift(1)

    tr = pd.concat(
        [
            df[HIGH] - df[LOW],
            (df[HIGH] - prev_close).abs(),
            (df[LOW] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    feat["tr"] = tr

    feat["atr"] = (
        tr.rolling(
            ATR_PERIOD,
            min_periods=1
        ).mean()
    )

    feat["atr_pct"] = (
        feat["atr"] /
        df[CLOSE]
    )

    feat["range_pct"] = (
        (df[HIGH] - df[LOW]) /
        df[CLOSE]
    )

    feat["rolling_std20"] = (
        df[CLOSE]
        .rolling(
            20,
            min_periods=1
        )
        .std()
    )

    feat["volatility_expanding"] = (
        feat["atr"] >
        feat["atr"].shift(1)
    ).astype("int8")

    return feat


if __name__ == "__main__":
    print("volatility.py v2.0")