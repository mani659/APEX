"""
=========================================================
APEX Quant Research Framework

Module      : feature_builder.py
Version     : 1.0

Description :
Master Feature Builder

Automatically builds every registered feature module.

Author      : APEX
=========================================================
"""

# ==========================================================
# Imports
# ==========================================================

import time

import pandas as pd

from features.registry import FEATURE_REGISTRY


# ==========================================================
# Build Features
# ==========================================================

def build_features(
    df: pd.DataFrame,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Build all registered features.
    """

    feature_frames = []

    start = time.time()

    for name, builder in FEATURE_REGISTRY.items():

        print(f"\nBuilding {name}...")

        feat = builder(df)

        print(f"Returned from {name}")
        print(f"Shape : {feat.shape}")

        print("Appending...")
        feature_frames.append(feat)
        print("Done.")

    print("\nConcatenating ALL features...")

    features = pd.concat(
        feature_frames,
        axis=1
    )

    print("Feature matrix built.")

    total = time.time() - start

    if verbose:

        print()

        print("=" * 50)
        print("Feature Build Complete")
        print("=" * 50)

        print(f"Modules : {len(FEATURE_REGISTRY)}")
        print(f"Columns : {features.shape[1]}")
        print(f"Rows    : {features.shape[0]}")
        print(f"Time    : {total:.2f} sec")

        print("=" * 50)

    return features


# ==========================================================
# Summary
# ==========================================================

def feature_summary(
    features: pd.DataFrame
):
    """
    Print summary statistics.
    """

    print()

    print("=" * 50)

    print("Feature Summary")

    print("=" * 50)

    print(f"Rows    : {len(features):,}")

    print(f"Columns : {len(features.columns)}")

    print()

    print(features.dtypes.value_counts())

    print()

    print("=" * 50)


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("APEX Feature Builder v1.0")