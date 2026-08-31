# RC015 Session Handoff Document

**Date**: August 18, 2026
**Repository**: `APEX` (`d:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex`)
**Current Branch**: `main` (11 commits ahead of `origin/main`, clean and safe to push)

---

## 1. Current State & Achievements

### RC015 Study 007 (Options Volatility Discovery)
* **Stage 1 Complete**: We successfully ran the Stage 1 instrument discovery using the Databento API.
* **Results**: Out of 222 frozen qualifying events, 60 events successfully resolved to an exact Friday-expiry option within the ±0.0020 moneyness rule.
* **Diagnostic Complete**: 162 events failed Stage 1. We ran a deep-dive diagnostic and proved **none** of the failures were due to missing data or moneyness constraints. 
  * **130 events** failed due to *Futures Mapping Errors* (Class D). The script expected front-month futures, but the options actually mapped to quarterly cycle futures.
  * **32 events** failed due to *Wrong Option Root* (Class C). The script expected weekly roots (`1EU`, `2EU`) but CME historically archived these specific 3rd-Friday or holiday-shifted options under `EUU`.
* **Artifacts Generated**:
  * `reports/RC015_Study_007_Stage1_Acquisition_Report.md`
  * `reports/RC015_Study_007_Missing_Event_Diagnostic.md`
  * `reports/RC015_Study_007_Acquisition_Summary.csv`

### Security Remediation (Git History Scrub)
* We identified that hardcoded Exness MT5 trial passwords and Telegram Bot tokens were accidentally committed to local git history in the `Super/` directory.
* We successfully ran `git filter-repo` to entirely **scrub and redact** these credentials from the local Git history.
* The Databento API key was removed from tracked/untracked scripts and is now safely managed via `.gitignore` and `os.environ.get("DATABENTO_API_KEY")`.
* **Status**: `CLEAN — LOCAL HISTORY SCRUBBED`. The remote `origin/main` was completely untouched and the local repository is safe to push.
* **Artifact Generated**: `reports/RC015_GitHub_Security_Remediation.md`

---

## 2. Technical Context & Rules for the Next Agent

### Databento API Authentication
* The Databento API key is saved locally in the untracked file `DATABENTO_API_KEY.md`.
* Python scripts MUST authenticate using the environment variable:
  ```python
  import os
  api_key = os.environ.get("DATABENTO_API_KEY")
  ```

### Repository Rules
* **Do NOT force-push or modify `origin/main`** without explicit user permission.
* **Do NOT blindly ignore folders** like `reports/`, `scripts/`, or `data/` in `.gitignore`. Only sensitive/untracked configuration files are ignored.

---

## 3. Immediate Next Steps / Open Decisions

You are now at a crossroads for RC015 Study 007. The new agent should ask the user how they wish to proceed regarding the 162 missing events:

**Option A: Recover the Missing Events (Recommended)**
Update the Stage 1 acquisition logic in `scripts/rc015_study_007_instrument_manifest.py` to dynamically accept `EUU.OPT` for weeklies and implement a flexible futures underlying lookup (e.g., checking quarterly cycle futures instead of strictly front-month) to successfully recover the 162 failed events.

**Option B: Proceed to Stage 2 with Existing Sample**
Ignore the 162 missing events and proceed directly to **Stage 2 (BBO-1m Acquisition)** using only the 60 successfully resolved events.

> **Instruction for the new agent**: Read this document, parse the mentioned reports in the `reports/` directory to build your context, and then prompt the user to choose between Option A and Option B.
