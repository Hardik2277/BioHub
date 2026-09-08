from typing import Any, Dict, List
from pydantic import BaseModel, Field, field_validator

CANONICAL_FEATURES: List[str] = [
    "marR_S3N",
    "tet(B)",
    "tet(A)",
    "soxS_A12S",
    "aac(3)-IId",
    "aph(6)-Id",
    "aph(3'')-Ib",
    "dfrA1",
]


class ResistancePredictionRequest(BaseModel):
    sample_id: str = Field(
        ...,
        description="Unique sample or experiment identifier",
        examples=["SAMPLE-001"],
    )
    features: Dict[str, Any] = Field(
        ...,
        description="Dictionary of exactly 8 binary genomic feature values (0 or 1)",
        examples=[
            {
                "marR_S3N": 1,
                "tet(B)": 0,
                "tet(A)": 1,
                "soxS_A12S": 0,
                "aac(3)-IId": 1,
                "aph(6)-Id": 0,
                "aph(3'')-Ib": 0,
                "dfrA1": 0,
            }
        ],
    )

    @field_validator("sample_id")
    @classmethod
    def validate_sample_id(cls, v: Any) -> str:
        if not isinstance(v, str):
            raise ValueError("sample_id must be a string")
        v_stripped = v.strip()
        if not v_stripped:
            raise ValueError("sample_id must not be empty or whitespace-only")
        return v_stripped

    @field_validator("features")
    @classmethod
    def validate_features(cls, features: Any) -> Dict[str, int]:
        if not isinstance(features, dict):
            raise ValueError("features must be a dictionary")

        provided_keys = set(features.keys())
        expected_keys = set(CANONICAL_FEATURES)

        missing_keys = expected_keys - provided_keys
        extra_keys = provided_keys - expected_keys

        if missing_keys or extra_keys:
            errors = []
            if missing_keys:
                errors.append(
                    f"Missing required feature(s): {sorted(list(missing_keys))}"
                )
            if extra_keys:
                errors.append(
                    f"Unknown or extra feature(s) provided: {sorted(list(extra_keys))}"
                )
            raise ValueError("; ".join(errors))

        validated_features = {}
        for key in CANONICAL_FEATURES:
            val = features[key]
            # Strict binary numeric validation: reject bool, float, str, None, etc.
            if isinstance(val, bool) or not isinstance(val, int) or val not in (0, 1):
                raise ValueError(
                    f"Feature '{key}' must be an explicit binary integer (0 or 1), got: {repr(val)}"
                )
            validated_features[key] = val

        return validated_features


class ModelInfo(BaseModel):
    model_name: str = Field(..., description="Name of the model")
    model_version: str = Field(..., description="Version of the model")


class ResistancePredictionResponse(BaseModel):
    sample_id: str = Field(..., description="Sample identifier")
    prediction_label: str = Field(
        ..., description="Resistance phenotype prediction (Susceptible or Resistant)"
    )
    predicted_class: int = Field(..., description="Predicted class integer (0 or 1)")
    resistance_probability: float = Field(
        ..., description="Probability of resistance [0.0, 1.0]"
    )
    susceptibility_probability: float = Field(
        ..., description="Probability of susceptibility [0.0, 1.0]"
    )
    features_analyzed: List[str] = Field(
        ..., description="Canonical ordered list of features analyzed"
    )
    model_info: ModelInfo = Field(..., description="Model name and version metadata")
    scientific_disclaimer: str = Field(
        default="Research Prediction / Resistance Risk Indicator. Not for clinical use.",
        description="Scientific scope disclaimer",
    )
