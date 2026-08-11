"""
=========================================================
APEX Quant Research Framework
Module      : future_returns.py
Version     : 1.0
=========================================================
"""

import pandas as pd

from config.constants import CLOSE, LOOKAHEAD_BARS


def build_future_return_labels(df: pd.DataFrame) -> pd.DataFrame:

    close = df[CLOSE]

    out = pd.DataFrame(index=df.index)

    future_close = close.shift(-LOOKAHEAD_BARS)

    out["future_return"] = (
        (future_close - close) / close
    )

    out["future_direction"] = (
        out["future_return"] > 0
    ).astype("int8")

    out["future_up"] = (
        out["future_return"] > 0.002
    ).astype("int8")

    out["future_down"] = (
        out["future_return"] < -0.002
    ).astype("int8")

    return out