# RC015 Study 007 — Final Acquisition Scope

## A. Frozen Sample Definition
- **Period**: 2022-01-01 through 2026-06-30
- **Total Calendar Fridays**: 234
- **Holiday/Unavailable Exclusions**: 11
- **Final Candidate Observation Events**: 222
- **Primary Maturity Framework**: Wednesday Observation (~2 DTE) → Friday Expiry
- **Primary Quote Schema**: BBO-1m
- **Primary Moneyness Rule**: `abs(strike - futures_mid) <= 0.0020`

## B. Exact Option-Root Mapping
*Note: Roots are assigned based on the CME rule where standard monthly options (EUU) expire on the Friday immediately preceding the second Wednesday of the contract month. All other Fridays use the ordinal weekly roots (1EU-5EU).*

| Expiry Date | Observation Date | Expected Option Root | Confidence / Status |
| :--- | :--- | :--- | :--- |
| 2022-01-07 | 2022-01-05 | EUU | QUALIFIED |
| 2022-01-14 | 2022-01-12 | 2EU | QUALIFIED |
| 2022-01-21 | 2022-01-19 | 3EU | QUALIFIED |
| 2022-01-28 | 2022-01-26 | 4EU | QUALIFIED |
| 2022-02-04 | 2022-02-02 | EUU | QUALIFIED |
| 2022-02-11 | 2022-02-09 | 2EU | QUALIFIED |
| 2022-02-18 | 2022-02-16 | 3EU | QUALIFIED |
| 2022-02-25 | 2022-02-23 | 4EU | QUALIFIED |
| 2022-03-04 | 2022-03-02 | EUU | QUALIFIED |
| 2022-03-11 | 2022-03-09 | 2EU | QUALIFIED |
| 2022-03-18 | 2022-03-16 | 3EU | QUALIFIED |
| 2022-03-25 | 2022-03-23 | 4EU | QUALIFIED |
| 2022-04-01 | 2022-03-30 | 1EU | QUALIFIED |
| 2022-04-08 | 2022-04-06 | EUU | QUALIFIED |
| 2022-04-15 | 2022-04-13 | 3EU | UNAVAILABLE (HOLIDAY) |
| 2022-04-22 | 2022-04-20 | 4EU | QUALIFIED |
| 2022-04-29 | 2022-04-27 | 5EU | QUALIFIED |
| 2022-05-06 | 2022-05-04 | EUU | QUALIFIED |
| 2022-05-13 | 2022-05-11 | 2EU | QUALIFIED |
| 2022-05-20 | 2022-05-18 | 3EU | QUALIFIED |
| 2022-05-27 | 2022-05-25 | 4EU | QUALIFIED |
| 2022-06-03 | 2022-06-01 | EUU | QUALIFIED |
| 2022-06-10 | 2022-06-08 | 2EU | QUALIFIED |
| 2022-06-17 | 2022-06-15 | 3EU | QUALIFIED |
| 2022-06-24 | 2022-06-22 | 4EU | QUALIFIED |
| 2022-07-01 | 2022-06-29 | 1EU | QUALIFIED |
| 2022-07-08 | 2022-07-06 | EUU | QUALIFIED |
| 2022-07-15 | 2022-07-13 | 3EU | QUALIFIED |
| 2022-07-22 | 2022-07-20 | 4EU | QUALIFIED |
| 2022-07-29 | 2022-07-27 | 5EU | QUALIFIED |
| 2022-08-05 | 2022-08-03 | EUU | QUALIFIED |
| 2022-08-12 | 2022-08-10 | 2EU | QUALIFIED |
| 2022-08-19 | 2022-08-17 | 3EU | QUALIFIED |
| 2022-08-26 | 2022-08-24 | 4EU | QUALIFIED |
| 2022-09-02 | 2022-08-31 | 1EU | QUALIFIED |
| 2022-09-09 | 2022-09-07 | EUU | QUALIFIED |
| 2022-09-16 | 2022-09-14 | 3EU | QUALIFIED |
| 2022-09-23 | 2022-09-21 | 4EU | QUALIFIED |
| 2022-09-30 | 2022-09-28 | 5EU | QUALIFIED |
| 2022-10-07 | 2022-10-05 | EUU | QUALIFIED |
| 2022-10-14 | 2022-10-12 | 2EU | QUALIFIED |
| 2022-10-21 | 2022-10-19 | 3EU | QUALIFIED |
| 2022-10-28 | 2022-10-26 | 4EU | QUALIFIED |
| 2022-11-04 | 2022-11-02 | EUU | QUALIFIED |
| 2022-11-11 | 2022-11-09 | 2EU | UNAVAILABLE (HOLIDAY) |
| 2022-11-18 | 2022-11-16 | 3EU | QUALIFIED |
| 2022-11-25 | 2022-11-23 | 4EU | QUALIFIED |
| 2022-12-02 | 2022-11-30 | 1EU | QUALIFIED |
| 2022-12-09 | 2022-12-07 | EUU | QUALIFIED |
| 2022-12-16 | 2022-12-14 | 3EU | QUALIFIED |
| 2022-12-23 | 2022-12-21 | 4EU | QUALIFIED |
| 2022-12-30 | 2022-12-28 | 5EU | QUALIFIED |
| 2023-01-06 | 2023-01-04 | EUU | QUALIFIED |
| 2023-01-13 | 2023-01-11 | 2EU | QUALIFIED |
| 2023-01-20 | 2023-01-18 | 3EU | QUALIFIED |
| 2023-01-27 | 2023-01-25 | 4EU | QUALIFIED |
| 2023-02-03 | 2023-02-01 | EUU | QUALIFIED |
| 2023-02-10 | 2023-02-08 | 2EU | QUALIFIED |
| 2023-02-17 | 2023-02-15 | 3EU | QUALIFIED |
| 2023-02-24 | 2023-02-22 | 4EU | QUALIFIED |
| 2023-03-03 | 2023-03-01 | EUU | QUALIFIED |
| 2023-03-10 | 2023-03-08 | 2EU | QUALIFIED |
| 2023-03-17 | 2023-03-15 | 3EU | QUALIFIED |
| 2023-03-24 | 2023-03-22 | 4EU | QUALIFIED |
| 2023-03-31 | 2023-03-29 | 5EU | QUALIFIED |
| 2023-04-07 | 2023-04-05 | EUU | UNAVAILABLE (HOLIDAY) |
| 2023-04-14 | 2023-04-12 | 2EU | QUALIFIED |
| 2023-04-21 | 2023-04-19 | 3EU | QUALIFIED |
| 2023-04-28 | 2023-04-26 | 4EU | QUALIFIED |
| 2023-05-05 | 2023-05-03 | EUU | QUALIFIED |
| 2023-05-12 | 2023-05-10 | 2EU | QUALIFIED |
| 2023-05-19 | 2023-05-17 | 3EU | QUALIFIED |
| 2023-05-26 | 2023-05-24 | 4EU | QUALIFIED |
| 2023-06-02 | 2023-05-31 | 1EU | QUALIFIED |
| 2023-06-09 | 2023-06-07 | EUU | QUALIFIED |
| 2023-06-16 | 2023-06-14 | 3EU | QUALIFIED |
| 2023-06-23 | 2023-06-21 | 4EU | QUALIFIED |
| 2023-06-30 | 2023-06-28 | 5EU | QUALIFIED |
| 2023-07-07 | 2023-07-05 | EUU | QUALIFIED |
| 2023-07-14 | 2023-07-12 | 2EU | QUALIFIED |
| 2023-07-21 | 2023-07-19 | 3EU | QUALIFIED |
| 2023-07-28 | 2023-07-26 | 4EU | QUALIFIED |
| 2023-08-04 | 2023-08-02 | EUU | QUALIFIED |
| 2023-08-11 | 2023-08-09 | 2EU | QUALIFIED |
| 2023-08-18 | 2023-08-16 | 3EU | QUALIFIED |
| 2023-08-25 | 2023-08-23 | 4EU | QUALIFIED |
| 2023-09-01 | 2023-08-30 | 1EU | QUALIFIED |
| 2023-09-08 | 2023-09-06 | EUU | QUALIFIED |
| 2023-09-15 | 2023-09-13 | 3EU | QUALIFIED |
| 2023-09-22 | 2023-09-20 | 4EU | QUALIFIED |
| 2023-09-29 | 2023-09-27 | 5EU | QUALIFIED |
| 2023-10-06 | 2023-10-04 | EUU | QUALIFIED |
| 2023-10-13 | 2023-10-11 | 2EU | QUALIFIED |
| 2023-10-20 | 2023-10-18 | 3EU | QUALIFIED |
| 2023-10-27 | 2023-10-25 | 4EU | QUALIFIED |
| 2023-11-03 | 2023-11-01 | EUU | QUALIFIED |
| 2023-11-10 | 2023-11-08 | 2EU | UNAVAILABLE (HOLIDAY) |
| 2023-11-17 | 2023-11-15 | 3EU | QUALIFIED |
| 2023-11-24 | 2023-11-22 | 4EU | QUALIFIED |
| 2023-12-01 | 2023-11-29 | 1EU | QUALIFIED |
| 2023-12-08 | 2023-12-06 | EUU | QUALIFIED |
| 2023-12-15 | 2023-12-13 | 3EU | QUALIFIED |
| 2023-12-22 | 2023-12-20 | 4EU | QUALIFIED |
| 2023-12-29 | 2023-12-27 | 5EU | QUALIFIED |
| 2024-01-05 | 2024-01-03 | EUU | QUALIFIED |
| 2024-01-12 | 2024-01-10 | 2EU | QUALIFIED |
| 2024-01-19 | 2024-01-17 | 3EU | QUALIFIED |
| 2024-01-26 | 2024-01-24 | 4EU | QUALIFIED |
| 2024-02-02 | 2024-01-31 | 1EU | QUALIFIED |
| 2024-02-09 | 2024-02-07 | EUU | QUALIFIED |
| 2024-02-16 | 2024-02-14 | 3EU | QUALIFIED |
| 2024-02-23 | 2024-02-21 | 4EU | QUALIFIED |
| 2024-03-01 | 2024-02-28 | 1EU | QUALIFIED |
| 2024-03-08 | 2024-03-06 | EUU | QUALIFIED |
| 2024-03-15 | 2024-03-13 | 3EU | QUALIFIED |
| 2024-03-22 | 2024-03-20 | 4EU | QUALIFIED |
| 2024-03-29 | 2024-03-27 | 5EU | UNAVAILABLE (HOLIDAY) |
| 2024-04-05 | 2024-04-03 | EUU | QUALIFIED |
| 2024-04-12 | 2024-04-10 | 2EU | QUALIFIED |
| 2024-04-19 | 2024-04-17 | 3EU | QUALIFIED |
| 2024-04-26 | 2024-04-24 | 4EU | QUALIFIED |
| 2024-05-03 | 2024-05-01 | EUU | QUALIFIED |
| 2024-05-10 | 2024-05-08 | 2EU | QUALIFIED |
| 2024-05-17 | 2024-05-15 | 3EU | QUALIFIED |
| 2024-05-24 | 2024-05-22 | 4EU | QUALIFIED |
| 2024-05-31 | 2024-05-29 | 5EU | QUALIFIED |
| 2024-06-07 | 2024-06-05 | EUU | QUALIFIED |
| 2024-06-14 | 2024-06-12 | 2EU | QUALIFIED |
| 2024-06-21 | 2024-06-19 | 3EU | UNAVAILABLE (HOLIDAY) |
| 2024-06-28 | 2024-06-26 | 4EU | QUALIFIED |
| 2024-07-05 | 2024-07-03 | EUU | QUALIFIED |
| 2024-07-12 | 2024-07-10 | 2EU | QUALIFIED |
| 2024-07-19 | 2024-07-17 | 3EU | QUALIFIED |
| 2024-07-26 | 2024-07-24 | 4EU | QUALIFIED |
| 2024-08-02 | 2024-07-31 | 1EU | QUALIFIED |
| 2024-08-09 | 2024-08-07 | EUU | QUALIFIED |
| 2024-08-16 | 2024-08-14 | 3EU | QUALIFIED |
| 2024-08-23 | 2024-08-21 | 4EU | QUALIFIED |
| 2024-08-30 | 2024-08-28 | 5EU | QUALIFIED |
| 2024-09-06 | 2024-09-04 | EUU | QUALIFIED |
| 2024-09-13 | 2024-09-11 | 2EU | QUALIFIED |
| 2024-09-20 | 2024-09-18 | 3EU | QUALIFIED |
| 2024-09-27 | 2024-09-25 | 4EU | QUALIFIED |
| 2024-10-04 | 2024-10-02 | EUU | QUALIFIED |
| 2024-10-11 | 2024-10-09 | 2EU | QUALIFIED |
| 2024-10-18 | 2024-10-16 | 3EU | QUALIFIED |
| 2024-10-25 | 2024-10-23 | 4EU | QUALIFIED |
| 2024-11-01 | 2024-10-30 | 1EU | QUALIFIED |
| 2024-11-08 | 2024-11-06 | EUU | QUALIFIED |
| 2024-11-15 | 2024-11-13 | 3EU | QUALIFIED |
| 2024-11-22 | 2024-11-20 | 4EU | QUALIFIED |
| 2024-11-29 | 2024-11-27 | 5EU | QUALIFIED |
| 2024-12-06 | 2024-12-04 | EUU | QUALIFIED |
| 2024-12-13 | 2024-12-11 | 2EU | QUALIFIED |
| 2024-12-20 | 2024-12-18 | 3EU | QUALIFIED |
| 2024-12-27 | 2024-12-25 | 4EU | UNAVAILABLE (HOLIDAY) |
| 2025-01-03 | 2025-01-01 | EUU | UNAVAILABLE (HOLIDAY) |
| 2025-01-10 | 2025-01-08 | 2EU | QUALIFIED |
| 2025-01-17 | 2025-01-15 | 3EU | QUALIFIED |
| 2025-01-24 | 2025-01-22 | 4EU | QUALIFIED |
| 2025-01-31 | 2025-01-29 | 5EU | QUALIFIED |
| 2025-02-07 | 2025-02-05 | EUU | QUALIFIED |
| 2025-02-14 | 2025-02-12 | 2EU | QUALIFIED |
| 2025-02-21 | 2025-02-19 | 3EU | QUALIFIED |
| 2025-02-28 | 2025-02-26 | 4EU | QUALIFIED |
| 2025-03-07 | 2025-03-05 | EUU | QUALIFIED |
| 2025-03-14 | 2025-03-12 | 2EU | QUALIFIED |
| 2025-03-21 | 2025-03-19 | 3EU | QUALIFIED |
| 2025-03-28 | 2025-03-26 | 4EU | QUALIFIED |
| 2025-04-04 | 2025-04-02 | EUU | QUALIFIED |
| 2025-04-11 | 2025-04-09 | 2EU | QUALIFIED |
| 2025-04-18 | 2025-04-16 | 3EU | UNAVAILABLE (HOLIDAY) |
| 2025-04-25 | 2025-04-23 | 4EU | QUALIFIED |
| 2025-05-02 | 2025-04-30 | 1EU | QUALIFIED |
| 2025-05-09 | 2025-05-07 | EUU | QUALIFIED |
| 2025-05-16 | 2025-05-14 | 3EU | QUALIFIED |
| 2025-05-23 | 2025-05-21 | 4EU | QUALIFIED |
| 2025-05-30 | 2025-05-28 | 5EU | QUALIFIED |
| 2025-06-06 | 2025-06-04 | EUU | QUALIFIED |
| 2025-06-13 | 2025-06-11 | 2EU | QUALIFIED |
| 2025-06-20 | 2025-06-18 | 3EU | QUALIFIED |
| 2025-06-27 | 2025-06-25 | 4EU | QUALIFIED |
| 2025-07-04 | 2025-07-02 | EUU | UNAVAILABLE (HOLIDAY) |
| 2025-07-11 | 2025-07-09 | 2EU | QUALIFIED |
| 2025-07-18 | 2025-07-16 | 3EU | QUALIFIED |
| 2025-07-25 | 2025-07-23 | 4EU | QUALIFIED |
| 2025-08-01 | 2025-07-30 | 1EU | QUALIFIED |
| 2025-08-08 | 2025-08-06 | EUU | QUALIFIED |
| 2025-08-15 | 2025-08-13 | 3EU | QUALIFIED |
| 2025-08-22 | 2025-08-20 | 4EU | QUALIFIED |
| 2025-08-29 | 2025-08-27 | 5EU | QUALIFIED |
| 2025-09-05 | 2025-09-03 | EUU | QUALIFIED |
| 2025-09-12 | 2025-09-10 | 2EU | QUALIFIED |
| 2025-09-19 | 2025-09-17 | 3EU | QUALIFIED |
| 2025-09-26 | 2025-09-24 | 4EU | QUALIFIED |
| 2025-10-03 | 2025-10-01 | EUU | QUALIFIED |
| 2025-10-10 | 2025-10-08 | 2EU | QUALIFIED |
| 2025-10-17 | 2025-10-15 | 3EU | QUALIFIED |
| 2025-10-24 | 2025-10-22 | 4EU | QUALIFIED |
| 2025-10-31 | 2025-10-29 | 5EU | QUALIFIED |
| 2025-11-07 | 2025-11-05 | EUU | QUALIFIED |
| 2025-11-14 | 2025-11-12 | 2EU | QUALIFIED |
| 2025-11-21 | 2025-11-19 | 3EU | QUALIFIED |
| 2025-11-28 | 2025-11-26 | 4EU | QUALIFIED |
| 2025-12-05 | 2025-12-03 | EUU | QUALIFIED |
| 2025-12-12 | 2025-12-10 | 2EU | QUALIFIED |
| 2025-12-19 | 2025-12-17 | 3EU | QUALIFIED |
| 2025-12-26 | 2025-12-24 | 4EU | QUALIFIED |
| 2026-01-02 | 2025-12-31 | 1EU | QUALIFIED |
| 2026-01-09 | 2026-01-07 | EUU | QUALIFIED |
| 2026-01-16 | 2026-01-14 | 3EU | QUALIFIED |
| 2026-01-23 | 2026-01-21 | 4EU | QUALIFIED |
| 2026-01-30 | 2026-01-28 | 5EU | QUALIFIED |
| 2026-02-06 | 2026-02-04 | EUU | QUALIFIED |
| 2026-02-13 | 2026-02-11 | 2EU | QUALIFIED |
| 2026-02-20 | 2026-02-18 | 3EU | QUALIFIED |
| 2026-02-27 | 2026-02-25 | 4EU | QUALIFIED |
| 2026-03-06 | 2026-03-04 | EUU | QUALIFIED |
| 2026-03-13 | 2026-03-11 | 2EU | QUALIFIED |
| 2026-03-20 | 2026-03-18 | 3EU | QUALIFIED |
| 2026-03-27 | 2026-03-25 | 4EU | QUALIFIED |
| 2026-04-03 | 2026-04-01 | EUU | UNAVAILABLE (HOLIDAY) |
| 2026-04-10 | 2026-04-08 | 2EU | QUALIFIED |
| 2026-04-17 | 2026-04-15 | 3EU | QUALIFIED |
| 2026-04-24 | 2026-04-22 | 4EU | QUALIFIED |
| 2026-05-01 | 2026-04-29 | 1EU | QUALIFIED |
| 2026-05-08 | 2026-05-06 | EUU | QUALIFIED |
| 2026-05-15 | 2026-05-13 | 3EU | QUALIFIED |
| 2026-05-22 | 2026-05-20 | 4EU | QUALIFIED |
| 2026-05-29 | 2026-05-27 | 5EU | QUALIFIED |
| 2026-06-05 | 2026-06-03 | EUU | QUALIFIED |
| 2026-06-12 | 2026-06-10 | 2EU | QUALIFIED |
| 2026-06-19 | 2026-06-17 | 3EU | UNAVAILABLE (HOLIDAY) |
| 2026-06-26 | 2026-06-24 | 4EU | QUALIFIED |

## C. Exact Futures Mapping
*Note: The identified underlying futures contract corresponds directly to the active quarterly delivery month for the option's expiry.*

| Expiry Date | Observation Date | Underlying Futures Symbol | Expected Active |
| :--- | :--- | :--- | :--- |
| 2022-01-07 | 2022-01-05 | 6EH2 | Yes |
| 2022-01-14 | 2022-01-12 | 6EH2 | Yes |
| 2022-01-21 | 2022-01-19 | 6EH2 | Yes |
| 2022-01-28 | 2022-01-26 | 6EH2 | Yes |
| 2022-02-04 | 2022-02-02 | 6EH2 | Yes |
| 2022-02-11 | 2022-02-09 | 6EH2 | Yes |
| 2022-02-18 | 2022-02-16 | 6EH2 | Yes |
| 2022-02-25 | 2022-02-23 | 6EH2 | Yes |
| 2022-03-04 | 2022-03-02 | 6EH2 | Yes |
| 2022-03-11 | 2022-03-09 | 6EH2 | Yes |
| 2022-03-18 | 2022-03-16 | 6EH2 | Yes |
| 2022-03-25 | 2022-03-23 | 6EH2 | Yes |
| 2022-04-01 | 2022-03-30 | 6EM2 | Yes |
| 2022-04-08 | 2022-04-06 | 6EM2 | Yes |
| 2022-04-15 | 2022-04-13 | 6EM2 | No (Holiday) |
| 2022-04-22 | 2022-04-20 | 6EM2 | Yes |
| 2022-04-29 | 2022-04-27 | 6EM2 | Yes |
| 2022-05-06 | 2022-05-04 | 6EM2 | Yes |
| 2022-05-13 | 2022-05-11 | 6EM2 | Yes |
| 2022-05-20 | 2022-05-18 | 6EM2 | Yes |
| 2022-05-27 | 2022-05-25 | 6EM2 | Yes |
| 2022-06-03 | 2022-06-01 | 6EM2 | Yes |
| 2022-06-10 | 2022-06-08 | 6EM2 | Yes |
| 2022-06-17 | 2022-06-15 | 6EM2 | Yes |
| 2022-06-24 | 2022-06-22 | 6EM2 | Yes |
| 2022-07-01 | 2022-06-29 | 6EU2 | Yes |
| 2022-07-08 | 2022-07-06 | 6EU2 | Yes |
| 2022-07-15 | 2022-07-13 | 6EU2 | Yes |
| 2022-07-22 | 2022-07-20 | 6EU2 | Yes |
| 2022-07-29 | 2022-07-27 | 6EU2 | Yes |
| 2022-08-05 | 2022-08-03 | 6EU2 | Yes |
| 2022-08-12 | 2022-08-10 | 6EU2 | Yes |
| 2022-08-19 | 2022-08-17 | 6EU2 | Yes |
| 2022-08-26 | 2022-08-24 | 6EU2 | Yes |
| 2022-09-02 | 2022-08-31 | 6EU2 | Yes |
| 2022-09-09 | 2022-09-07 | 6EU2 | Yes |
| 2022-09-16 | 2022-09-14 | 6EU2 | Yes |
| 2022-09-23 | 2022-09-21 | 6EU2 | Yes |
| 2022-09-30 | 2022-09-28 | 6EU2 | Yes |
| 2022-10-07 | 2022-10-05 | 6EZ2 | Yes |
| 2022-10-14 | 2022-10-12 | 6EZ2 | Yes |
| 2022-10-21 | 2022-10-19 | 6EZ2 | Yes |
| 2022-10-28 | 2022-10-26 | 6EZ2 | Yes |
| 2022-11-04 | 2022-11-02 | 6EZ2 | Yes |
| 2022-11-11 | 2022-11-09 | 6EZ2 | No (Holiday) |
| 2022-11-18 | 2022-11-16 | 6EZ2 | Yes |
| 2022-11-25 | 2022-11-23 | 6EZ2 | Yes |
| 2022-12-02 | 2022-11-30 | 6EZ2 | Yes |
| 2022-12-09 | 2022-12-07 | 6EZ2 | Yes |
| 2022-12-16 | 2022-12-14 | 6EZ2 | Yes |
| 2022-12-23 | 2022-12-21 | 6EZ2 | Yes |
| 2022-12-30 | 2022-12-28 | 6EZ2 | Yes |
| 2023-01-06 | 2023-01-04 | 6EH3 | Yes |
| 2023-01-13 | 2023-01-11 | 6EH3 | Yes |
| 2023-01-20 | 2023-01-18 | 6EH3 | Yes |
| 2023-01-27 | 2023-01-25 | 6EH3 | Yes |
| 2023-02-03 | 2023-02-01 | 6EH3 | Yes |
| 2023-02-10 | 2023-02-08 | 6EH3 | Yes |
| 2023-02-17 | 2023-02-15 | 6EH3 | Yes |
| 2023-02-24 | 2023-02-22 | 6EH3 | Yes |
| 2023-03-03 | 2023-03-01 | 6EH3 | Yes |
| 2023-03-10 | 2023-03-08 | 6EH3 | Yes |
| 2023-03-17 | 2023-03-15 | 6EH3 | Yes |
| 2023-03-24 | 2023-03-22 | 6EH3 | Yes |
| 2023-03-31 | 2023-03-29 | 6EH3 | Yes |
| 2023-04-07 | 2023-04-05 | 6EM3 | No (Holiday) |
| 2023-04-14 | 2023-04-12 | 6EM3 | Yes |
| 2023-04-21 | 2023-04-19 | 6EM3 | Yes |
| 2023-04-28 | 2023-04-26 | 6EM3 | Yes |
| 2023-05-05 | 2023-05-03 | 6EM3 | Yes |
| 2023-05-12 | 2023-05-10 | 6EM3 | Yes |
| 2023-05-19 | 2023-05-17 | 6EM3 | Yes |
| 2023-05-26 | 2023-05-24 | 6EM3 | Yes |
| 2023-06-02 | 2023-05-31 | 6EM3 | Yes |
| 2023-06-09 | 2023-06-07 | 6EM3 | Yes |
| 2023-06-16 | 2023-06-14 | 6EM3 | Yes |
| 2023-06-23 | 2023-06-21 | 6EM3 | Yes |
| 2023-06-30 | 2023-06-28 | 6EM3 | Yes |
| 2023-07-07 | 2023-07-05 | 6EU3 | Yes |
| 2023-07-14 | 2023-07-12 | 6EU3 | Yes |
| 2023-07-21 | 2023-07-19 | 6EU3 | Yes |
| 2023-07-28 | 2023-07-26 | 6EU3 | Yes |
| 2023-08-04 | 2023-08-02 | 6EU3 | Yes |
| 2023-08-11 | 2023-08-09 | 6EU3 | Yes |
| 2023-08-18 | 2023-08-16 | 6EU3 | Yes |
| 2023-08-25 | 2023-08-23 | 6EU3 | Yes |
| 2023-09-01 | 2023-08-30 | 6EU3 | Yes |
| 2023-09-08 | 2023-09-06 | 6EU3 | Yes |
| 2023-09-15 | 2023-09-13 | 6EU3 | Yes |
| 2023-09-22 | 2023-09-20 | 6EU3 | Yes |
| 2023-09-29 | 2023-09-27 | 6EU3 | Yes |
| 2023-10-06 | 2023-10-04 | 6EZ3 | Yes |
| 2023-10-13 | 2023-10-11 | 6EZ3 | Yes |
| 2023-10-20 | 2023-10-18 | 6EZ3 | Yes |
| 2023-10-27 | 2023-10-25 | 6EZ3 | Yes |
| 2023-11-03 | 2023-11-01 | 6EZ3 | Yes |
| 2023-11-10 | 2023-11-08 | 6EZ3 | No (Holiday) |
| 2023-11-17 | 2023-11-15 | 6EZ3 | Yes |
| 2023-11-24 | 2023-11-22 | 6EZ3 | Yes |
| 2023-12-01 | 2023-11-29 | 6EZ3 | Yes |
| 2023-12-08 | 2023-12-06 | 6EZ3 | Yes |
| 2023-12-15 | 2023-12-13 | 6EZ3 | Yes |
| 2023-12-22 | 2023-12-20 | 6EZ3 | Yes |
| 2023-12-29 | 2023-12-27 | 6EZ3 | Yes |
| 2024-01-05 | 2024-01-03 | 6EH4 | Yes |
| 2024-01-12 | 2024-01-10 | 6EH4 | Yes |
| 2024-01-19 | 2024-01-17 | 6EH4 | Yes |
| 2024-01-26 | 2024-01-24 | 6EH4 | Yes |
| 2024-02-02 | 2024-01-31 | 6EH4 | Yes |
| 2024-02-09 | 2024-02-07 | 6EH4 | Yes |
| 2024-02-16 | 2024-02-14 | 6EH4 | Yes |
| 2024-02-23 | 2024-02-21 | 6EH4 | Yes |
| 2024-03-01 | 2024-02-28 | 6EH4 | Yes |
| 2024-03-08 | 2024-03-06 | 6EH4 | Yes |
| 2024-03-15 | 2024-03-13 | 6EH4 | Yes |
| 2024-03-22 | 2024-03-20 | 6EH4 | Yes |
| 2024-03-29 | 2024-03-27 | 6EH4 | No (Holiday) |
| 2024-04-05 | 2024-04-03 | 6EM4 | Yes |
| 2024-04-12 | 2024-04-10 | 6EM4 | Yes |
| 2024-04-19 | 2024-04-17 | 6EM4 | Yes |
| 2024-04-26 | 2024-04-24 | 6EM4 | Yes |
| 2024-05-03 | 2024-05-01 | 6EM4 | Yes |
| 2024-05-10 | 2024-05-08 | 6EM4 | Yes |
| 2024-05-17 | 2024-05-15 | 6EM4 | Yes |
| 2024-05-24 | 2024-05-22 | 6EM4 | Yes |
| 2024-05-31 | 2024-05-29 | 6EM4 | Yes |
| 2024-06-07 | 2024-06-05 | 6EM4 | Yes |
| 2024-06-14 | 2024-06-12 | 6EM4 | Yes |
| 2024-06-21 | 2024-06-19 | 6EM4 | No (Holiday) |
| 2024-06-28 | 2024-06-26 | 6EM4 | Yes |
| 2024-07-05 | 2024-07-03 | 6EU4 | Yes |
| 2024-07-12 | 2024-07-10 | 6EU4 | Yes |
| 2024-07-19 | 2024-07-17 | 6EU4 | Yes |
| 2024-07-26 | 2024-07-24 | 6EU4 | Yes |
| 2024-08-02 | 2024-07-31 | 6EU4 | Yes |
| 2024-08-09 | 2024-08-07 | 6EU4 | Yes |
| 2024-08-16 | 2024-08-14 | 6EU4 | Yes |
| 2024-08-23 | 2024-08-21 | 6EU4 | Yes |
| 2024-08-30 | 2024-08-28 | 6EU4 | Yes |
| 2024-09-06 | 2024-09-04 | 6EU4 | Yes |
| 2024-09-13 | 2024-09-11 | 6EU4 | Yes |
| 2024-09-20 | 2024-09-18 | 6EU4 | Yes |
| 2024-09-27 | 2024-09-25 | 6EU4 | Yes |
| 2024-10-04 | 2024-10-02 | 6EZ4 | Yes |
| 2024-10-11 | 2024-10-09 | 6EZ4 | Yes |
| 2024-10-18 | 2024-10-16 | 6EZ4 | Yes |
| 2024-10-25 | 2024-10-23 | 6EZ4 | Yes |
| 2024-11-01 | 2024-10-30 | 6EZ4 | Yes |
| 2024-11-08 | 2024-11-06 | 6EZ4 | Yes |
| 2024-11-15 | 2024-11-13 | 6EZ4 | Yes |
| 2024-11-22 | 2024-11-20 | 6EZ4 | Yes |
| 2024-11-29 | 2024-11-27 | 6EZ4 | Yes |
| 2024-12-06 | 2024-12-04 | 6EZ4 | Yes |
| 2024-12-13 | 2024-12-11 | 6EZ4 | Yes |
| 2024-12-20 | 2024-12-18 | 6EZ4 | Yes |
| 2024-12-27 | 2024-12-25 | 6EZ4 | No (Holiday) |
| 2025-01-03 | 2025-01-01 | 6EH5 | No (Holiday) |
| 2025-01-10 | 2025-01-08 | 6EH5 | Yes |
| 2025-01-17 | 2025-01-15 | 6EH5 | Yes |
| 2025-01-24 | 2025-01-22 | 6EH5 | Yes |
| 2025-01-31 | 2025-01-29 | 6EH5 | Yes |
| 2025-02-07 | 2025-02-05 | 6EH5 | Yes |
| 2025-02-14 | 2025-02-12 | 6EH5 | Yes |
| 2025-02-21 | 2025-02-19 | 6EH5 | Yes |
| 2025-02-28 | 2025-02-26 | 6EH5 | Yes |
| 2025-03-07 | 2025-03-05 | 6EH5 | Yes |
| 2025-03-14 | 2025-03-12 | 6EH5 | Yes |
| 2025-03-21 | 2025-03-19 | 6EH5 | Yes |
| 2025-03-28 | 2025-03-26 | 6EH5 | Yes |
| 2025-04-04 | 2025-04-02 | 6EM5 | Yes |
| 2025-04-11 | 2025-04-09 | 6EM5 | Yes |
| 2025-04-18 | 2025-04-16 | 6EM5 | No (Holiday) |
| 2025-04-25 | 2025-04-23 | 6EM5 | Yes |
| 2025-05-02 | 2025-04-30 | 6EM5 | Yes |
| 2025-05-09 | 2025-05-07 | 6EM5 | Yes |
| 2025-05-16 | 2025-05-14 | 6EM5 | Yes |
| 2025-05-23 | 2025-05-21 | 6EM5 | Yes |
| 2025-05-30 | 2025-05-28 | 6EM5 | Yes |
| 2025-06-06 | 2025-06-04 | 6EM5 | Yes |
| 2025-06-13 | 2025-06-11 | 6EM5 | Yes |
| 2025-06-20 | 2025-06-18 | 6EM5 | Yes |
| 2025-06-27 | 2025-06-25 | 6EM5 | Yes |
| 2025-07-04 | 2025-07-02 | 6EU5 | No (Holiday) |
| 2025-07-11 | 2025-07-09 | 6EU5 | Yes |
| 2025-07-18 | 2025-07-16 | 6EU5 | Yes |
| 2025-07-25 | 2025-07-23 | 6EU5 | Yes |
| 2025-08-01 | 2025-07-30 | 6EU5 | Yes |
| 2025-08-08 | 2025-08-06 | 6EU5 | Yes |
| 2025-08-15 | 2025-08-13 | 6EU5 | Yes |
| 2025-08-22 | 2025-08-20 | 6EU5 | Yes |
| 2025-08-29 | 2025-08-27 | 6EU5 | Yes |
| 2025-09-05 | 2025-09-03 | 6EU5 | Yes |
| 2025-09-12 | 2025-09-10 | 6EU5 | Yes |
| 2025-09-19 | 2025-09-17 | 6EU5 | Yes |
| 2025-09-26 | 2025-09-24 | 6EU5 | Yes |
| 2025-10-03 | 2025-10-01 | 6EZ5 | Yes |
| 2025-10-10 | 2025-10-08 | 6EZ5 | Yes |
| 2025-10-17 | 2025-10-15 | 6EZ5 | Yes |
| 2025-10-24 | 2025-10-22 | 6EZ5 | Yes |
| 2025-10-31 | 2025-10-29 | 6EZ5 | Yes |
| 2025-11-07 | 2025-11-05 | 6EZ5 | Yes |
| 2025-11-14 | 2025-11-12 | 6EZ5 | Yes |
| 2025-11-21 | 2025-11-19 | 6EZ5 | Yes |
| 2025-11-28 | 2025-11-26 | 6EZ5 | Yes |
| 2025-12-05 | 2025-12-03 | 6EZ5 | Yes |
| 2025-12-12 | 2025-12-10 | 6EZ5 | Yes |
| 2025-12-19 | 2025-12-17 | 6EZ5 | Yes |
| 2025-12-26 | 2025-12-24 | 6EZ5 | Yes |
| 2026-01-02 | 2025-12-31 | 6EH6 | Yes |
| 2026-01-09 | 2026-01-07 | 6EH6 | Yes |
| 2026-01-16 | 2026-01-14 | 6EH6 | Yes |
| 2026-01-23 | 2026-01-21 | 6EH6 | Yes |
| 2026-01-30 | 2026-01-28 | 6EH6 | Yes |
| 2026-02-06 | 2026-02-04 | 6EH6 | Yes |
| 2026-02-13 | 2026-02-11 | 6EH6 | Yes |
| 2026-02-20 | 2026-02-18 | 6EH6 | Yes |
| 2026-02-27 | 2026-02-25 | 6EH6 | Yes |
| 2026-03-06 | 2026-03-04 | 6EH6 | Yes |
| 2026-03-13 | 2026-03-11 | 6EH6 | Yes |
| 2026-03-20 | 2026-03-18 | 6EH6 | Yes |
| 2026-03-27 | 2026-03-25 | 6EH6 | Yes |
| 2026-04-03 | 2026-04-01 | 6EM6 | No (Holiday) |
| 2026-04-10 | 2026-04-08 | 6EM6 | Yes |
| 2026-04-17 | 2026-04-15 | 6EM6 | Yes |
| 2026-04-24 | 2026-04-22 | 6EM6 | Yes |
| 2026-05-01 | 2026-04-29 | 6EM6 | Yes |
| 2026-05-08 | 2026-05-06 | 6EM6 | Yes |
| 2026-05-15 | 2026-05-13 | 6EM6 | Yes |
| 2026-05-22 | 2026-05-20 | 6EM6 | Yes |
| 2026-05-29 | 2026-05-27 | 6EM6 | Yes |
| 2026-06-05 | 2026-06-03 | 6EM6 | Yes |
| 2026-06-12 | 2026-06-10 | 6EM6 | Yes |
| 2026-06-19 | 2026-06-17 | 6EM6 | No (Holiday) |
| 2026-06-26 | 2026-06-24 | 6EM6 | Yes |

## D. Exact Quote Windows
The exact required data window for each event is:
- **Start**: Wednesday (00:00:00 UTC)
- **End**: Friday (23:59:59 UTC)

No additional surrounding period is required. The `Definition` schema fetched on Wednesday inherently contains the `strike_price` metadata required to interpret the `BBO-1m` instrument IDs. The BBO quotes stream initializes fully on Wednesday and does not require prior-day quotes for maturity-matched modeling.

## E. Exact Schema & Product Isolation
- **Primary Schema**: `BBO-1m` (Top-of-book quotes, minute-resampled)
- **Definition Schema**: `Definition` (For instrument metadata mapping)
- **Option Parent Product**: `6E.OPT` (This Databento parent inherently encompasses EUU and 1EU-5EU roots in a single query).
- **Futures Parent Product**: `6E` (Or direct exact symbols e.g. `6EM2`).
- **Product Filtering**: Ensure Databento queries request `security_type=OPT` for options and `security_type=FUT` for futures. Multi-leg (`MLEG`) instruments are explicitly **excluded**.

## F. Estimated Volume
- **Total Option Parent/Root Requests**: 1 (Using `6E.OPT` parent)
- **Total Futures Parent Requests**: 1 (Using `6E` parent)
- **Number of Dates**: 669 market-data days (223 events × 3 days)
- **Approximate BBO-1m Volume (Options)**: ~8,000 MB compressed (~12 MB/day)
- **Approximate BBO-1m Volume (Futures)**: ~1,300 MB compressed (~2 MB/day)
- **Total Estimated Volume**: ~9.3 GB

## G. Estimated Cost
Based on standard Databento historical tier pricing for highly compressed `BBO-1m` and `Definition` schemas:
- **Options Cost**: ~$4.00
- **Futures Cost**: ~$0.75
- **Total Estimate**: < $5.00 USD

## H. Operational Batching Plan
Acquiring 669 days of high-density BBO options data in a single zip file introduces decompression risk and memory overhead. The 223 events **should** safely be acquired in chronological batches by calendar year:
- **Batch 1**: 2022 (51 events)
- **Batch 2**: 2023 (51 events)
- **Batch 3**: 2024 (51 events)
- **Batch 4**: 2025 (50 events)
- **Batch 5**: 2026 H1 (20 events)

This reduces operational risk, keeps file sizes under 2 GB per batch, and avoids any change to the frozen sample structure.

## I. Data-Integrity Risks
1. **Moneyness Calculation**: Because we cannot know the true ATM strike until observing the active `6E` futures midpoint, we cannot query only a single expected strike. We must download the full `6E.OPT` chain and filter for `abs(strike - futures_mid) <= 0.0020` post-hoc.
2. **Missing Futures Connection**: Databento option BBO streams do not embed the underlying futures price. If the `6E` BBO-1m data is not perfectly synchronized with the `6E.OPT` data, the Black-76 implied volatility inversion will fail.

## J. Final Acquisition Checklist
- [x] Options Data: `6E.OPT` / `BBO-1m` & `Definition` (Calls/Puts only, NO MLEG)
- [x] Futures Data: `6E` / `BBO-1m`
- [x] Date Range: 223 specific Wed-Fri windows strictly defined by the frozen manifest.
- [x] Cost Approval: Verified < $5.00 limit.
- [x] Integrity: Confirmed sufficient parameters to calculate remaining-life IV, ATM alignment, and VRP mapping.
