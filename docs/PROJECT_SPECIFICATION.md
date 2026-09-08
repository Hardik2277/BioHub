# BioHub — Project Specification

**Project Title:**
BioHub: An End-to-End Automated Platform for Microbial Image Analytics, Genomic Data Pipelines, and Resistance Phenotype Prediction

**Project Type:**
Final-Year Engineering Project / Academic Research Prototype

**Status:**
Planning / Phase 0

**Last Updated:** 2026-09-01

---

## 1. Project Overview

BioHub is a full-stack, research-oriented digital platform designed to demonstrate an integrated computational workflow for microbiology-related data.

The platform connects four computational modules:

1. Automated microbial colony image analytics
2. Biological sequence-file ingestion and normalization
3. Interactive genomic feature visualization
4. Machine-learning-based antimicrobial resistance phenotype prediction

The modules are connected through a centralized Sample/Experiment identity so that different types of data belonging to the same experimental sample can be related inside one system.

BioHub is intended as an academic/research prototype and is not a clinically validated diagnostic or treatment system.

---

# 2. Problem Statement

Microbiology workflows can involve multiple disconnected data types, including culture-plate images, genomic sequence files, genomic annotations, and antimicrobial resistance information.

These data often require different software tools and technical workflows.

BioHub aims to demonstrate how these computational tasks can be integrated into a single web-based workspace.

The system will provide:

* Automated image analysis
* Biological data ingestion and processing
* Genomic feature visualization
* Research-oriented resistance prediction

---

# 3. Project Objectives

## Primary Objectives

* Build a unified web-based microbiology research workspace.
* Establish a central Sample/Experiment data model.
* Automate microbial colony image analysis.
* Develop a biological sequence-file ingestion and normalization pipeline.
* Visualize genomic/plasmid features interactively.
* Develop and evaluate an ML model for antimicrobial resistance phenotype prediction.
* Provide a unified dashboard for viewing results associated with a sample.
* Evaluate each module using measurable technical metrics.

## Secondary Objectives

* Demonstrate modern full-stack engineering practices.
* Apply computer vision to biological image analysis.
* Apply bioinformatics processing techniques to genomic data.
* Apply machine learning to genotype-to-phenotype prediction.
* Maintain reproducible data-processing workflows.
* Document limitations and assumptions clearly.

---

# 4. Scope

## In Scope

### Module 1 — Colony Analytics

* Culture-plate image upload
* Image preprocessing
* Colony detection/segmentation
* Colony counting
* Visual anomaly flagging
* Analysis-result storage
* Evaluation against appropriate labeled public data

### Module 2 — BioConverter

* FASTA ingestion
* FASTQ ingestion
* CSV/metadata ingestion where appropriate
* File validation
* Sequence parsing
* Metadata extraction
* Quality processing where applicable
* Normalization into structured biological data
* Processing-status tracking
* Preservation of original uploaded files

### Module 3 — Genomic Feature Visualizer

* Genomic feature data retrieval
* Interactive 2D circular visualization
* Feature hover/details
* Gene/ORF location display where annotations are available
* Zoom/pan/interaction
* Integration with Sample/Experiment records

### Module 4 — Resistance Prediction

* Public genomic/phenotypic dataset selection
* Genomic feature extraction
* Baseline machine-learning model
* XGBoost model where justified
* Model evaluation
* Resistance-risk/prediction display
* Model-version tracking
* Integration with Sample/Experiment records

---

# 5. Out of Scope

The following are NOT project objectives:

* Clinical diagnosis
* Clinical treatment recommendations
* Autonomous laboratory equipment control
* Real-time clinical decision-making
* Replacement of microbiologists or laboratory technicians
* Claiming medical-grade contamination detection
* Claiming clinically validated antimicrobial resistance prediction
* Generating laboratory results without appropriate evidence
* Pretending public/synthetic data are laboratory-generated data

---

# 6. Target Users

Potential users of the prototype include:

* Microbiology researchers
* Laboratory technicians
* Bioinformatics students/researchers
* Academic researchers
* Students demonstrating computational biology workflows

The exact user-role model will be finalized during architecture design.

---

# 7. System Architecture

Initial architecture:

React Frontend
↓
FastAPI Backend
↓
Application/Service Layer
↓
PostgreSQL Database
+
File Storage

Computational processing may use background workers when required.

The project will initially follow a modular-monolith architecture.

Microservices will not be introduced unless a clear technical requirement is demonstrated.

---

# 8. Central Integration Concept

The central integration key is:

**Sample ID / Experiment ID**

A sample can contain:

* Sample metadata
* Culture images
* Image-analysis results
* Sequence files
* Processing runs
* Genomic features
* Visualization data
* Resistance predictions

Conceptual relationship:

User
↓
Sample
├── Culture Image
│      └── Image Analysis
│
├── Sequence File
│      └── Processing Run
│             └── Genomic Features
│
├── Visualization Data
│
└── Resistance Prediction

---

# 9. Module 1 Specification

## Name

Automated Colony Counting & Visual Anomaly Detection

## Input

Culture-plate images.

## Potential Processing

* Image validation
* Resizing where appropriate
* Contrast adjustment
* Noise reduction
* Thresholding
* Edge/contour analysis
* Blob detection
* Segmentation

A lightweight deep-learning segmentation/detection model may be evaluated if traditional computer vision is insufficient.

## Output

* Colony count
* Colony locations
* Segmentation/detection information
* Confidence information where available
* Visual anomaly flags

## Important Limitation

Visual anomaly detection must not automatically be described as medically validated contamination detection.

Any contamination-related claim requires suitable labeled data and validation.

---

# 10. Module 2 Specification

## Name

BioConverter — Biological Data Ingestion & Normalization Pipeline

## Inputs

Potentially:

* FASTA
* FASTQ
* CSV
* Biological metadata
* Other justified biological file formats

## Processing

* File validation
* Format identification
* Parsing
* Sequence validation
* Metadata extraction
* Quality processing where applicable
* Normalization
* Structured representation

Biopython will be evaluated as the primary biological parsing library.

## Data Preservation

Original uploaded files must not be silently overwritten.

Raw and processed data must remain distinguishable.

FASTQ quality information must not be discarded without explicit justification.

---

# 11. Module 3 Specification

## Name

Interactive Genomic Feature Visualizer

## Input

Normalized genomic feature/annotation data.

## Output

Interactive 2D circular genomic/plasmid visualization.

Potential functionality:

* Zoom
* Pan
* Hover
* Feature selection
* Gene information
* ORF information
* Start/end coordinates
* Strand
* Feature type
* Annotation/product information

Potential technologies:

* React
* D3.js
* BioJS or another suitable library

## Important Scientific Constraint

A raw FASTA sequence does not automatically provide complete genomic annotations.

The project must explicitly define how genomic features/annotations are obtained.

---

# 12. Module 4 Specification

## Name

Machine Learning Predictive Resistance Engine

## Objective

Estimate antimicrobial resistance phenotype from genomic information using supervised machine learning.

## Input

Genomic information and appropriate genomic features.

Potential features include:

* k-mer representations
* SNPs
* mutations
* resistance-associated genomic features
* Other scientifically justified features

## Models

Potential models:

* Scikit-learn baseline models
* XGBoost

Model selection must be supported by experimental evaluation rather than assumption.

## Required Training Relationship

Training data must contain an appropriate relationship between:

Genomic Information
+
Antibiotic
+
Observed Resistance Phenotype

## Output

The system should use terminology such as:

**Research Prediction / Resistance Risk Indicator**

The result must not be presented as a clinical diagnosis or treatment recommendation.

---

# 13. Dataset Strategy

Because BioHub currently has no laboratory access, development and evaluation will primarily use appropriate public research datasets.

Potential dataset sources will be investigated and verified before implementation.

Possible sources include:

* Public microbial colony-image datasets
* NCBI genomic datasets
* NCBI Sequence Read Archive
* Public antimicrobial-resistance genotype/phenotype datasets
* Other reputable research repositories

For every selected dataset, the project will document:

* Source
* License/access conditions
* Organism
* File format
* Number of samples/images
* Labels
* Metadata
* Intended module
* Processing requirements
* Limitations

No public dataset will be represented as laboratory-generated data.

---

# 14. Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic
* PostgreSQL

## Bioinformatics

* Biopython

## Computer Vision

* OpenCV
* Deep-learning detection/segmentation framework if justified

## Machine Learning

* Scikit-learn
* XGBoost

## Frontend

* React
* JavaScript or TypeScript based on the final architecture
* D3.js or suitable genomic visualization technology

## Development

* Git
* GitHub
* Antigravity
* VS Code

Docker may be introduced when useful.

---

# 15. Non-Functional Requirements

## Maintainability

The codebase should use clear module boundaries and consistent naming.

## Reliability

Invalid files and invalid requests must produce controlled errors.

## Security

The system should consider:

* Authentication
* Authorization
* File validation
* File-size limits
* Safe filenames
* Path traversal protection
* Input validation
* SQL injection protection
* Secrets management
* CORS configuration

## Performance

Large biological files should not automatically be loaded entirely into memory.

Processing strategies should consider:

* Streaming
* Chunk processing
* Background jobs
* Processing status
* Temporary files
* Cleanup

## Reproducibility

Data-processing and ML experiments should be reproducible wherever practical.

---

# 16. Validation Strategy

Each module must have measurable evaluation criteria.

### Module 1

Potential metrics:

* Counting error
* Precision
* Recall
* Detection/segmentation metrics where applicable

### Module 2

Potential metrics:

* Parsing correctness
* Validation correctness
* Processing time
* Error handling

### Module 3

Potential validation:

* Correct rendering of known genomic features
* Coordinate correctness
* Interaction correctness

### Module 4

Potential metrics:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix
* ROC-AUC where appropriate

Model performance must never be fabricated.

---

# 17. Data Leakage Prevention

For resistance prediction, dataset splitting must consider:

* Duplicate samples
* Closely related isolates
* Source/site relationships
* Temporal relationships
* Feature leakage
* Antibiotic leakage

A simple random split must not automatically be assumed to produce a scientifically valid evaluation.

---

# 18. Academic Honesty

BioHub must clearly distinguish:

* Public data
* Synthetic/test data
* User-provided data
* Laboratory-generated data
* Model predictions
* Experimental measurements

No unsupported scientific claims may be made.

---

# 19. Project Status

Current status:

**Phase 0 — Planning**

No implementation has started.

Current resources:

* No codebase
* No datasets
* No laboratory-generated data
* No trained ML model
* No database
* No frontend
* No backend

Domain support:

A microbiology-domain friend is available for general workflow and terminology review.

---

# 20. Future Scope

Potential future improvements may include:

* Additional biological file formats
* More advanced image analysis
* More genomic annotation sources
* Additional bacterial species
* Additional antimicrobial classes
* Better model interpretability
* Laboratory information-system integration
* Cloud deployment
* Advanced authentication/RBAC
* Background job infrastructure
* More extensive validation

Future scope must not be presented as implemented functionality.

---

# 21. Document Status

This document is a living specification.

Changes must be recorded through the project's decision and change-management process.

Do not silently change major requirements.
