# RC015 Study 003 — Implied vs Realized Volatility Methodology Pilot

## 3. Maturity Normalization
Year fraction convention: Exact total seconds to 20:00 UTC on expiry date divided by (365.25 * 24 * 3600).
Sample days to expiry: 115.0 days.

## 4. Realized Volatility
- **Method**: Standard deviation of 1-minute log returns.
- **Horizons**: 1-hour (60 mins) and 4-hour (240 mins) forward looking.
- **Annualization**: $\sqrt{252 \times 24 \times 60}$ = 602.395
- **Source Price**: Auxiliary EURUSD MT5 spot midpoint.

## 5. Implied vs Realized Comparison
### 1-Hour Volatility Gap (RV - IV)
- mean: -0.011028
- median: -0.018495
- std: 0.024912
- min: -0.041878
- max: 0.079906
- p5: -0.035212
- p25: -0.025992
- p50: -0.018495
- p75: -0.004535
- p95: 0.054810

### 4-Hour Volatility Gap (RV - IV)
- mean: -0.011563
- median: -0.018139
- std: 0.019502
- min: -0.037753
- max: 0.026934
- p5: -0.034906
- p25: -0.026351
- p50: -0.018139
- p75: 0.003371
- p95: 0.024735

## 6. RC012 HIGH_VOL Linkage
- High Vol Obs Count: 3746
- Mean IV: 0.054294
- Mean 1h RV: 0.045829
- Mean 1h Gap: -0.008465

## 7. RC013 Session Linkage
### ASIA_TO_LONDON (06:00-08:00 UTC)
- Obs Count: 706
- Mean IV: 0.054876
- Mean 1h RV: 0.029883
- Mean 1h Gap: -0.024993

### LONDON_NY_OVERLAP (12:00-16:00 UTC)
- Obs Count: 2622
- Mean IV: 0.054337
- Mean 1h RV: 0.066278
- Mean 1h Gap: 0.011941

## 8. Moneyness
Sample observation:
- Strike: 1.14
- Futures: 1.1599249999999999
- Moneyness (K/F): 0.982822
- State: OTM

## 9. Option-Market Quality
- Median Quote Spread: 0.000200
- Median IV Spread (Ask IV - Bid IV): 0.000977
- Total Synchronized Quotes: 9602

## 11. Lookahead Audit
LOOKAHEAD VIOLATIONS = 0
Forward realized volatility uses strictly `.shift(-H)` on the rolling standard deviation, guaranteeing that at time `t`, only returns from `t+1` to `t+H` are included.

## 13. Final Classification
### PASS
The methodology is technically ready for historical research. All primitives can be linked natively without lookahead.
