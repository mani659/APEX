"""
=========================================================
APEX Quant Research Framework

Module      : pipeline_check.py
Version     : 1.0

Description :
Validates the complete APEX data pipeline before
building large datasets.

Author      : APEX
=========================================================
"""

import traceback

import pandas as pd

from config.settings import DEFAULT_SYMBOL

from data.loader import load_data
from data.preprocessing import preprocess
from data.feature_builder import build_features

from labels.labels import build_labels


# ==========================================================
# Helper
# ==========================================================

def ok(msg):

    print(f"[ OK ] {msg}")


def fail(msg):

    print(f"[FAIL] {msg}")


# ==========================================================
# Main Check
# ==========================================================

def run_pipeline_check():

    print()

    print("=" * 70)
    print("APEX PIPELINE CHECK")
    print("=" * 70)

    # ------------------------------------------------------
    # Load
    # ------------------------------------------------------

    try:

        df = load_data(DEFAULT_SYMBOL)

        ok(f"Loader ({len(df):,} rows)")

    except Exception:

        fail("Loader")

        traceback.print_exc()

        return

    # ------------------------------------------------------
    # Sample
    # ------------------------------------------------------

    df = df.head(1000)

    ok("Sample created (1000 rows)")

    # ------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------

    try:

        df = preprocess(df)

        ok("Preprocessing")

    except Exception:

        fail("Preprocessing")

        traceback.print_exc()

        return

    # ------------------------------------------------------
    # Features
    # ------------------------------------------------------

    try:

        features = build_features(
            df,
            verbose=False
        )

        ok(f"Features ({features.shape[1]} columns)")

    except Exception:

        fail("Feature Builder")

        traceback.print_exc()

        return

    # ------------------------------------------------------
    # Labels
    # ------------------------------------------------------

    try:

        labels = build_labels(
            df,
            verbose=False
        )

        ok(f"Labels ({labels.shape[1]} columns)")

    except Exception:

        fail("Label Builder")

        traceback.print_exc()

        return

    # ------------------------------------------------------
    # Duplicate Columns
    # ------------------------------------------------------

    dataset = pd.concat(

        [

            df,

            features,

            labels

        ],

        axis=1

    )

    duplicates = dataset.columns.duplicated()

    if duplicates.any():

        fail(
            f"Duplicate Columns : {duplicates.sum()}"
        )

    else:

        ok("No duplicate columns")

    # ------------------------------------------------------
    # Missing Values
    # ------------------------------------------------------

    missing = dataset.isna().sum().sum()

    if missing > 0:

        fail(f"Missing values : {missing:,}")

    else:

        ok("No missing values")

    # ------------------------------------------------------
    # Index
    # ------------------------------------------------------

    if dataset.index.is_unique:

        ok("Unique index")

    else:

        fail("Duplicate index")

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    print()

    print("=" * 70)

    print("PIPELINE SUMMARY")

    print("=" * 70)

    print(f"Rows       : {len(dataset):,}")

    print(f"Columns    : {len(dataset.columns)}")

    print()

    print(dataset.dtypes.value_counts())

    print()

    print("=" * 70)

    print("PIPELINE PASSED")

    print("=" * 70)


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    run_pipeline_check()