import duckdb

URL = "https://ftp.ebi.ac.uk/pub/databases/amr_portal/releases/2026-07/phenotype_genotype_merged.parquet"

OUTPUT = "ecoli_ampicillin_ml_dataset.csv"

FEATURES = [
    "marR_S3N",
    "tet(B)",
    "tet(A)",
    "soxS_A12S",
    "aac(3)-IId",
    "aph(6)-Id",
    "aph(3'')-Ib",
    "dfrA1"
]

con = duckdb.connect()

# Safely escape feature names for SQL string literals
feature_values = ", ".join(
    "'" + feature.replace("'", "''") + "'"
    for feature in FEATURES
)

query = f"""
WITH target AS (
    SELECT DISTINCT
        assembly_ID,
        CASE
            WHEN lower(trim(resistance_phenotype)) = 'resistant'
                THEN 1
            WHEN lower(trim(resistance_phenotype)) = 'susceptible'
                THEN 0
        END AS target
    FROM read_parquet('{URL}')
    WHERE lower(species) = 'escherichia coli'
      AND lower(antibiotic_name) = 'ampicillin'
      AND lower(trim(resistance_phenotype))
            IN ('resistant', 'susceptible')
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
      AND amr_element_symbol IN ({feature_values})
),

feature_matrix AS (
    SELECT
        assembly_ID,
        amr_element_symbol
    FROM features
)

SELECT
    t.assembly_ID,
    t.target,
    fm.amr_element_symbol
FROM target t
LEFT JOIN feature_matrix fm
    ON t.assembly_ID = fm.assembly_ID
ORDER BY t.assembly_ID;
"""

long_df = con.execute(query).fetchdf()

# ---------------------------------------------------------
# Build binary feature matrix in Python
# ---------------------------------------------------------

target_df = (
    long_df[["assembly_ID", "target"]]
    .drop_duplicates()
    .copy()
)

feature_df = (
    long_df
    .dropna(subset=["amr_element_symbol"])
    .assign(value=1)
    .pivot_table(
        index="assembly_ID",
        columns="amr_element_symbol",
        values="value",
        aggfunc="max",
        fill_value=0
    )
    .reset_index()
)

# Make sure every expected feature exists
for feature in FEATURES:
    if feature not in feature_df.columns:
        feature_df[feature] = 0

# Keep ONLY the required columns
feature_df = feature_df[
    ["assembly_ID"] + FEATURES
]

# ---------------------------------------------------------
# IMPORTANT:
# LEFT JOIN feature matrix onto the complete target table
# ---------------------------------------------------------

df = target_df.merge(
    feature_df,
    on="assembly_ID",
    how="left"
)

# Missing feature values mean feature absent
df[FEATURES] = (
    df[FEATURES]
    .fillna(0)
    .astype(int)
)

df = df[
    ["assembly_ID", "target"] + FEATURES
]

# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

df.to_csv(
    OUTPUT,
    index=False
)

print("=== FINAL ML DATASET ===")

print("\nRows:")
print(len(df))

print("\nUnique assemblies:")
print(df["assembly_ID"].nunique())

print("\nTarget distribution:")
print(
    df["target"]
    .value_counts()
    .sort_index()
)

print("\nNumber of features:")
print(len(FEATURES))

print("\nMissing values:")
print(df.isna().sum().sum())

print("\nDuplicate assemblies:")
print(df["assembly_ID"].duplicated().sum())

print("\nFeature prevalence:")
print(
    df[FEATURES]
    .sum()
    .sort_values(ascending=False)
)

print("\nFirst 10 rows:")
print(
    df.head(10).to_string(index=False)
)

print(f"\nSaved to: {OUTPUT}")

con.close()