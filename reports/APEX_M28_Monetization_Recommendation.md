# APEX M28: Monetization Recommendation

## 1. Primary Recommendation: Direction-Neutral Dispersion Boundary
The highest-information-value economic research direction is **Candidate B: Direction-Neutral Dispersion Boundary Translation**.

**Economic Uncertainty Resolved**: M27 proved we can predict the maximum absolute excursion envelope. However, knowing the envelope is only economically useful if it can bound risk. The dispersion boundary test resolves whether this predictive signal can mathematically constrain the maximum theoretical drawdown (capital requirement) of a non-directional, symmetric liquidity-provision or dispersion model.

**Why it is superior**: It embraces the M24 directional failure. Since we know the market will expand in variance (M21) to a predictable distance (M27) without a predictable trend (M24), the optimal structural payoff is symmetric. A dispersion framework places symmetric exposure, and its sole risk is unbounded excursion. If the APEX signal bounds that excursion, it creates an economically viable, directionless synthetic payoff.

## 2. Backup Recommendation
**Candidate C: Symmetric Double-Barrier Breach Probability**. If bounding a continuous dispersion grid is too complex, evaluating the discrete probability of hitting a symmetric take-profit on *both* sides of the market (straddle-like spot execution) is the next most logical translation.

## 3. Future Data Requirements
To test the Dispersion Boundary realistically in later stages, the following non-predictive execution data will eventually be required:
- Average EURUSD Bid/Ask spread per session.
- Standard 12-hour broker funding/swap rates.
*(Note: These are not required for the immediate M29 structural hypothesis, but are required before PnL is claimed).*

## 4. Future Execution Requirements
The methodology must account for:
- **Path Dependence**: Unlike M27 which just searched for a max value, dispersion drawdown is strictly path-dependent. The sequence of highs and lows within the 12 hours dictates the intermediate capital draw.
- **Margin Mechanics**: Spot FX margin requirements and lot sizing.

## 5. Major Methodological Risks
- **Curve-Fitting the Payoff**: The greatest risk is explicitly using the M27 coefficients to retroactively tune the dispersion grid size. The grid spacing and boundary definitions *must* be defined strictly ex-ante, completely independent of the M27 slope, to avoid leakage.

## 6. Exact Next Milestone
**M29 — Dispersion Boundary Economic Methodology Design**.
M29 will design and freeze the rigid rules for calculating the theoretical capital drawdown of a synthetic direction-neutral dispersion execution, mapping it directly against the M17-R2 prediction.
