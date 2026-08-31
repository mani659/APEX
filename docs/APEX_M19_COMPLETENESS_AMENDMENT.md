Original unresolved choices:

Annualization convention:
Chosen value: N_annual = 24,192 (Convention A)
Scientific rationale: EURUSD operates on a 24/5 trading calendar. Assuming 252 trading days per year and 24 hours per day (96 M15 periods per day), the correct annualization factor is 96 * 252 = 24,192. Convention B (365 calendar days) is inappropriate as it assumes volatility generation over weekends when the market is closed.

HAC specification:
Chosen maxlags: 48 (Candidate A)
Scientific rationale: The explicitly chosen forward RV horizon is 48 M15 bars. The maximum structural overlap of the dependent variable for sequential but non-simultaneous HIGH_VOL onsets is exactly 48 periods. Truncating the HAC lag at 48 directly targets the physical temporal dependence created by the window design.

Inference:
Alpha: 0.05
Tail: Two-sided
Scientific rationale: M19 stated the relationship must be "materially different" from zero, implying no firm predefined directional hypothesis regarding whether longer persistence implies higher or lower forward variance. A standard alpha of 0.05 with a two-sided test is the universal scientific default for exploratory translation.

Primary null:
H0: beta = 0
H1: beta != 0

What remains unchanged:
The entire M19 frozen methodology (horizon, baseline, outcome metric, prediction boundary, dependence treatment class, effect measure, and sample) remains exactly as frozen.

New researcher degrees of freedom: None.
How each is frozen: The explicit integer variables `N_annual = 24192`, `maxlags = 48`, and `alpha = 0.05 (two-tailed)` are now hardcoded requirements for the M21 execution.

M21 execution requirements: M21 is now authorized to execute the exact OLS regression defined in M19 using the parameters frozen in this amendment.
