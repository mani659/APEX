# RC009 Study 001 Candidate Analysis

Total Evaluated Candidates: 4

## Baseline A: Unconditional (100k random samples)
- 60-bar Forward Return Mean: 0.00000 (Std: 0.00105)
- 240-bar Forward Return Mean: -0.00001 (Std: 0.00209)

## Candidate: C1_Squeeze
- **Occurrence Count**: 5
- **Frequency**: 0.0002% of all bars
- **60-Bar Mean Return**: 0.00043 (Median: 0.00046)
- **240-Bar Mean Return**: 0.00068 (Median: 0.00071)
- **Mean MFE / MAE (60-bar)**: 0.00068 / 0.00021
- **Win Rate (60-bar)**: 100.0%
- **Effect Size vs Baseline A (60-bar)**: 0.4060
- **Effect Size vs Control C (60-bar)**: -1.3138

**Classification**: REJECTED (Insufficient Sample Size)

---

## Candidate: C2_Absorption
- **Occurrence Count**: 15432
- **Frequency**: 0.7559% of all bars
- **60-Bar Mean Return**: 0.00002 (Median: 0.00001)
- **240-Bar Mean Return**: 0.00002 (Median: 0.00001)
- **Mean MFE / MAE (60-bar)**: 0.00135 / 0.00132
- **Win Rate (60-bar)**: 50.1%
- **Effect Size vs Baseline A (60-bar)**: 0.0197
- **Effect Size vs Control C (60-bar)**: 0.0080

**Classification**: REJECTED (No Meaningful Effect Size)

---

## Candidate: C3_Ignition
- **Occurrence Count**: 19014
- **Frequency**: 0.9313% of all bars
- **60-Bar Mean Return**: -0.00001 (Median: -0.00002)
- **240-Bar Mean Return**: -0.00002 (Median: -0.00003)
- **Mean MFE / MAE (60-bar)**: 0.00074 / 0.00075
- **Win Rate (60-bar)**: 48.4%
- **Effect Size vs Baseline A (60-bar)**: -0.0092
- **Effect Size vs Control C (60-bar)**: -0.0090

**Classification**: REJECTED (No Meaningful Effect Size)

---

## Candidate: C4_Flag
- **Occurrence Count**: 15843
- **Frequency**: 0.7760% of all bars
- **60-Bar Mean Return**: -0.00006 (Median: -0.00006)
- **240-Bar Mean Return**: -0.00011 (Median: -0.00009)
- **Mean MFE / MAE (60-bar)**: 0.00039 / 0.00048
- **Win Rate (60-bar)**: 42.7%
- **Effect Size vs Baseline A (60-bar)**: -0.0564
- **Effect Size vs Control C (60-bar)**: -0.0322

**Classification**: REJECTED (No Meaningful Effect Size)

---

## Candidate Ranking Table
| Candidate | Count | Effect Size (Base) | Effect Size (Ctrl) | Classification |
| :--- | :--- | :--- | :--- | :--- |
| C1_Squeeze | 5 | 0.406 | -1.3138 | REJECTED (Insufficient Sample Size) |
| C4_Flag | 15843 | -0.0564 | -0.0322 | REJECTED (No Meaningful Effect Size) |
| C2_Absorption | 15432 | 0.0197 | 0.008 | REJECTED (No Meaningful Effect Size) |
| C3_Ignition | 19014 | -0.0092 | -0.009 | REJECTED (No Meaningful Effect Size) |


## Rejected Candidate Register
- C1_Squeeze
- C2_Absorption
- C3_Ignition
- C4_Flag
