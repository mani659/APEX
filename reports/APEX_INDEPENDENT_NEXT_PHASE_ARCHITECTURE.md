# APEX — Independent Next-Phase Architecture

**Date**: 2026-08-25
**Author**: Independent Research Architect
**Status**: RECOMMENDATION ONLY — REQUIRES USER AUTHORIZATION

---

## 1. Selected Architecture

### **Architecture C — Economic Mechanism Discovery**

Shift the research question from:
> "What else does our signal predict?"

To:
> "What economic market behavior could rationally monetize predictable volatility expansion?"

---

## 2. Why Architecture C

| Architecture | Assessment | Selected? |
|---|---|---|
| A — Continue HIGH_VOL | Correctly closed. No new economic question identified. Would re-enter signal re-expression loop. | ❌ |
| B — Close HIGH_VOL and search for another primitive | Risk of repeating the HIGH_VOL pattern: discover phenomenon → characterize → fail to monetize. Does not address the fundamental bottleneck (economic mechanism). | ❌ |
| **C — Economic Mechanism Discovery** | **Directly addresses the dominant missing piece. Forces every experiment to target a specific trade hypothesis. Inverts the research sequence.** | **✅** |
| D — Freeze APEX temporarily | Defensible if no viable instrument can be identified. Should be the fallback if Architecture C's instrument survey produces no viable candidates. | FALLBACK |

---

## 3. Phase Structure

### Phase C1: Instrument Feasibility Survey (1 milestone)

**Objective**: Identify which available instruments could monetize a non-directional volatility prediction under realistic constraints.

**Deliverable**: A ranked list of candidate instruments with:
- Payoff structure (convex/linear/binary)
- Transaction costs (spread, commission, funding)
- Liquidity assessment
- Access constraints (broker, exchange, account type)
- Data availability for backtesting
- Alignment with APEX's non-directional volatility signal

**Candidate instrument classes**:
1. Crypto perpetual options (Deribit, OKX — straddles on BTC/ETH)
2. Crypto volatility indices (DVOL)
3. DeFi structured products (Lyra, Hegic — on-chain options)
4. VIX futures / options (requires different account type)
5. Listed FX options (CME — partially explored in RC015)
6. CFD volatility indices (VIX CFDs via existing broker)
7. Spot FX grid with bounded risk budget (revisit with explicit cost model)

**Gate**: If no candidate instrument satisfies all constraints (accessible, liquid, convex payoff, testable with available data), trigger **Architecture D — Freeze APEX**.

### Phase C2: Economic Hypothesis Design (1 milestone)

**Objective**: For the top-ranked instrument from C1, design a single falsifiable economic hypothesis.

**Format**: "If APEX predicts [specific condition], then [specific trade] on [specific instrument] produces [specific measurable outcome] after [specific costs]."

**Example**: "If APEX HIGH_VOL onset with low risk score (predicted long persistence) is detected on EURUSD, and a 24-hour at-the-money straddle on Deribit BTCUSD costs X in premium, then the realized movement over the next 12 hours exceeds X + costs with probability > 0.5."

**Gate**: The hypothesis must be falsifiable, testable with available or cheaply acquirable data, and specify entry/exit/cost structure before execution.

### Phase C3: Economic Test Execution (1 milestone)

**Objective**: Execute the frozen economic hypothesis from C2.

**Deliverable**: A result file containing:
- Net expected value after all costs
- Win rate
- Average PnL per trade
- Maximum drawdown
- Sharpe ratio equivalent
- Sample size
- Statistical significance of the result

**Decision rule**: 
- If net expected value > 0 with p < 0.05 → proceed to robustness testing
- If net expected value ≤ 0 → the economic mechanism is rejected; return to C2 with next candidate or trigger Architecture D

---

## 4. Governance Rules for Next Phase

### Rule 1: Economic Mechanism Gate
No statistical decomposition experiment is authorized unless preceded by a written hypothesis of the form: "If result X is obtained, the specific trade Y becomes viable because Z."

### Rule 2: Instrument Feasibility Gate
Before methodology design, a written instrument-feasibility analysis must answer: What instrument? What are the costs? Is the market liquid? Can the trade be executed?

### Rule 3: Three-Milestone Limit
No research direction may consume more than 3 milestones before producing either a falsified economic hypothesis or a concrete strategy blueprint.

### Rule 4: Independent Replication Before Depth
No phenomenon may be investigated beyond Level 2 on a single instrument. Independent replication on a second instrument is required before economic translation.

### Rule 5: Anti-Lateral-Drift Rule
Each new milestone must advance vertically (toward tradability), not laterally (new representations of the same phenomenon).

---

## 5. What To Stop Immediately

1. **M40 (Session-Transition Characterization)** — should not proceed unless a specific economic hypothesis depends on the characterization output. "Characterize mean, variance, skewness, tails" is a lateral (descriptive) milestone, not a vertical (economic) milestone.

2. **Any further statistical decomposition of HIGH_VOL** — the branch is correctly closed.

3. **Any new distributional test on EURUSD M15** without an upstream strategy hypothesis.

---

## 6. What To Preserve

1. All validated findings (RC012, M13, M17-R2, M21, M24, M27, M39-R2).
2. The entire methodological infrastructure (frozen methodology, control reviews, OOS walk-forward).
3. The APEX stopping principle.
4. The HIGH_VOL episode ledger and M17-R2 prediction artifacts.
5. The RC015 option infrastructure (may become relevant if a new option instrument is identified).

---

## 7. Fallback: Architecture D — Freeze APEX

If the C1 instrument survey identifies no viable monetization instrument:

1. Formally acknowledge that APEX's current findings are scientifically valid but cannot be monetized with currently available instruments.
2. Preserve all research artifacts and methodology.
3. Document the precise instrument/data requirements that would re-activate research.
4. Set a calendar review (6 months) to reassess instrument availability.
5. **Stop all research activity.** Do not consume further milestones exploring the same phenomena.

This is a legitimate and scientifically honest outcome.

---

## 8. Exact Next Authorized Milestone

**IC1 — Instrument Feasibility Survey**

Status: PLANNED — REQUIRES USER AUTHORIZATION

IC1 must:
- Survey all candidate instrument classes listed in Section 3
- Score each on: payoff alignment, cost structure, liquidity, data availability, access constraints
- Produce a ranked recommendation
- Include a STOP gate (if no viable instrument exists)

IC1 must NOT:
- Run any experiment
- Acquire any data
- Design any strategy
- Modify any existing research artifact
- Test any hypothesis

---

*This architecture recommendation is a read-only document. No experiments have been run. No code has been modified.*
