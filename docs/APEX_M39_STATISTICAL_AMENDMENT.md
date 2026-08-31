# APEX M39 Statistical Amendment

**Milestone:** M39-CR (Control Review)
**Date:** 2026-08-24
**Type:** Methodology / Implementation Amendment
**Required By:** Future controlled re-execution of M39 (e.g., M39-R2 or M39 Amendment)

---

## 1. What Is Wrong

The M38 bootstrap specification (and M39 implementation) does not construct the null distribution of the Anderson-Darling statistic under H₀.

**M38 Step 6 says:**
> "Split Y_bootstrap back into treatment and control using the same session-state labels."

**This preserves group labels within each resampled day-block.** Under H₀, group labels should be randomly assigned. Without label shuffling, the bootstrap tests day-level variation, not group-level distributional differences.

---

## 2. The Correct Bootstrap Procedure

The corrected bootstrap must:

### Step 1: Pool all observations
```python
all_returns = np.concatenate([lno_returns, ctrl_returns])
```

### Step 2: Assign day labels
```python
all_dates = pd.DatetimeIndex(all_timestamps).normalize()
unique_days = np.sort(np.unique(all_dates))
day_ids = np.array([day_id_map[d] for d in all_dates])
```

### Step 3: Partition into day-boundary blocks
```python
blocks = []
for day_idx in range(n_days):
    mask = day_ids == day_idx
    blocks.append(all_returns[mask])
```

### Step 4: Resample blocks with replacement
```python
sample_indices = rng.choice(n_blocks, size=n_blocks, replace=True)
boot_returns = np.concatenate([blocks[i] for i in sample_indices])
```

### Step 5: Randomly assign group labels (THE CORRECTED STEP)
```python
# Under H₀, group labels are exchangeable
# Randomly assign LNO/control labels, preserving ORIGINAL group sizes
n_lno_original = len(lno_returns)
n_ctrl_original = len(ctrl_returns)

# Create shuffled labels
all_labels = np.concatenate([np.ones(n_lno_original), np.zeros(n_ctrl_original)])
rng.shuffle(all_labels)  # Shuffle labels

boot_lno = boot_returns[all_labels == 1]
boot_ctrl = boot_returns[all_labels == 0]
```

**Alternatively (block-aware label shuffling):**
```python
# Shuffle group labels WITHIN each resampled day-block
boot_lno_list = []
boot_ctrl_list = []
for block_idx in sample_indices:
    block_data = blocks[block_idx]
    block_n = len(block_data)
    # Determine LNO fraction from original data on this day
    # Then randomly assign labels preserving that fraction
    n_lno_in_block = original_lno_count_per_day[block_idx]
    labels = np.concatenate([np.ones(n_lno_in_block), np.zeros(block_n - n_lno_in_block)])
    rng.shuffle(labels)
    boot_lno_list.append(block_data[labels == 1])
    boot_ctrl_list.append(block_data[labels == 0])
boot_lno = np.concatenate(boot_lno_list)
boot_ctrl = np.concatenate(boot_ctrl_list)
```

### Step 6: Compute AD statistic
```python
boot_result = anderson_ksamp([boot_lno, boot_ctrl])
ad_stats[b] = boot_result.statistic
```

### Step 7: Compute p-value
```python
p_value = np.sum(ad_stats >= observed_ad_stat) / n_successful
```

---

## 3. Why This Fixes the Problem

Under the corrected procedure:
- The bootstrap pools all observations (removing group-label association)
- Resamples day-blocks (preserving temporal correlation)
- Randomly assigns group labels (simulating H₀)
- Computes AD statistic from the labeled bootstrap sample
- The empirical distribution of bootstrap AD statistics approximates the null distribution

The observed AD statistic will now be compared against a null distribution that properly accounts for:
1. Day-level serial correlation (via block resampling)
2. The null hypothesis of identical distributions (via random label assignment)

---

## 4. Inference Hierarchy Amendment

M38 does not specify an explicit hierarchy between the SciPy significance level and the bootstrap p-value. The amendment must specify one of:

### Option A (Recommended): Bootstrap-primary

> The corrected bootstrap p-value is the primary decision criterion.
> SciPy significance level is reported as secondary/descriptive.
> Reject H₀ if corrected bootstrap p-value < 0.05.

**Rationale:** The bootstrap was designated by M38 as the null-calibration mechanism. It accounts for serial correlation (the reason it was specified). The SciPy asymptotic test does not account for serial correlation.

### Option B: SciPy-primary

> SciPy significance level is the primary decision criterion.
> The corrected bootstrap is reported as a robustness check.
> Reject H₀ if SciPy significance_level < 0.05.

**Rationale:** Simpler, does not depend on bootstrap implementation quality.

### Option C: Both required

> Reject H₀ only if BOTH SciPy significance_level < 0.05 AND corrected bootstrap p-value < 0.05.

**Rationale:** Most conservative; requires agreement from both inference mechanisms.

---

## 5. What Must NOT Change

The following M38 frozen parameters must NOT be amended:

| Parameter | Value |
|---|---|
| Block length | 24 |
| Block boundaries | Day (00:00 UTC) |
| Replications | 10,000 |
| Seed | 42 |
| RNG | PCG-64 |
| AD test | `scipy.stats.anderson_ksamp` |
| Forward horizon | 60 minutes |
| Session definition | LONDON_NY_OVERLAP (RC013 frozen) |
| Control definition | Non-LNO, forward window non-overlapping |
| Calendar exclusions | Sat/Sun, Dec 25–Jan 1, Good Friday, Thanksgiving, NFP |
| Alpha | 0.05 two-sided |

---

## 6. What MUST Change

| Component | Current (M38/M39) | Corrected |
|---|---|---|
| Bootstrap Step 6 | Preserve group labels | Randomly assign group labels after resampling |
| Inference hierarchy | Unspecified | Explicitly specified (bootstrap-primary recommended) |

---

## 7. Expected Outcome

With the corrected bootstrap:

- The bootstrap null distribution will be centered near zero (reflecting H₀ of identical distributions)
- The observed AD statistic of 228.38 will be far in the right tail
- The corrected bootstrap p-value will be very small (likely ≈ 0)
- The SciPy and bootstrap results will be **consistent**

This is because the AD statistic of 228.38 is so extreme (35× the 0.1% critical value) that even a properly specified bootstrap with serial correlation should produce a tiny p-value.

---

## 8. Classification

This is a **methodology / implementation amendment**, not a new research question. The core scientific question remains unchanged. Only the bootstrap null-construction procedure and inference hierarchy need correction.

The amendment does NOT:
- Change the research question
- Change the session definition
- Change the horizon
- Change the control population
- Add new tests
- Optimize toward a result
- Reopen RC013 monetization

---

## 9. Authorization Required

A future controlled milestone (e.g., M39-R2) must:
1. Implement the corrected bootstrap procedure
2. Establish the inference hierarchy
3. Re-run the experiment
4. Report corrected results

This must be authorized by the APEX control session. Do not begin without authorization.
