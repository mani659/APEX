"""
=========================================================
APEX Quant Research Framework

Module      : validation.py
Version     : 1.0

Description :
Label validation utilities.

Author      : APEX
=========================================================
"""

import pandas as pd


def validate_labels(labels: pd.DataFrame):

    print()

    print("=" * 60)

    print("LABEL VALIDATION")

    print("=" * 60)

    print()

    print(f"Rows    : {len(labels):,}")

    print(f"Columns : {len(labels.columns)}")

    print()

    print("Missing Values")

    print("------------------------")

    print(labels.isna().sum())

    print()

    print("Data Types")

    print("------------------------")

    print(labels.dtypes)

    print()

    print("=" * 60)

    return True


if __name__ == "__main__":

    print("Label Validation v1.0")