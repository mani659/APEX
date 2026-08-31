# RC015 Study 007 - API Request Plan (Stage 2)

## Exact Proposed Request Structure
The following requests will fetch the exact eligible option instruments resolved in Stage 1.

### Global Parameters
- **Dataset**: `GLBX.MDP3`
- **Schema**: `bbo-1m`
- **stype_in**: `instrument_id`

### Batching Plan
To maximize operational safety and align with Databento limits, requests will be batched chronologically by event.

### Request Manifest
| Batch ID | Start Time | End Time | Instrument IDs |
| :--- | :--- | :--- | :--- |
