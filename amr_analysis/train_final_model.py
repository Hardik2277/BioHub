import json
import os
from datetime import datetime, timezone

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression


# ============================================================
# Configuration
# ============================================================

TRAIN_FILE = "ecoli_ampicillin_train.csv"

MODEL_DIR = "models"

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "logistic_regression_model.pkl"
)

METADATA_FILE = os.path.join(
    MODEL_DIR,
    "model_metadata.json"
)

RANDOM_STATE = 42

FEATURES = [
    "marR_S3N",
    "tet(B)",
    "tet(A)",
    "soxS_A12S",
    "aac(3)-IId",
    "aph(6)-Id",
    "aph(3'')-Ib",
    "dfrA1",
]

TARGET = "target"


# ============================================================
# Create model directory
# ============================================================

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# Load training dataset
# ============================================================

print("=" * 70)
print("FINAL LOGISTIC REGRESSION MODEL TRAINING")
print("=" * 70)

print(f"\nLoading training dataset: {TRAIN_FILE}")

train_df = pd.read_csv(TRAIN_FILE)

print(f"Training samples: {len(train_df)}")


# ============================================================
# Validate dataset
# ============================================================

required_columns = FEATURES + [TARGET]

for column in required_columns:
    if column not in train_df.columns:
        raise ValueError(
            f"Required column missing from training dataset: {column}"
        )


# ============================================================
# Prepare features and target
# ============================================================

X_train = train_df[FEATURES]
y_train = train_df[TARGET]


# ============================================================
# Validate target
# ============================================================

valid_targets = {0, 1}

if not set(y_train.unique()).issubset(valid_targets):
    raise ValueError(
        "Target column must contain only 0 and 1."
    )


# ============================================================
# Check missing values
# ============================================================

missing_values = X_train.isnull().sum().sum()

if missing_values > 0:
    raise ValueError(
        f"Training data contains {missing_values} missing feature values."
    )


# ============================================================
# Check duplicate assemblies
# ============================================================

if "assembly_ID" in train_df.columns:

    duplicate_count = train_df[
        "assembly_ID"
    ].duplicated().sum()

    print(
        f"Duplicate assemblies: {duplicate_count}"
    )

    if duplicate_count > 0:
        raise ValueError(
            "Duplicate assembly_ID values detected."
        )


# ============================================================
# Display dataset information
# ============================================================

print("\nTarget distribution:")

print(
    y_train.value_counts()
    .sort_index()
    .rename(
        index={
            0: "Susceptible",
            1: "Resistant"
        }
    )
)


print("\nFeatures used:")

for feature in FEATURES:
    print(f"  - {feature}")


# ============================================================
# Create final Logistic Regression model
# ============================================================
#
# These settings match the Logistic Regression experiment
# used for model comparison.
#
# The test dataset is NOT used here.
#
# ============================================================

model = LogisticRegression(
    random_state=RANDOM_STATE,
    max_iter=1000
)


# ============================================================
# Train final model
# ============================================================

print("\nTraining final Logistic Regression model...")

model.fit(
    X_train,
    y_train
)

print("Training completed successfully.")


# ============================================================
# Model information
# ============================================================

print("\n" + "=" * 70)
print("MODEL INFORMATION")
print("=" * 70)

print(f"Model: Logistic Regression")
print(f"Training samples: {len(X_train)}")
print(f"Number of features: {len(FEATURES)}")
print(f"Random state: {RANDOM_STATE}")

print("\nClasses:")

for class_value, class_name in zip(
    model.classes_,
    ["Susceptible", "Resistant"]
):
    print(
        f"  {class_value} = {class_name}"
    )


# ============================================================
# Display model coefficients
# ============================================================

coefficients = pd.DataFrame({
    "feature": FEATURES,
    "coefficient": model.coef_[0]
})

print("\n" + "=" * 70)
print("MODEL COEFFICIENTS")
print("=" * 70)

print(
    coefficients.to_string(index=False)
)


# ============================================================
# Save model
# ============================================================

joblib.dump(
    model,
    MODEL_FILE
)

print(
    f"\nModel saved to: {MODEL_FILE}"
)


# ============================================================
# Save model metadata
# ============================================================

metadata = {
    "model_name": "Logistic Regression",
    "model_version": "1.0",
    "task": "E. coli Ampicillin resistance prediction",
    "target": {
        "column": TARGET,
        "0": "Susceptible",
        "1": "Resistant"
    },
    "features": FEATURES,
    "training_file": TRAIN_FILE,
    "training_samples": int(len(X_train)),
    "training_class_counts": {
        "susceptible": int((y_train == 0).sum()),
        "resistant": int((y_train == 1).sum())
    },
    "random_state": RANDOM_STATE,
    "max_iter": 1000,
    "selection_note": (
        "Selected as the primary model after comparison "
        "with Majority Baseline, Random Forest, and XGBoost."
    ),
    "scientific_status": (
        "Research Prediction / Resistance Risk Indicator"
    ),
    "clinical_use": False,
    "test_set_used_for_training": False,
    "created_at_utc": datetime.now(
        timezone.utc
    ).isoformat()
}


with open(
    METADATA_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        indent=4
    )


print(
    f"Metadata saved to: {METADATA_FILE}"
)


# ============================================================
# Final verification
# ============================================================

print("\n" + "=" * 70)
print("FINAL MODEL VERIFICATION")
print("=" * 70)

loaded_model = joblib.load(
    MODEL_FILE
)

if not isinstance(
    loaded_model,
    LogisticRegression
):
    raise ValueError(
        "Saved model is not a LogisticRegression model."
    )


print("Saved model loaded successfully.")

print(
    f"Model type: {type(loaded_model).__name__}"
)

print(
    f"Number of coefficients: "
    f"{len(loaded_model.coef_[0])}"
)

print(
    f"Number of expected features: "
    f"{len(FEATURES)}"
)

if len(loaded_model.coef_[0]) != len(FEATURES):
    raise ValueError(
        "Model coefficient count does not match feature count."
    )


# ============================================================
# Completion
# ============================================================

print("\n" + "=" * 70)
print("FINAL MODEL TRAINING COMPLETED")
print("=" * 70)

print("\nOutput files:")

print(
    f"  {MODEL_FILE}"
)

print(
    f"  {METADATA_FILE}"
)

print(
    "\nThe final Logistic Regression model is ready "
    "for Module 4 backend integration."
)