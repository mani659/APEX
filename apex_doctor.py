"""
=========================================================
APEX Quant Research Framework
Project Doctor
Version : 1.0
Author  : OpenAI + Ama
=========================================================

Purpose
-------
Checks the entire APEX project structure.

✓ Creates missing folders
✓ Creates missing files
✓ Warns about unexpected files
✓ Generates audit report

Nothing is deleted automatically.
=========================================================
"""

from pathlib import Path
from datetime import datetime

# =========================================================
# PROJECT ROOT
# =========================================================

ROOT = Path(__file__).resolve().parent

# =========================================================
# EXPECTED STRUCTURE
# =========================================================

STRUCTURE = {

    "config": [
        "settings.py",
        "constants.py",
        "experiment_profiles.py"
    ],

    "data": [
        "loader.py",
        "validator.py",
        "preprocessing.py",
        "indicators.py",
        "feature_builder.py",
        "dataset_builder.py"
    ],

    "data/labels": [
        "labels.py",
        "future_returns.py",
        "grid_labels.py",
        "survival_labels.py",
        "execution_labels.py",
        "validation.py"
    ],

    "features": [
        "__init__.py",
        "registry.py",
        "helpers.py",
        "price.py",
        "volume.py",
        "session.py",
        "volatility.py",
        "trend.py",
        "momentum.py",
        "structure.py",
        "smart_money.py",
        "regime.py"
    ],

    "regimes": [
        "baseline.py",
        "continuation.py",
        "persistence.py",
        "transition.py",
        "adaptive_inventory.py",
        "classifier.py"
    ],

    "simulator": [
        "basket.py",
        "grid_engine.py",
        "payoff_engine.py",
        "execution.py",
        "inventory.py",
        "flash_events.py",
        "monte_carlo.py"
    ],

    "analytics": [
        "statistics.py",
        "parameter_surface.py",
        "feature_importance.py",
        "tail_analysis.py",
        "reporting.py"
    ],

    "ml": [
        "train.py",
        "validation.py",
        "inference.py"
    ],

    "mt5": [
        "signal_generator.py",
        "order_manager.py",
        "bridge.py",
        "live_monitor.py"
    ],

    "experiments": [],

    "datasets": [],

    "datasets/raw": [],
    "datasets/features": [],
    "datasets/labels": [],
    "datasets/master": [],
    "datasets/train": [],
    "datasets/validation": [],
    "datasets/test": [],

    "reports": [],

    "notebooks": []
}

ROOT_FILES = [
    "apex.py",
    "apex_doctor.py"
]

# =========================================================

HEADER = '''"""
APEX Quant Research Framework

This file was automatically created by
apex_doctor.py

Status : Placeholder
Version: 1.0
"""
'''

created_files = []
created_dirs = []
warnings = []

print("="*60)
print("APEX PROJECT DOCTOR")
print("="*60)

# =========================================================
# ROOT FILES
# =========================================================

print("\nChecking root files...")

for file in ROOT_FILES:

    path = ROOT / file

    if path.exists():

        print(f"✓ {file}")

    else:

        path.write_text(HEADER, encoding="utf8")

        created_files.append(file)

        print(f"+ Created {file}")

# =========================================================
# DIRECTORIES
# =========================================================

print("\nChecking folders...")

for folder, files in STRUCTURE.items():

    folder_path = ROOT / folder

    if not folder_path.exists():

        folder_path.mkdir(parents=True)

        created_dirs.append(folder)

        print(f"+ Created folder : {folder}")

    else:

        print(f"✓ {folder}")

    for file in files:

        file_path = folder_path / file

        if not file_path.exists():

            file_path.write_text(HEADER, encoding="utf8")

            created_files.append(str(file_path.relative_to(ROOT)))

            print(f"    + Created {file}")

# =========================================================
# UNKNOWN FILES
# =========================================================

print("\nScanning for unknown files...")

expected = set(ROOT_FILES)

for folder, files in STRUCTURE.items():

    for f in files:

        expected.add(str(Path(folder)/f))

for py in ROOT.rglob("*.py"):

    rel = str(py.relative_to(ROOT))

    if rel not in expected:

        warnings.append(rel)

# =========================================================
# REPORT
# =========================================================

report_dir = ROOT / "reports"

report_dir.mkdir(exist_ok=True)

report = report_dir / f"ProjectAudit_{datetime.now():%Y%m%d_%H%M}.txt"

with open(report,"w",encoding="utf8") as f:

    f.write("="*60+"\n")
    f.write("APEX PROJECT AUDIT\n")
    f.write("="*60+"\n\n")

    f.write("Created Folders\n")
    f.write("-------------------------\n")

    if created_dirs:

        for d in created_dirs:

            f.write(d+"\n")

    else:

        f.write("None\n")

    f.write("\nCreated Files\n")
    f.write("-------------------------\n")

    if created_files:

        for c in created_files:

            f.write(c+"\n")

    else:

        f.write("None\n")

    f.write("\nWarnings\n")
    f.write("-------------------------\n")

    if warnings:

        for w in warnings:

            f.write(w+"\n")

    else:

        f.write("None\n")

# =========================================================

print("\n"+"="*60)
print("SUMMARY")
print("="*60)

print(f"Folders Created : {len(created_dirs)}")
print(f"Files Created   : {len(created_files)}")
print(f"Warnings        : {len(warnings)}")

if warnings:

    print("\nUnknown Python files:")

    for w in warnings:

        print(" -", w)

print("\nAudit report saved to:")

print(report)

print("\nDone.")