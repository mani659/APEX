"""
=========================================================
APEX Doctor

Duplicate Feature Checker
=========================================================
"""

import pandas as pd

from data.loader import load_data
from data.preprocessing import preprocess
from data.feature_builder import build_features


def run_duplicate_check():

    print()
    print("="*60)
    print("DUPLICATE COLUMN CHECK")
    print("="*60)

    df = preprocess(load_data().head(500))

    feat = build_features(df,verbose=False)

    dup = feat.columns.duplicated()

    if dup.any():

        print("[FAIL] Duplicate columns")

        for c in feat.columns[dup]:

            print("   ",c)

    else:

        print("[ OK ] No duplicate feature names")