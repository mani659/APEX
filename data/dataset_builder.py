"""
=========================================================
APEX Quant Research Framework

Module      : dataset_builder.py
Version     : 1.0

Description :
Master Dataset Builder.

Author      : APEX
=========================================================
"""

import pandas as pd

from data.loader import load_data
from data.preprocessing import preprocess
from data.feature_builder import build_features

from labels.labels import build_labels

from config.settings import (
    DEFAULT_SYMBOL,
    MASTER_DATASET,
)


def build_master_dataset(
    symbol=DEFAULT_SYMBOL,
    save=True
):

    print()

    print("=" * 60)

    print("APEX MASTER DATASET")

    print("=" * 60)

    # -------------------------------------

    print("Loading data...")

    df = load_data(symbol)

    # -------------------------------------

    print("Preprocessing...")

    df = preprocess(df)

    # -------------------------------------

    print("Building features...")

    features = build_features(df)

    # -------------------------------------

    print("Building labels...")

    labels = build_labels(df)

    # -------------------------------------

    print("Combining dataset...")

    dataset = pd.concat(

        [

            df,

            features,

            labels

        ],

        axis=1

    )

    # -------------------------------------

    dataset = dataset.dropna()

    # -------------------------------------

    if save:

        print()

        print("Saving...")

        dataset.to_parquet(

            MASTER_DATASET,

            index=True

        )

        print(MASTER_DATASET)

    # -------------------------------------

    print()

    print("=" * 60)

    print("MASTER DATASET COMPLETE")

    print("=" * 60)

    print(f"Rows    : {len(dataset):,}")

    print(f"Columns : {len(dataset.columns)}")

    print("=" * 60)

    return dataset


if __name__ == "__main__":

    build_master_dataset()