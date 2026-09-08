import duckdb

URL = "https://ftp.ebi.ac.uk/pub/databases/amr_portal/releases/2026-07/phenotype_genotype_merged.parquet"

con = duckdb.connect()

query = f"""
DESCRIBE
SELECT *
FROM read_parquet('{URL}')
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

result.to_csv("cabbage_schema.csv", index=False)

print("\nSaved to cabbage_schema.csv")

con.close()