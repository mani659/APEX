"""
=========================================================
APEX Quant Research Framework

Module      : doctor.py
Version     : 2.0

Description :
Master diagnostics launcher for the entire APEX framework.

Runs all health checks and reports overall framework status.

Author      : APEX
=========================================================
"""

from doctor.check_structure import run_structure_check
from doctor.check_imports import run_import_check
from doctor.check_constants import run_constants_check
from doctor.check_config import run_config_check
from doctor.check_contracts import run_contract_check
from doctor.check_registry import run_registry_check
from doctor.check_pipeline import run_pipeline_check
from doctor.check_duplicates import run_duplicate_check
from doctor.check_dataset import run_dataset_check
from doctor.report import print_report

import traceback


# ==========================================================
# Banner
# ==========================================================

def banner():

    print()

    print("=" * 70)
    print("                 APEX DOCTOR v2.0")
    print("=" * 70)


# ==========================================================
# Safe Runner
# ==========================================================

def run_check(title, func):

    print()

    print("-" * 70)
    print(title)
    print("-" * 70)

    try:

        func()

        return True

    except Exception:

        traceback.print_exc()

        return False


# ==========================================================
# Main
# ==========================================================

def main():

    banner()

    results = []

    results.append(run_check(
        "PROJECT STRUCTURE",
        run_structure_check
    ))

    results.append(run_check(
        "IMPORT CHECK",
        run_import_check
    ))

    results.append(run_check(
        "CONSTANTS",
        run_constants_check
    ))

    results.append(run_check(
        "CONFIGURATION",
        run_config_check
    ))

    results.append(run_check(
        "FEATURE CONTRACTS",
        run_contract_check
    ))

    results.append(run_check(
        "FEATURE REGISTRY",
        run_registry_check
    ))

    results.append(run_check(
        "PIPELINE",
        run_pipeline_check
    ))

    results.append(run_check(
        "DUPLICATE FEATURES",
        run_duplicate_check
    ))

    results.append(run_check(
        "MASTER DATASET",
        run_dataset_check
    ))

    print_report()

    print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(results)
    failed = len(results) - passed

    print(f"Checks Run : {len(results)}")
    print(f"Passed     : {passed}")
    print(f"Failed     : {failed}")

    if failed == 0:

        print()
        print("FRAMEWORK STATUS : HEALTHY")
        print("Ready for research.")

    else:

        print()
        print("FRAMEWORK STATUS : NEEDS ATTENTION")
        print("Fix the failed checks above.")

    print("=" * 70)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()