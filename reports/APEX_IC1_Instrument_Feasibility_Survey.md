# APEX IC1 — Instrument Feasibility & Economic Mechanism Discovery

**Date**: 2026-08-25
**Milestone**: IC1
**Classification**: CONTROL / RESEARCH-DESIGN ONLY — no economic experiment, no backtest, no strategy

---

## 1. Validated Information Inventory

### Evidence Level Classification

| # | Finding | Source | Evidence Level | Monetizable? |
|---|---------|--------|---------------|-------------|
| 1 | HIGH_VOL is a structural distributional primitive | RC012 | L1 Descriptive | No (requires translation) |
| 2 | HIGH_VOL persistence is non-memoryless | M13/M14 | L1 Descriptive | No (requires translation) |
| 3 | Onset features predict future persistence | M17-R2 | L2 Predictive | Maybe (C-index=0.6656) |
| 4 | Predicted persistence scales forward RV | M21 | L3 Economic Translation | Yes (if RV prediction → payoff) |
| 5 | Predicted persistence does NOT predict direction | M24 | Negative | Constraining |
| 6 | Predicted persistence scales excursion envelope | M27 | L3 Economic Translation | Yes (if excursion → payoff) |
| 7 | Expansion is near-symmetric | M27 | L3 | Constraining (no directional edge) |
| 8 | LNO session state has different 1-hour return CDF | M39-R2 | L1 Descriptive | Maybe (skewness component) |
| 9 | Cross-asset transmission rejected | RC014 | Negative | Constraining |

### What APEX Knows

1. **When EURUSD is likely to experience sustained high volatility** (M17-R2 risk score)
2. **How much forward volatility/excursion to expect** (M21, M27)
3. **That the movement is direction-neutral** (M24, M27 ratio=0.9218)
4. **That LNO hours have a different return distribution** (M39-R2, p=0.0001)

### What APEX Does NOT Know

1. **Direction** — no directional edge exists
2. **Cross-asset generalization** — all findings are EURUSD-specific
3. **Whether the information creates economic value** — no payoff mechanism tested
4. **Whether the market already prices this information** — IV-RV relationship untested

---

## 2. Candidate Mechanisms — Full Analysis

### Candidate A — Direct Volatility / Convex Payoff

**Concept**: Use options or similar convex instruments to monetize predicted volatility expansion.

#### Mechanism Chain

```
VALIDATED INFORMATION: M17-R2 risk score predicts forward RV/excursion
        ↓
ECONOMIC MECHANISM: When predicted RV > IV premium → buy convex instrument → realized movement exceeds cost
        ↓
INSTRUMENT: Long straddle / strangle / volatility swap
        ↓
PAYOFF: max(realized vol × position size - premium paid, -premium paid)
        ↓
TRADEABLE CONDITION: Predicted risk score above threshold AND IV discount to predicted RV
        ↓
MEASURABLE OUTCOME: P&L per trade after costs
```

#### Why This Could Work

- The signal directly predicts what straddles profit from (movement magnitude)
- The signal is direction-neutral, matching the straddle's direction-neutral payoff
- APEX has evidence that predicted persistence maps to forward RV (p=0.0032) and excursion (p=7.5e-05)
- If the market does NOT fully price this predictability into options premiums, expected value exists

#### Why This Could Fail

- RC015 (the original IV-RV divergence test on EURUSD options) was closed due to data infeasibility
- EURUSD options data is still problematic (CME listed-option liquidity was insufficient)
- Crypto options are accessible but HIGH_VOL has NOT been validated on crypto
- The APEX signal is trained on EURUSD — transfer to BTC/ETH is an unvalidated assumption
- IV typically exceeds RV (the "volatility risk premium") — buying straddles requires RV to exceed IV by enough to overcome premium + costs

#### External Market Facts

| Dimension | EURUSD Options | BTC/ETH Options (Deribit) |
|-----------|---------------|--------------------------|
| Exchange access | CME (institutional) | Deribit (retail accessible) |
| Historical data | Problematic (RC015) | Available since 2019 (Tardis, CryptoDataDownload) |
| Liquidity | Low for listed options | Moderate-High (85% BTC market share on Deribit) |
| Typical IV-RV spread | Unknown (untested) | IV typically > RV by 5-15 vol points |
| Contract structure | Standardized, European | Standardized, European, inverse & linear |
| Retail access | Difficult | Straightforward |

#### Hard Elimination Check

- Rule A (payoff alignment): ✅ Convex payoff rewards movement magnitude
- Rule B (historical reconstruction): ⚠️ EURUSD options data problematic; BTC options data available
- Rule C (liquidity/execution): ⚠️ EURUSD listed options insufficient; BTC options moderate
- Rule D (discretionary assumptions): ✅ Minimal — threshold score + IV comparison
- Rule E (reopened rejection): ⚠️ RC015 was closed, but this is a fresh instrument class (BTC options vs CME EURUSD)
- Rule F (outcome-driven tuning): ✅ Pre-definable threshold
- Rule G (no causal explanation): ✅ Clear mechanism (RV > IV = profit from convexity)

**Verdict: PROMISING BUT REQUIRES VALIDATION OF CROSS-ASSET TRANSFER**

---

### Candidate B — Direction-Neutral Movement-Range Payoff

**Concept**: Use instruments that profit from any large movement regardless of direction (range breakouts, one-touch barriers, digit options).

#### Mechanism Chain

```
VALIDATED INFORMATION: Predicted excursion scales with risk score
        ↓
ECONOMIC MECHANISM: Place symmetric barriers; price is predicted to breach both
        ↓
INSTRUMENT: Binary/barrier options, range accruals
        ↓
PAYOFF: Binary payout if price breaches barrier within time window
        ↓
TRADEABLE CONDITION: Risk score above threshold
        ↓
MEASURABLE OUTCOME: Binary payout minus premium
```

#### Why This Could Work

- APEX predicts excursion magnitude — barrier products reward exactly this
- No directional prediction needed
- Binary payoff avoids path-dependency issues

#### Why This Could Fail

- **M31 already failed**: 99.75% boundary saturation at 1.0xRV20 — the signal cannot discriminate breach vs non-breach at reasonable boundaries
- Barrier options have severe gamma risk and are typically overpriced relative to theoretical value
- Binary pricing by market makers already accounts for known volatility seasonality
- No single-instrument barrier product exists that exactly matches APEX's 12-hour horizon

#### Hard Elimination Check

- Rule A (payoff alignment): ✅ Movement magnitude rewards prediction
- Rule B (historical reconstruction): ⚠️ Barrier product payoffs are reconstructable from spot data but pricing depends on IV surface
- Rule C (liquidity/execution): ❌ Exotic barrier products typically have wide spreads and limited liquidity
- Rule D (discretionary assumptions): ⚠️ Barrier level selection requires assumptions
- Rule E (reopened rejection): ❌ M31 (boundary test) already failed at Level 3
- Rule F (outcome-driven tuning): ⚠️ Barrier level is a researcher degree of freedom
- Rule G (no causal explanation): ✅ Mechanism exists but implementation failed

**Verdict: REJECT — M31 already demonstrated boundary saturation; exotic barriers are illiquid**

---

### Candidate C — Relative-Value Volatility Structure

**Concept**: Exploit relationships between volatility quantities (e.g., term structure, skew, cross-asset vol ratios) rather than absolute levels.

#### Mechanism Chain

```
VALIDATED INFORMATION: APEX predicts forward RV for EURUSD
        ↓
ECONOMIC MECHANISM: If predicted RV diverges from vol surface expectations → sell/buy relative structure
        ↓
INSTRUMENT: Calendar spread, ratio spread, cross-asset vol spread
        ↓
PAYOFF: Profit from convergence/divergence of two related vol quantities
        ↓
TRADEABLE CONDITION: Predicted divergence exceeds transaction cost
        ↓
MEASURABLE OUTCOME: Spread P&L
```

#### Why This Could Work

- Relative-value strategies are inherently lower-risk than outright positions
- APEX predicts a specific future quantity (forward RV) which is one leg of the comparison

#### Why This Could Fail

- APEX only predicts EURUSD forward RV — there is no second leg of the comparison
- Cross-asset transmission was REJECTED (RC014) — no cross-asset vol prediction exists
- APEX has no term structure prediction capability
- The mechanism requires TWO predictive legs; APEX has only one
- A single-leg prediction is a directional bet on vol, not relative value

#### Hard Elimination Check

- Rule A (payoff alignment): ❌ Requires two predictive legs; APEX has one
- Rule B (historical reconstruction): ⚠️ Partial — one leg reconstructable
- Rule C (liquidity/execution): ⚠️ Depends on specific structure
- Rule D (discretionary assumptions): ⚠️ Second leg requires assumptions
- Rule E (reopened rejection): ❌ RC014 cross-asset transmission rejected
- Rule F (outcome-driven tuning): ⚠️ Spread structure requires tuning
- Rule G (no causal explanation): ❌ No second validated leg

**Verdict: REJECT — Insufficient predictive information for relative-value structure**

---

### Candidate D — Directional Instrument

**Concept**: Use spot/futures/CFD/perpetual on EURUSD to profit from predicted directional movement.

#### Mechanism Chain

```
VALIDATED INFORMATION: Predicted excursion during HIGH_VOL / LNO
        ↓
ECONOMIC MECHANISM: Directional position captures movement
        ↓
INSTRUMENT: EURUSD spot, CFD, futures, perpetual
        ↓
PAYOFF: Price change × position size - costs
        ↓
TRADEABLE CONDITION: Directional prediction above noise
        ↓
MEASURABLE OUTCOME: Directional P&L
```

#### Why This Could Fail (Critical)

- **M24 conclusively rejected directional translation** (p=0.6418)
- APEX's best signal is explicitly non-directional
- Every spot monetization attempt failed (RC012 Studies 007–011)
- Spot instruments require directional prediction to generate positive expectancy
- The movement is symmetric (ratio=0.9218) — no directional bias to capture

#### Hard Elimination Check

- Rule A (payoff alignment): ❌ Payoff requires direction; APEX has none
- Rule B (historical reconstruction): ✅ Fully available
- Rule C (liquidity/execution): ✅ EURUSD spot is highly liquid
- Rule D (discretionary assumptions): ⚠️ Direction assumption required
- Rule E (reopened rejection): ❌ RC012 Studies 007–011 rejected spot monetization
- Rule F (outcome-driven tuning): ⚠️ Direction prediction requires tuning
- Rule G (no causal explanation): ❌ No directional mechanism exists

**Verdict: REJECT — M24 conclusively eliminates directional translation; RC012 spot monetization already failed**

---

### Candidate E — Cross-Instrument Volatility Manifestation

**Concept**: Does the validated information naturally map to an instrument where the payoff is more directly observable? Specifically: does the HIGH_VOL prediction, if it generalizes beyond EURUSD, map to crypto options where IV-RV divergence is observable?

#### Mechanism Chain

```
VALIDATED INFORMATION: M17-R2 predicts EURUSD forward RV and excursion
        ↓
HYPOTHESIS: If similar volatility dynamics exist on BTC/ETH → crypto options instrument
        ↓
ECONOMIC MECHANISM: Predicted realized vol > options-implied vol → long straddle
        ↓
INSTRUMENT: BTC/ETH options on Deribit
        ↓
PAYOFF: Realized vol × vega × time - premium - costs
        ↓
TRADEABLE CONDITION: (1) HIGH_VOL transfers to crypto; (2) IV < predicted RV
        ↓
MEASURABLE OUTCOME: Straddle P&L after costs
```

#### Why This Is the Strongest Candidate

1. **Instrument access is real**: Deribit has ~85% BTC options market share, retail-accessible, historical data available since 2019 via Tardis/CryptoDataDownload
2. **Payoff alignment is exact**: Convex payoff rewards the exact quantity APEX predicts (movement magnitude), without requiring direction
3. **The mechanism is economically intelligible**: Market makers price options with a volatility risk premium (IV > RV on average). If APEX can predict when realized vol will exceed the implied vol, it captures the IV-RV spread
4. **Historical data is reconstructable**: BTC spot + options data both available on Tardis (since 2019) and CryptoDataDownload
5. **It is genuinely new**: This is NOT RC015 (CME EURUSD listed options). This is BTC options on Deribit — a different instrument, different exchange, different data architecture

#### Why This Could Still Fail

1. **HIGH_VOL has NOT been validated on BTC**: All APEX findings are EURUSD-specific. The M17-R2 model would need to be retrained and re-validated on BTC data. This is a significant unvalidated assumption.
2. **IV typically exceeds RV**: In normal markets, IV > RV by 5-15 vol points. The APEX signal would need to predict vol expansion that exceeds this premium — a high bar.
3. **Crypto vol dynamics may differ**: BTC volatility clustering, GARCH properties, and intraday patterns may differ structurally from EURUSD. The HIGH_VOL primitive may not exist on BTC, or its predictability characteristics may differ.
4. **Funding costs**: BTC options on Deribit are typically inverse (BTC-denominated), introducing funding/carry considerations.
5. **Transaction costs**: Options bid-ask spreads in crypto can be 1-3 vol points for ATM, potentially eroding edge.

#### External Market Facts — Deribit BTC Options

| Dimension | Detail |
|-----------|--------|
| Exchange | Deribit (Panama-based, retail-accessible) |
| BTC market share | ~85% of global BTC options |
| Options volume | ~$4.2B daily (as of 2026) |
| Contract types | European options, inverse & linear |
| Expiries | Daily, weekly, monthly, quarterly |
| Historical data | Available since March 2019 (Tardis, CryptoDataDownload, Deribit API) |
| Greeks | Delta, gamma, vega, theta, rho available via API |
| IV surface | Full surface available (multiple strikes, expiries) |
| Funding | Inverse contracts use BTC margin; linear use USD |
| Access | Retail account with KYC, no geographic restrictions for most jurisdictions |

#### Hard Elimination Check

- Rule A (payoff alignment): ✅ Convex payoff matches vol prediction
- Rule B (historical reconstruction): ✅ BTC options + spot data available since 2019
- Rule C (liquidity/execution): ✅ Deribit is liquid, retail-accessible
- Rule D (discretionary assumptions): ⚠️ Requires assumption that HIGH_VOL transfers
- Rule E (reopened rejection): ✅ Genuinely new — NOT RC015 (different asset class, different exchange)
- Rule F (outcome-driven tuning): ✅ Pre-definable: score threshold, IV-RV comparison
- Rule G (no causal explanation): ✅ Clear mechanism: predict RV > IV → profit from convexity

**Verdict: HIGH PRIORITY — strongest candidate, but requires cross-asset validation milestone**

---

## 3. Rejected Candidates Summary

| Candidate | Primary Rejection Reason | Reopened Branch? |
|-----------|------------------------|-----------------|
| B: Barrier/Range products | M31 boundary saturation (99.75%); exotic barriers illiquid | Yes — M31 variant |
| C: Relative-value vol | Requires two predictive legs; APEX has one | No (new concept, insufficient data) |
| D: Directional instrument | M24 conclusively eliminated directional translation | Yes — RC012 spot monetization |

---

## 4. Top-Candidate Hypothesis

### Primary Candidate: E — Crypto Options Volatility Monetization

```text
IF:
    HIGH_VOL onset dynamics transfer from EURUSD to BTC
    (i.e., BTC exhibits similar predictable volatility clustering,
    and the M17-R2 risk-score methodology produces comparable
    predictive discrimination on BTC price data)

THEN:
    Buy ATM straddles or strangles on BTC options via Deribit
    when the crypto-adapted risk score exceeds a predetermined
    threshold, with expiry matched to the predicted excursion
    horizon.

BECAUSE:
    The APEX signal predicts realized volatility expansion.
    If the predicted RV exceeds the implied volatility priced
    into the options, the straddle position captures the
    IV-RV spread as positive expected value after costs.

THEREFORE:
    The measurable economic outcome is the mean straddle P&L
    per trade after premium, bid-ask, funding, and exchange
    costs, tested over a defined OOS period on BTC options.
```

### Secondary Candidate: A — EURUSD Options (if data becomes available)

```text
IF:
    EURUSD options data quality improves or a liquid
    alternative source is identified

THEN:
    Same mechanism as E but on EURUSD options

BECAUSE:
    The signal IS validated on EURUSD; only the instrument
    is currently inaccessible

THEREFORE:
    Same measurable outcome — straddle P&L on EURUSD options
```

---

## 5. Economic Mechanism Audit — Primary Candidate (E)

### 1. What exactly does the trader know?

The trader knows (via M17-R2 style prediction) that a HIGH_VOL episode is beginning and that the subsequent 12-hour realized volatility will be higher than typical. The prediction discriminates between longer/more-intense and shorter/less-intense episodes with C-index = 0.6656.

### 2. Why could that information have economic value?

Options markets price implied volatility as a forecast of future realized volatility. If the market systematically underestimates the magnitude of vol expansion during HIGH_VOL onset, options will be underpriced relative to what they will be worth at expiry. The trader can buy cheap options and benefit from the expansion.

### 3. What market participant is paying/receiving for the risk being taken?

Options sellers (market makers, volatility funds) receive premium and assume the risk of being short gamma/vega. They are compensated by the volatility risk premium (IV > RV on average). The buyer pays premium and receives the right to benefit from vol expansion.

### 4. What payoff asymmetry converts the information into expected value?

Long straddle: maximum loss = premium paid. Upside = unbounded (proportional to realized movement). If the probability-weighted upside exceeds the premium, expected value is positive. The APEX signal increases the probability of large movement beyond what IV pricing implies.

### 5. What risks does the trader assume?

- **IV exceeds realized vol**: The most common case. The trader pays a premium that exceeds the eventual payout.
- **Timing mismatch**: The APEX signal may predict the overall 12-hour RV but the straddle may be purchased at a moment when IV has already spiked (absorbing the information).
- **Cross-asset failure**: HIGH_VOL may not transfer to BTC.
- **Funding/carry**: Inverse option contracts have BTC-denominated margin.
- **Path dependency**: A straddle needs movement at specific times relative to the option's remaining life.
- **Liquidity risk**: Wide spreads during volatile periods may erode edge.

### 6. What costs can destroy the edge?

- Bid-ask spread (1-3 vol points for ATM BTC options)
- Exchange fees (Deribit taker: 0.04% of notional)
- Funding/margin costs
- Slippage during high-volatility periods
- IV re-pricing between signal detection and execution

### 7. What observation would falsify the mechanism?

- **Cross-asset validation fails**: BTC does not exhibit the HIGH_VOL primitive or its onset is not predictable (C-index ≤ 0.55 on BTC OOS)
- **IV systematically exceeds predicted RV**: Even during HIGH_VOL onset, options remain overpriced relative to realized vol
- **Execution costs exceed edge**: After realistic costs, straddle P&L is negative on average
- **Timing problem**: By the time the signal is detected, IV has already repriced to incorporate the information

---

## 6. Economic Cost Audit — Primary Candidate

| Cost Component | Source | Expected Magnitude | Verifiable? |
|---------------|--------|-------------------|-------------|
| Bid-ask spread | Deribit order book | 1-3 vol points for ATM | Yes (historical data) |
| Exchange fees | Deribit fee schedule | 0.04% taker / 0.02% maker | Yes (published) |
| Slippage | Execution during vol | Variable, higher during vol events | Partially |
| Funding/margin | Inverse contract structure | BTC-denominated, variable | Yes |
| Roll cost | Expiry management | Zero if European, linear if rolled | Yes |
| IV premium | Market pricing | Typically 5-15 vol points > RV | Yes (historical IV vs RV) |

---

## 7. What This Establishes vs. What It Does NOT

### IC1 establishes:
- The strongest surviving economic mechanism for APEX information monetization
- The instrument class most likely to align with APEX's non-directional signal
- The specific economic hypothesis for IC2
- The data requirements for IC2

### IC1 does NOT establish:
- That HIGH_VOL transfers to BTC (unvalidated assumption)
- That the IV-RV spread is exploitable (untested)
- That the mechanism produces positive expected value (untested)
- That the strategy is profitable (untested)

---

*IC1 is a control/research-design milestone. No experiments were run. No data was acquired. No strategy was coded.*
