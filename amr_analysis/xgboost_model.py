import pandas as pd
import numpy as np

from xgboost import XGBClassifier

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


# ============================================================
# Configuration
# ============================================================

TRAIN_FILE = "ecoli_ampicillin_train.csv"
TEST_FILE = "ecoli_ampicillin_test.csv"

TARGET = "target"
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


# ============================================================
# Load datasets
# ============================================================

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

print("=" * 70)
print("XGBOOST MODEL - E. coli + Ampicillin")
print("=" * 70)

print(f"\nTraining samples: {len(train_df)}")
print(f"Test samples:     {len(test_df)}")


# ============================================================
# Validate dataset
# ============================================================

required_columns = FEATURES + [TARGET]

for column in required_columns:
    if column not in train_df.columns:
        raise ValueError(
            f"Missing column in training dataset: {column}"
        )

    if column not in test_df.columns:
        raise ValueError(
            f"Missing column in test dataset: {column}"
        )


X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]


# ============================================================
# Validate target values
# ============================================================

valid_targets = {0, 1}

if not set(y_train.unique()).issubset(valid_targets):
    raise ValueError("Training target must contain only 0 and 1.")

if not set(y_test.unique()).issubset(valid_targets):
    raise ValueError("Test target must contain only 0 and 1.")


# ============================================================
# Check missing values
# ============================================================

if X_train.isnull().sum().sum() > 0:
    raise ValueError("Missing values found in training features.")

if X_test.isnull().sum().sum() > 0:
    raise ValueError("Missing values found in test features.")


# ============================================================
# Check duplicate assemblies and train/test overlap
# ============================================================

if "assembly_ID" in train_df.columns:
    if train_df["assembly_ID"].duplicated().any():
        raise ValueError(
            "Duplicate assembly_ID found in training dataset."
        )

if "assembly_ID" in test_df.columns:
    if test_df["assembly_ID"].duplicated().any():
        raise ValueError(
            "Duplicate assembly_ID found in test dataset."
        )

if (
    "assembly_ID" in train_df.columns
    and "assembly_ID" in test_df.columns
):
    overlap = set(train_df["assembly_ID"]) & set(
        test_df["assembly_ID"]
    )

    print(f"Assembly overlap: {len(overlap)}")

    if overlap:
        raise ValueError(
            "Assembly overlap detected between train and test sets."
        )


# ============================================================
# Target distribution
# ============================================================

print("\nTraining target distribution:")
print(y_train.value_counts().sort_index())

print("\nTest target distribution:")
print(y_test.value_counts().sort_index())


# ============================================================
# Create XGBoost model
# ============================================================
#
# Initial model comparison only.
# No test-set tuning is performed.
#
# The parameters are intentionally kept fixed so that
# XGBoost can be compared fairly with the previous models.
#
# ============================================================

model = XGBClassifier(
    n_estimators=300,
    max_depth=3,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=RANDOM_STATE,
    n_jobs=-1,
)


# ============================================================
# 5-Fold Stratified Cross-Validation
# ============================================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=RANDOM_STATE
)

scoring = {
    "accuracy": "accuracy",
    "balanced_accuracy": "balanced_accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1",
    "roc_auc": "roc_auc",
}

cv_results = cross_validate(
    model,
    X_train,
    y_train,
    cv=cv,
    scoring=scoring,
    n_jobs=-1
)


# ============================================================
# Display Cross-Validation Results
# ============================================================

print("\n" + "=" * 70)
print("5-FOLD STRATIFIED CROSS-VALIDATION")
print("=" * 70)

for metric in scoring:
    scores = cv_results[f"test_{metric}"]

    print(
        f"{metric:20s}: "
        f"{scores.mean():.4f} ± {scores.std():.4f}"
    )


# ============================================================
# Train final model on complete training set
# ============================================================

model.fit(X_train, y_train)


# ============================================================
# Held-Out Test Evaluation
# ============================================================

y_pred = model.predict(X_test)

y_prob = model.predict_proba(X_test)[:, 1]


accuracy = accuracy_score(y_test, y_pred)

balanced_accuracy = balanced_accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

cm = confusion_matrix(
    y_test,
    y_pred
)


# ============================================================
# Display Test Results
# ============================================================

print("\n" + "=" * 70)
print("HELD-OUT TEST SET")
print("=" * 70)

print(f"Accuracy:           {accuracy:.4f}")
print(f"Balanced Accuracy:  {balanced_accuracy:.4f}")
print(f"Precision:          {precision:.4f}")
print(f"Recall:             {recall:.4f}")
print(f"F1 Score:           {f1:.4f}")
print(f"ROC-AUC:            {roc_auc:.4f}")


# ============================================================
# Confusion Matrix
# ============================================================

print("\nConfusion Matrix")
print("(Rows = Actual, Columns = Predicted)")

print("                Predicted")
print("              S       R")

print(
    f"Actual S   {cm[0, 0]:4d}   {cm[0, 1]:4d}"
)

print(
    f"Actual R   {cm[1, 0]:4d}   {cm[1, 1]:4d}"
)


# ============================================================
# Classification Report
# ============================================================

print("\nClassification Report")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Susceptible",
            "Resistant"
        ],
        zero_division=0
    )
)


# ============================================================
# Feature Importance
# ============================================================

feature_importance = pd.DataFrame({
    "feature": FEATURES,
    "importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)


print("\n" + "=" * 70)
print("XGBOOST FEATURE IMPORTANCE")
print("=" * 70)

print(
    feature_importance.to_string(
        index=False
    )
)


# ============================================================
# Save Feature Importance
# ============================================================

feature_importance.to_csv(
    "xgboost_feature_importance.csv",
    index=False
)

print(
    "\nFeature importance saved to "
    "xgboost_feature_importance.csv"
)


# ============================================================
# Save Test Predictions
# ============================================================

predictions = test_df.copy()

predictions["predicted_class"] = y_pred

predictions[
    "predicted_probability_resistant"
] = y_prob

predictions.to_csv(
    "xgboost_test_predictions.csv",
    index=False
)

print(
    "Test predictions saved to "
    "xgboost_test_predictions.csv"
)


# ============================================================
# Save Model Metrics
# ============================================================

metrics_df = pd.DataFrame({
    "metric": [
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc"
    ],
    "value": [
        accuracy,
        balanced_accuracy,
        precision,
        recall,
        f1,
        roc_auc
    ]
})

metrics_df.to_csv(
    "xgboost_test_metrics.csv",
    index=False
)

print(
    "Test metrics saved to "
    "xgboost_test_metrics.csv"
)


# ============================================================
# Final Summary
# ============================================================

print("\n" + "=" * 70)
print("MODEL SUMMARY")
print("=" * 70)

print("Model: XGBoost Classifier")
print("Dataset: E. coli + Ampicillin")
print("Target: 0 = Susceptible, 1 = Resistant")

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

print(f"Number of features: {len(FEATURES)}")

print("Cross-validation: 5-fold Stratified")
print(f"Random state: {RANDOM_STATE}")

print("\nXGBoost parameters:")
print("n_estimators: 300")
print("max_depth: 3")
print("learning_rate: 0.05")
print("subsample: 0.8")
print("colsample_bytree: 0.8")

print("\nHeld-out test performance:")

print(f"Accuracy:          {accuracy:.4f}")
print(f"Balanced Accuracy: {balanced_accuracy:.4f}")
print(f"Precision:         {precision:.4f}")
print(f"Recall:            {recall:.4f}")
print(f"F1 Score:          {f1:.4f}")
print(f"ROC-AUC:           {roc_auc:.4f}")

print("\nXGBoost experiment completed.")