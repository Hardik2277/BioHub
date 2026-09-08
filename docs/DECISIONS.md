# BioHub — Architecture & Engineering Decisions

**Last Updated:** 2026-09-01

This document records important project decisions.

Decisions should not be silently changed.

If a decision changes, record the new decision and explain why.

---

# Decision Status

* PROPOSED
* ACCEPTED
* REJECTED
* SUPERSEDED

---

# ADR-001 — Initial Backend Framework

**Status:** ACCEPTED

**Decision:**

Use Python + FastAPI for the initial backend.

**Reason:**

FastAPI fits the project's Python-centric architecture and integrates naturally with:

* Bioinformatics libraries
* Computer vision
* Machine learning
* Pydantic validation

---

# ADR-002 — Initial Frontend Framework

**Status:** ACCEPTED

**Decision:**

Use React for the frontend.

**Reason:**

The project requires an interactive dashboard and genomic visualization.

React provides a suitable component-based frontend architecture.

---

# ADR-003 — Initial Database

**Status:** ACCEPTED

**Decision:**

Use PostgreSQL.

**Reason:**

BioHub contains strongly related entities and requires relational integrity around Sample/Experiment relationships.

---

# ADR-004 — Architecture Style

**Status:** ACCEPTED

**Decision:**

Start with a modular monolith.

**Reason:**

BioHub is a final-year project.

Microservices would introduce additional operational complexity without an established requirement.

---

# ADR-005 — Central Integration Identifier

**Status:** ACCEPTED

**Decision:**

Use Sample ID / Experiment ID as the central integration mechanism.

**Reason:**

Different modules must be able to associate their data and results with the same biological sample.

---

# ADR-006 — Raw Biological Files

**Status:** ACCEPTED

**Decision:**

Original uploaded biological files must not be silently overwritten.

**Reason:**

Raw data should remain distinguishable from processed data for reproducibility and debugging.

---

# ADR-007 — Public Dataset Strategy

**Status:** ACCEPTED

**Decision:**

Use appropriate public research datasets for development/evaluation because the project currently has no laboratory access.

**Reason:**

Public datasets allow reproducible development without falsely claiming laboratory-generated results.

---

# ADR-008 — Clinical Claims

**Status:** ACCEPTED

**Decision:**

BioHub is a research/academic prototype.

**Reason:**

The project will not have sufficient clinical validation to support medical diagnosis or treatment claims.

---

# ADR-009 — Genomic Visualization

**Status:** ACCEPTED**

**Decision:**

The primary visualization will be an interactive 2D circular genomic/plasmid feature map.

**Reason:**

A circular representation is appropriate for suitable plasmid/genomic feature data.

Raw sequence alone is not assumed to contain complete annotation.

---

# ADR-010 — ML Prediction Terminology

**Status:** ACCEPTED

**Decision:**

Use:

**Research Prediction / Resistance Risk Indicator**

rather than presenting predictions as clinical diagnoses.

---

# ADR-011 — Machine Learning Model

**Status:** PROPOSED

**Decision:**

Evaluate Scikit-learn baseline models and XGBoost.

**Reason:**

XGBoost is a strong candidate for tabular genomic features, but the final model must be selected based on actual dataset characteristics and evaluation.

---

# ADR-012 — Computer Vision Approach

**Status:** PROPOSED**

**Decision:**

Begin with a traditional OpenCV baseline before introducing a deep-learning segmentation model.

**Reason:**

This provides a measurable baseline and avoids unnecessary model complexity.

A deep-learning model may be introduced if the baseline cannot adequately handle the target images.

---

# ADR-013 — Background Processing

**Status:** PROPOSED

**Decision:**

Do not introduce a job queue immediately.

Introduce background processing if biological-file processing, image analysis, or ML workloads demonstrate a need.

---

# Pending Decisions

The following are not finalized:

* Exact public datasets
* Target bacterial organism(s)
* Target antibiotics
* ML prediction target
* Exact genomic features
* Exact database schema
* Authentication implementation
* File storage technology
* Background-job framework
* Frontend state-management approach
* Deployment platform
* Exact deep-learning model
* Exact visualization library

---

# Decision Change Rule

If a major decision changes:

1. Do not silently overwrite the previous decision.
2. Add a new ADR.
3. Explain the previous decision.
4. Explain why the new decision is better.
5. Update PROJECT_STATE.md.
6. Update ARCHITECTURE.md if required.
