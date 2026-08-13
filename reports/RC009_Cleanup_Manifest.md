# RC009 Cleanup Manifest

This manifest formally logs the artifacts removed or archived during the final freeze and cleanup of the RC009 Discovery Campaign. The purpose of this cleanup is to permanently separate proven/frozen negative knowledge from temporary experimental implementation artifacts.

## Summary Metrics
- **Pre-cleanup Repository Size:** 810.90 MB (813 files)
- **RC009 Artifacts Size (Before):** 31.22 MB
- **Space Recovered:** 29.56 MB
- **Files Deleted:** 199 files
- **Post-cleanup Repository Size:** 781.33 MB (614 files)

## Deletions Log

| Path | Action | Reason |
|---|---|---|
| `reports/Development_Status_*.txt` | DELETE | Temporary debug logs. |
| `reports/ProjectAudit_*.txt` | DELETE | Temporary telemetry dumps. |
| `dummy.txt` | DELETE | Scratch file without scientific value. |
| `tmp_probe.py` | DELETE | Temporary debugging script. |
| `reports/analyze_005.py` | DELETE | One-off analysis script superseded by canonical reports. |
| `reports/RC009_Study_003_Sequence_Dataset.parquet` | DELETE | Intermediate dataset (12MB). Reproducible via `run_rc009_study003.py`. |
| `reports/RC009_Study_004_Cross_Market_Dataset.parquet` | DELETE | Intermediate dataset (9MB). Reproducible via `run_rc009_study004.py`. |
| `reports/RC009_Study_006_HTF_Regime_Dataset.parquet` | DELETE | Intermediate dataset (8MB). Reproducible via `run_rc009_study006.py`. |
| `__pycache__/*` | DELETE | System-generated compilation caches. |

## Artifacts Kept & Archived

| Path | Action | Reason |
|---|---|---|
| `data/m1/EURUSD_M1.parquet` | KEEP | Canonical data source. |
| `reports/RC009_Baseline_Dataset.parquet` | KEEP | Contains randomized base samples (Study 001) required for absolute strict reproducibility. |
| `reports/RC009_Control_Dataset.parquet` | KEEP | Canonical control match dataset. |
| `reports/RC009_Discovery_Dataset.parquet` | KEEP | Primary discovery subset dataset. |
| `reports/RC009_*.md` | KEEP | Frozen scientific conclusions for Studies 001-006. |
| `research/run_rc009_*.py` | KEEP | Canonical methodology execution scripts required for reproducible science. |
| `docs/RC009_FREEZE.md` | KEEP | The formal campaign closure document. |
| `docs/Apex_Knowledge_Base.md` | KEEP | Canonical repository memory. |

**Final Assessment:** The repository is now clean. All RC009 knowledge is formally preserved in the Knowledge Base and Frozen reports, while obsolete bloat has been discarded. The project is ready for a new strategic research phase.
