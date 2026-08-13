# RC013 Freeze — Session / Calendar Structural Mechanics

## 1. Campaign Objective
The RC013 campaign was initiated to determine whether deterministic session and time-of-day structure creates a persistent, measurable change in the distribution of future EURUSD price behavior, without requiring short-term directional prediction.

## 2. Studies Summary
- **RC013 Study 001:** Session / Calendar Structural Mechanics Discovery. Found that deterministic session transitions materially alter the movement distribution.
- **RC013 Study 002:** Independent Validation. Applied chronological partitioning (Discovery 2021-2023, Validation 2024-2026) to independently validate `LONDON_NY_OVERLAP` and `ASIA_TO_LONDON`. Both survived out-of-sample as structurally valid, directionally neutral volatility/expansion edges.
- **RC013 Study 003:** Session Transition Path Geometry. Diagnosed the M1 path geometry, classifying both candidates as TYPE A (Directionally Efficient Expansion), characterized by significant path length increase without a collapse in path efficiency or explosive whipsaw.
- **RC013 Study 004:** Session Transition Breakout Monetization. Tested a raw, zero-buffer, fixed-horizon breakout architecture using the immediate pre-transition range without stop-losses. The result was negative expectancy due to unmitigated tail-loss reversals and transaction cost friction.

## 3. Validated Structural Knowledge
- Deterministic session transitions materially alter EURUSD future movement distributions.
- `LONDON_NY_OVERLAP` is a validated structural primitive.
- `ASIA_TO_LONDON` is a validated structural primitive.
- The session effects survived independent chronological validation.
- The effects are approximately direction-neutral.
- Session expansion exhibits higher movement with directionally efficient path geometry relative to the HIGH_VOL chop regime.

## 4. Rejected Monetization Architecture
The specific raw immediate range-breakout monetization architecture tested in RC013 Study 004 is rejected.
- The breakout architecture is affected by negative expectancy and significant tail-loss exposure.
- Transaction-cost reduction alone does not rescue the tested architecture.
- The validated session primitive must therefore be treated as **information**, not as a validated trading strategy.

## 5. Exact Final Metrics (Study 004 Monetization)
### ASIA_TO_LONDON (4H Horizon)
- **Expectancy:** -0.99 pips
- **Win Rate:** 43.6%
- **Profit Factor:** 0.87
- **Worst 5% Tail Loss:** -29.6 pips (24.3% of total losses)

### LONDON_NY_OVERLAP (1H Horizon)
- **Expectancy:** -1.54 pips
- **Win Rate:** 42.6%
- **Profit Factor:** 0.72
- **Worst 5% Tail Loss:** -20.8 pips (28.8% of total losses)

## 6. Methodological Boundaries
- **Timezone Handling:** IANA `Europe/London` and `America/New_York` converted to UTC (DST-aware).
- **Chronological Split:** 2021–2023 (Discovery), 2024–2026 (Validation).
- **Path Reconstruction:** Strictly non-inferred, chronological M1 close-price walking.
- **Directional Neutrality:** Rigorously enforced, meaning the path expansion is purely geometric, not an exploitable directional trend drift.

## 7. Future Research Boundary (Prohibited Drift)
The following are prohibited within the closed RC013 branch unless a future project-level review explicitly reopens session monetization:
- Optimizing breakout buffer
- Optimizing stop distance
- Optimizing take-profit
- Optimizing holding duration
- Adding ATR filters, HIGH_VOL filters, trend filters, or ML
- Testing dozens of range/session windows
- Grid/recovery logic or martingale

## 8. Final Decision
**RC013 STATUS: CLOSED — STRUCTURAL PRIMITIVE VALIDATED, MONETIZATION ARCHITECTURE REJECTED**

RC013 established that deterministic session transitions create a robust, direction-neutral structural change in the future EURUSD movement distribution. Independent validation confirmed the effect. Path analysis showed directionally efficient expansion relative to the previously studied HIGH_VOL chop regime. However, the tested raw session-range breakout architecture produced negative expectancy and significant tail losses. Therefore the session effect is preserved as validated structural information, while the tested breakout monetization architecture is rejected. The campaign is closed to prevent parameter optimization and research drift.
