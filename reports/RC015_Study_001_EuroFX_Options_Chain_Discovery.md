# RC015 Study 001 - Euro FX Options Chain Discovery

## 1. Is 6E.OPT Sufficient?
Databento's official documentation states that appending `.OPT` to a futures root (e.g., `6E.OPT`) acts as an aggregate parent symbol that automatically includes all option series whose underlying is that futures product. However, because CME explicitly splits Euro FX options across many disparate product codes based on expiration day, we cannot *blindly* assume `6E.OPT` will resolve every single weekly and monthly root without verification. The safest approach is to use `6E.OPT` while being explicitly aware of the alternate CME roots to verify they are present in the resulting download.

## 2. Alternate CME Option Roots
Yes, CME maintains a wide array of alternate raw option roots for Euro FX options that do not use the "6E" string at all. The underlying futures contract uses the root `6E`, but the options contracts use specific codes depending on their frequency and expiration type.

## 3. Standard Options Roots
- **Standard Monthly Options**: The primary product code on Globex is **`EUU`** (though historically and on some platforms it may be represented as `O6E`). 

## 4. Weekly/EOM Options Roots
CME lists weekly Euro FX options expiring on different days of the week, utilizing the following root prefixes:
- **Weekly Mondays**: `MO1`, `MO2`, `MO3`, `MO4`, `MO5`
- **Weekly Tuesdays**: `TU1`, `TU2`, `TU3`, `TU4`, `TU5`
- **Weekly Wednesdays**: `WE1`, `WE2`, `WE3`, `WE4`, `WE5`
- **Weekly Thursdays**: `SU1`, `SU2`, `SU3`, `SU4`, `SU5`
- **Weekly Fridays**: `1EU`, `2EU`, `3EU`, `4EU`, `5EU`

## 5. Available Expiries
The Euro FX options chain features an exceptionally dense expiration calendar:
- **Monthly Expiries**: Serial months and quarterly cycle months.
- **Weekly Expiries**: Monday, Tuesday, Wednesday, Thursday, and Friday expirations for up to 4-5 consecutive weeks.

## 6. Available Strikes
The exact strike prices will be populated in the `strike_price` field of the Definition file. For Euro FX, these typically occur in highly granular increments (e.g., 0.0050 intervals) spanning a wide range above and below the at-the-money (ATM) forward price. 

## 7. Mapping Options to 6E Futures
In the Databento MDP3 Definition schema, individual option contracts map to their underlying `6E` futures via the following fields:
- **`underlying_id`**: The integer ID of the specific `6E` futures contract the option expires into.
- **`underlying`**: The string representation of the underlying product (usually `6E`).
- **`group`**: The overarching product group (usually `6E`).
Once the options Definition file is obtained, we will join the `underlying_id` of the options to the `instrument_id` of the futures contracts from our previous audit to prove the exact structural linkage.

## 8. Manual Portal Feasibility
**Can the manual portal retrieve the required universe?**
**Yes.** The Databento Data Portal supports parent symbology and explicit symbol lists. You can query the required universe manually by using the parent `6E.OPT`. To ensure absolute completeness and prevent missing any weekly expirations, you can input a comma-separated list of the roots into the portal's symbol selector.

## 9. API Specification (If Portal Fails)
If the portal were insufficient, the explicit API request for definition data would use:
`symbols="6E.OPT,EUU,MO1,MO2,MO3,MO4,MO5,TU1,TU2,TU3,TU4,TU5,WE1,WE2,WE3,WE4,WE5,SU1,SU2,SU3,SU4,SU5,1EU,2EU,3EU,4EU,5EU"`
with `stype_in="parent"`.

## 10. Next Manual Download Required
To rigorously prove the options linkage without over-downloading, we need **one** Definition file that captures all of the above roots for a single day.

---

## Options Definition Download Specification
Please perform the following download manually via the Databento portal. 

- **Dataset**: `GLBX.MDP3`
- **Schema**: `Definition`
- **Symbols**: `6E.OPT, EUU, MO1, MO2, MO3, MO4, MO5, TU1, TU2, TU3, TU4, TU5, WE1, WE2, WE3, WE4, WE5, SU1, SU2, SU3, SU4, SU5, 1EU, 2EU, 3EU, 4EU, 5EU`
*(Note: Start by typing `6E.OPT` and `EUU`. If the portal validates them as parent options, include the weekly ones as well to guarantee exhaustion).*
- **Date**: `2026-08-15` (A single recent trading day)
- **Format**: `CSV`
- **Timestamp**: `ISO 8601`
- **Price format**: `Decimal`
- **Split**: `None`

*We will use this single-day Definition dataset to verify the strikes, expiries, and underlying mappings before requesting any BBO-1s quote data.*
