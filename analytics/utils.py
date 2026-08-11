"""
=========================================================
APEX Quant Research Framework
Module      : analytics/utils.py
Description : Shared dataclasses, safe file I/O, and helper functions.
=========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, Union

import numpy as np
import pandas as pd


@dataclass
class AnalyticsResult:
    """Standardized result object returned by all analytics modules."""

    module: str
    success: bool
    rows: int
    columns: int
    files: int
    metrics: Dict[str, Any] = field(default_factory=dict)
    elapsed_seconds: float = 0.0
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert AnalyticsResult to a dictionary for JSON serialization."""
        return {
            "module": self.module,
            "success": self.success,
            "rows": self.rows,
            "columns": self.columns,
            "files": self.files,
            "metrics": self.metrics,
            "elapsed_seconds": round(self.elapsed_seconds, 4),
            "message": self.message,
        }


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure directory exists and return resolved Path object."""
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def write_csv(df: pd.DataFrame, path: Union[str, Path]) -> Path:
    """Safely write DataFrame to CSV."""
    target_path = Path(path)
    ensure_dir(target_path.parent)
    df.to_csv(target_path, index=False)
    return target_path


def write_markdown(content: str, path: Union[str, Path]) -> Path:
    """Safely write string content to a Markdown file."""
    target_path = Path(path)
    ensure_dir(target_path.parent)
    target_path.write_text(content, encoding="utf-8")
    return target_path


def write_json(data: Dict[str, Any], path: Union[str, Path]) -> Path:
    """Safely write dictionary to formatted JSON."""
    target_path = Path(path)
    ensure_dir(target_path.parent)

    def convert_types(obj: Any) -> Any:
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, (np.ndarray, pd.Series)):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, Path):
            return str(obj)
        return str(obj)

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=convert_types)
    return target_path


def get_timestamp() -> str:
    """Return formatted current timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_bytes(num_bytes: int) -> str:
    """Format byte count into human-readable string (KB, MB, GB)."""
    if num_bytes < 1024:
        return f"{num_bytes} B"
    elif num_bytes < 1024**2:
        return f"{num_bytes / 1024:.2f} KB"
    elif num_bytes < 1024**3:
        return f"{num_bytes / (1024**2):.2f} MB"
    else:
        return f"{num_bytes / (1024**3):.2f} GB"


def compute_mad(series: pd.Series) -> float:
    """Compute Median Absolute Deviation (MAD) for numeric series."""
    clean = series.dropna()
    if clean.empty:
        return float("nan")
    med = clean.median()
    return float((clean - med).abs().median())


def df_to_markdown(df: pd.DataFrame, max_rows: int = 25) -> str:
    """Convert pandas DataFrame to Markdown table string without tabulate dependency."""
    if df.empty:
        return "_Empty DataFrame_\n"

    subset = df.head(max_rows)
    headers = [str(c) for c in subset.columns]
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join([":---"] * len(headers)) + " |"

    rows = []
    for _, row in subset.iterrows():
        formatted_vals = []
        for v in row:
            if pd.isna(v):
                formatted_vals.append("")
            elif isinstance(v, float):
                formatted_vals.append(f"{v:.4g}")
            else:
                formatted_vals.append(str(v))
        rows.append("| " + " | ".join(formatted_vals) + " |")

    return "\n".join([header_line, separator_line] + rows) + "\n"

