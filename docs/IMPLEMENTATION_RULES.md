# APEX Implementation Rules

This document serves as the constitution for implementation within the APEX Quant Research Framework. 

## 1. Mission

The primary directive is to protect the integrity of the architecture during coding. 
**Implementation follows architecture. Architecture does not follow implementation.** No architecture redesign should occur during implementation unless a genuine, fatal architectural defect is discovered.

---

## 2. Architecture Freeze

**Simulation Architecture v1 Status: FROZEN**

Any proposed changes to the runtime contracts or simulation pipeline structure require:
1. Evidence of an architectural defect or missing capability.
2. Formal Architecture Review.
3. An Architecture Decision Record (ADR).
4. Explicit Approval.

---

## 3. Engineering Principles

Implementation must **always** be:
- **Deterministic:** The exact same inputs must yield the exact same outputs.
- **Reproducible:** Anyone running the code must get identical results.
- **Modular:** Components must be swappable without breaking the system.
- **Typed:** Use strict type hinting across all modules.
- **Testable:** Built for unit testing from the ground up.
- **Documented:** Self-explanatory code backed by clear docstrings.
- **Simple:** Avoid unnecessary complexity.
- **Readable:** Code is read vastly more often than it is written.

---

## 4. Non-Negotiable Rules

- **Never** violate runtime contracts (e.g., `Signal`, `ExecutionReport`).
- **Never** bypass Data Transfer Objects (DTOs).
- **Never** introduce hidden state to circumvent structural limitations.
- **Never** use global mutable variables.
- **Never** couple Strategy directly to Execution.
- **Never** place Research logic inside Simulation logic.
- **Never** place Analytics logic inside Execution logic.
- **One responsibility** per module.
- **Evidence** before optimization.
- **Research** before optimization.
- **Doctor** (resilience and validation framework) must pass before merging.

---

## 5. Testing Rules

Every subsystem:
- **Must** have comprehensive unit tests.
- **Must** be independently executable.
- **Must** remain entirely deterministic.

---

## 6. Coding Rules

- Prefer readability over cleverness.
- Avoid premature optimization. Write clean logic first; optimize only if profiling proves it necessary.
- Avoid unnecessary abstraction. Do not create interfaces or factories for things that will only ever have one implementation.
- Do not over-engineer. 
- YAGNI (You Aren't Gonna Need It) applies unconditionally, unless the frozen architecture specifications explicitly require otherwise.

---

## 7. Documentation Rules

- Every public module
- Every public class
- Every public function

**Must contain professional, accurate documentation (docstrings).**

---

## 8. Definition of Done

A sprint or feature branch is considered complete **only when**:
- Implementation works exactly as specified by the architecture.
- All unit tests pass.
- The Doctor validation framework passes.
- All relevant documentation is updated.
- No runtime contracts are broken or bypassed.

---

## Final Statement

With the approval of the Simulation Architecture Gate, APEX officially enters the Simulation Implementation phase. The architecture is considered frozen. Future effort focuses on disciplined engineering, validation, and evidence-based evolution rather than architectural redesign.

---

## Architecture Notes

### Architecture Note 1

The Monte Carlo Engine currently uses a RecordingPortfolioEngine adapter to observe immutable Trade objects.

This adapter is considered an internal research utility rather than part of the Simulation Core.

It must never be reused as a production PortfolioEngine implementation.

Future framework versions may replace this adapter with an event bus or observation interface without affecting the frozen Simulation Core.

### Architecture Note 2

The current implementation uses Python's global random generator for deterministic replay.

Future framework versions may migrate to isolated random.Random(seed) instances to improve thread safety and parallel execution.

This is considered a low-priority architectural enhancement and is not a defect.

### Architecture Note 3

Optimization Engine is a research orchestration layer.

It must never contain simulation logic, execution logic, portfolio accounting, or statistical calculations beyond objective extraction.

It may only coordinate evaluations through public interfaces.

Future optimization algorithms (Bayesian Optimization, CMA-ES, Genetic Algorithms, Particle Swarm, etc.) shall be implemented by extending the Optimization layer without modifying the Simulation Core or Research Core.
