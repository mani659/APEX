# RC015 Study 007 - Observation-Time Methodology Audit

## 1. Authoritative Observation Rule
After auditing `scripts/rc015_study_007_volatility_pricing_discovery.py`, the frozen methodology is definitively **Model A: Any Wednesday M15 observation qualifies**.
The discovery script executes the following logic:
1. Groups BBO observations into 15-minute buckets across the entire Wednesday.
2. Evaluates the contemporaneous ATM distance for all quotes inside that bucket.
3. Selects the closest eligible option cross-sectionally for each M15 bucket.

Therefore, the event observation time is not a single predetermined hour (like 15:00 UTC). The entire Wednesday price path is evaluated.

## 2. Selection Bias Audit
The 700-row universe was generated using an algorithm that effectively chose the Wednesday timestamp where each candidate option was closest to ATM.
- **Events Affected:** 128 (out of 222)
- **Options Affected:** 512
- **Different Timestamps Permitted?:** YES. Different options within the same event were legitimately allowed to choose different timestamps.

**Is this selection bias?** NO.
Because the frozen economic script (Model A) evaluates every M15 bucket on Wednesday, any option that achieves ATM status (`<= 0.0020`) at *any* point on Wednesday is a legitimate candidate that the script might select for that specific bucket. The reporting timestamp in the previous revalidation was simply proof of eligibility (the point of minimum distance). Retaining all options that are ATM at any M15 bucket guarantees that the superset of options required for the simulation is downloaded, preventing missing-data errors. The lookahead logic in selecting the "best" timestamp for the CSV does not alter the economic integrity of the universe; it correctly identifies the required BBO subset.

## 3. Universe Comparison
- **Old Stage-1 (530 IDs):** Failed to cover all 222 events (only covered 60).
- **Repaired Candidates (707 IDs):** Reconstructed full 222-event coverage, but erroneously used the daily close `ohlcv-1d`, drifting from the true intraday BBO ATM threshold.
- **True-BBO Revalidation (699 IDs):** Rigorously applied the exact M15 contemporaneous BBO midpoints. The 8 IDs that dropped out did so because they never satisfied the `<= 0.0020` threshold at any point during Wednesday. The differences are fully and deterministically explained by the frozen moneyness rule.

## 4. Reproducibility Test
The deterministic rule used (finding the minimum absolute distance across all 96 M15 buckets for each candidate) acts as an absolute mathematical bound. Given the identical `BBO-1m` inputs, the 700 rows will reproduce identically. The BBO-1m futures data is not cached permanently (as requested, no new Databento downloads), but the algorithm itself relies on no stochastic or discretionary inputs.

## 5. Final Decision Classification
**PASS**
The 699-ID / 700-row universe correctly captures the superset of options required by the frozen "every Wednesday M15 bucket" methodology.

## 6. Mandatory Stop Checklist
1. **Rule:** Model A (Any Wednesday M15 observation qualifies).
2. **Current 699-ID Universe Valid?:** YES.
3. **Methodological Drift from Timestamp Selection?:** NO. The "closest ATM" selection guarantees the superset of data needed for the cross-sectional M15 discovery script.
4. **Affected Events/Options:** 128 events / 512 options have multiple timestamps.
5. **Ready for Option BBO Purchase?:** YES.

> **Final Question:** Is the 699-option / 700-row universe genuinely the frozen RC015 Study 007 universe, or did the “closest M15 point on Wednesday” selection introduce a methodological change that must be repaired before buying Option BBO?
>
> **Answer:** It is genuinely the frozen universe. The "closest M15 point" selection was used safely to prove eligibility for the superset of options that the frozen M15 discovery script will eventually evaluate. It did not introduce a methodological change, and no repair is needed. The universe is ready for Option BBO acquisition.
