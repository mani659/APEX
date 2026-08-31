# RC015 Study 005 — Short-Dated EUR/USD Option Availability Test

## 1. Local Audit Results

A comprehensive audit of the previously downloaded EUR/USD Definition dataset (`glbx-mdp3-20260813-20260815.definition.csv.zst`) confirmed the presence of highly liquid, short-dated outright options (Calls and Puts) expiring before the spot-history cutoff.

### Identified Short-Dated Weekly Roots
The dataset contains multiple weekly roots that satisfy the `2026-08-12 < expiry <= 2026-08-14` constraint:
1. **WE2Q6** (Wednesday Week 2) - Expires `2026-08-12 14:00:00 UTC` (0-DTE intra-day)
2. **SU2Q6** (Thursday Week 2) - Expires `2026-08-13 14:00:00 UTC` (1-DTE)
3. **2EUQ6** (Friday Week 2) - Expires `2026-08-14 14:00:00 UTC` (2-DTE)

All three roots strictly map to the **6EU6 (Euro FX Futures Sep 2026)** underlying contract (Underlying ID: `10573`), not the December `6EZ6` contract.

## 2. Selection

To satisfy the requirement of "preferring the shortest available outright maturity" while avoiding the potential intra-day fragmentation of a 0-DTE option, the **SU2Q6 (1-DTE)** root is selected. 

The contemporaneous `6EZ6` futures midpoint on August 12, 2026 was approximately 1.1592, establishing **1.160** as the nearest ATM strike. 

For the **SU2Q6** expiry (`2026-08-13 14:00:00 UTC`), 39 distinct strikes are available. The two representative contracts are:

- **Nearest-ATM Call:** 
  - Symbol: `SU2Q6 C1160`
  - Instrument ID: `42478432`
  - Expiry: `2026-08-13 14:00:00 UTC`

- **Nearest-ATM Put:**
  - Symbol: `SU2Q6 P1160`
  - Instrument ID: `42634873`
  - Expiry: `2026-08-13 14:00:00 UTC`

*(Note: If 2-DTE is preferred for volatility normalization stability, the `2EUQ6` equivalents are ID `42156372` [Call] and `42474896` [Put]).*

## 3. Answers to Required Questions

1. **Do suitable outright options exist?** 
   Yes.
2. **Which weekly root contains them?** 
   The `SU2` (Thursday), `2EU` (Friday), and `WE2` (Wednesday) roots.
3. **Which expiry is shortest?** 
   Strictly `2026-08-12 14:00:00 UTC` (`WE2`), but `2026-08-13 14:00:00 UTC` (`SU2`) is the shortest clean 1-day maturity.
4. **Which underlying futures contract do they map to?** 
   `6EU6` (September 2026 Euro FX Futures, ID `10573`).
5. **What exact two contracts should be requested for the next BBO test?** 
   Instrument ID **`42478432`** (Call) and Instrument ID **`42634873`** (Put).

## Final Conclusion
> **Yes.** We can obtain outright 1-DTE EUR/USD options (`SU2Q6`) expiring squarely on August 13, 2026. This expiration is firmly bounded by our available spot data (which extends to August 14th), permitting an exact, truly maturity-matched implied-vs-realized variance calculation without any lookahead or extrapolation.
