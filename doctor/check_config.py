"""
=========================================================
APEX Doctor

Configuration Validation
=========================================================
"""

from config.settings import *
from config.constants import *


def run_config_check():

    print()
    print("="*60)
    print("CONFIGURATION")
    print("="*60)

    print(f"Default Symbol : {DEFAULT_SYMBOL}")

    print(f"ATR Period     : {ATR_PERIOD}")

    print(f"Lookahead      : {LOOKAHEAD_BARS}")

    print()

    print("[ OK ] Configuration Loaded")