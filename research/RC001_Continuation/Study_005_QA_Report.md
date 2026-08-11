# Research Study 005 QA: Statistical Verification Pass

## 1. Verified Statistics & 4. Practical Significance

### Asian Session
- **Bullish**: Mean=0.15505 | 95% CI=[-0.15932, 0.46943] | Effect=0.011 | Win Rate=52.3% | Expectancy=0.15059 | Sig=False
- **Bearish**: Mean=0.18286 | 95% CI=[-0.15902, 0.52474] | Effect=0.013 | Win Rate=52.6% | Expectancy=0.18286 | Sig=False

### London Session
- **Bullish**: Mean=-0.14102 | 95% CI=[-0.48447, 0.20243] | Effect=-0.011 | Win Rate=51.1% | Expectancy=-0.14733 | Sig=False
- **Bearish**: Mean=-0.53853 | 95% CI=[-0.92014, -0.15691] | Effect=-0.044 | Win Rate=48.5% | Expectancy=-0.54642 | Sig=False

### London/NY Overlap Session
- **Bullish**: Mean=-1.34525 | 95% CI=[-2.04225, -0.64825] | Effect=-0.069 | Win Rate=49.3% | Expectancy=-1.34525 | Sig=False
- **Bearish**: Mean=-0.83530 | 95% CI=[-1.50034, -0.17025] | Effect=-0.049 | Win Rate=51.2% | Expectancy=-0.85048 | Sig=False

### New York Session
- **Bullish**: Mean=0.29608 | 95% CI=[-0.08388, 0.67603] | Effect=0.022 | Win Rate=51.8% | Expectancy=0.29275 | Sig=False
- **Bearish**: Mean=-0.15045 | 95% CI=[-0.54544, 0.24453] | Effect=-0.012 | Win Rate=51.1% | Expectancy=-0.15859 | Sig=False

### Other Session
- **Bullish**: Mean=1.67648 | 95% CI=[0.93974, 2.41322] | Effect=0.104 | Win Rate=53.4% | Expectancy=1.67648 | Sig=True
- **Bearish**: Mean=1.90368 | 95% CI=[1.03075, 2.77661] | Effect=0.112 | Win Rate=53.9% | Expectancy=1.90368 | Sig=True

## 5. Temporal Stability (Year-by-Year for 'Other')
- Bullish profitable years: 2 / 2
- Bearish profitable years: 0 / 2
- Stability OK: False

## 6. Sample Adequacy
- **Asian**: N=13969 (14.0%) - Sufficient: True
- **London**: N=8972 (9.0%) - Sufficient: True
- **London/NY Overlap**: N=5544 (5.5%) - Sufficient: True
- **New York**: N=9005 (9.0%) - Sufficient: True
- **Other**: N=3295 (3.3%) - Sufficient: True

## 7. Timestamp Verification
Confirmed timezone mappings to UTC were properly aligned and generated the expected distribution sizes.

## 8. Consistency Audit
- CONTRADICTION: Report claims SUPPORTED, but the edge is not temporally stable across years.

## 9. Automatic Verdict
**FRAGILE**

**Outcome C**: Major inconsistencies discovered. Original Study 005 conclusions invalidated.
