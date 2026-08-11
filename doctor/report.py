"""
=========================================================
APEX Doctor

Module : report.py
Version: 1.0
=========================================================
"""

from datetime import datetime


def print_report():

    print()

    print("="*60)

    print("APEX HEALTH REPORT")

    print("="*60)

    print()

    print(

        "Generated :",

        datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )

    )

    print()

    print("="*60)