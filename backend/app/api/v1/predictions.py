from fastapi import APIRouter, HTTPException, status
from app.schemas.predictions import (
    ResistancePredictionRequest,
    ResistancePredictionResponse,
)
from app.services.resistance_service import resistance_service

router = APIRouter(prefix="/predictions", tags=["Module 4 — Resistance Prediction"])


@router.post(
    "/resistance",
    response_model=ResistancePredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict E. coli Ampicillin resistance from genomic features",
    description=(
        "Research endpoint evaluating E. coli Ampicillin resistance risk based on 8 binary genomic features. "
        "Returns calculated resistance/susceptibility probabilities and prediction class. "
        "Not for clinical use."
    ),
)
def predict_resistance(
    request: ResistancePredictionRequest,
) -> ResistancePredictionResponse:
    """Evaluate resistance prediction for a validated sample feature vector."""
    if not resistance_service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Prediction model is currently unavailable or not loaded.",
        )

    try:
        return resistance_service.predict(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during prediction inference.",
        ) from e
