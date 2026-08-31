# RC015 GitHub Security & Secret Exposure Audit

## 1. Repository Identification
* **Repository Root**: `D:/Gold Scripts/MQL5/Ticks Data/XAUUSD/grid research/apex`
* **Current Branch**: `main`

## 2. Remote Configuration
* **Configured Git Remotes**: `origin`
* **Remote GitHub Repository URL**: `https://github.com/mani659/APEX.git`
* **Remote Branch Status**: The local `main` branch is 11 commits ahead of `origin/main`. `origin/main` currently has only a single initial commit (`cf6398b fresh clean setup tracking only scripts`).

## 3. Working-Tree Audit
An inspection of `git status` reveals several untracked files, including:
* **Untracked Sensitive Files**: 
  * `DATABENTO_API_KEY.md` (Contains actual Databento credential)
  * `scripts/discover_instruments.py` (Contains actual hardcoded Databento credential)
* **Untracked Temporary/Report Files**: `scratch/`, `data/databento/`, and several markdown/CSV reports in `reports/`.

## 4. Tracked-File Secret Scan
A full scan of currently tracked files using `git ls-files` combined with regular expressions for secrets found the following:
* **`Super/config/config.json`**:
  * Line 5: Hardcoded trading password `[REDACTED]`
  * Line 80: Telegram bot token `[REDACTED]`
  * Line 88: App password `[REDACTED]`
* **`Super/core/supertrend_bot.py`** and **`Super/supertrend_bot.py`**:
  * Line 1515: Hardcoded MT5 login `262464396`, password `[REDACTED]`, server `Exness-MT5Trial16`.
* **Note**: No Databento API keys or other RC015-related credentials were found in tracked files.

## 5. Git-History Secret Scan
An exhaustive search of the entire Git commit history (`git log --all --oneline` and `git rev-list`) confirms:
* The `Super/` files containing the Exness MT5 trial passwords and tokens were committed to the local repository history starting at commit `7a1e965 RC013: close session structural research campaign`.
* **No Databento credentials** have ever been committed to Git history.

## 6. RC015-Specific Scan
All files prefixed with `RC015` or located in `scripts/rc015*` were specifically audited:
* Tracked scripts (e.g., `scripts/rc015_study_001.py`, `scripts/rc015_study_007_instrument_manifest.py`) correctly use environment variable resolution `os.environ.get("DATABENTO_API_KEY")`.
* **No actual Databento keys** exist in tracked RC015 files or RC015 git history.

## 7. IDE/Temp-File Scan
An audit of IDE logs, `.system_generated`, and `scratch/` files determined:
* `.system_generated` logs reside outside the Git repository root.
* `scratch/` logs and temporary `task-*.log` files were created but are **untracked**. 
* The actual Databento key was NOT found leaked inside these local `scratch/` temporary transcripts.

## 8. Sensitive-Data Findings
* **Financial/Private Data**: The `Super/` directory contains MT5 Trial account details and passwords. These are classified as sensitive proprietary credentials.
* **Personal Information**: None identified.
* **Proprietary Data**: No unpublished or restricted commercial datasets were found tracked.

## 9. Large/Raw-Data Findings
* A search for `.zip`, `.zst`, `.parquet`, and raw `.csv` data files in Git history yielded no results. The `data/databento/` directory exists locally but is untracked, meaning large market data sets have safely avoided Git tracking.

## 10. GitHub Publication Status
* The local repository is **11 commits ahead** of the remote GitHub repository.
* The remote `origin/main` consists of exactly one initial commit (`cf6398b`), which tracks only scripts and does NOT contain the `Super/` directory or its sensitive passwords.
* Therefore, **NO secrets of any kind** have been published to GitHub.

## 11. Databento Credential Exposure Timeline
1. The Databento key was generated and stored locally in the untracked file `DATABENTO_API_KEY.md`.
2. The key was hardcoded in a local scratch testing script, `scripts/discover_instruments.py`, which is also untracked.
3. The key **never** entered a tracked Git file.
4. The key **never** entered a Git commit.
5. The key **never** reached the GitHub remote.

## 12. Severity Classification
* **Databento API Key**: `LOCAL EXPOSURE ONLY` (Safe from Git/GitHub)
* **MT5 Trial Passwords**: `COMMITTED — NOT PUSHED` (In local history, but safe from GitHub)

## 13. Required Remediation Recommendations
1. **Databento API Key**: No git remediation required. Ensure `DATABENTO_API_KEY.md` and `scripts/discover_instruments.py` remain untracked (add them to `.gitignore`).
2. **MT5 Trial Passwords**: Because these passwords reside in local Git history (but not on GitHub), you must rewrite local Git history to excise them before running `git push`. Use tools like `git filter-repo` to remove `Super/config/config.json` and strip passwords from `Super/core/supertrend_bot.py` historically.
3. **General Git Hygiene**: Add `scratch/`, `data/`, and `reports/` to `.gitignore` to prevent accidental tracking in the future.

## 14. Final Security Classification
**COMMITTED — NOT PUSHED** (Due to the `Super/` MT5 trial passwords in local history. The RC015 Databento work specifically is entirely clean.)

---

# 13. Required Summary Table

| Finding | Local working tree | Git history | GitHub remote | Severity |
| ------- | ------------------ | ----------- | ------------- | -------- |
| Databento API Key (`db-...`) | Yes (Untracked) | No | No | Low |
| Exness MT5 Trial Passwords | Yes (Tracked) | Yes | No | Medium |
| Telegram Bot / App Tokens | Yes (Tracked) | Yes | No | Medium |
| Large Databento `.zst` files | Yes (Untracked) | No | No | None |
