# RC009 Study 003 Sequence Analysis

## Multiple-Testing Disclosure
- **Number of state dimensions**: 2 (Volatility, Direction)
- **Number of composite states**: 9
- **Sequence lengths tested**: N=3, N=5
- **Unique N=3 sequences observed**: 691
- **Unique N=5 sequences observed**: 22853
- **Number of outcome metrics**: 4 (ret_60, ret_240, mfe_60, mae_60)
The exploratory nature of this search means these findings must be validated independently.

## State Frequency Table
| State | Count | Frequency |
| :--- | :--- | :--- |
| NORMAL_VOL_BULL | 23771 | 17.5% |
| NORMAL_VOL_BEAR | 23552 | 17.4% |
| NORMAL_VOL_FLAT | 21018 | 15.5% |
| LOW_VOL_FLAT | 15813 | 11.7% |
| HIGH_VOL_BEAR | 14415 | 10.6% |
| HIGH_VOL_BULL | 14049 | 10.4% |
| LOW_VOL_BULL | 9138 | 6.7% |
| LOW_VOL_BEAR | 8703 | 6.4% |
| HIGH_VOL_FLAT | 5149 | 3.8% |

## State Transition Matrix (Probability of Next State)
| Current State | HIGH_VOL_BEAR | HIGH_VOL_BULL | HIGH_VOL_FLAT | LOW_VOL_BEAR | LOW_VOL_BULL | LOW_VOL_FLAT | NORMAL_VOL_BEAR | NORMAL_VOL_BULL | NORMAL_VOL_FLAT |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIGH_VOL_BEAR | 20.5% | 21.7% | 10.7% | 0.3% | 0.5% | 2.4% | 10.5% | 12.9% | 20.5% |
| HIGH_VOL_BULL | 21.0% | 21.5% | 10.7% | 0.4% | 0.3% | 2.3% | 12.7% | 10.8% | 20.3% |
| HIGH_VOL_FLAT | 27.6% | 24.3% | 14.9% | 0.1% | 0.1% | 1.2% | 6.8% | 7.7% | 17.2% |
| LOW_VOL_BEAR | 2.2% | 1.5% | 0.1% | 16.8% | 20.0% | 22.1% | 15.6% | 16.8% | 4.9% |
| LOW_VOL_BULL | 2.2% | 1.4% | 0.2% | 19.2% | 18.3% | 22.6% | 16.5% | 15.0% | 4.5% |
| LOW_VOL_FLAT | 2.5% | 2.3% | 0.3% | 15.0% | 16.3% | 21.9% | 17.6% | 17.6% | 6.6% |
| NORMAL_VOL_BEAR | 8.1% | 7.7% | 1.4% | 4.8% | 5.6% | 12.3% | 20.3% | 22.4% | 17.5% |
| NORMAL_VOL_BULL | 7.9% | 7.3% | 1.5% | 5.7% | 5.0% | 12.8% | 22.2% | 20.8% | 16.8% |
| NORMAL_VOL_FLAT | 12.1% | 11.8% | 2.7% | 2.6% | 2.5% | 8.1% | 19.9% | 19.9% | 20.5% |

## N=3 Sequence Analysis
Evaluating 9 highly populated sequences (N > 1000).

| Sequence | Count | Mean Ret | Ctrl Mean | Effect Size (vs Ctrl) | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| NORMAL_VOL_BULL -> NORMAL_VOL_BULL -> NORMAL_VOL_BULL | 1111 | -0.00012 | -0.00003 | -0.1010 | EXPLORATORY (Weak Edge) |
| NORMAL_VOL_BULL -> NORMAL_VOL_BEAR -> NORMAL_VOL_BEAR | 1165 | -0.00002 | 0.00002 | -0.0327 | REJECTED (No Edge) |
| NORMAL_VOL_BULL -> NORMAL_VOL_BEAR -> NORMAL_VOL_BULL | 1273 | 0.00000 | -0.00003 | 0.0317 | REJECTED (No Edge) |
| NORMAL_VOL_FLAT -> NORMAL_VOL_BEAR -> NORMAL_VOL_BULL | 1018 | -0.00004 | -0.00003 | -0.0161 | REJECTED (No Edge) |
| NORMAL_VOL_BULL -> NORMAL_VOL_BULL -> NORMAL_VOL_BEAR | 1164 | 0.00000 | 0.00002 | -0.0128 | REJECTED (No Edge) |
| NORMAL_VOL_BEAR -> NORMAL_VOL_BULL -> NORMAL_VOL_BULL | 1142 | -0.00002 | -0.00003 | 0.0087 | REJECTED (No Edge) |
| NORMAL_VOL_BEAR -> NORMAL_VOL_BULL -> NORMAL_VOL_BEAR | 1224 | 0.00002 | 0.00002 | 0.0086 | REJECTED (No Edge) |
| NORMAL_VOL_BEAR -> NORMAL_VOL_BEAR -> NORMAL_VOL_BULL | 1130 | -0.00003 | -0.00003 | -0.0062 | REJECTED (No Edge) |
| NORMAL_VOL_BEAR -> NORMAL_VOL_BEAR -> NORMAL_VOL_BEAR | 1032 | 0.00002 | 0.00002 | 0.0036 | REJECTED (No Edge) |

## N=5 Sequence Analysis
Evaluating 0 highly populated sequences (N > 1000).

No sequences met the population criteria.

## Candidate Register
None.

## Conclusion
**Status:** Negative. The sequence of states does NOT contain meaningful predictive information beyond the final state itself. All sequences converged back to their baseline distributions.
