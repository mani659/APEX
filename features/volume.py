"""
=========================================================
APEX Quant Research Framework

Module  : volume.py
Version : 2.0
=========================================================
"""

import numpy as np
import pandas as pd

from config.constants import VOLUME


def build_volume_features(df: pd.DataFrame) -> pd.DataFrame:

    feat = pd.DataFrame(index=df.index)

    volume = df[VOLUME].astype(float)

    ma20 = volume.rolling(
        20,
        min_periods=1
    ).mean()

    std20 = volume.rolling(
        20,
        min_periods=1
    ).std()

    feat["volume"] = volume

    feat["volume_ma20"] = ma20

    feat["volume_ratio"] = (
        volume /
        ma20.replace(0, np.nan)
    )

    feat["volume_zscore"] = (
        (volume - ma20) /
        std20.replace(0, np.nan)
    )

    feat["volume_delta"] = (
        volume.diff()
    )

    feat["volume_pct_change"] = (
        volume.pct_change()
    )

    feat["volume_expanding"] = (
        feat["volume_delta"] > 0
    ).astype(np.int8)

    feat["volume_contracting"] = (
        feat["volume_delta"] < 0
    ).astype(np.int8)

    feat["high_volume"] = (
        feat["volume_zscore"] > 2
    ).astype(np.int8)

    feat["low_volume"] = (
        feat["volume_zscore"] < -1
    ).astype(np.int8)

    return feat


if __name__ == "__main__":
    print("volume.py v2.0")