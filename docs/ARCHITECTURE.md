# BioHub — System Architecture

**Status:** Draft
**Last Updated:** 2026-09-01

---

# 1. Architecture Goal

BioHub should provide a unified computational workflow connecting microbial image analysis, genomic data processing, genomic visualization, and resistance prediction.

The architecture must prioritize:

* Simplicity
* Maintainability
* Clear module boundaries
* Data integrity
* Reproducibility
* Security
* Testability

---

# 2. Initial Architecture Style

BioHub will initially use a:

**Modular Monolith**

The backend will be one FastAPI application containing logically separated services/modules.

Microservices will not be introduced unless a measurable requirement justifies them.

---

# 3. High-Level Architecture

```text
                    ┌───────────────────────┐
                    │    React Frontend     │
                    │      Web UI           │
                    └───────────┬───────────┘
                                │
                             HTTP/API
                                │
                    ┌───────────▼───────────┐
                    │    FastAPI Backend     │
                    │                       │
                    │ ┌───────────────────┐ │
                    │ │ Sample Management  │ │
                    │ ├───────────────────┤ │
                    │ │ BioConverter       │ │
                    │ ├───────────────────┤ │
                    │ │ Colony Analytics   │ │
                    │ ├───────────────────┤ │
                    │ │ Visualization API  │ │
                    │ ├───────────────────┤ │
                    │ │ ML Prediction      │ │
                    │ └───────────────────┘ │
                    └───────────┬───────────┘
                                │
                ┌───────────────┼────────────────┐
                │               │                │
                ▼               ▼                ▼
        ┌────────────┐  ┌──────────────┐  ┌──────────────┐
        │ PostgreSQL │  │ File Storage  │  │ ML / Compute │
        │            │  │              │  │ Components   │
        └────────────┘  └──────────────┘  └──────────────┘
```

---

# 4. Central Entity

The central entity is:

**Sample**

A Sample may belong to an Experiment.

Every module must be capable of associating its output with a Sample ID.

---

# 5. Logical Data Flow

```text
                    SAMPLE
                      │
          ┌───────────┼────────────┐
          │           │            │
          ▼           ▼            ▼
       IMAGE       SEQUENCE      METADATA
          │           │
          ▼           ▼
     Module 1      Module 2
     Colony        BioConverter
     Analytics         │
          │             ▼
          │       Genomic Features
          │          /         \
          │         /           \
          │        ▼             ▼
          │   Module 3       Module 4
          │   Visualizer      ML Engine
          │        │             │
          └────────┴─────────────┘
                   │
                   ▼
             Sample Dashboard
```

---

# 6. Backend Logical Structure

The backend should eventually separate responsibilities approximately as follows:

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── modules/
│   │   ├── bioconverter/
│   │   ├── colony_analytics/
│   │   ├── visualizer/
│   │   └── resistance_ml/
│   └── utils/
└── tests/
```

This structure is a proposal and must be reviewed before implementation.

---

# 7. Frontend Logical Structure

Potential structure:

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── services/
│   ├── hooks/
│   ├── state/
│   ├── features/
│   │   ├── samples/
│   │   ├── bioconverter/
│   │   ├── colony-analytics/
│   │   ├── visualizer/
│   │   └── resistance/
│   └── utils/
└── tests/
```

Final structure will depend on the chosen frontend architecture.

---

# 8. Module Boundaries

## Module 1

Responsible for:

* Image processing
* Colony detection
* Colony counting
* Visual anomaly analysis

It should not directly manipulate unrelated database entities.

---

## Module 2

Responsible for:

* Biological file ingestion
* Parsing
* Validation
* Normalization
* Processing metadata

It must preserve the original uploaded file.

---

## Module 3

Responsible for:

* Genomic feature retrieval
* Visualization transformation
* Interactive display support

It should not perform unrelated ML processing.

---

## Module 4

Responsible for:

* Feature extraction
* Model loading
* Prediction
* Evaluation
* Prediction metadata

It should not silently retrain models during normal prediction requests.

---

# 9. Sample Lifecycle

Conceptual lifecycle:

```text
Created
   ↓
Data Uploaded
   ↓
Processing
   ↓
Analysis Available
   ↓
Results Available
   ↓
Archived
```

Exact statuses will be finalized during database design.

---

# 10. Raw vs Processed Data

The architecture must distinguish:

```text
RAW DATA
   ↓
PROCESSING
   ↓
PROCESSED DATA
```

Original data must remain recoverable unless the project's storage policy explicitly states otherwise.

---

# 11. Computational Processing

Small operations may execute directly through API services.

Potentially expensive operations may use background processing:

```text
Frontend
   ↓
FastAPI
   ↓
Create Processing Job
   ↓
Background Worker
   ↓
Processing
   ↓
Store Result
   ↓
Frontend retrieves status/result
```

A job queue will only be introduced if processing requirements justify it.

---

# 12. Database

PostgreSQL is the initial database choice.

Potential entities:

* User
* Sample
* Experiment
* CultureImage
* ImageAnalysis
* SequenceFile
* ProcessingRun
* GenomicFeature
* ResistancePrediction

The exact schema is not finalized.

---

# 13. API Layer

The frontend must communicate with the backend through defined API contracts.

Potential groups:

```text
/api/samples
/api/images
/api/sequences
/api/processing
/api/genomic-features
/api/predictions
```

Exact endpoints must be finalized in API_CONTRACTS.md before implementation of dependent frontend features.

---

# 14. Security Architecture

The system should consider:

* Authentication
* Authorization
* Secure password handling
* Input validation
* File validation
* File-size restrictions
* Safe file paths
* CORS
* Secrets management
* Database security
* Error handling
* Logging

---

# 15. Deployment Concept

Initial development:

```text
Local Machine
├── React
├── FastAPI
├── PostgreSQL
└── Local File Storage
```

Later:

```text
Docker
├── Frontend
├── Backend
├── Database
└── Supporting Services
```

Cloud deployment is future work unless required.

---

# 16. Architecture Principles

1. Keep modules loosely coupled.
2. Use Sample ID as the integration key.
3. Do not duplicate business logic.
4. Keep raw data separate from processed data.
5. Define API contracts explicitly.
6. Validate data at system boundaries.
7. Avoid unnecessary infrastructure.
8. Test modules independently.
9. Document architectural changes.
10. Prefer measurable engineering decisions.

---

# 17. Current Architecture Status

Status:

**DRAFT**

The architecture must be reviewed before implementation begins.

Open decisions:

* Exact database schema
* File storage strategy
* Authentication strategy
* Background processing
* API contract
* Frontend state management
* Dataset architecture
* ML model-serving architecture
