import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

TRAIN_FILE = "ecoli_ampicillin_train.csv"
TEST_FILE = "ecoli_ampicillin_test.csv"

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


# =========================================================
# 1. Load datasets
# =========================================================

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]


# =========================================================
# 2. Create Logistic Regression pipeline
# =========================================================

model = Pipeline([
    ("scaler", StandardScaler()),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )
])


# =========================================================
# 3. Five-fold stratified cross-validation
# =========================================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scoring = [
    "accuracy",
    "balanced_accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc"
]

cv_results = cross_validate(
    model,
    X_train,
    y_train,
    cv=cv,
    scoring=scoring
)


print("=== LOGISTIC REGRESSION ===")

print("\n=== 5-FOLD CROSS-VALIDATION ===")

for metric in scoring:
    values = cv_results[f"test_{metric}"]

    print(
        f"{metric}: "
        f"{values.mean():.4f} "
        f"(± {values.std():.4f})"
    )


# =========================================================
# 4. Fit final Logistic Regression on full training data
# =========================================================

model.fit(
    X_train,
    y_train
)


# =========================================================
# 5. Evaluate on untouched test set
# =========================================================

y_pred = model.predict(X_test)

y_prob = model.predict_proba(X_test)[:, 1]


accuracy = accuracy_score(
    y_test,
    y_pred
)

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


# =========================================================
# 6. Print test results
# =========================================================

print("\n=== HELD-OUT TEST RESULTS ===")

print(f"Accuracy:           {accuracy:.4f}")
print(f"Balanced Accuracy:  {balanced_accuracy:.4f}")
print(f"Precision:          {precision:.4f}")
print(f"Recall:             {recall:.4f}")
print(f"F1-score:           {f1:.4f}")
print(f"ROC-AUC:            {roc_auc:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")

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


# =========================================================
# 7. Logistic Regression coefficients
# =========================================================

classifier = model.named_steps["classifier"]

coefficients = pd.DataFrame({
    "feature": FEATURES,
    "coefficient": classifier.coef_[0]
})

coefficients["absolute_coefficient"] = (
    coefficients["coefficient"].abs()
)

coefficients = coefficients.sort_values(
    "absolute_coefficient",
    ascending=False
)

print("\n=== FEATURE COEFFICIENTS ===")

print(
    coefficients.to_string(index=False)
)

coefficients.to_csv(
    "logistic_regression_coefficients.csv",
    index=False
)

print(
    "\nSaved coefficients to "
    "logistic_regression_coefficients.csv"
)