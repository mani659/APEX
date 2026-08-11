"""
=========================================================
APEX Doctor

Module : check_pipeline.py
Version: 1.0
=========================================================
"""

import traceback

from data.loader import load_data

from data.preprocessing import preprocess

from data.feature_builder import build_features

from labels.labels import build_labels


def run_pipeline_check():

    print()

    print("="*60)

    print("PIPELINE")

    print("="*60)

    try:

        df = load_data()

        print("[ OK ] Loader")

    except Exception:

        print("[FAIL] Loader")

        traceback.print_exc()

        return

    try:

        df = preprocess(df)

        print("[ OK ] Preprocessing")

    except Exception:

        print("[FAIL] Preprocessing")

        traceback.print_exc()

        return

    try:

        feat = build_features(df)

        print(

            f"[ OK ] Features "

            f"({feat.shape[1]})"

        )

    except Exception:

        print("[FAIL] Features")

        traceback.print_exc()

        return

    try:

        lab = build_labels(df)

        print(

            f"[ OK ] Labels "

            f"({lab.shape[1]})"

        )

    except Exception:

        print("[FAIL] Labels")

        traceback.print_exc()

        return

    print()

    print("[ OK ] Pipeline Completed")