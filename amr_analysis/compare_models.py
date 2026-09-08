import pandas as pd
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

RESULTS_DIR = Path(".")

OUTPUT_FILE = "model_comparison.csv"


# ============================================================
# Model Results
# ============================================================
#
# These are the HELD-OUT TEST SET results from the completed
# experiments.
#
# 0 = Susceptible
# 1 = Resistant
#
# ============================================================

results = [
    {
        "model": "Majority Baseline",
        "accuracy": 0.5787,
        "balanced_accuracy": 0.5000,
        "precision": 0.0000,
        "recall": 0.0000,
        "f1": 0.0000,
        "roc_auc": None,
    },
    {
        "model": "Logistic Regression",
        "accuracy": 0.6936,
        "balanced_accuracy": 0.6474,
        "precision": 0.8140,
        "recall": 0.3535,
        "f1": 0.4930,
        "roc_auc": 0.6452,
    },
    {
        "model": "Random Forest",
        "accuracy": 0.6894,
        "balanced_accuracy": 0.6423,
        "precision": 0.8095,
        "recall": 0.3434,
        "f1": 0.4823,
        "roc_auc": 0.6556,
    },
    {
        "model": "XGBoost",
        "accuracy": 0.6936,
        "balanced_accuracy": 0.6474,
        "precision": 0.8140,
        "recall": 0.3535,
        "f1": 0.4930,
        "roc_auc": 0.6476,
    },
]


# ============================================================
# Create DataFrame
# ============================================================

df = pd.DataFrame(results)


# ============================================================
# Display comparison table
# ============================================================

print("=" * 95)
print("FINAL MODEL COMPARISON - E. coli + Ampicillin")
print("=" * 95)

display_df = df.copy()

percentage_columns = [
    "accuracy",
    "balanced_accuracy",
    "precision",
    "recall",
]

for column in percentage_columns:
    display_df[column] = (
        display_df[column] * 100
    ).round(2)

display_df["f1"] = display_df["f1"].round(4)
display_df["roc_auc"] = display_df["roc_auc"].round(4)


print(
    display_df.to_string(index=False)
)


# ============================================================
# Detailed formatted table
# ============================================================

print("\n" + "=" * 95)
print("PERFORMANCE SUMMARY")
print("=" * 95)

print(
    f"{'Model':<22}"
    f"{'Accuracy':>12}"
    f"{'Bal. Acc.':>12}"
    f"{'Precision':>12}"
    f"{'Recall':>12}"
    f"{'F1':>10}"
    f"{'ROC-AUC':>12}"
)

print("-" * 95)

for _, row in df.iterrows():

    roc_auc = (
        f"{row['roc_auc']:.4f}"
        if pd.notna(row["roc_auc"])
        else "N/A"
    )

    print(
        f"{row['model']:<22}"
        f"{row['accuracy'] * 100:>11.2f}%"
        f"{row['balanced_accuracy'] * 100:>11.2f}%"
        f"{row['precision'] * 100:>11.2f}%"
        f"{row['recall'] * 100:>11.2f}%"
        f"{row['f1']:>10.4f}"
        f"{roc_auc:>12}"
    )


# ============================================================
# Identify Best Models
# ============================================================

print("\n" + "=" * 95)
print("BEST PERFORMANCE BY METRIC")
print("=" * 95)


metrics = {
    "accuracy": "Accuracy",
    "balanced_accuracy": "Balanced Accuracy",
    "precision": "Precision",
    "recall": "Recall",
    "f1": "F1 Score",
    "roc_auc": "ROC-AUC",
}


for column, label in metrics.items():

    valid_df = df.dropna(subset=[column])

    if valid_df.empty:
        continue

    best_value = valid_df[column].max()

    best_models = valid_df[
        valid_df[column] == best_value
    ]["model"].tolist()

    print(
        f"{label:<22}: "
        f"{best_value:.4f} -> "
        f"{', '.join(best_models)}"
    )


# ============================================================
# Improvement over Majority Baseline
# ============================================================

baseline_accuracy = df.loc[
    df["model"] == "Majority Baseline",
    "accuracy"
].iloc[0]

baseline_balanced_accuracy = df.loc[
    df["model"] == "Majority Baseline",
    "balanced_accuracy"
].iloc[0]


print("\n" + "=" * 95)
print("IMPROVEMENT OVER MAJORITY BASELINE")
print("=" * 95)

for _, row in df.iterrows():

    if row["model"] == "Majority Baseline":
        continue

    accuracy_improvement = (
        row["accuracy"] - baseline_accuracy
    ) * 100

    balanced_accuracy_improvement = (
        row["balanced_accuracy"]
        - baseline_balanced_accuracy
    ) * 100

    print(f"\n{row['model']}")

    print(
        f"  Accuracy improvement: "
        f"+{accuracy_improvement:.2f} percentage points"
    )

    print(
        f"  Balanced accuracy improvement: "
        f"+{balanced_accuracy_improvement:.2f} percentage points"
    )


# ============================================================
# Recommended Primary Model
# ============================================================
#
# Selection is based on overall classification performance,
# interpretability, and avoiding unnecessary complexity.
#
# Logistic Regression and XGBoost have identical held-out
# classification metrics. Logistic Regression is therefore
# preferred as the primary model because it is simpler and
# more interpretable.
#
# Random Forest remains the model with the highest ROC-AUC.
#
# ============================================================

recommended_model = "Logistic Regression"

print("\n" + "=" * 95)
print("MODEL SELECTION")
print("=" * 95)

print(
    f"\nRecommended primary model: {recommended_model}"
)

print(
    "\nReason:"
)

print(
    "Logistic Regression provides the strongest overall "
    "classification performance while remaining simple "
    "and interpretable."
)

print(
    "\nXGBoost produced the same held-out classification "
    "metrics as Logistic Regression, but did not provide "
    "a meaningful improvement."
)

print(
    "\nRandom Forest achieved the highest ROC-AUC, but its "
    "accuracy, balanced accuracy, recall, and F1 score were "
    "slightly lower."
)


# ============================================================
# Scientific Interpretation
# ============================================================

print("\n" + "=" * 95)
print("SCIENTIFIC INTERPRETATION")
print("=" * 95)

print(
    "\nThe evaluated models improve substantially over the "
    "majority-class baseline."
)

print(
    "\nHowever, Resistant-class recall remains approximately "
    "34-35%, indicating limited sensitivity for detecting "
    "resistant samples."
)

print(
    "\nTherefore, the model should be presented as a "
    "\"Research Prediction / Resistance Risk Indicator\" "
    "and not as a clinical diagnostic system."
)

print(
    "\nFeature importance and model coefficients indicate "
    "model associations and should not be interpreted as "
    "causal biological effects."
)


# ============================================================
# Save Results
# ============================================================

output_path = RESULTS_DIR / OUTPUT_FILE

df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 95)
print("OUTPUT")
print("=" * 95)

print(
    f"\nModel comparison saved to: {output_path}"
)

print("\nComparison completed successfully.")