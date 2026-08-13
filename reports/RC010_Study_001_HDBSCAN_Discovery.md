# RC010 Study 001 - Unsupervised Behavioral State Discovery

## 1. Methodology
- **Algorithm:** HDBSCAN
- **Min Cluster Size:** 500
- **Features (5):** `path_15`, `path_60`, `vol_pct`, `partic_pct`, `body_imbalance`
- **Preprocessing:** RobustScaler
- **Total Samples Analyzed:** 135612

## 2. Cluster Overview
Number of clusters found: 0

| Cluster | N | % of Pop | Mean 60 | Med 60 | Cohen D | Temporal Dist (P1/P2/P3) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Noise (-1) | 135612 | 100.0% | -0.00000 | 0.00000 | 0.000 | 33% / 33% / 33% |

## 3. Explaining Discovered Clusters
## 4. Final Conclusion
**NEGATIVE RESULT**

HDBSCAN did not discover any naturally occurring behavioral states with a strong predictive edge (Cohen's d >= 0.2). The market does not naturally separate into distinct, predictive behavioral clusters using these fundamental descriptors.
