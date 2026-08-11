"""
=========================================================
APEX Doctor

Dataset Health Check
=========================================================
"""

from pathlib import Path

from config.settings import MASTER_DATASET


def run_dataset_check():

    print()
    print("="*60)
    print("MASTER DATASET")
    print("="*60)

    path = Path(MASTER_DATASET)

    if path.exists():

        print("[ OK ] Dataset Found")

        print(path)

    else:

        print("[WARN] Master dataset not created yet")