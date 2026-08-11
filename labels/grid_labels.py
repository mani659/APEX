"""
=========================================================
APEX Quant Research Framework
Module      : grid_labels.py
Version     : 1.0
=========================================================
"""

import pandas as pd

from config.constants import (
    HIGH,
    LOW,
    CLOSE,
    LOOKAHEAD_BARS,
)


def build_grid_labels(df: pd.DataFrame) -> pd.DataFrame:

    out = pd.DataFrame(index=df.index)

    future_high = (
        df[HIGH]
        .rolling(LOOKAHEAD_BARS)
        .max()
        .shift(-LOOKAHEAD_BARS)
    )

    future_low = (
        df[LOW]
        .rolling(LOOKAHEAD_BARS)
        .min()
        .shift(-LOOKAHEAD_BARS)
    )

    close = df[CLOSE]

    out["future_max_up"] = (
        future_high - close
    ) / close

    out["future_max_down"] = (
        future_low - close
    ) / close

    out["grid_expansion"] = (
        out["future_max_up"]
        - out["future_max_down"]
    )

    return out