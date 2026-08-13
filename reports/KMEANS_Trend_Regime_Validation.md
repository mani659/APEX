# K-Means Trend / Regime Validation

## 1. Original Script Audit
> The original K-means clusters historical strategy-parameter performance, while market regimes are assigned by deterministic rules.

## 2. Deterministic Baseline (OOS Period)
| Regime     |     N |     H1_Mean |     H1_Std |   Continuation_Prob |
|:-----------|------:|------------:|-----------:|--------------------:|
| TRENDING   |  8931 | 4.59294e-05 | 0.0026645  |            0.485276 |
| STABLE     | 27028 | 5.0023e-05  | 0.00233799 |            0.485386 |
| EXHAUSTION |  3428 | 9.60329e-05 | 0.00253839 |            0.518378 |

## 3. Walk-Forward ML Results
| Model      |   Regime |     N |     H1_Mean |   Cohens_D_H1 |   ml_vol_avg |   ml_adx_avg |
|:-----------|---------:|------:|------------:|--------------:|-------------:|-------------:|
| wf_KMeans  |        1 | 18191 | 3.94613e-05 |  -0.000966624 |     0.480752 |      357.414 |
| wf_KMeans  |        0 | 16293 | 5.61664e-05 |   0.00620739  |     0.519692 |      361.355 |
| wf_KMeans  |        2 | 15664 | 2.93181e-05 |  -0.00524337  |     0.510212 |      385.552 |
| wf_GMM     |        1 | 16741 | 5.56497e-05 |   0.00606364  |     0.516225 |      369.443 |
| wf_GMM     |        0 | 16881 | 5.31368e-05 |   0.00480305  |     0.506149 |      361.456 |
| wf_GMM     |        2 | 16526 | 1.59486e-05 |  -0.0109451   |     0.485189 |      371.655 |
| wf_HDBSCAN |       -1 | 50148 | 4.17205e-05 |   0           |     0.502605 |      367.483 |

## 4. Final Scientific Conclusion
> **Negative:** Regime classification does not provide meaningful predictive information.

### REJECTED. The ML models do not materially improve over the deterministic baseline.
