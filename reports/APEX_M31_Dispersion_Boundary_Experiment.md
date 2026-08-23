# APEX M31: Dispersion Boundary Empirical Experiment

## 1. Primary Empirical Result
The empirical boundary breach experiment establishes that the M17-R2 conditionally predicted `HIGH_VOL` duration does **not** significantly condition the probability of breaching the ex-ante $1.0 \times \text{RV20}_{onset}$ symmetric boundary. 

- **Baseline Unconditional Breach Probability**: 99.75% (395 out of 396 episodes breached).
- **Slope ($\beta$)**: 0.054025
- **HAC Robust SE**: 0.045732
- **t-statistic**: 1.1813
- **p-value**: 0.2375
- **95% CI**: [-0.035608, 0.143658]

## 2. Scientific Interpretation
**`BOUNDARY TRANSLATION NOT ESTABLISHED`**.

Because the p-value ($0.2375$) is greater than the predefined alpha ($0.05$), we fail to reject the null hypothesis ($H_0: \beta = 0$). 

**Mechanistic Explanation**:
The failure to reject the null is driven by a massive base-rate saturation. 395 out of 396 episodes (99.75%) successfully breached the $1.0 \times \text{RV20}_{onset}$ boundary. This means that during a structurally confirmed `HIGH_VOL` event, the 12-hour excursion is so fundamentally expansive that it practically guarantees a breach of the standard trailing 20-period volatility magnitude, *regardless* of whether the M17-R2 risk score predicts the event will be short-lived or deeply persistent. The specific boundary chosen was too narrow to act as a discriminative threshold.

## 3. Relationship to M27
**M27 (Continuous MAE) + M31 (Binary Boundary)**: M27 was strongly positive ($p < 0.0001$), but M31 is null. 
This is completely scientifically valid. It confirms that while the M17-R2 signal strictly governs the **continuous structural envelope** of the variance expansion (M27), the specific arbitrary distance of $1.0 \times \text{RV20}_{onset}$ (M31) lies far inside that envelope for almost all events. The continuous relationship exists, but this particular ex-ante threshold does not discriminate breach probability because it is breached universally.

## 4. Capital-Requirement Interpretation
M31 establishes only that this specific spatial boundary ($1.0 \times \text{RV20}_{onset}$) has no predictive breach information conditional on the APEX signal. It does **not** establish margin limits, capital requirements, or true drawdown, nor does it invalidate the idea of a direction-neutral execution structure. It simply proves that if a dispersion grid bounds its maximum risk exactly at the prior rolling $RV20$ distance, it will almost certainly be blown out (99.75% of the time).

## 5. Methodology Integrity Audit
- **Prediction Vector**: Unaltered M17-R2 artifacts.
- **Sample**: 396 valid OOS episodes.
- **Boundary**: Exactly $1.0 \times \text{RV20}_{onset}$ derived strictly prior to $t$.
- **HAC Lag**: Fixed exactly at $48$.
- **Verdict**: `PASS`. The methodology was executed flawlessly according to M29 constraints, preventing boundary hacking.

## 6. M32 Recommendation
The continuous expansion is highly predictable (M27), but the first naive binary threshold test (M31) hit 99% saturation. This proves that blindly translating physical continuous relationships into arbitrary economic thresholds is fragile. M32 must revisit the **Economic Monetization Strategy**, potentially determining if the boundary threshold itself should be scaled *as a function of the risk score* (a dynamically predicted boundary) rather than a static historical one, or if we must proceed directly to a full path-dependent execution simulation to capture the continuous variance dynamically rather than discretely.
