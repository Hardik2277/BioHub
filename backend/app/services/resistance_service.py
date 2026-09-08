import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import joblib
from sklearn.linear_model import LogisticRegression

from app.core.config import settings
from app.schemas.predictions import (
    CANONICAL_FEATURES,
    ModelInfo,
    ResistancePredictionRequest,
    ResistancePredictionResponse,
)

logger = logging.getLogger(__name__)


class ResistanceService:
    def __init__(
        self,
        model_path: Optional[Path] = None,
        metadata_path: Optional[Path] = None,
    ):
        self.model_path = model_path or settings.MODEL_PATH
        self.metadata_path = metadata_path or settings.METADATA_PATH
        self.model: Optional[LogisticRegression] = None
        self.metadata: Optional[Dict[str, Any]] = None
        self.is_loaded: bool = False

    def load_model(self) -> None:
        """Load and validate model artifact and metadata from disk."""
        if not self.model_path.exists():
            raise RuntimeError(f"Model artifact not found at: {self.model_path}")
        if not self.metadata_path.exists():
            raise RuntimeError(f"Model metadata file not found at: {self.metadata_path}")

        try:
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to read model metadata: {e}") from e

        try:
            loaded = joblib.load(self.model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model pickle artifact: {e}") from e

        if not isinstance(loaded, LogisticRegression):
            raise RuntimeError(
                f"Expected LogisticRegression model, got {type(loaded).__name__}"
            )

        if not hasattr(loaded, "predict_proba"):
            raise RuntimeError("Loaded model does not support predict_proba().")

        # Validate feature count and names
        metadata_features = self.metadata.get("features", [])
        if metadata_features != CANONICAL_FEATURES:
            raise RuntimeError(
                f"Metadata feature list does not match canonical features.\n"
                f"Metadata: {metadata_features}\n"
                f"Canonical: {CANONICAL_FEATURES}"
            )

        if len(loaded.coef_[0]) != len(CANONICAL_FEATURES):
            raise RuntimeError(
                f"Model coefficient count ({len(loaded.coef_[0])}) does not match canonical feature count ({len(CANONICAL_FEATURES)})"
            )

        self.model = loaded
        self.is_loaded = True
        logger.info(
            "ResistanceService successfully loaded model from %s", self.model_path
        )

    def predict(
        self, request: ResistancePredictionRequest
    ) -> ResistancePredictionResponse:
        """Execute resistance prediction inference for a validated request."""
        if not self.is_loaded or self.model is None:
            raise RuntimeError("Prediction model is not loaded or unavailable.")

        # Extract features in exact canonical order
        feature_vector = [
            [request.features[feature_name] for feature_name in CANONICAL_FEATURES]
        ]

        # Inference
        probs = self.model.predict_proba(feature_vector)[0]
        predicted_class_int = int(self.model.predict(feature_vector)[0])

        susceptibility_prob = float(probs[0])
        resistance_prob = float(probs[1])

        label_map = {0: "Susceptible", 1: "Resistant"}
        prediction_label = label_map.get(predicted_class_int, "Unknown")

        model_name = (
            self.metadata.get("model_name", "Logistic Regression")
            if self.metadata
            else "Logistic Regression"
        )
        model_version = (
            self.metadata.get("model_version", "1.0") if self.metadata else "1.0"
        )

        return ResistancePredictionResponse(
            sample_id=request.sample_id,
            prediction_label=prediction_label,
            predicted_class=predicted_class_int,
            resistance_probability=round(resistance_prob, 4),
            susceptibility_probability=round(susceptibility_prob, 4),
            features_analyzed=CANONICAL_FEATURES,
            model_info=ModelInfo(
                model_name=model_name,
                model_version=model_version,
            ),
            scientific_disclaimer=(
                "Research Prediction / Resistance Risk Indicator. Not for clinical use."
            ),
        )


# Global singleton instance
resistance_service = ResistanceService()
