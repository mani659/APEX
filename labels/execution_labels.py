"""
=========================================================
APEX Quant Research Framework

Module      : execution_labels.py
Version     : 1.0

Description :
Execution quality labels.

Author      : APEX
=========================================================
"""

import pandas as pd

from config.constants import (
    HIGH,
    LOW,
    CLOSE,
    LOOKAHEAD_BARS,
)


def build_execution_labels(df: pd.DataFrame) -> pd.DataFrame:

    out = pd.DataFrame(index=df.index)

    close = df[CLOSE]

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

    out["reward_risk"] = (
        (future_high - close) /
        (close - future_low).replace(0, pd.NA)
    )

    out["good_execution"] = (
        out["reward_risk"] > 2.0
    ).astype("int8")

    return out


if __name__ == "__main__":

    print("Execution Labels v1.0")