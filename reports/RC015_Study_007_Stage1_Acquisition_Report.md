# RC015 Study 007 - Stage 1 Acquisition Report

## 1. Event Coverage Statistics
- **Events processed**: 222
- **Events with valid futures quotes**: 222
- **Events with no futures coverage**: 0
- **Events with valid option definitions**: 221
- **Events with no matching option expiry**: 161
- **Events with no eligible near-ATM options**: 162

## 2. Discovered Instruments
- **Number of unique futures instruments**: 55
- **Number of exact eligible option instruments**: 530
- **Unique Option Parents used**: 3EU.OPT, 4EU.OPT, EUU.OPT, 1EU.OPT, 5EU.OPT
- **Eligible Calls**: 9168
- **Eligible Puts**: 9168
- **MLEG/Spreads excluded**: Confirmed by security_type=OOF filtering.

## 3. Diagnostics
- **API/Symbology errors**: 0
- **Missing Market Data (Definitions)**: 1

## 4. Stage-2 Acquisition Projections
- **Proposed Stage-2 Option BBO requests**: 530 unique exact option instruments discovered across the subset of events that successfully resolved the frozen expiry, underlying, and moneyness rules.
- **Note**: The 162-event coverage shortfall is retained explicitly; do not silently exclude those events from future denominators.
- **Estimated Stage-2 data volume**: ~26.50 MB
- **Estimated Stage-2 cost**: $0.45
