# RC015 Final Adjudication — CME Listed-Option Path Closure

## 1. Proven Facts vs. Stronger Claims

### Proven by the existing data:
* The 24-hour Wednesday M15 chronological observation grid failed.
* The predefined 5, 15, 30, and 60-minute quote-age policies failed to provide adequate event coverage for the original grid.
* The four structurally justified candidate designs evaluated in Study 008 failed to satisfy the proposed 15-minute minimum liquidity gate.
* The option quote-age distribution for EUR/USD listed options on Globex is extremely sparse (often spanning several hours between quotes).
* Acquisition and data recovery integrity is complete (222/222 events, zero missing datasets).
* No lookahead bias was introduced (strict `ts_event <= t` logic was proven).
* The economic hypothesis (IV/RV variance gaps) was strictly protected and never tested.

### Claims that are too strong (Rejected):
* *"No possible observation design exists."* -> **Corrected Claim**: No tested structurally justified observation design satisfied the predefined liquidity gate on the acquired CME EUR/USD listed-option dataset.

## 2. Audit of the Predeclared Liquidity Gate

The liquidity gate utilized in Study 008 demanded an option quote age of $\le 15$ minutes covering at least 80% of the 222 frozen events. 

While this threshold represents a sound scientific standard for Contemporaneous pricing, it was technically established *after* Study 007 had already revealed the total failure of the original M15 grid and demonstrated the massive quote-age sparsity of the dataset. Therefore, the exact threshold (80% / 15m) cannot claim pure *ex ante* provenance from the beginning of RC015. 

**Status**: `EX_POST_GATE_PROVENANCE_UNCERTAIN`

Despite this uncertain provenance, the magnitude of the quote sparsity is so severe (failing even a 60-minute tolerance across most events) that the study would remain methodologically paralyzed under any defensible scientific standard.

## 3. Final Scientific Classification

**`CLOSED — LISTED-OPTION PATH METHOD INFEASIBLE`**

The evidence firmly supports closing the CME listed-option implementation because it is fundamentally unable to meet the project's required chronological observation standards without compromising data integrity.

## 4. Protection of the Economic Hypothesis

**The following have NOT been established by RC015:**
* That HIGH_VOL has no economic value.
* That IV/RV has no relationship.
* That volatility pricing has no edge.
* That options cannot price volatility inefficiently.

**What has been established is strictly that:**
> The tested CME listed-option observation architecture could not generate a sufficiently reliable historical IV panel under the study's data-quality requirements.

The core economic hypothesis remains formally **UNTESTED** and perfectly valid.

## 5. Quantification of the Full Evidence Chain

**Study 007 Original Framework:**
```text
222 frozen events
699 option IDs
19 futures IDs
Stage-2 acquisition complete
1.2570 USD acquisition cost
Stage-2 recovery complete
21,312 predetermined M15 slots
91 exact-fresh synchronized slots
1.8% <=5m
4.4% <=15m
7.6% <=30m
12.9% <=60m
0 events with >=75% coverage
0 events with 100% coverage
```

**Study 008 Candidate Designs (Coverage at $\le 15m$ quote-age):**
* **Design A (14:00 UTC fixed anchor)**: 10.3% of target slots.
* **Design B (08:00 & 14:00 UTC)**: 7.0% of target slots.
* **Design C (12:00–16:00 UTC window)**: 10.0% of target slots.
* **Design D (RC013 Transition anchors)**: 5.0% of target slots.

## 6. The True Failure Point

The failure of RC015 is definitively classified as a:
**`MARKET-STRUCTURE + METHODOLOGY-DESIGN LIMITATION`**

This is specifically because the asset (listed EUR/USD options on CME Globex) does not trade with sufficient density to populate the strict, predetermined chronological observation frameworks demanded by the methodology. 

It is emphatically **NOT**:
* missing data acquisition (Stage-2 was 100% complete and fully recovered);
* incorrect instrument mapping (the exact 699 options were properly mapped);
* wrong moneyness calculation (the $\le 0.0020$ rule correctly identified the ATM candidates);
* processing failure (the pipeline operated with mathematical perfection and refused to hallucinate data via forward-filling);
* lookahead (0 violations proven);
* insufficient Databento data (the complete historical book was acquired, it simply lacked quotes).

## 7. Future Research Boundary

The current RC015 implementation is closed. Any of the following ideas are explicitly **UNAPPROVED RESEARCH IDEAS ONLY** and are `NOT PART OF RC015`:
* Another market/instrument (e.g., equity index options, crypto options).
* A different options market for EUR/USD (e.g., OTC dealer data, EBS).
* OTC volatility data sets.
* A drastically different observation horizon (e.g., end-of-day daily settlement only).
* A deliberately redesigned study opening a completely new campaign.

These paths must not be executed without formal project-level approval and a new charter.
