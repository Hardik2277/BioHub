import pandas as pd

from sklearn.dummy import DummyClassifier
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

# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]

# --------------------------------------------------
# 2. Majority-class baseline
# --------------------------------------------------

model = DummyClassifier(
    strategy="most_frequent"
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# --------------------------------------------------
# 3. Evaluation
# --------------------------------------------------

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

# ROC-AUC is not meaningful for a constant prediction
roc_auc = None

cm = confusion_matrix(
    y_test,
    y_pred
)

# --------------------------------------------------
# 4. Print results
# --------------------------------------------------

print("=== MAJORITY CLASS BASELINE ===")

print("\nTraining samples:", len(train_df))
print("Test samples:", len(test_df))

print("\nTest target distribution:")
print(y_test.value_counts().sort_index())

print("\nMetrics:")
print(f"Accuracy:           {accuracy:.4f}")
print(f"Balanced Accuracy:  {balanced_accuracy:.4f}")
print(f"Precision:          {precision:.4f}")
print(f"Recall:             {recall:.4f}")
print(f"F1-score:           {f1:.4f}")

print("\nROC-AUC:")
print("Not applicable for constant majority prediction.")

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