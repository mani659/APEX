# RC013 Cleanup Manifest

## Execution Date
2026-08-15

## Campaign Status
CLOSED - STRUCTURAL PRIMITIVE VALIDATED, MONETIZATION ARCHITECTURE REJECTED

## Objective
Retain only files that are useful for permanent scientific history, reproducibility, future decision-making, and canonical execution. Remove intermediate discovery scripts to prevent parameter hunting and optimization drift.

## Files Removed

| File | Type | Reason for Removal |
| :--- | :--- | :--- |
| `scripts/rc013_study_001.py` | Python Script | Intermediate discovery/exploration script. Replaced by final datasets and Study 004 execution architecture. |
| `scripts/rc013_study_002.py` | Python Script | Intermediate validation script. Replaced by final datasets and Study 004 execution architecture. |
| `scripts/rc013_study_003.py` | Python Script | Intermediate path analysis script. Replaced by final datasets and Study 004 execution architecture. |

## Files Preserved

| File | Type | Reason for Preservation |
| :--- | :--- | :--- |
| `reports/RC013_Study_000_Data_Qualification.md` | Report | Historical QA evidence. |
| `reports/RC013_Study_001_Session_Mechanics_Analysis.md` | Report | Core discovery conclusions. |
| `reports/RC013_Study_002_Session_Validation.md` | Report | Independent validation evidence. |
| `reports/RC013_Study_003_Session_Path_Analysis.md` | Report | Path geometry structural evidence. |
| `reports/RC013_Study_004_Session_Breakout_Analysis.md` | Report | Failed monetization architecture evidence. |
| `reports/RC013_Study_001_Session_Mechanics_Dataset.parquet` | Dataset | Essential for statistical reproducibility. |
| `reports/RC013_Study_002_Session_Validation_Dataset.parquet` | Dataset | Essential for statistical reproducibility. |
| `reports/RC013_Study_003_Session_Path_Dataset.parquet` | Dataset | Essential for statistical reproducibility. |
| `reports/RC013_Study_004_Session_Breakout_Dataset.parquet` | Dataset | Essential for statistical reproducibility. |
| `scripts/rc013_study_004.py` | Python Script | Final canonical execution script representing the tested (and rejected) breakout architecture. |
| `docs/RC013_CHARTER.md` | Document | Original campaign scope and hypotheses. |
| `docs/RC013_FREEZE.md` | Document | Final structural knowledge preservation and closure order. |
| `docs/Apex_Knowledge_Base.md` | Document | Central repository for project-level confirmed knowledge and rejected ideas. |
| `reports/APEX_POST_RC013_STRATEGY_REVIEW.md` | Report | Post-campaign project strategy guidance. |
