# RC015 Study 008 — Ex-Ante Observation-Design Discovery

## 1. Candidate Observation Designs

Four structurally justified candidate observation designs were constructed to replace the failed 24-hour continuous M15 grid. These designs were selected entirely *ex ante*, based purely on exchange mechanics and existing RC013 definitions, without observing the variance gap outcomes.

### Design A — Fixed Daily Anchor
- **Schedule**: A single fixed observation at `14:00 UTC`.
- **Structural Justification**: Represents the peak of the London/NY overlap session, historically the most liquid period for EUR/USD spot and futures.

### Design B — Fixed Two-Anchor Session
- **Schedule**: Two fixed observations at `08:00 UTC` and `14:00 UTC`.
- **Structural Justification**: Corresponds to the London open (end of Asian session) and the NY/London overlap, capturing the two most significant daily institutional liquidity entry points.

### Design C — Fixed Liquid-Session Window
- **Schedule**: A contiguous M15 block from `12:00 UTC` to `16:00 UTC` (17 slots).
- **Structural Justification**: Directly maps to the `LONDON_NY_OVERLAP` session previously frozen and validated in RC013, avoiding the illiquid Asian and late NY sessions entirely.

### Design D — Session-Transition Anchors
- **Schedule**: Four fixed observations at `06:00`, `08:00`, `12:00`, and `16:00 UTC`.
- **Structural Justification**: Aligned precisely with the already frozen RC013 session transition boundaries, ensuring observation points capture structural regime shifts.

## 2. Pre-Economic Liquidity Diagnostic Results

Using strictly the already acquired Stage-2 BBO-1m data, the candidate designs were evaluated for option quote freshness (without looking at futures prices or IV/RV):

| Design | Events Covered | <=5m Coverage | <=15m Coverage | <=30m Coverage | <=60m Coverage | Median Option Age |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A (Fixed Anchor)** | 219 (98.6%) | 4.1% | 10.3% | 20.0% | 28.3% | ~2.9 hours |
| **B (Two-Anchor)** | 219 (98.6%) | 2.9% | 7.0% | 13.5% | 19.5% | ~11.0 hours |
| **C (Liquid Window)**| 221 (99.5%) | 4.4% | 10.0% | 16.6% | 26.4% | ~2.7 hours |
| **D (Transitions)** | 221 (99.5%) | 2.0% | 5.0% | 8.6% | 14.8% | ~11.1 hours |

*Note: Percentage coverage refers to the ratio of synchronized observation slots achieving the age threshold versus the total slots dictated by the schedule. The events covered metric simply indicates that at least one technically observable option existed on that date, regardless of its severe staleness.*

## 3. Analysis

Even when restricting observations to the absolute most liquid institutional windows (Design C) or a single peak-liquidity anchor (Design A), listed EUR/USD option quotes remain unacceptably sparse. A 15-minute tolerance yields roughly 10% coverage, meaning 90% of predetermined observation slots would require matching a completely fresh futures price against an option quote that has not been updated in over 15 minutes. 

Because the minimum threshold for a scientifically defensible variance-gap study requires contemporaneous IV and RV measurements, none of the structurally justified schedules can be populated using the current Globex listed options dataset.
