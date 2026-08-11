"""
=========================================================
APEX Quant Research Framework

Module      : settings.py
Version     : 1.0

Description :
Global project configuration and filesystem paths.

=========================================================
"""

from pathlib import Path

# =========================================================
# PROJECT
# =========================================================

PROJECT_NAME = "APEX Quant Research Framework"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =========================================================
# DIRECTORIES
# =========================================================

DATA_DIR = PROJECT_ROOT / "data"

M1_DIR = DATA_DIR / "m1"

DATASET_DIR = PROJECT_ROOT / "datasets"

REPORT_DIR = PROJECT_ROOT / "reports"

EXPERIMENT_DIR = PROJECT_ROOT / "experiments"

DOCS_DIR = PROJECT_ROOT / "docs"

FEATURE_DIR = PROJECT_ROOT / "features"

LABEL_DIR = PROJECT_ROOT / "labels"

# =========================================================
# DEFAULTS
# =========================================================

DEFAULT_SYMBOL = "XAUUSD"

DEFAULT_TIMEFRAME = "M1"

# =========================================================
# SYMBOL FILES
# =========================================================

SYMBOL_FILES = {

    "XAUUSD": M1_DIR / "XAUUSD_M1.csv",

    "XAGUSD": M1_DIR / "XAGUSD_M1.csv",

    "BTCUSD": M1_DIR / "BTCUSD_M1.csv",

    "EURUSD": M1_DIR / "EURUSD_M1.csv",

    "NAS100": M1_DIR / "USATECHIDXUSD_M1.csv",

}

# =========================================================
# OUTPUT FILES
# =========================================================

MASTER_DATASET = DATASET_DIR / "master_dataset.parquet"

FEATURE_DATASET = DATASET_DIR / "feature_dataset.parquet"

LABEL_DATASET = DATASET_DIR / "label_dataset.parquet"