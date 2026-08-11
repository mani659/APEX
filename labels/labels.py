"""
=========================================================
APEX Quant Research Framework

Module      : labels.py
Version     : 1.0

Description :
Master Label Builder

Builds all registered labels into a single dataset.

Author      : APEX
=========================================================
"""

# ==========================================================
# Imports
# ==========================================================

import time
import pandas as pd

from labels.future_returns import build_future_return_labels
from labels.grid_labels import build_grid_labels
from labels.survival_labels import build_survival_labels
from labels.execution_labels import build_execution_labels


# ==========================================================
# Registry
# ==========================================================

LABEL_REGISTRY = {

    "future_returns": build_future_return_labels,

    "grid": build_grid_labels,

    "survival": build_survival_labels,

    "execution": build_execution_labels,

}


# ==========================================================
# Main Builder
# ==========================================================

def build_labels(
    df: pd.DataFrame,
    verbose: bool = True
) -> pd.DataFrame:

    label_frames = []

    start = time.time()

    for name, builder in LABEL_REGISTRY.items():

        if verbose:
            print(f"Building {name}...")

        t0 = time.time()

        lbl = builder(df)

        elapsed = time.time() - t0

        if verbose:
            print(
                f"   {lbl.shape[1]} columns "
                f"({elapsed:.2f} sec)"
            )

        label_frames.append(lbl)

    labels = pd.concat(
        label_frames,
        axis=1
    )

    total = time.time() - start

    if verbose:

        print()

        print("=" * 50)

        print("Label Build Complete")

        print("=" * 50)

        print(f"Modules : {len(LABEL_REGISTRY)}")

        print(f"Columns : {labels.shape[1]}")

        print(f"Rows    : {labels.shape[0]}")

        print(f"Time    : {total:.2f} sec")

        print("=" * 50)

    return labels


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("APEX Label Builder v1.0")