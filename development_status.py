"""
=========================================================
APEX Quant Research Framework
Development Status
Version : 1.0

Scans every Python module and reports:

✓ Status
✓ Lines of Code
✓ Functions
✓ Classes
✓ TODOs
✓ FIXMEs
✓ Version

Creates:

reports/Development_Status.txt
=========================================================
"""

from pathlib import Path
import ast
import re
from datetime import datetime

ROOT = Path(__file__).resolve().parent

# ----------------------------------------------------------
# Project Sections
# ----------------------------------------------------------

SECTIONS = {
    "CONFIG": ROOT / "config",
    "DATA": ROOT / "data",
    "LABELS": ROOT / "data" / "labels",
    "FEATURES": ROOT / "features",
    "REGIMES": ROOT / "regimes",
    "SIMULATOR": ROOT / "simulator",
    "ANALYTICS": ROOT / "analytics",
    "ML": ROOT / "ml",
    "MT5": ROOT / "mt5",
    "EXPERIMENTS": ROOT / "experiments",
}

REPORT = []

TOTAL = 0
COMPLETE = 0
PARTIAL = 0
EMPTY = 0
PLACEHOLDER = 0


# ----------------------------------------------------------
def analyse_file(file_path):
# ----------------------------------------------------------

    global COMPLETE
    global PARTIAL
    global EMPTY
    global PLACEHOLDER
    global TOTAL

    TOTAL += 1

    try:
        text = file_path.read_text(encoding="utf8")
    except:
        text = ""

    lines = len(text.splitlines())

    stripped = text.strip()

    if stripped == "":
        status = "EMPTY"
        EMPTY += 1

        return {
            "status": status,
            "lines": 0,
            "functions": 0,
            "classes": 0,
            "todos": 0,
            "fixmes": 0,
            "version": "-"
        }

    placeholder = (
        "placeholder" in text.lower()
        and lines < 30
    )

    try:
        tree = ast.parse(text)

        funcs = sum(
            isinstance(n, ast.FunctionDef)
            for n in ast.walk(tree)
        )

        classes = sum(
            isinstance(n, ast.ClassDef)
            for n in ast.walk(tree)
        )

    except:

        funcs = 0
        classes = 0

    todos = len(re.findall(r"TODO", text, re.IGNORECASE))
    fixmes = len(re.findall(r"FIXME", text, re.IGNORECASE))

    version = "-"

    m = re.search(
        r"Version\s*[:=]\s*([0-9.]+)",
        text,
        re.IGNORECASE
    )

    if m:
        version = m.group(1)

    if placeholder:

        status = "PLACEHOLDER"
        PLACEHOLDER += 1

    elif funcs == 0 and classes == 0:

        status = "EMPTY"
        EMPTY += 1

    elif funcs <= 2:

        status = "PARTIAL"
        PARTIAL += 1

    else:

        status = "COMPLETE"
        COMPLETE += 1

    return {

        "status": status,
        "lines": lines,
        "functions": funcs,
        "classes": classes,
        "todos": todos,
        "fixmes": fixmes,
        "version": version

    }


# ----------------------------------------------------------
def section_report(name, folder):
# ----------------------------------------------------------

    REPORT.append("")
    REPORT.append("=" * 60)
    REPORT.append(name)
    REPORT.append("=" * 60)

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    if not folder.exists():

        REPORT.append("Folder Missing")

        print("Folder Missing")

        return

    pyfiles = sorted(folder.glob("*.py"))

    if not pyfiles:

        REPORT.append("No Files")

        print("No Files")

        return

    for f in pyfiles:

        info = analyse_file(f)

        line = (
            f"{f.name:<28}"
            f"{info['status']:<14}"
            f"Lines:{info['lines']:<5}"
            f"Func:{info['functions']:<3}"
            f"Class:{info['classes']:<3}"
            f"TODO:{info['todos']:<3}"
            f"FIX:{info['fixmes']:<3}"
            f"Ver:{info['version']}"
        )

        REPORT.append(line)

        print(line)


# ----------------------------------------------------------
print("=" * 60)
print("APEX DEVELOPMENT STATUS")
print("=" * 60)

for name, folder in SECTIONS.items():
    section_report(name, folder)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

completion = 0

if TOTAL:
    completion = COMPLETE / TOTAL * 100

summary = [
    "",
    "=" * 60,
    "SUMMARY",
    "=" * 60,
    f"Total Files       : {TOTAL}",
    f"Complete          : {COMPLETE}",
    f"Partial           : {PARTIAL}",
    f"Empty             : {EMPTY}",
    f"Placeholder       : {PLACEHOLDER}",
    f"Completion        : {completion:.1f} %",
]

for s in summary:
    REPORT.append(s)
    print(s)

reports = ROOT / "reports"
reports.mkdir(exist_ok=True)

outfile = reports / f"Development_Status_{datetime.now():%Y%m%d_%H%M}.txt"

outfile.write_text("\n".join(REPORT), encoding="utf8")

print("\nReport saved to:")
print(outfile)