# APEX IC2 — Cross-Market Transferability & Crypto-Volatility Economic Methodology Design

**Date**: 2026-08-25
**Milestone**: IC2
**Classification**: CONTROL / RESEARCH-DESIGN ONLY — no economic experiment, no backtest, no strategy, no data acquisition

---

## 1. Core Transfer Question

Frozen research-design question:

> **Can the validated APEX volatility-state information be transferred from EURUSD to BTC in a causally clean, ex-ante, observable manner such that the resulting BTC volatility forecast can later be compared against BTC implied volatility?**

This contains two gates:

| Gate | Question | Status |
|------|----------|--------|
| **Gate A** | Does an EURUSD-derived HIGH_VOL-style onset signal have a defensible BTC analogue? | Must be determined |
| **Gate B** | Can the BTC analogue produce a forward realized-volatility forecast comparable with contemporaneous BTC IV? | Must be determined |

IC2 does not assume either gate passes.

---

## 2. What Transfers vs. What Must Be Redefined

### EURUSD HIGH_VOL State — Conceptual Decomposition

The M17-R2 experiment validated a chain of relationships on EURUSD:

```
RV20 > 80th percentile → HIGH_VOL state triggered
        ↓
Onset features (Breakout Intensity, Variance Momentum) extracted at t_onset
        ↓
Cox PH model predicts episode duration
        ↓
Predicted duration scales forward 12h RV (M21, p=0.0032)
Predicted duration scales forward 12h excursion (M27, p=7.5e-05)
```

IC2 decomposes this into transferable and non-transferable components:

### What Transfers (Conceptual Architecture)

| Component | What It Is | Why It Transfers |
|-----------|-----------|-----------------|
| Volatility clustering as regime | Markets exhibit persistent high/low vol regimes | Universal market microstructure property; well-documented across asset classes |
| RV-style measure as state indicator | Rolling realized volatility identifies vol regimes | Standard technique; applicable to any time series with sufficient observations |
| Percentile-based threshold activation | Vol regime is triggered when RV exceeds a historical threshold | Structural concept; percentile is distribution-independent |
| Onset-state variables predict future vol | Features at regime onset contain information about episode duration | Structural insight from M17-R2; testable on any asset |
| Cox PH as duration model | Semi-parametric survival model for regime duration | Asset-agnostic statistical methodology |
| Forward RV as economic outcome | Predicted duration maps to forward realized volatility | RV is a standard financial quantity; definition is universal |
| Non-directional payoff alignment | Predicted vol expansion → convex instrument payoff | Instrument-agnostic economic reasoning |

### What Must Be Redefined (EURUSD-Specific Parameters)

| Component | EURUSD Value | Why It Cannot Transfer |
|-----------|-------------|----------------------|
| RV20 window length | 20 M15 bars (5 hours) | BTC intraday microstructure differs; optimal window may differ |
| 80th percentile threshold | EURUSD-specific distribution | BTC volatility distribution has different scale, shape, and dynamics |
| Breakout Intensity definition | EURUSD-calibrated | Feature coefficients are data-dependent |
| Variance Momentum definition | EURUSD-calibrated | Feature coefficients are data-dependent |
| Cox PH coefficients | EURUSD-trained | Model parameters are instrument-specific |
| C-index expectation | 0.6656 | May differ on BTC; unknown until tested |
| Forward RV horizon | 12 hours (48 M15 bars) | Must match BTC option expiry availability |

### Critical Implication

**No EURUSD-specific numerical parameter transfers to BTC.** What transfers is:
1. The mathematical architecture (RV-based state → onset features → duration model → forward RV forecast)
2. The structural insight (volatility clustering onset contains predictive information)
3. The economic logic (predicted RV > IV → convex payoff)

The BTC implementation must be built on BTC data using BTC-specific parameters.

---

## 3. Transfer Approach Selection

### Candidate Approaches Evaluated

#### Approach A — Direct Structural Transfer

Apply EURUSD state architecture to BTC with deterministic normalization.

- Same RV20 window, same 80th percentile threshold, same feature definitions
- Only the price data changes from EURUSD to BTC

**Assessment:**
- Scientific continuity: 3/5 — uses the same architecture
- Cross-market defensibility: 2/5 — EURUSD parameters are unlikely to be optimal for BTC
- Ex-ante freezeability: 4/5 — deterministic application
- Data feasibility: 4/5 — requires BTC price data
- IV/RV observability: 3/5 — depends on BTC options data
- Liquidity realism: 3/5 — depends on Deribit liquidity
- OOS feasibility: 3/5 — limited by parameter appropriateness
- Complexity: 5/5 — simplest approach
- Independence: 3/5 — partially disguised EURUSD rescue if parameters fail
- Information value: 3/5 — tests whether EURUSD parameters happen to work

**Verdict: REJECT** — Direct parameter transfer across fundamentally different asset classes is not scientifically defensible. EURUSD and BTC have different volatility dynamics, different trading hours, different market microstructure, and different distributional properties. Applying EURUSD-specific percentile thresholds to BTC would produce an arbitrary state definition with no scientific justification.

#### Approach B — BTC Re-estimation (SAME ARCHITECTURE, BTC-SPECIFIC PARAMETERS)

Rebuild the same mathematical architecture on BTC data. All parameters re-estimated from BTC.

- BTC RV calculation (window TBD, likely 20 M15 bars or adapted)
- BTC-specific percentile threshold (80th percentile of BTC RV distribution)
- BTC-specific onset features (redefined for BTC price dynamics)
- BTC-trained Cox PH model
- BTC-specific forward RV horizon

**Assessment:**
- Scientific continuity: 5/5 — exact same mathematical architecture
- Cross-market defensibility: 4/5 — parameters are BTC-native; architecture is validated
- Ex-ante freezeability: 5/5 — all parameters computable from BTC data before testing
- Data feasibility: 4/5 — requires BTC M15 price data (available via Tardis)
- IV/RV observability: 4/5 — requires BTC options data (available via Deribit historical)
- Liquidity realism: 3/5 — depends on Deribit options liquidity
- OOS feasibility: 5/5 — full walk-forward validation possible on BTC
- Complexity: 3/5 — more complex than A, but manageable
- Independence: 5/5 — fully independent BTC model; EURUSD serves as architectural motivation only
- Information value: 5/5 — resolves the key transfer question definitively

**Verdict: SELECTED** — This is the scientifically defensible approach. It tests whether the EURUSD-validated *concept* (not parameters) works on BTC. The EURUSD findings serve as motivation for the architecture, not as a source of parameters. This is honest about what actually transfers.

#### Approach C — Cross-Market Latent State

Use EURUSD signal to condition BTC state. E.g., when EURUSD enters HIGH_VOL, use this as additional information for BTC volatility prediction.

**Assessment:**
- Scientific continuity: 3/5 — uses EURUSD signal but in a different way
- Cross-market defensibility: 2/5 — RC014 rejected cross-asset transmission for tested relationships
- Ex-ante freezeability: 2/5 — requires defining the conditioning structure
- Data feasibility: 3/5 — requires both EURUSD and BTC data
- IV/RV observability: 3/5 — depends on BTC options
- Liquidity realism: 3/5 — same as B
- OOS feasibility: 2/5 — complex two-market design
- Complexity: 1/5 — most complex approach
- Independence: 2/5 — closely tied to EURUSD signal
- Information value: 3/5 — tests cross-market conditioning

**Verdict: REJECT** — RC014 already conclusively rejected cross-asset transmission for the tested relationships (source vol → target vol). While the specific question here (EURUSD vol state → BTC vol state) is slightly different, the fundamental architecture is the same: using one market's information to predict another's. RC014 provides strong prior evidence against this approach. Additionally, the complexity is unwarranted given that Approach B provides a cleaner test.

#### Approach D — No Transfer (STOP)

Conclude that EURUSD state is instrument-specific and abandon the crypto-options mechanism.

**Assessment:**
- Scientific continuity: 1/5 — abandons the research direction
- Cross-market defensibility: 5/5 — avoids potentially invalid transfer
- Ex-ante freezeability: 5/5 — no methodology to freeze
- Data feasibility: 5/5 — no data needed
- IV/RV observability: 5/5 — N/A
- Liquidity realism: 5/5 — N/A
- OOS feasibility: 5/5 — N/A
- Complexity: 5/5 — simplest (no work)
- Independence: 5/5 — fully independent
- Information value: 1/5 — resolves nothing new

**Verdict: MAINTAIN AS FALLBACK** — This is the correct action if Approach B fails at IC3. But it should not be the default action when a scientifically defensible test (Approach B) exists.

### Final Approach Selection

**Primary: Approach B — BTC Re-estimation**

This approach:
1. Uses the EURUSD-validated architecture as scientific motivation
2. Rebuilds the model entirely on BTC data
3. Tests whether the *concept* (not parameters) transfers
4. Can be frozen before any empirical execution
5. Produces a clean, independently validated BTC volatility forecast
6. Can legitimately be compared with BTC implied volatility

### What This Means for the Transfer Claim

The IC1 hypothesis stated: "HIGH_VOL onset dynamics transfer from EURUSD to BTC."

Under Approach B, the refined claim becomes:

> "The EURUSD-validated *architectural concept* — that realized volatility regime onsets contain predictive information about future volatility duration, which in turn predicts forward realized volatility — can be reconstructed on BTC using BTC-native parameters, producing a BTC-specific volatility forecast."

This is a weaker but more honest claim than direct parameter transfer. It tests whether the *phenomenon* (predictable vol clustering) exists on BTC, not whether EURUSD parameters happen to work.

---

## 4. BTC State Construction — Frozen Architecture

### Step 1: BTC Realized Volatility Measure

**Frozen measure:** Rolling realized volatility over N M15 bars.

```
RV_N(t) = sqrt(252 * 24 * (4/N) * sum_{i=1}^{N} r_{t-i}^2)
```

Where:
- r = log return of BTC M15 close prices
- Annualization constant: 252 trading days × 24 hours × 4 M15 bars per hour = 24,192
- N = window length (to be frozen in IC3 based on BTC microstructure)

**Parameter to freeze in IC3:** Window length N. Options: 8 (2 hours), 12 (3 hours), 20 (5 hours), 24 (6 hours).

### Step 2: BTC HIGH_VOL Threshold

**Frozen rule:** RV_N(t) > 80th percentile of the BTC RV_N historical distribution.

The percentile is computed over the full available BTC history (expanding window or fixed lookback — to be frozen in IC3).

**Parameter to freeze in IC3:** Lookback window for percentile calculation.

### Step 3: Onset Feature Extraction

At each HIGH_VOL onset timestamp t_onset:

- **Breakout Intensity:** Magnitude of the initial volatility spike. Defined as RV_N(t_onset) / RV_N(t_onset - 1).
- **Variance Momentum:** Short-term trend in RV. Defined as RV_N(t_onset) - RV_N(t_onset - k) for some lag k.

**Parameters to freeze in IC3:** Exact feature definitions and lag k.

### Step 4: Duration Model

**Frozen model class:** Cox Proportional Hazards (statsmodels.PHReg).

Trained on BTC HIGH_VOL episodes using BTC onset features as predictors.

**Target:** Duration of HIGH_VOL episode (number of contiguous M15 bars above threshold).

**Validation:** Walk-forward expanding window, chronological split.

**Parameter to freeze in IC3:** Minimum training episodes before first OOS prediction.

### Step 5: Forward RV Forecast

The Cox PH model produces a continuous risk score at each onset.

This risk score is then used as a predictor in a secondary regression:

```
Forward_RV_12h(t) = α + β * RiskScore(t) + ε(t)
```

Where Forward_RV_12h is the realized volatility over the subsequent 12 hours.

**This is the BTC volatility forecast that will be compared with BTC implied volatility.**

**Parameter to freeze in IC3:** Forward RV horizon (12 hours or adapted to match option expiry).

---

## 5. IV/RV Comparability

### Primary Comparison

```
Predicted BTC Forward RV (from Step 5) vs. BTC ATM Implied Volatility at t_onset
```

### Why ATM IV

- Most liquid option on any expiry
- Directly comparable to realized volatility (both are annualized vol measures)
- Minimizes skew/smile contamination
- Standard reference in vol trading

### Maturity Matching

| Component | Value | Rationale |
|-----------|-------|-----------|
| Forward RV horizon | 12 hours (48 M15 bars) | Matches EURUSD M27 horizon; standard for intraday vol |
| Primary option maturity | 12-hour expiry (if available) or next daily expiry | Direct maturity match |
| Maximum maturity mismatch | 6 hours | Prevents comparing 12h RV with 7-day IV |
| Interpolation | NOT permitted | Introduces researcher degrees of freedom |
| If no matching expiry | Use nearest expiry ≤ 24 hours | Practical constraint on Deribit expiries |

### Information Boundary

At timestamp t_onset (BTC HIGH_VOL onset):

- **Observable:** BTC price history → RV computation, onset features, Cox PH risk score, forward RV forecast
- **Observable:** BTC options market → ATM IV for available expiries
- **NOT observable:** Future BTC prices, future RV, future IV, future option prices

The comparison is:

```
At t_onset:
    Predicted future RV = f(RiskScore)
    Current ATM IV = observable from options market
    Future realized RV = unknown (will be computed later for validation)
```

### Why This Comparison Is Meaningful

If the Cox PH model predicts that BTC will experience sustained high volatility over the next 12 hours, and the current ATM IV for a 12-hour option is below the predicted RV, then:

- The option is "cheap" relative to what it will be worth at expiry
- A long straddle captures the IV-RV spread as positive expected value
- This is the economic mechanism that IC3-IC6 will ultimately test

If ATM IV is already above the predicted RV, no edge exists — the market has already priced the expected volatility.

---

## 6. Economic Mechanism — Full Chain

```
EURUSD-validated concept (motivation)
        ↓
BTC RV-based state construction (BTC-native parameters)
        ↓
BTC onset features → Cox PH → risk score
        ↓
Risk score → forward 12h RV forecast
        ↓
Compare predicted RV with contemporaneous ATM IV
        ↓
If predicted RV > IV → long straddle has positive expected value
If predicted RV ≤ IV → no edge (market already priced it)
        ↓
Direction-neutral convex payoff captures IV-RV spread
```

### Why Predicted RV > IV ≠ Automatic Profit

Even if predicted RV > IV, the straddle P&L depends on:

- **Option premium:** The upfront cost of buying the straddle
- **Bid-ask spread:** 1-3 vol points for ATM BTC options on Deribit
- **Theta decay:** The option loses value as time passes; the predicted RV must materialize within the option's remaining life
- **Vega exposure:** If IV rises after purchase, the straddle gains on vega even before expiry
- **Path dependency:** The straddle needs movement at specific times relative to the option's life
- **Execution timing:** If IV spikes immediately after the onset signal, the edge may disappear before execution
- **Funding costs:** Inverse BTC options have BTC-denominated margin requirements

IC2 acknowledges these cost components. IC5 (Economic Execution) will model them explicitly. IC2's scope is limited to establishing whether the forecast/IV comparison is methodologically defensible.

---

## 7. BTC Data Requirements

### Existing/Local Data

| Dataset | Status | Use |
|---------|--------|-----|
| EURUSD M1/M15 OHLCV | ✅ Available in repository | NOT USED for BTC model (EURUSD serves as motivation only) |
| Existing APEX Python infrastructure | ✅ Available | Can be adapted for BTC analysis |

### Required External Data

| Dataset | Provider | Granularity | Period | Required Fields | Approx. Scale | Why Necessary |
|---------|----------|-------------|--------|----------------|---------------|---------------|
| BTC M15 OHLCV | Tardis / CryptoDataDownload / Deribit API | 15-minute | March 2019 – present | Timestamp, Open, High, Low, Close, Volume | ~500K rows | BTC RV computation, state construction, onset features, forward RV |
| BTC M1 OHLCV | Same providers | 1-minute | March 2019 – present | Timestamp, Open, High, Low, Close, Volume | ~3M rows | Alternative RV calculation (realized variance) |
| BTC Deribit options tick/ohlcv | Tardis / CryptoDataDownload | Per-option OHLCV | March 2019 – present | Instrument ID, expiry, strike, type, timestamp, OHLCV, bid/ask | ~10M+ rows | IV surface construction, ATM IV extraction |
| BTC perpetual/futures prices | Deribit API | 1-minute or tick | March 2019 – present | Timestamp, price, funding rate | ~3M rows | Mark price for option valuation |
| BTC option instrument definitions | Deribit API | Static | Full history | Instrument ID, expiry, strike, type, settlement | ~10K instruments | Map option IDs to strike/expiry |

### Data Cost

- Tardis: Free historical data for Deribit (no API key required for historical download)
- CryptoDataDownload: Free CSV downloads
- Deribit API: Free for historical market data (public endpoints)
- Approximate total data volume: ~15-20 GB uncompressed
- **Cost: $0.00**

### Data Quality Considerations

| Risk | Mitigation |
|------|-----------|
| Missing option expiries | Deribit has continuous daily expiries since 2021; weekly since 2019 |
| Thin early data (2019) | Use expanding window; early period has lower weight in training |
| Options bid-ask data quality | Use mid-price from Tardis bid/ask; filter for wide spreads |
| BTC hard fork / exchange events | Deribit BTC is continuous; no fork splits in options data |
| Exchange downtime | Filter out periods with no option data |

---

## 8. Instrument Feasibility Re-Audit

### Can BTC Options Support Maturity-Matched IV/RV Comparison?

| Requirement | Available? | Detail |
|-------------|-----------|--------|
| Historical ATM IV | ✅ Yes | Deribit options chain available since 2019; ATM strike can be identified from instrument definitions |
| Maturity matching | ✅ Yes | Deribit offers daily expiries (12h, 24h, 48h, etc.); sufficient granularity for 12h RV comparison |
| Timestamp alignment | ✅ Yes | Options OHLCV timestamps align with BTC spot timestamps |
| Bid/ask availability | ✅ Yes | Tardis provides bid/ask for each option tick |
| Liquidity for ATM options | ⚠️ Moderate | ATM options are most liquid; bid-ask 1-3 vol points; sufficient for observation, may be wide for execution |
| Strike granularity | ✅ Yes | Deribit uses $500 or $1000 strikes for BTC; sufficient for ATM identification |
| Expiry availability | ✅ Yes | Daily, weekly, monthly, quarterly expiries available |
| Full surface | ✅ Yes | Multiple strikes × multiple expiries available via Deribit API |

### Key Feasibility Finding

**The BTC options observation architecture CAN support maturity-matched IV/RV comparison.** This is a material improvement over RC015 (CME EURUSD listed options), where the observation architecture failed the liquidity test.

The difference:
- RC015 required exact-fresh synchronized option/futures observations → extremely rare → liquidity failed
- IC2 requires daily ATM IV snapshots → available on every Deribit trading day → sufficient

### Remaining Risk

The IC2 observation architecture is for **observation** (comparing predicted RV with observed IV). The eventual **execution** architecture (IC6) requires additional feasibility checks for:
- Options order book depth at signal time
- Execution speed during vol events
- Ability to enter/exit straddle positions at target prices

These are IC6 concerns, not IC2 concerns.

---

## 9. Cross-Market Validation Architecture

### Proposed Milestone Sequence

```
IC2 (THIS MILESTONE)
    Methodology design for BTC transfer
    ↓
IC3 — BTC Transferability Pre-Economic Validation
    Reconstruct BTC HIGH_VOL state (BTC-native parameters)
    Validate BTC onset predictability (walk-forward Cox PH)
    Compute BTC forward RV forecast
    Falsification gate: BTC C-index ≤ 0.55 → STOP
    ↓
IC4 — BTC IV-RV Observability Audit
    Construct BTC IV surface from Deribit historical data
    Verify ATM IV extractability at BTC HIGH_VOL onset
    Verify maturity matching (12h RV vs 12h/24h IV)
    Falsification gate: IV data insufficient → STOP
    ↓
IC5 — Economic Methodology Design
    Design frozen straddle test methodology
    Define trade entry/exit/hold rules
    Define cost model
    Freeze all parameters
    Falsification gate: methodology not defensible → STOP
    ↓
IC6 — Economic Execution / Validation
    Execute frozen straddle test
    Compute PnL after costs
    Falsification gate: PnL ≤ 0 after costs → STOP
```

**Note:** This is planning only. IC3-IC6 are NOT authorized. Each requires explicit control-session authorization.

### Why 5 Milestones (Not 3)

The three-milestone limit was proposed by the independent audit for a single research direction. The crypto-options direction has a structural complication: it requires a **cross-market transfer** (EURUSD → BTC) before the economic test can begin. This adds 1-2 milestones compared to a same-instrument research direction.

The audit's governance rules apply: each milestone must advance vertically toward tradability. IC3 (predictive validation on BTC) is the critical gate. If IC3 fails, the direction dies. If IC3 succeeds, IC4-IC6 are a standard 3-milestone economic sequence.

---

## 10. Hidden Reparameterization — Prohibited Actions

IC2 explicitly prohibits the following in any future milestone:

| Prohibited Action | Why |
|------------------|-----|
| Tuning BTC percentile threshold to maximize C-index | Outcome-dependent parameter selection |
| Tuning BTC RV window to maximize predictive power | Researcher degree of freedom |
| Selecting BTC forward horizon after viewing outcomes | Horizon selection must be frozen before IC3 |
| Choosing option maturity from profitable results | Maturity must be frozen before IC4 |
| Selecting strikes after observing payoff | Strike selection must be frozen before IC5 |
| Choosing IV measure after viewing economics | IV representation must be frozen before IC5 |
| Adding features after seeing null results | Feature set frozen before IC3 |

**All parameters must be frozen in IC2/IC3 before any empirical execution.**

---

## 11. Falsification Gates

| Gate | Milestone | Criterion | Action if Failed |
|------|-----------|-----------|-----------------|
| BTC state definition | IC3 | HIGH_VOL-style state cannot be defined on BTC (insufficient episodes, threshold undefined) | STOP — abandon crypto-options mechanism |
| BTC predictability | IC3 | Walk-forward C-index ≤ 0.55 on BTC OOS | STOP — onset features do not predict BTC vol duration |
| BTC forward RV mapping | IC3 | β coefficient for risk score → forward RV is insignificant (p > 0.05) | STOP — BTC risk score does not map to forward RV |
| IV data availability | IC4 | ATM IV not extractable for sufficient BTC option expiries | STOP — IV comparison infeasible |
| IV maturity matching | IC4 | No option expiry within 6 hours of 12h forward RV horizon | STOP — maturity mismatch too large |
| Economic defensibility | IC5 | Straddle methodology not defensible under frozen rules | STOP — economic test not designable |
| Execution costs | IC6 | Straddle PnL ≤ 0 after realistic costs | STOP — no economic edge after costs |

---

## 12. Control Questions — Answers

### 1. Is the EURUSD-derived information structurally transferable to BTC?

**The architectural concept is transferable. The specific parameters are not.**

The EURUSD findings establish that:
- Volatility clustering creates identifiable regimes
- Onset features predict regime duration
- Predicted duration maps to forward RV

These are structural market properties that are well-documented across asset classes in the academic literature. The *concept* that BTC exhibits similar dynamics is highly plausible.

However, no EURUSD-specific numerical parameter (threshold, feature coefficient, model weight) can be applied to BTC without re-estimation. The transfer is conceptual, not parametric.

### 2. If yes, what exactly transfers and what must be redefined?

**Transfers:**
- Mathematical architecture (RV-based state → Cox PH → forward RV forecast)
- Economic logic (predicted RV > IV → convex payoff)
- Statistical methodology (walk-forward OOS validation)

**Must be redefined:**
- All model parameters (threshold, features, coefficients)
- Window lengths and lookback periods
- Forward RV horizon (must match available option expiries)
- Feature definitions (adapted for BTC price dynamics)

### 3. Can future BTC realized volatility be compared to an observable contemporaneous BTC implied-volatility measure?

**Yes, with appropriate maturity matching.**

Deribit offers BTC options with daily, weekly, and monthly expiries. ATM IV for a 12-hour or 24-hour expiry is observable at any timestamp when the options market is open. The 12-hour forward RV horizon can be matched with a 12-hour or 24-hour option expiry. Maturity mismatch can be kept within 6 hours.

### 4. Is the BTC options observation architecture realistically researchable?

**Yes.** Unlike RC015 (CME EURUSD listed options), BTC options on Deribit have:
- Continuous historical data since March 2019
- Daily expiry availability
- Sufficient ATM liquidity for observation
- Free public data access
- No synchronization requirements beyond standard timestamp alignment

### 5. What is the strongest falsifiable economic hypothesis for IC3?

> "BTC HIGH_VOL-style onset features (Breakout Intensity, Variance Momentum computed from BTC M15 data) predict future BTC episode duration with walk-forward C-index > 0.55 (above random baseline of 0.50), and the resulting risk score is significantly associated with forward 12-hour BTC realized volatility (β ≠ 0, p < 0.05)."

### 6. If any key link is not defensible, should APEX stop rather than force the crypto-options mechanism?

**Yes.** If IC3 falsifies BTC predictability, the crypto-options mechanism has no foundation. APEX should then either:
- Pause economic development (Architecture D from the independent audit)
- Return to broader instrument/mechanism discovery (restart IC1 with different candidates)
- NOT force the mechanism by adjusting parameters until it "works"

---

*IC2 is a control/research-design milestone. No experiments were run. No data was acquired. No strategy was coded. No options were traded.*
