"""
=========================================================
APEX Quant Research Framework
Module      : analytics/reporting.py
Description : Master report assembly analytics module.
=========================================================
"""

import json
from pathlib import Path
import time
from typing import Dict, List, Union

import pandas as pd

from analytics.utils import (
    AnalyticsResult,
    ensure_dir,
    get_timestamp,
    write_json,
    write_markdown,
)


def _load_module_summary(module_dir: Path) -> Dict:
    """Safely load summary.json for a module."""
    summary_file = module_dir / "summary.json"
    if summary_file.exists():
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _read_file_text(file_path: Path) -> str:
    """Safely read text file content."""
    if file_path.exists():
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception:
            return ""
    return ""


def analyze(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    verbose: bool = True,
) -> AnalyticsResult:
    """
    Assemble generated analytics outputs into unified Markdown and HTML research reports.

    Parameters
    ----------
    df : pd.DataFrame
        Master dataset DataFrame (read-only).
    output_dir : Union[str, Path]
        Target base report directory (e.g. reports/analytics/latest).
    verbose : bool
        Whether to log progress.

    Returns
    -------
    AnalyticsResult
        Standardized analytics result object.
    """
    start_time = time.time()
    out_root = Path(output_dir)
    ensure_dir(out_root)

    sub_dirs = {
        "statistics": out_root / "statistics",
        "tail_statistics": out_root / "tails",
        "regime_analysis": out_root / "regimes",
        "correlation_analysis": out_root / "correlation",
        "stability_analysis": out_root / "stability",
        "hypothesis_discovery": out_root / "hypotheses",
        "feature_importance": out_root / "importance",
        "parameter_surface": out_root / "surfaces",
    }

    summaries = {}
    md_sections = {}

    for mod_name, mod_dir in sub_dirs.items():
        summaries[mod_name] = _load_module_summary(mod_dir)

    # 1. Build Research_Report.md
    report_md = f"""# APEX Quant Research Framework - Unified Research Report

**Generated:** {get_timestamp()}  
**Dataset Shape:** {df.shape[0]:,} rows x {df.shape[1]:,} columns  

---

## 1. Executive Summary

| Analytics Module | Status | Key Artifacts | Summary Message |
| :--- | :--- | :--- | :--- |
"""
    for mod_name, sum_data in summaries.items():
        metrics = sum_data.get("metrics", {})
        files = sum_data.get("files_generated", [])
        msg = sum_data.get("message", "Completed")
        status_str = "✅ Success" if sum_data else "⚠️ Missing/Skipped"
        report_md += f"| **{mod_name}** | {status_str} | {len(files)} files | {msg} |\n"

    report_md += "\n---\n\n"

    # Append Statistics Section
    stats_md = _read_file_text(sub_dirs["statistics"] / "dataset_summary.md")
    if stats_md:
        report_md += stats_md + "\n\n---\n\n"

    # Append Tail Statistics Section
    tails_md = _read_file_text(sub_dirs["tail_statistics"] / "tail_summary.md")
    if tails_md:
        report_md += tails_md + "\n\n---\n\n"

    # Append Regime Analysis Section
    regimes_md = _read_file_text(sub_dirs["regime_analysis"] / "regime_report.md")
    if regimes_md:
        report_md += regimes_md + "\n\n---\n\n"

    # Append Correlation Analysis Section
    corr_md = _read_file_text(sub_dirs["correlation_analysis"] / "correlation_report.md")
    if corr_md:
        report_md += corr_md + "\n\n---\n\n"

    # Append Stability Analysis Section
    stab_md = _read_file_text(sub_dirs["stability_analysis"] / "stability_summary.md")
    if not stab_md:
        stab_md = _read_file_text(sub_dirs["stability_analysis"] / "stability_report.md")
    if stab_md:
        report_md += stab_md + "\n\n---\n\n"

    # Append Hypothesis Discovery Section
    hyp_md = _read_file_text(sub_dirs["hypothesis_discovery"] / "hypothesis_report.md")
    if hyp_md:
        report_md += hyp_md + "\n\n---\n\n"

    # Append Feature Importance Section
    imp_md = _read_file_text(sub_dirs["feature_importance"] / "importance_summary.md")
    if imp_md:
        report_md += imp_md + "\n\n---\n\n"

    # Append Parameter Surface Section
    surf_md = _read_file_text(sub_dirs["parameter_surface"] / "surface_summary.md")
    if surf_md:
        report_md += surf_md + "\n\n---\n\n"

    # Write Research_Report.md
    file_report_md = write_markdown(report_md, out_root / "Research_Report.md")

    # 2. Build Research_Report.html (HTML format)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APEX Research Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            background-color: #f8fafc;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}
        h1 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }}
        h2 {{ color: #1e3a8a; margin-top: 32px; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; }}
        h3 {{ color: #334155; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }}
        th, td {{
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{
            background-color: #f1f5f9;
            color: #334155;
            font-weight: 600;
        }}
        tr:hover {{ background-color: #f8fafc; }}
        code {{
            background-color: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 13px;
        }}
        pre {{
            background-color: #0f172a;
            color: #f8fafc;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <pre>{report_md}</pre>
    </div>
</body>
</html>
"""
    file_report_html = out_root / "Research_Report.html"
    file_report_html.write_text(html_content, encoding="utf-8")

    # 3. Build top-level summary.json
    summary_data = {
        "framework": "APEX Quant Research Framework",
        "module": "reporting",
        "timestamp": get_timestamp(),
        "dataset_rows": df.shape[0],
        "dataset_columns": df.shape[1],
        "sub_modules": list(sub_dirs.keys()),
        "generated_reports": [
            "Research_Report.md",
            "Research_Report.html",
            "summary.json",
        ],
    }
    file_summary_json = write_json(summary_data, out_root / "summary.json")

    elapsed = time.time() - start_time
    if verbose:
        print(
            f"[analytics.reporting] Unified report assembled successfully in {elapsed:.2f}s."
        )

    return AnalyticsResult(
        module="reporting",
        success=True,
        rows=df.shape[0],
        columns=df.shape[1],
        files=3,
        metrics=summary_data,
        elapsed_seconds=elapsed,
        message="Reporting completed successfully. Unified reports written to output directory.",
    )
