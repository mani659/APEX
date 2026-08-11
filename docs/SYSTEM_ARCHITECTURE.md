# APEX System Architecture

This document describes the high-level architecture and dependencies of the APEX framework.

## Core Architectural Principle
**Presentation Layer performs:**
- **NO calculations**
- **NO simulations**
- **NO optimization**
- **NO statistical processing**
*The Presentation Layer is strictly read-only.*

---

## Dependency Graph

```mermaid
graph TD;
    subgraph Market Data
    Data(Data Loader)
    end

    subgraph Simulation Core [Simulation Core - Frozen]
    Runner(Simulation Runner)
    OrderMgr(Order Manager)
    ExecEngine(Execution Engine)
    PosEngine(Position Engine)
    PortEngine(Portfolio Engine)
    StatEngine(Statistics Engine)
    end

    subgraph Phase 2 Research Infrastructure [Phase 2 Research Layer - Frozen]
    MarketData(Market Data) --> FeatLib(Research Feature Library)
    FeatLib --> FeatPipe(Feature Pipeline)
    FeatPipe --> FeatStore(Feature Store)
    FeatStore --> LabelEng(Research Labeling Engine)
    LabelEng --> DsBuilder(Dataset Builder)
    DsBuilder --> DsVal(Dataset Validation Engine)
    DsVal --> FeatAna(Feature Analysis Engine)
    FeatAna --> DsSplit(Dataset Split Engine)
    DsSplit --> ExpEng(Experiment Engine)
    ExpEng --> ExpRepo(Experiment Repository)
    end

    subgraph Presentation Layer [Presentation Layer - Frozen]
    Report(Report Generator)
    Vis(Visualization Engine)
    end

    subgraph Deployment Layer [Deployment Layer - Frozen]
    ExpTracker(Experiment Tracking)
    Exporter(Data Exporter)
    Validator(Validation)
    end

    Data --> Runner;
    Runner --> OrderMgr;
    OrderMgr --> ExecEngine;
    ExecEngine --> PosEngine;
    PosEngine --> PortEngine;
    PortEngine --> StatEngine;

    StatEngine --> WF;
    StatEngine --> MC;
    StatEngine --> Opt;

    WF --> Vis;
    MC --> Vis;
    Opt --> Vis;
    PortEngine -.-> Vis;
    StatEngine -.-> Vis;
    ExpTracker -.-> Vis;

    WF --> Report;
    MC --> Report;
    Opt --> Report;
```

## Visualization Engine Connections
The **Visualization Engine** is exclusively connected to immutable DTOs:
- `PortfolioSnapshot`
- `StatisticsSummary`
- `WalkForwardResult`
- `MonteCarloResult`
- `OptimizationResult`
- `ExperimentRecord`
