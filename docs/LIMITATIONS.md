# BioHub — Limitations

**Last Updated:** 2026-09-01

This document records known limitations, assumptions, and boundaries of the BioHub project.

---

# 1. Research Prototype

BioHub is an academic/research prototype.

It is not a clinically validated laboratory information system.

---

# 2. No Direct Laboratory Data

The project currently does not have direct laboratory access.

Development and evaluation will therefore rely primarily on:

* Public research datasets
* Openly available biological data
* Controlled test data
* Synthetic data where appropriate

Public data must not be represented as laboratory-generated data.

---

# 3. Colony Analysis Limitations

Colony-counting performance depends on:

* Image quality
* Lighting
* Plate background
* Colony density
* Colony overlap
* Colony morphology
* Dataset characteristics

Performance on public datasets may not generalize to every laboratory imaging setup.

---

# 4. Visual Anomaly Detection

Visual anomaly detection is not equivalent to laboratory-confirmed contamination identification.

Any contamination-related functionality requires suitable labeled data and validation.

The system should therefore describe such results as visual anomalies unless stronger validation exists.

---

# 5. Biological File Processing

FASTA and FASTQ files contain different types of information.

FASTQ includes sequencing quality information that must not be discarded accidentally.

Normalization into JSON may require careful schema design to avoid unnecessary information loss.

---

# 6. Genomic Visualization

A raw sequence does not automatically contain complete gene annotations.

Interactive feature visualization therefore depends on suitable annotation data.

The visualization is a computational representation and does not itself establish biological function.

---

# 7. Resistance Prediction

Resistance prediction depends heavily on:

* Dataset quality
* Organism selection
* Antibiotic selection
* Phenotype labeling
* Genomic feature representation
* Dataset bias
* Population structure
* Class imbalance
* Data leakage
* Model assumptions

A high test score does not automatically imply clinical usefulness.

---

# 8. Public Dataset Bias

Public research datasets may not represent:

* All bacterial populations
* All geographic regions
* All laboratory conditions
* All sequencing technologies
* All resistance mechanisms

Therefore model generalization must be discussed carefully.

---

# 9. No Clinical Use

BioHub predictions must not be used as:

* Clinical diagnoses
* Patient treatment recommendations
* Definitive antimicrobial susceptibility results

The resistance module is a research prediction system.

---

# 10. No Clinical Validation

Unless future work introduces appropriate validation, BioHub will not claim:

* Clinical validation
* Diagnostic accuracy
* Clinical deployment readiness
* Regulatory approval

---

# 11. Dataset Availability

Public datasets may change:

* URLs
* versions
* access requirements
* licenses
* file formats

Dataset provenance must therefore be documented.

---

# 12. Computational Limitations

Large genomic files can require significant:

* RAM
* CPU
* Storage
* Processing time

The system may require streaming, chunk processing, or background jobs for larger workloads.

---

# 13. ML Limitations

Machine-learning predictions can be affected by:

* Training-data bias
* Class imbalance
* Overfitting
* Feature leakage
* Population structure
* Distribution shift

Model performance must therefore be evaluated using appropriate experimental methodology.

---

# 14. Domain Review

A microbiology-domain friend may provide general feedback on:

* Terminology
* Workflow assumptions
* Biological interpretation

This does not constitute formal laboratory validation or clinical validation.

---

# 15. Current Unknowns

The following remain unresolved:

* Final colony-image dataset
* Final genomic dataset
* Final AMR dataset
* Target organism
* Target antibiotics
* Exact ML feature representation
* Exact anomaly-detection scope
* Final deployment environment

These must be resolved before the relevant modules are implemented.

---

# 16. Limitation Management Rule

When a new limitation is discovered:

1. Document it here.
2. Determine whether the architecture must change.
3. Update PROJECT_STATE.md.
4. Record major architectural decisions in DECISIONS.md.
5. Do not hide limitations merely to make the project appear stronger.
