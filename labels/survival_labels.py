"""
=========================================================
APEX Quant Research Framework
Module      : survival_labels.py
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


def build_survival_labels(df: pd.DataFrame) -> pd.DataFrame:

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

    out["mae"] = (
        future_low - close
    ) / close

    out["mfe"] = (
        future_high - close
    ) / close

    out["survived"] = (
        out["mae"] > -0.01
    ).astype("int8")

    return out