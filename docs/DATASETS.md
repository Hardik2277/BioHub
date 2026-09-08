# BioHub — Dataset Registry

**Last Updated:** 2026-09-01

---

# Purpose

This document records all external datasets used or evaluated by BioHub.

Every dataset must be verified before being used.

Do not record estimated values as confirmed facts.

Do not represent public datasets as laboratory-generated data.

---

# Dataset Selection Rules

Before using a dataset, verify:

* Official source
* Dataset availability
* Dataset purpose
* Organism/species
* Number of samples/images
* File formats
* Labels
* Metadata
* License/access conditions
* Download size
* Data quality
* Suitability for the intended module
* Known limitations

---

# Module 1 — Colony Image Dataset

## Status

NOT SELECTED

## Required Characteristics

The dataset should ideally contain:

* Microbial culture-plate images
* Colony annotations or reliable colony counts
* Sufficient variation in image conditions
* Appropriate usage rights

## Intended Use

* Colony detection
* Colony counting
* Evaluation
* Potential anomaly-analysis research

## Dataset

To be selected after current web research.

## Official Source

Not selected.

## License

Not selected.

## Organism

Not selected.

## Image Count

Not selected.

## Annotation Type

Not selected.

## Limitations

To be documented after dataset selection.

---

# Module 2 — Sequence Dataset

## Status

NOT SELECTED

## Required Characteristics

Potential formats:

* FASTA
* FASTQ
* CSV metadata

The dataset should allow testing of:

* Parsing
* Validation
* Metadata extraction
* Quality information
* Normalization

## Potential Sources

Public research repositories such as NCBI may be investigated.

## Dataset

To be selected after current web research.

## Official Source

Not selected.

## License/Access

Not selected.

## File Size

Not selected.

## Processing Requirements

Not selected.

---

# Module 3 — Genome + Annotation Dataset

## Status

NOT SELECTED

## Required Characteristics

The dataset should contain suitable:

* Genome sequence
* Genomic features
* Gene annotations
* Coordinates
* Strand information where available

Potential formats may include:

* FASTA
* GFF3
* GenBank/GBFF
* Other verified annotation formats

## Potential Sources

Public genome repositories such as NCBI may be investigated.

## Dataset

To be selected after current web research.

## Official Source

Not selected.

## License/Access

Not selected.

## Annotation Type

Not selected.

---

# Module 4 — AMR Dataset

## Status

NOT SELECTED

## Critical Requirement

The dataset must provide a scientifically appropriate relationship between genomic information and observed antimicrobial resistance phenotype.

Required concepts may include:

* Genome/sample identifier
* Organism
* Antibiotic
* Resistance/susceptibility phenotype
* Genomic information or features

## Potential Sources

Public AMR research resources may be investigated, including resources from established biological databases.

## Dataset

To be selected after current web research.

## Official Source

Not selected.

## Organism

Not selected.

## Antibiotics

Not selected.

## Labels

Not selected.

## License/Access

Not selected.

## Limitations

Not selected.

---

# Dataset Provenance

For every selected dataset, record:

```text
Dataset Name:
Official Source:
URL:
Access Date:
Version:
License:
Organism:
Number of Samples:
File Formats:
Labels:
Metadata:
BioHub Module:
Processing:
Train/Test Use:
Known Limitations:
```

---

# Dataset Integrity Rules

1. Never modify raw downloaded datasets in place.
2. Preserve source/version information.
3. Keep preprocessing reproducible.
4. Record transformations.
5. Do not commit large datasets to Git unless explicitly justified.
6. Do not commit restricted/private data.
7. Respect dataset licenses.
8. Do not claim ownership of third-party datasets.
9. Clearly distinguish training, validation, and test data.
10. Prevent data leakage during ML evaluation.

---

# Current Dataset Status

No datasets have been selected yet.

Dataset research is a Phase 0 task.
