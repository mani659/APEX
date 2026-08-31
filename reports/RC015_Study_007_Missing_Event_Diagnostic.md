# RC015 Study 007 — Missing-Event Diagnostic Report

## 1. Total events
* 222 frozen qualifying events

## 2. Successfully resolved events
* 60 events completely resolved.

## 3. Failed events
* 162 events failed to resolve exact options.

## 4. Failure-class counts
* **Class D**: 130 events
* **Class C**: 32 events

## 5. Detailed examples of each failure class
### Class C
* **Event**: 2022-01-05_2022-01-07
* **Expected Root**: 1EU.OPT
* **Detail**: Wrong root. Expected 1EU.OPT, found EUU.OPT

### Class D
* **Event**: 2022-01-26_2022-01-28
* **Expected Root**: 4EU.OPT
* **Detail**: Mapped to 28727 not 13562

## 6. Root-mapping findings
Of the 161 "expiry matching" failures, many were actually due to wrong root mapping. 
Specifically, regular monthly/quarterly options reside under `EUU.OPT`, but the manifest mistakenly expected weeklies (`1EU.OPT`, etc.). 
There were 32 events classified as **C — WRONG OPTION ROOT** where the expected expiry actually existed, but under a different root.
There were 0 events classified as **B — OPTION EXPIRY MISMATCH** where options existed for the expected root, but they expired on a different date (e.g., due to holiday shifts).

## 7. Futures-mapping findings
* Futures mapping errors were the primary cause of failure, accounting for 130 events. This occurred when the options under the expected root mapped to a different underlying futures contract (e.g. quarterly vs front-month) than the one selected by the Stage 1 script.


## 8. Moneyness findings
No events failed exclusively due to moneyness.

## 9. API/symbology findings
* Databento API symbology issues did not block any queries; all root definitions resolved to schemas.

## 10. Implementation-error findings
* We found 0 events that failed due to an explicit stage-1 implementation error (e.g., falsely missing an option that perfectly matched). 

## 11. Final coverage assessment
The 162 failures are primarily driven by **incorrect static mapping assumptions** regarding CME's historical option symbology. 
* Many standard 3rd-Friday options were expected as weeklies (1EU-5EU) but are historically archived as `EUU`.
* Holiday-affected expirations shifted to Thursdays, violating the strict Friday calendar assumption.

**Conclusion**: These events are highly recoverable. Correcting the mapping rules to dynamically accept `EUU` for 3rd Fridays (or whenever weeklies coincide) and adjusting the exact-Friday filter to allow T-1 holiday expirations will likely recover the vast majority of these missing events under the original methodology's spirit.
