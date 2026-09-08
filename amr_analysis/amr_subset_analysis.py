import duckdb

URL = "https://ftp.ebi.ac.uk/pub/databases/amr_portal/releases/2026-07/phenotype_genotype_merged.parquet"

con = duckdb.connect("amr_analysis.duckdb")

query = f"""
SELECT
    species,
    antibiotic_name,
    resistance_phenotype,

    COUNT(*) AS records,

    COUNT(DISTINCT BioSample_ID) AS samples,

    COUNT(DISTINCT assembly_ID) AS assemblies,

    COUNT(DISTINCT CASE
        WHEN assembly_ID IS NOT NULL
        AND assembly_ID != ''
        THEN BioSample_ID
    END) AS samples_with_assembly

FROM read_parquet('{URL}')

WHERE
    lower(species) IN (
        'escherichia coli',
        'staphylococcus aureus',
        'klebsiella pneumoniae'
    )

    AND lower(resistance_phenotype) IN (
        'resistant',
        'susceptible'
    )

GROUP BY
    species,
    antibiotic_name,
    resistance_phenotype

ORDER BY
    species,
    antibiotic_name,
    resistance_phenotype;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

result.to_csv("amr_genotype_availability.csv", index=False)

print("\nSaved to amr_genotype_availability.csv")

con.close()