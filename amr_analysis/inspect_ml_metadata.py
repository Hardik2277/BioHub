import duckdb

URL = "https://ftp.ebi.ac.uk/pub/databases/amr_portal/releases/2026-07/phenotype_genotype_merged.parquet"

con = duckdb.connect()

query = f"""
SELECT
    COUNT(DISTINCT BioSample_ID) AS biosamples,
    COUNT(DISTINCT assembly_ID) AS assemblies,
    COUNT(DISTINCT isolate) AS isolates,
    COUNT(DISTINCT taxon_id) AS taxon_ids,
    COUNT(DISTINCT organism) AS organisms,
    COUNT(DISTINCT genus) AS genera,
    COUNT(DISTINCT species) AS species
FROM read_parquet('{URL}')
WHERE lower(species) = 'escherichia coli'
  AND lower(antibiotic_name) = 'ampicillin'
  AND lower(trim(resistance_phenotype))
      IN ('resistant', 'susceptible')
  AND assembly_ID IS NOT NULL;
"""

result = con.execute(query).fetchdf()

print("=== ML SUBSET METADATA ===")
print(result.to_string(index=False))

print("\n=== POSSIBLE GROUPING VARIABLES ===")

query2 = f"""
SELECT
    COUNT(DISTINCT BioSample_ID) AS biosamples,
    COUNT(DISTINCT assembly_ID) AS assemblies,
    COUNT(DISTINCT isolate) AS isolates,
    COUNT(DISTINCT SRA_accession) AS SRA_records
FROM read_parquet('{URL}')
WHERE lower(species) = 'escherichia coli'
  AND lower(antibiotic_name) = 'ampicillin'
  AND lower(trim(resistance_phenotype))
      IN ('resistant', 'susceptible')
  AND assembly_ID IS NOT NULL;
"""

result2 = con.execute(query2).fetchdf()

print(result2.to_string(index=False))

query3 = f"""
SELECT
    isolate,
    COUNT(DISTINCT assembly_ID) AS assembly_count,
    COUNT(DISTINCT BioSample_ID) AS biosample_count,
    COUNT(DISTINCT lower(trim(resistance_phenotype))) AS phenotype_count
FROM read_parquet('{URL}')
WHERE lower(species) = 'escherichia coli'
  AND lower(antibiotic_name) = 'ampicillin'
  AND lower(trim(resistance_phenotype))
      IN ('resistant', 'susceptible')
  AND assembly_ID IS NOT NULL
  AND isolate IS NOT NULL
  AND trim(isolate) != ''
GROUP BY isolate
HAVING COUNT(DISTINCT assembly_ID) > 1
ORDER BY assembly_count DESC;
"""

result3 = con.execute(query3).fetchdf()

print("\n=== REPEATED ISOLATE IDENTIFIERS ===")
print(result3.to_string(index=False))

result3.to_csv(
    "ecoli_ampicillin_repeated_isolates.csv",
    index=False
)

print(
    f"\nRepeated isolate identifiers found: {len(result3)}"
)

result2 = con.execute(query2).fetchdf()

print(result2.to_string(index=False))

con.close()