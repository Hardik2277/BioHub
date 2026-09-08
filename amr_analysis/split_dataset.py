import pandas as pd
from sklearn.model_selection import train_test_split

INPUT = "ecoli_ampicillin_ml_dataset.csv"

TRAIN_OUTPUT = "ecoli_ampicillin_train.csv"
TEST_OUTPUT = "ecoli_ampicillin_test.csv"

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT)

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

TARGET = "target"

# --------------------------------------------------
# 2. Basic validation
# --------------------------------------------------

print("=== INPUT DATASET ===")

print("\nRows:", len(df))
print("Unique assemblies:", df["assembly_ID"].nunique())

print("\nTarget distribution:")
print(df[TARGET].value_counts().sort_index())

print("\nMissing values:")
print(df.isna().sum().sum())

print("\nDuplicate assemblies:")
print(df["assembly_ID"].duplicated().sum())

# --------------------------------------------------
# 3. Separate features and target
# --------------------------------------------------

X = df[FEATURES]
y = df[TARGET]

# --------------------------------------------------
# 4. Stratified 80/20 split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# --------------------------------------------------
# 5. Recover assembly IDs
# --------------------------------------------------

train_ids = df.loc[X_train.index, "assembly_ID"]
test_ids = df.loc[X_test.index, "assembly_ID"]

train_df = df.loc[X_train.index].copy()
test_df = df.loc[X_test.index].copy()

# --------------------------------------------------
# 6. Save datasets
# --------------------------------------------------

train_df.to_csv(TRAIN_OUTPUT, index=False)
test_df.to_csv(TEST_OUTPUT, index=False)

# --------------------------------------------------
# 7. Validation
# --------------------------------------------------

print("\n=== TRAINING SET ===")

print("Rows:", len(train_df))
print("Unique assemblies:", train_df["assembly_ID"].nunique())

print("\nTarget distribution:")
print(train_df[TARGET].value_counts().sort_index())

print("\n=== TEST SET ===")

print("Rows:", len(test_df))
print("Unique assemblies:", test_df["assembly_ID"].nunique())

print("\nTarget distribution:")
print(test_df[TARGET].value_counts().sort_index())

# --------------------------------------------------
# 8. Check for leakage between train/test
# --------------------------------------------------

overlap = set(train_ids) & set(test_ids)

print("\n=== LEAKAGE CHECK ===")
print("Assembly overlap:", len(overlap))

if len(overlap) == 0:
    print("PASS: No assembly appears in both train and test.")
else:
    print("FAIL: Assembly overlap detected!")
    print(overlap)

# --------------------------------------------------
# 9. Feature validation
# --------------------------------------------------

print("\n=== FEATURE VALIDATION ===")

print("Number of features:", len(FEATURES))

print("\nTraining feature prevalence:")
print(train_df[FEATURES].sum().sort_values(ascending=False))

print("\nTest feature prevalence:")
print(test_df[FEATURES].sum().sort_values(ascending=False))

print("\n=== FILES SAVED ===")
print(TRAIN_OUTPUT)
print(TEST_OUTPUT)