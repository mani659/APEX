# RC007 Study 004 — Entry Isolation Experiment (Model D: Pure Observation)

## Scientific Objective

Execute the first uncontaminated experiment using the RC007 Entry Isolation framework.

The purpose is **not profitability**.

The purpose is to observe the natural behaviour of every isolated Apex entry without allowing grid expansion, recovery logic, or basket averaging to influence the outcome.

This experiment establishes the statistical baseline of the behavioural hypothesis itself.

---

## Experimental Configuration

Dataset:
- EURUSD_M1.parquet

Execution Mode:
- ENTRY_ISOLATION

Exit Model:
- MODEL_D_OBSERVE

Configuration Rules:
- Exactly one position per signal
- No averaging
- No basket expansion
- No grid
- No parameter optimisation
- No stop-loss optimisation
- No take-profit optimisation

The engine should simply observe every trade until the predefined observation window expires while continuously recording:

- MAE
- MFE
- Bars Held
- Time to MAE
- Time to MFE
- Final PnL

---

## Required Outputs

Generate a complete statistical report containing:

### 1. Entry Statistics

- Total behavioural events
- Total valid entries
- Long entries
- Short entries

---

### 2. Distribution Statistics

For every isolated trade calculate:

- Mean MAE
- Median MAE
- 95th percentile MAE

- Mean MFE
- Median MFE
- 95th percentile MFE

- Mean holding time
- Median holding time

---

### 3. Excursion Analysis

Determine:

- How often MAE occurs before MFE
- How often MFE occurs before MAE
- Average time until MAE
- Average time until MFE

These numbers describe the natural behaviour of the setup.

---

### 4. Behaviour Classification

Automatically classify every trade into groups such as:

- Immediate winner
- Immediate loser
- Deep adverse then recovery
- Small excursion then trend
- Flat/no movement

Report the percentage of trades belonging to each class.

---

### 5. Outcome Distribution

Produce the distribution of final PnL.

Do not optimise anything.

Simply describe what actually happened.

---

### 6. Scientific Interpretation

Based only on the observed statistics, answer:

- Does the raw Apex entry possess measurable edge?
- Does the edge appear asymmetric?
- Is the edge fast or slow?
- Does the edge rely on recovery mechanisms?
- What does the isolated behaviour suggest about the underlying market microstructure?

Support every conclusion with measured evidence.

---

## Constraints

Do NOT:

- modify thresholds
- optimise exits
- change ATR calculations
- tune parameters
- introduce ML
- change the engine

The objective is observation only.

---

## Success Criteria

The study succeeds if it produces the first uncontaminated behavioural profile of the Apex entry signal.

This dataset will become the statistical foundation for every subsequent RC007 study.
