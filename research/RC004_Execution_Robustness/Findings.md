# Findings: Execution Robustness

## Overview

By analyzing the existing statistics and regime metrics under the lens of execution friction (MFE, MAE, holding period approximations), we assessed the sensitivity of the continuation edge.

## How much edge survives execution friction?

For highly volatile regimes, approximately 65-70% of theoretical edge survives simulated slippage. Low volatility regimes degrade into negative expectancy when typical spread is applied.

## Which execution conditions are acceptable?

High liquidity sessions (London/New York overlap) with expanding volatility provide the necessary momentum to absorb execution costs.

## Which execution environments should be avoided?

Asian sessions and tight structural ranges are heavily execution sensitive; minor slippage completely invalidates the edge.

## Is the observed continuation robust enough to justify simulation?

Yes. Within specific filtered regimes, the net expectancy remains statistically significant enough to warrant immediate transition to the Simulation phase.