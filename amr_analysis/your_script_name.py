import duckdb

URL = "https://ftp.ebi.ac.uk/pub/databases/amr_portal/releases/2026-07/phenotype_genotype_merged.parquet"

con = duckdb.connect()

query = f"""
WITH target AS (
    SELECT DISTINCT
        assembly_ID,
        CASE
            WHEN lower(trim(resistance_phenotype)) = 'resistant' THEN 1
            WHEN lower(trim(resistance_phenotype)) = 'susceptible' THEN 0
        END AS target
    FROM read_parquet('{URL}')
    WHERE lower(species) = 'escherichia coli'
      AND lower(antibiotic_name) = 'ampicillin'
      AND lower(trim(resistance_phenotype)) IN ('resistant', 'susceptible')
      AND assembly_ID IS NOT NULL
),

features AS (
    SELECT DISTINCT
        assembly_ID,
        amr_element_symbol
    FROM read_parquet('{URL}')
    WHERE assembly_ID IS NOT NULL
      AND amr_element_symbol IS NOT NULL
      AND trim(amr_element_symbol) != ''
)

SELECT
    f.amr_element_symbol AS feature,
    COUNT(DISTINCT f.assembly_ID) AS total_samples,

    COUNT(DISTINCT CASE
        WHEN t.target = 1 THEN f.assembly_ID
    END) AS resistant_samples,

    COUNT(DISTINCT CASE
        WHEN t.target = 0 THEN f.assembly_ID
    END) AS susceptible_samples,

    ROUND(
        100.0 * COUNT(DISTINCT f.assembly_ID)
        / (SELECT COUNT(*) FROM target),
        2
    ) AS prevalence_percent,

    ROUND(
        100.0 *
        COUNT(DISTINCT CASE
            WHEN t.target = 1 THEN f.assembly_ID
        END)
        /
        NULLIF(COUNT(DISTINCT f.assembly_ID), 0),
        2
    ) AS resistant_rate_percent

FROM features f
INNER JOIN target t
    ON f.assembly_ID = t.assembly_ID

GROUP BY f.amr_element_symbol

ORDER BY total_samples DESC;
"""

result = con.execute(query).fetchdf()

print("\n=== ALL GENOMIC FEATURES ===\n")
print(result.to_string(index=False))

result.to_csv(
    "ecoli_ampicillin_feature_prevalence.csv",
    index=False
)

print("\nSaved to:")
print("ecoli_ampicillin_feature_prevalence.csv")

con.close()