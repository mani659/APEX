Milestone: M35
Status: COMPLETE

APEX state after HIGH_VOL closure:
- HIGH_VOL branch: CLOSED (M34)
- Surviving validated knowledge: HIGH_VOL primitive, session-transition primitives, cross-asset rejection
- Closed branches: HIGH_VOL (M34), RC015 listed-option path
- Data-constrained hypotheses: Carry/funding (untested), institutional liquidity (untested)

Validated knowledge:
- HIGH_VOL distributional primitive (RC012)
- HIGH_VOL non-memoryless lifecycle (M13/M14)
- HIGH_VOL onset predictability (M17-R2, C-index=0.6656)
- HIGH_VOL scales forward RV (M21, p=0.0032)
- HIGH_VOL scales excursion envelope (M27, p=7.5×10⁻⁵)
- Session-transition primitives (RC013)
- Cross-asset transmission rejected (RC014)

Rejected/closed branches:
- V1 directional alpha (RC007)
- Context rescue (RC008)
- Behavioral discovery (RC009-010)
- Microstructure (RC011 — paused)
- Spot monetization (RC012 S007-011)
- Cross-asset transmission (RC014)
- HIGH_VOL boundary translation (M31)
- Dynamic translation (M33)
- HIGH_VOL branch (M34)
- RC015 listed-option path

Unresolved questions:
- Carry/funding premium (data-constrained)
- Institutional liquidity (data-constrained)
- Session-transition distributional asymmetry (untested)
- LOW_VOL compression (untested)

Candidate branches:
- C1: Session-Transition Distributional Asymmetry (score=45, HIGH PRIORITY)
- C2: LOW_VOL Compression Breakout (score=44, HIGH PRIORITY)
- C3: Cross-Asset Relative Value Ranking (score=39, PROMISING)
- C4: Intraday Volatility Seasonality (score=42, PROMISING)
- C5: Options-Based VRP (score=35, LOW PRIORITY — data-constrained)
- C6: Multi-Asset Volatility Regime Generalization (score=39, PROMISING)
- C7: Path-Dependent Harvesting Simulation (score=33, REJECT)

Primary recommendation: C1 — Session-Transition Distributional Asymmetry
Backup recommendation: C2 — LOW_VOL Compression Breakout

Why primary is superior:
- Highest information value (resolves whether session mechanics create distributional asymmetry)
- Zero data cost (uses existing EURUSD M1 data)
- Strong scientific continuity (builds on RC013 validated primitives)
- High ex-ante defensibility (session windows are deterministic)
- Clear falsification path
- Independent of closed branches

Existing resources:
- EURUSD M1/M15 OHLCV (5.5 years)
- RC013 session definitions
- Existing Python infrastructure

Future data requirements: None (uses existing canonical datasets)

Major risks:
- Multiple testing (session × distribution combinations)
- Overfitting to calendar patterns
- Mitigation: Pre-declare exact session windows and tests before execution

Exact next milestone:
M36 — Candidate Research Methodology Design

Authorization:
PLANNED — NOT STARTED

External API calls: 0
New data acquired: 0
Spend: $0.00

Repository files changed:
- reports/APEX_M35_Next_Research_Direction_Discovery.md (NEW)
- reports/APEX_M35_Next_Research_Direction_Scoring.csv (NEW)
- reports/APEX_M35_Next_Research_Direction_Recommendation.md (NEW)
- reports/APEX_M35_RESULT.md (NEW)
- docs/APEX_SESSION_HANDOFF.md (MODIFIED)
- docs/APEX_SESSION_STATE.json (MODIFIED)
