"""
=========================================================
APEX Quant Research Framework
Module      : analytics/analytics.py
Description : Central runner for the APEX Analytics layer.
=========================================================
"""

import argparse
from pathlib import Path
import sys
import time
from typing import Dict, Optional, Union

import pandas as pd

# Add project root to sys.path if needed
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from analytics.correlation_analysis import analyze as analyze_correlation
from analytics.feature_importance import analyze as analyze_importance
from analytics.hypothesis_discovery import analyze as analyze_hypotheses
from analytics.parameter_surface import analyze as analyze_surface
from analytics.regime_analysis import analyze as analyze_regimes
from analytics.reporting import analyze as analyze_reporting
from analytics.stability_analysis import analyze as analyze_stability
from analytics.statistics import analyze as analyze_statistics
from analytics.tail_statistics import analyze as analyze_tails
from analytics.utils import (
    AnalyticsResult,
    ensure_dir,
    get_timestamp,
    write_json,
)

try:
    from config.settings import MASTER_DATASET, REPORT_DIR
except ImportError:
    MASTER_DATASET = PROJECT_ROOT / "datasets" / "master_dataset.parquet"
    REPORT_DIR = PROJECT_ROOT / "reports"


def resolve_dataset_path(provided_path: Optional[Union[str, Path]] = None) -> Path:
    """Resolve path to master dataset parquet/csv file."""
    if provided_path:
        p = Path(provided_path)
        if p.exists() and p.stat().st_size > 0:
            return p
        raise FileNotFoundError(
            f"Specified master dataset file not found or is 0 bytes: {provided_path}"
        )

    # Default configured location
    if MASTER_DATASET.exists() and MASTER_DATASET.stat().st_size > 0:
        return MASTER_DATASET

    # Fallback checks in datasets/
    dataset_dir = PROJECT_ROOT / "datasets"
    candidates = [
        dataset_dir / "MASTER_DATASET.parquet",
        dataset_dir / "master_dataset.parquet",
        dataset_dir / "master_dataset.csv",
        dataset_dir / "MASTER_DATASET.csv",
    ]
    for cand in candidates:
        if cand.exists() and cand.stat().st_size > 0:
            return cand

    raise FileNotFoundError(
        f"Master dataset not found or is empty (0 bytes). Checked '{MASTER_DATASET}' and candidates in '{dataset_dir}'."
    )


def load_dataset(dataset_path: Path) -> pd.DataFrame:
    """Load dataset from Parquet or CSV file into a pandas DataFrame."""
    suffix = dataset_path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(dataset_path)
    elif suffix in [".csv", ".txt"]:
        return pd.read_csv(dataset_path)
    else:
        raise ValueError(f"Unsupported dataset file format: {suffix}")


def run_analytics(
    dataset_path: Optional[Union[str, Path]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    verbose: bool = True,
) -> Dict[str, AnalyticsResult]:
    """
    Execute the full APEX analytics suite on the master dataset.

    Parameters
    ----------
    dataset_path : Optional[Union[str, Path]]
        Path to master dataset file. If None, uses configured default.
    output_dir : Optional[Union[str, Path]]
        Path to output directory. Defaults to reports/analytics/latest.
    verbose : bool
        Whether to print console updates.

    Returns
    -------
    Dict[str, AnalyticsResult]
        Mapping of module names to their AnalyticsResult objects.
    """
    start_total = time.time()

    # Determine paths
    ds_path = resolve_dataset_path(dataset_path)
    out_root = (
        Path(output_dir)
        if output_dir
        else REPORT_DIR / "analytics" / "latest"
    )
    ensure_dir(out_root)

    if verbose:
        print("=" * 65)
        print("APEX QUANT RESEARCH FRAMEWORK - ANALYTICS RUNNER")
        print("=" * 65)
        print(f"Master Dataset : {ds_path}")
        print(f"Output Root    : {out_root}")
        print("=" * 65)

    df = load_dataset(ds_path)

    if verbose:
        print(f"Dataset Loaded : {df.shape[0]:,} rows x {df.shape[1]:,} columns\n")

    # Define execution sequence
    modules = [
        ("statistics", analyze_statistics),
        ("tail_statistics", analyze_tails),
        ("regime_analysis", analyze_regimes),
        ("correlation_analysis", analyze_correlation),
        ("stability_analysis", analyze_stability),
        ("hypothesis_discovery", analyze_hypotheses),
        ("feature_importance", analyze_importance),
        ("parameter_surface", analyze_surface),
        ("reporting", analyze_reporting),
    ]

    results: Dict[str, AnalyticsResult] = {}

    for mod_name, analyze_fn in modules:
        if verbose:
            print(f"--> Running module: {mod_name}...")

        try:
            res = analyze_fn(df=df, output_dir=out_root, verbose=verbose)
            results[mod_name] = res
        except Exception as e:
            if verbose:
                print(f"[ERROR] Module '{mod_name}' failed with exception: {e}")
            results[mod_name] = AnalyticsResult(
                module=mod_name,
                success=False,
                rows=df.shape[0],
                columns=df.shape[1],
                files=0,
                metrics={},
                elapsed_seconds=0.0,
                message=f"Failed with error: {str(e)}",
            )

    elapsed_total = time.time() - start_total

    # Master top-level summary.json
    master_summary = {
        "timestamp": get_timestamp(),
        "dataset_path": str(ds_path),
        "output_dir": str(out_root),
        "total_elapsed_seconds": round(elapsed_total, 4),
        "modules": {k: v.to_dict() for k, v in results.items()},
    }
    write_json(master_summary, out_root / "summary.json")

    # Console summary table
    if verbose:
        print("\n" + "=" * 65)
        print("ANALYTICS RUN COMPLETE - SUMMARY")
        print("=" * 65)
        print(f"{'Module':<20} | {'Status':<10} | {'Files':<6} | {'Time (s)':<8} | Message")
        print("-" * 65)
        for name, res in results.items():
            status_str = "SUCCESS" if res.success else "FAILED"
            print(
                f"{name:<20} | {status_str:<10} | {res.files:<6} | {res.elapsed_seconds:<8.2f} | {res.message[:30]}"
            )
        print("=" * 65)
        print(f"Total Elapsed Time : {elapsed_total:.2f}s")
        print(f"Summary Saved To   : {out_root / 'summary.json'}\n")

    return results


def main():
    """CLI entrypoint for running analytics."""
    parser = argparse.ArgumentParser(
        description="APEX Quant Research Framework - Analytics Runner"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="Path to master dataset file (parquet or csv).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to output directory (default: reports/analytics/latest/).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress console output.",
    )

    args = parser.parse_args()
    run_analytics(
        dataset_path=args.dataset,
        output_dir=args.output,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
