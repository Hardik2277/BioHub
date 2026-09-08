import duckdb

URL = "https://ftp.ebi.ac.uk/pub/databases/amr_portal/releases/2026-07/phenotype_genotype_merged.parquet"

con = duckdb.connect()

query = f"""
SELECT
    amr_element_symbol,
    gene_symbol,
    element_type,
    element_subtype,
    class,
    subclass,

    COUNT(DISTINCT BioSample_ID) AS total_samples,

    COUNT(DISTINCT CASE
        WHEN lower(resistance_phenotype) = 'resistant'
        THEN BioSample_ID
    END) AS resistant_samples,

    COUNT(DISTINCT CASE
        WHEN lower(resistance_phenotype) = 'susceptible'
        THEN BioSample_ID
    END) AS susceptible_samples

FROM read_parquet('{URL}')

WHERE
    lower(species) = 'escherichia coli'
    AND lower(antibiotic_name) = 'ampicillin'
    AND lower(resistance_phenotype) IN (
        'resistant',
        'susceptible'
    )
    AND amr_element_symbol IS NOT NULL
    AND TRIM(amr_element_symbol) != ''

GROUP BY
    amr_element_symbol,
    gene_symbol,
    element_type,
    element_subtype,
    class,
    subclass

ORDER BY
    total_samples DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

result.to_csv(
    "all_ampicillin_features.csv",
    index=False
)

print("\nSaved to all_ampicillin_features.csv")

con.close()