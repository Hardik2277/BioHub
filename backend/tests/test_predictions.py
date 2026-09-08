import pytest
from app.schemas.predictions import CANONICAL_FEATURES
from app.services.resistance_service import resistance_service


def test_model_loading_and_attributes():
    """Verify actual Logistic Regression model artifact loads and attributes match expected metadata."""
    assert resistance_service.is_loaded is True
    assert resistance_service.model is not None
    assert hasattr(resistance_service.model, "predict_proba")
    assert len(resistance_service.model.coef_[0]) == len(CANONICAL_FEATURES)


def test_valid_prediction_request(client):
    """Test valid prediction request returns HTTP 200 and actual calculated probabilities."""
    payload = {
        "sample_id": "TEST-SAMPLE-001",
        "features": {
            "marR_S3N": 1,
            "tet(B)": 0,
            "tet(A)": 1,
            "soxS_A12S": 0,
            "aac(3)-IId": 1,
            "aph(6)-Id": 0,
            "aph(3'')-Ib": 0,
            "dfrA1": 0,
        },
    }

    response = client.post("/api/v1/predictions/resistance", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()

    # Field assertions
    assert data["sample_id"] == "TEST-SAMPLE-001"
    assert data["prediction_label"] in ["Susceptible", "Resistant"]
    assert data["predicted_class"] in [0, 1]

    # Probability assertions
    res_prob = data["resistance_probability"]
    sus_prob = data["susceptibility_probability"]

    assert isinstance(res_prob, float)
    assert isinstance(sus_prob, float)
    assert 0.0 <= res_prob <= 1.0
    assert 0.0 <= sus_prob <= 1.0
    assert abs((res_prob + sus_prob) - 1.0) < 0.01

    # Metadata and features assertions
    assert data["features_analyzed"] == CANONICAL_FEATURES
    assert data["model_info"]["model_name"] == "Logistic Regression"
    assert data["model_info"]["model_version"] == "1.0"
    assert (
        data["scientific_disclaimer"]
        == "Research Prediction / Resistance Risk Indicator. Not for clinical use."
    )


def test_sample_id_whitespace_trimming(client):
    """Test sample_id surrounding whitespace is trimmed."""
    payload = {
        "sample_id": "   SAMPLE-TRIM-002   ",
        "features": {
            "marR_S3N": 0,
            "tet(B)": 0,
            "tet(A)": 0,
            "soxS_A12S": 0,
            "aac(3)-IId": 0,
            "aph(6)-Id": 0,
            "aph(3'')-Ib": 0,
            "dfrA1": 0,
        },
    }
    response = client.post("/api/v1/predictions/resistance", json=payload)
    assert response.status_code == 200
    assert response.json()["sample_id"] == "SAMPLE-TRIM-002"


@pytest.mark.parametrize(
    "invalid_payload, expected_reason",
    [
        (
            {
                "sample_id": "TEST-MISSING-FEATURE",
                "features": {
                    "marR_S3N": 1,
                    "tet(B)": 0,
                    "tet(A)": 1,
                    "soxS_A12S": 0,
                    "aac(3)-IId": 1,
                    "aph(6)-Id": 0,
                    "aph(3'')-Ib": 0,
                    # dfrA1 is missing!
                },
            },
            "Missing feature",
        ),
        (
            {
                "sample_id": "TEST-EXTRA-FEATURE",
                "features": {
                    "marR_S3N": 1,
                    "tet(B)": 0,
                    "tet(A)": 1,
                    "soxS_A12S": 0,
                    "aac(3)-IId": 1,
                    "aph(6)-Id": 0,
                    "aph(3'')-Ib": 0,
                    "dfrA1": 0,
                    "unknown_gene": 1,  # Extra feature!
                },
            },
            "Extra feature",
        ),
        (
            {
                "sample_id": "TEST-NON-BINARY-2",
                "features": {
                    "marR_S3N": 2,  # Value 2 is invalid!
                    "tet(B)": 0,
                    "tet(A)": 1,
                    "soxS_A12S": 0,
                    "aac(3)-IId": 1,
                    "aph(6)-Id": 0,
                    "aph(3'')-Ib": 0,
                    "dfrA1": 0,
                },
            },
            "Non-binary feature value 2",
        ),
        (
            {
                "sample_id": "TEST-STRING-FEATURE",
                "features": {
                    "marR_S3N": "1",  # String "1" is invalid!
                    "tet(B)": 0,
                    "tet(A)": 1,
                    "soxS_A12S": 0,
                    "aac(3)-IId": 1,
                    "aph(6)-Id": 0,
                    "aph(3'')-Ib": 0,
                    "dfrA1": 0,
                },
            },
            "String feature value",
        ),
        (
            {
                "sample_id": "TEST-FLOAT-FEATURE",
                "features": {
                    "marR_S3N": 1.5,  # Float 1.5 is invalid!
                    "tet(B)": 0,
                    "tet(A)": 1,
                    "soxS_A12S": 0,
                    "aac(3)-IId": 1,
                    "aph(6)-Id": 0,
                    "aph(3'')-Ib": 0,
                    "dfrA1": 0,
                },
            },
            "Float feature value",
        ),
        (
            {
                "sample_id": "TEST-BOOL-FEATURE",
                "features": {
                    "marR_S3N": True,  # Bool True is invalid!
                    "tet(B)": 0,
                    "tet(A)": 1,
                    "soxS_A12S": 0,
                    "aac(3)-IId": 1,
                    "aph(6)-Id": 0,
                    "aph(3'')-Ib": 0,
                    "dfrA1": 0,
                },
            },
            "Bool feature value",
        ),
        (
            {
                # sample_id missing!
                "features": {
                    "marR_S3N": 1,
                    "tet(B)": 0,
                    "tet(A)": 1,
                    "soxS_A12S": 0,
                    "aac(3)-IId": 1,
                    "aph(6)-Id": 0,
                    "aph(3'')-Ib": 0,
                    "dfrA1": 0,
                },
            },
            "Missing sample_id",
        ),
        (
            {
                "sample_id": "   ",  # Whitespace-only sample_id!
                "features": {
                    "marR_S3N": 1,
                    "tet(B)": 0,
                    "tet(A)": 1,
                    "soxS_A12S": 0,
                    "aac(3)-IId": 1,
                    "aph(6)-Id": 0,
                    "aph(3'')-Ib": 0,
                    "dfrA1": 0,
                },
            },
            "Empty sample_id",
        ),
    ],
)
def test_validation_failures_return_422(client, invalid_payload, expected_reason):
    """Verify invalid payloads trigger HTTP 422 Unprocessable Entity."""
    response = client.post("/api/v1/predictions/resistance", json=invalid_payload)
    assert response.status_code == 422, f"Failed for case: {expected_reason}"
