"""
=========================================================
APEX Quant Research Framework

Module  : check_constants.py
Version : 1.0
=========================================================
"""

import config.constants as C


REQUIRED = [

    "OPEN",
    "HIGH",
    "LOW",
    "CLOSE",
    "VOLUME",

    "ATR_PERIOD",

    "LOOKAHEAD_BARS",

]


def run_constants_check():

    print()

    print("=" * 60)
    print("CONSTANTS")
    print("=" * 60)

    ok = 0

    fail = 0

    for item in REQUIRED:

        if hasattr(C, item):

            print(f"[ OK ] {item}")

            ok += 1

        else:

            print(f"[FAIL] {item}")

            fail += 1

    print()

    print(f"Passed : {ok}")

    print(f"Failed : {fail}")