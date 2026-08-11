"""
=========================================================
APEX Quant Research Framework

Module  : check_imports.py
Version : 1.0
=========================================================
"""

import importlib

MODULES = [

    "data.loader",
    "data.validator",
    "data.preprocessing",
    "data.feature_builder",

    "features.price",
    "features.volume",
    "features.volatility",
    "features.trend",
    "features.momentum",
    "features.structure",
    "features.smart_money",
    "features.regime",
    "features.session",

    "labels.future_returns",
    "labels.grid_labels",
    "labels.survival_labels",
    "labels.execution_labels",
    "labels.labels",

]


def run_import_check():

    print()
    print("=" * 60)
    print("IMPORT CHECK")
    print("=" * 60)

    passed = 0
    failed = 0

    for module in MODULES:

        try:

            importlib.import_module(module)

            print(f"[ OK ] {module}")

            passed += 1

        except Exception as e:

            print(f"[FAIL] {module}")

            print(f"       {e}")

            failed += 1

    print()

    print(f"Passed : {passed}")

    print(f"Failed : {failed}")