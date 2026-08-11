"""
=========================================================
APEX Doctor

Module : check_structure.py
Version: 1.0
=========================================================
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [

    "config",

    "data",

    "features",

    "labels",

    "doctor",

    "analytics",

    "simulator",

    "experiments",

    "mt5",

]


def run_structure_check():

    print()

    print("="*60)

    print("PROJECT STRUCTURE")

    print("="*60)

    ok = 0

    fail = 0

    for item in REQUIRED:

        p = ROOT / item

        if p.exists():

            print(f"[ OK ] {item}")

            ok += 1

        else:

            print(f"[FAIL] {item}")

            fail += 1

    print()

    print(f"Passed : {ok}")

    print(f"Failed : {fail}")