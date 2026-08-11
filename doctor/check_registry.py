"""
=========================================================
APEX Quant Research Framework

Module  : check_registry.py
Version : 1.0
=========================================================
"""

import inspect

from features.registry import FEATURE_REGISTRY


def run_registry_check():

    print()

    print("=" * 60)
    print("FEATURE REGISTRY")
    print("=" * 60)

    ok = 0

    fail = 0

    for name, func in FEATURE_REGISTRY.items():

        if callable(func):

            print(f"[ OK ] {name}")

            ok += 1

        else:

            print(f"[FAIL] {name}")

            fail += 1

    print()

    print(f"Modules : {len(FEATURE_REGISTRY)}")

    print(f"Passed  : {ok}")

    print(f"Failed  : {fail}")