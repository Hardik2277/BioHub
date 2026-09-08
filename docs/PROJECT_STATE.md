# BioHub — Project State

**Last Updated:** 2026-09-01

---

# Current Phase

**Phase 0 — Project Definition & Preparation**

Status: NOT STARTED

---

# Project Overall Status

🟡 Planning

The project has not entered implementation.

---

# Completed

* [x] Project concept defined
* [x] Four-module architecture concept defined
* [x] Sample/Experiment ID identified as central integration concept
* [x] Public datasets identified as the planned data strategy
* [x] Microbiology-domain reviewer available

---

# Not Yet Completed

## Project Definition

* [ ] Final requirements
* [ ] Final scope
* [ ] Final non-goals
* [ ] User roles
* [ ] Acceptance criteria

## Dataset Strategy

* [ ] Colony-image dataset selected
* [ ] Sequence dataset selected
* [ ] Genome annotation source selected
* [ ] AMR genotype/phenotype dataset selected
* [ ] Dataset licenses/access conditions documented

## Architecture

* [ ] Final system architecture
* [ ] Database schema
* [ ] API contracts
* [ ] Frontend architecture
* [ ] File-storage strategy
* [ ] Background-processing strategy

## Development Environment

* [ ] Python environment
* [ ] Node.js environment
* [ ] Git
* [ ] GitHub repository
* [ ] PostgreSQL
* [ ] Antigravity project instructions
* [ ] Environment variables

## Implementation

* [ ] FastAPI foundation
* [ ] React foundation
* [ ] Database foundation
* [ ] Module 2
* [ ] Module 3
* [ ] Module 1
* [ ] Module 4
* [ ] Integration
* [ ] Testing
* [ ] Deployment

---

# Current Architecture

Frontend:

React

Backend:

FastAPI

Database:

PostgreSQL

Bioinformatics:

Biopython

Computer Vision:

OpenCV + optional deep-learning model

Machine Learning:

Scikit-learn + XGBoost

Architecture style:

Modular monolith initially.

---

# Central Integration Rule

**Sample ID / Experiment ID is the central integration key.**

Modules must not become independent systems with unrelated identifiers.

---

# Important Project Rules

1. Original biological files must never be silently overwritten.
2. Public data must not be represented as laboratory-generated data.
3. Synthetic/test data must be clearly identified.
4. ML performance must never be fabricated.
5. Clinical claims must not be made.
6. Raw and processed data must remain distinguishable.
7. Major architecture changes require an explicit decision.
8. Existing working code must not be rewritten unnecessarily.
9. Antigravity must inspect existing files before modifying them.
10. Relevant tests must be run after implementation changes.

---

# Current Blockers

None.

---

# Current Risks

1. No laboratory-generated data.
2. Dataset selection has not been finalized.
3. Module 4 requires a valid genomic + resistance phenotype dataset.
4. Module 3 requires genomic annotation/feature data.
5. Module 1 anomaly detection requires appropriate labeled data if advanced claims are made.

---

# Current Task

Determine:

1. Final project scope
2. Dataset requirements
3. Development environment
4. Initial repository structure
5. Architecture decisions

No module implementation should begin until these foundations are sufficiently defined.

---

# Next Task

Complete Phase 0 requirements and dataset strategy.

---

# Last Completed Development Task

None.

---

# Last Antigravity Task

None.

---

# Known Issues

None.

---

# Notes for AI Coding Agents

Before modifying the project:

1. Read this file.
2. Read PROJECT_SPECIFICATION.md.
3. Read ARCHITECTURE.md if it exists.
4. Read DECISIONS.md.
5. Inspect the actual repository.
6. Determine whether the requested change conflicts with existing decisions.
7. Make only the changes required for the current task.
8. Run relevant tests.
9. Update this file with the actual result.

Never mark a task complete merely because code was generated.

A task is complete only after verification.

---

# Status Legend

🟢 Complete

🟡 In progress

⚪ Not started

🔴 Blocked

---

# Change Log

## 2026-09-01

Initial project state created.
