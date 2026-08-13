# RC013 Cleanup Manifest

## 1. Audit Summary
A repository audit was conducted to finalize the RC013 campaign branch. The objective was to ensure only files with permanent scientific and reproducibility value were retained.

## 2. Files Preserved
The following files were preserved because they constitute the permanent scientific history, reproducibility mechanisms, and canonical execution paths for RC013:

- `docs/RC013_CHARTER.md`
- `docs/RC013_FREEZE.md`
- `reports/RC013_Study_000_Data_Qualification.md`
- `reports/RC013_Study_001_Session_Mechanics_Analysis.md`
- `reports/RC013_Study_001_Session_Mechanics_Dataset.parquet`
- `reports/RC013_Study_002_Session_Validation.md`
- `reports/RC013_Study_002_Session_Validation_Dataset.parquet`
- `reports/RC013_Study_003_Session_Path_Analysis.md`
- `reports/RC013_Study_003_Session_Path_Dataset.parquet`
- `reports/RC013_Study_004_Session_Breakout_Analysis.md`
- `reports/RC013_Study_004_Session_Breakout_Dataset.parquet`
- `scripts/rc013_study_001.py`
- `scripts/rc013_study_002.py`
- `scripts/rc013_study_003.py`
- `scripts/rc013_study_004.py`

## 3. Files Removed
**None.** 
Because the AI agent executed RC013 with strict discipline, no debug dumps, scratch notebooks, temporary caches, or duplicate artifacts were generated during the campaign. The repository state for RC013 remains perfectly clean and requires no file deletions.

## 4. Documentation Updates
- `docs/RC013_FREEZE.md` created to formally freeze the branch.
- `docs/Apex_Knowledge_Base.md` successfully updated to permanently record findings R018-R021 and log the campaign studies in the Duplicate Prevention register.
