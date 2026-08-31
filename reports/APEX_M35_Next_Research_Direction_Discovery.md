# APEX M35: Next Research Direction Discovery After HIGH_VOL Closure

## Section A — Current APEX State

| Item | Value |
|---|---|
| Branch | `main` |
| HEAD | `1f1be70` (M34 closure commit) |
| Remote | Untouched |
| HIGH_VOL branch | CLOSED (M34) |
| M35 status | COMPLETE |
| M36 status | PLANNED — NOT STARTED |

---

## Section B — Surviving APEX Knowledge Base

### Validated (Do Not Reopen)

| # | Finding | Source | Key Statistic |
|---|---|---|---|
| 1 | HIGH_VOL is a structural distributional primitive | RC012 | D=0.1927 |
| 2 | HIGH_VOL persistence is non-memoryless | M13/M14 | p<0.0001, n=794 |
| 3 | Onset features predict future persistence | M17-R2 | C-index=0.6656 |
| 4 | Predicted persistence scales forward RV | M21 | p=0.0032 |
| 5 | Predicted persistence does NOT predict direction | M24 | p=0.6418 |
| 6 | Predicted persistence scales excursion envelope | M27 | p=7.5×10⁻⁵ |
| 7 | Session-transition primitives are structural | RC013 | Validated |
| 8 | Cross-asset transmission rejected | RC014 | No incremental information |

### Rejected / Closed

| Branch | Status | Reason |
|---|---|---|
| V1 directional alpha | REJECTED (RC007) | Asymmetric exits mask negative expectancy |
| Context rescue | REJECTED (RC008) | Context cannot manufacture an edge |
| Behavioral discovery | REJECTED (RC009-010) | M1 directional prediction exhausted |
| Microstructure | PAUSED (RC011) | Insufficient data |
| Spot monetization of HIGH_VOL | REJECTED (RC012 S007-011) | Tail risk, whipsaw, friction |
| Cross-asset volatility transmission | REJECTED (RC014) | No incremental information |
| HIGH_VOL boundary translation | NOT ESTABLISHED (M31) | 99.75% saturation |
| Dynamic translation | REJECTED (M33) | Methodologically weak |
| HIGH_VOL branch | CLOSED (M34) | Scientifically mature, implementation unresolved |
| RC015 listed-option path | CLOSED | Liquidity requirements not met |

### Data-Constrained (Not Rejected)

| Hypothesis | Status | Constraint |
|---|---|---|
| Carry/funding premium | UNTESTED (RC013) | Historical financing data unavailable |
| True institutional liquidity | UNTESTED (RC011) | Level 3 order book data unavailable |

### Reusable Data & Infrastructure

| Asset | Type | Status |
|---|---|---|
| EURUSD M1/M15 | OHLCV | 5.5 years, canonical |
| XAUUSD M1 | OHLCV | Available |
| XAGUSD M1 | OHLCV | Available |
| BTCUSD M1 | OHLCV | Available |
| USATECHIDXUSD M1 | OHLCV | Available |
| RC015 option data | BBO/IV | 222 events, 699 options (Databento) |
| HIGH_VOL episode ledger | Derived | 794 episodes |
| M17-R2 prediction artifacts | Derived | Walk-forward Cox PH |
| Python infrastructure | Code | Research scripts, analysis pipeline |
| Databento API | External | Active key |

### Methodological Lessons (Reusable Governance)

1. Do not relax event definitions to inflate sample size.
2. Methodology must be repaired before economic testing.
3. Statistical calibration must match data structure.
4. Feature count is not scientific value.
5. Continuous relationships do not automatically translate into binary thresholds.
6. APEX stopping principle: continue only when next question is materially different.

---

## Section C — Candidate Branches

### Candidate 1: Session-Transition Distributional Asymmetry

**Research Question**: Do deterministic session transitions (London Open, NY Overlap, Asian compression) create persistent distributional asymmetry — e.g., reliable mean-reversion during low-liquidity windows versus reliable path-expansion during high-liquidity transitions — that can be characterized without localized behavioral prediction?

**Scientific Continuity**: Builds directly on RC013 validated session-transition primitives. The HIGH_VOL × session interaction became infeasible (n=8), but session transitions independently exist as structural market properties.

**Novel Information**: Resolves whether session mechanics create exploitable distributional differences independent of HIGH_VOL. This is a genuinely different question from HIGH_VOL translation.

**Existing Resources**: EURUSD M1 data (5.5 years), RC013 session definitions, existing Python infrastructure.

**Future Data Requirements**: None. Uses existing canonical datasets.

**Dominant Risk**: Multiple testing (many session × distribution combinations). **Mitigation**: Pre-declare exact session windows and distributional tests before execution.

**Classification**: `HIGH PRIORITY`

---

### Candidate 2: LOW_VOL Compression Breakout

**Research Question**: Do LOW_VOL compression states (RC012 Study 006 identified +3.55 pips net expectancy over 16-hour horizon) predict subsequent volatility expansion with measurable distributional asymmetry?

**Scientific Continuity**: Mirrors the HIGH_VOL approach but tests the opposite tail of the volatility distribution. RC012 Study 006 provided preliminary evidence.

**Novel Information**: Untested distributional primitive. LOW_VOL compression is the structural inverse of HIGH_VOL expansion.

**Existing Resources**: EURUSD M1 data, HIGH_VOL episode ledger (can derive LOW_VOL complement), existing infrastructure.

**Future Data Requirements**: None.

**Dominant Risk**: Survivorship bias in compression identification. **Mitigation**: Define compression states ex-ante using trailing volatility percentile thresholds.

**Classification**: `HIGH PRIORITY`

---

### Candidate 3: Cross-Asset Relative Value Ranking

**Research Question**: Does cross-sectional momentum or relative value ranking across the 5 available assets (EURUSD, XAUUSD, XAGUSD, BTCUSD, USATECHIDXUSD) create a portfolio-level edge independent of localized prediction?

**Scientific Continuity**: Extends RC014 cross-asset work from transmission to relative value. RC014 rejected volatility contagion but did not test relative ranking.

**Novel Information**: Untested structural relationship at the portfolio level.

**Existing Resources**: M1 data for all 5 assets, existing infrastructure.

**Future Data Requirements**: None.

**Dominant Risk**: Nonstationarity of cross-asset relationships. **Mitigation**: Walk-forward validation with expanding window.

**Classification**: `PROMISING BUT REQUIRES DESIGN WORK`

---

### Candidate 4: Intraday Volatility Seasonality

**Research Question**: Do intraday volatility patterns (hour-of-day, day-of-week) create persistent distributional differences that are independent of session-transition effects?

**Scientific Continuity**: Extends session-transition work to finer temporal granularity.

**Novel Information**: Untested temporal structure at sub-session resolution.

**Existing Resources**: EURUSD M1 data, existing infrastructure.

**Future Data Requirements**: None.

**Dominant Risk**: Overfitting to calendar patterns. **Mitigation**: Pre-declare exact hour/day bins and test only hypothesis-specified distributions.

**Classification**: `PROMISING BUT REQUIRES DESIGN WORK`

---

### Candidate 5: Options-Based Variance Risk Premium

**Research Question**: Does the APEX HIGH_VOL signal predict IV-RV divergence — i.e., is the validated volatility primitive mispriced by the options market?

**Scientific Continuity**: Directly addresses the instrument mismatch identified in post-RC012 review. RC015 infrastructure exists (222 events, 699 options, Databento).

**Novel Information**: Whether the validated volatility primitive is economically mispriced.

**Existing Resources**: RC015 option data, HIGH_VOL episode ledger, Databento API.

**Future Data Requirements**: Additional option IV data for the 222-event universe (BBO acquisition was incomplete).

**Dominant Risk**: Data acquisition cost and liquidity constraints (RC015 path was closed). **Mitigation**: Use only the existing RC015 dataset without new acquisition.

**Classification**: `LOW PRIORITY` — constrained by RC015 closure and data limitations

---

### Candidate 6: Multi-Asset Volatility Regime Generalization

**Research Question**: Does the HIGH_VOL regime classification (RC012) generalize across instruments — i.e., does EURUSD HIGH_VOL predict XAUUSD or BTCUSD volatility expansion?

**Scientific Continuity**: Tests cross-instrument robustness of RC012 primitive.

**Novel Information**: Generalization beyond EURUSD.

**Existing Resources**: M1 data for all 5 assets, HIGH_VOL definition.

**Future Data Requirements**: None.

**Dominant Risk**: Proxy mismatch (different assets may have different volatility dynamics). **Mitigation**: Test each asset independently with its own HIGH_VOL threshold.

**Classification**: `PROMISING BUT REQUIRES DESIGN WORK`

---

### Candidate 7: Path-Dependent Volatility Harvesting Simulation

**Research Question**: Can simple symmetric harvesting strategies capture positive expectancy from HIGH_VOL expansions using existing data?

**Scientific Continuity**: Directly tests the economic value question.

**Novel Information**: Whether the validated primitive has extractable economic value.

**Existing Resources**: EURUSD M1 data, HIGH_VOL episode ledger.

**Future Data Requirements**: None.

**Dominant Risk**: Implementation parameterization (stop/target distances are researcher degrees of freedom). This is the same problem that closed the HIGH_VOL branch.

**Classification**: `REJECT` — implementation parameterization, not scientific inquiry

---

## Section D — Scoring

| Dimension | C1 | C2 | C3 | C4 | C5 | C6 | C7 |
|---|---|---|---|---|---|---|---|
| Scientific continuity | 4 | 4 | 3 | 3 | 4 | 4 | 3 |
| Novel information | 4 | 4 | 3 | 3 | 5 | 3 | 2 |
| Data feasibility | 5 | 5 | 5 | 5 | 2 | 5 | 5 |
| Observability | 5 | 5 | 4 | 5 | 4 | 4 | 4 |
| Ex-ante defensibility | 5 | 5 | 4 | 4 | 3 | 4 | 2 |
| Falsifiability | 5 | 5 | 4 | 5 | 4 | 4 | 3 |
| Independence | 4 | 4 | 5 | 5 | 4 | 4 | 3 |
| Cost efficiency | 5 | 5 | 5 | 5 | 2 | 5 | 5 |
| Strategic relevance | 4 | 3 | 3 | 3 | 4 | 3 | 3 |
| Complexity | 4 | 5 | 3 | 4 | 3 | 3 | 3 |
| **TOTAL** | **45** | **44** | **39** | **42** | **35** | **39** | **33** |

---

## Section E — Primary Recommendation

**Candidate 1: Session-Transition Distributional Asymmetry (score=45/50)**

### Why It Is Superior
1. **Highest information value**: Resolves whether session mechanics — a validated structural primitive (RC013) — create persistent distributional differences. This is a genuinely different question from HIGH_VOL translation.
2. **Zero data cost**: Uses existing EURUSD M1 data (5.5 years). No acquisition needed.
3. **Strong scientific continuity**: Builds directly on RC013 validated primitives.
4. **High ex-ante defensibility**: Session windows are deterministic and can be frozen before execution.
5. **Clear falsification**: The test can produce a clean negative result without redesign.
6. **Independence**: Does not reopen HIGH_VOL or any closed branch.

### What Existing Evidence Supports It
- RC013 validated session transitions as structural distributional primitives.
- RC012 confirmed that volatility expansion is direction-neutral.
- Post-RC013 review identified session mechanics as the highest-value existing-data opportunity.
- Post-RC012 review confirmed that distributional/payoff-geometry approaches are scientifically superior to directional prediction.

### What Remains Unknown
- Whether session transitions create persistent distributional asymmetry.
- Whether the asymmetry is exploitable without localized behavioral prediction.
- How session effects interact with volatility state.

### How It Can Be Frozen Ex Ante
- Session windows defined by deterministic UTC timestamps (London Open: 08:00, NY Overlap: 13:00, Asian: 00:00–08:00).
- Distributional tests specified before viewing outcomes.
- Walk-forward validation with expanding window.

### What Would Falsify It
- If the distributional differences across session windows are not statistically significant under frozen HAC-corrected inference.
- If the differences are significant but too small to be economically meaningful.

---

## Section F — Backup Recommendation

**Candidate 2: LOW_VOL Compression Breakout (score=44/50)**

If session-transition research is not authorized, LOW_VOL compression is the next highest-value direction. It mirrors the HIGH_VOL approach, uses existing data, and tests an untested distributional primitive.

---

## Section G — Future Milestone Planning

> **M36 — Candidate Research Methodology Design**
> Status: `PLANNED — NOT STARTED`

M36 would design the frozen methodology for the selected primary direction (Session-Transition Distributional Asymmetry). No experiment is authorized in M36 — only methodology design.

---

## Section H — Mandatory HIGH_VOL Closure Constraint

HIGH_VOL is `CLOSED`. The following are NOT permitted:
- Another HIGH_VOL boundary
- Another HIGH_VOL multiplier
- Another HIGH_VOL monetization parameter
- Another grid optimization
- Another directional test designed to rescue M24
- Another economic translation of M27

Reopening HIGH_VOL requires explicit evidence that M34's closure was invalid. No such evidence exists.

---

**MANDATORY STOP. No M36 or later milestone authorized.**
