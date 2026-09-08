import duckdb

URL = "https://ftp.ebi.ac.uk/pub/databases/amr_portal/releases/2026-07/phenotype_genotype_merged.parquet"

con = duckdb.connect()

query = f"""
WITH target_samples AS (

    SELECT DISTINCT
        BioSample_ID,
        assembly_ID,
        resistance_phenotype

    FROM read_parquet('{URL}')

    WHERE
        lower(species) = 'escherichia coli'
        AND lower(antibiotic_name) = 'ampicillin'
        AND lower(resistance_phenotype) IN (
            'resistant',
            'susceptible'
        )
        AND assembly_ID IS NOT NULL
)

SELECT
    t.resistance_phenotype,

    g.amr_element_symbol,
    g.gene_symbol,
    g.element_type,
    g.element_subtype,
    g.class,
    g.subclass,

    COUNT(DISTINCT t.BioSample_ID) AS samples

FROM target_samples t

JOIN read_parquet('{URL}') g
    ON t.assembly_ID = g.assembly_ID

WHERE
    g.amr_element_symbol IS NOT NULL
    AND TRIM(g.amr_element_symbol) != ''

GROUP BY
    t.resistance_phenotype,
    g.amr_element_symbol,
    g.gene_symbol,
    g.element_type,
    g.element_subtype,
    g.class,
    g.subclass

ORDER BY
    samples DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

result.to_csv(
    "ecoli_ampicillin_all_genome_features.csv",
    index=False
)

print("\nSaved to ecoli_ampicillin_all_genome_features.csv")

con.close()