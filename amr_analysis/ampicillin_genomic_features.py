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
    COUNT(DISTINCT BioSample_ID) AS samples
FROM read_parquet('{URL}')

WHERE
    lower(species) = 'escherichia coli'
    AND lower(antibiotic_name) = 'ampicillin'
    AND lower(resistance_phenotype) IN (
        'resistant',
        'susceptible'
    )

GROUP BY
    amr_element_symbol,
    gene_symbol,
    element_type,
    element_subtype,
    class,
    subclass

ORDER BY samples DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()