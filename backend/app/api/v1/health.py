from typing import Any, Dict
from fastapi import APIRouter
from app.services.resistance_service import resistance_service

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=Dict[str, Any])
def health_check() -> Dict[str, Any]:
    """Health check endpoint to verify backend service operational status."""
    return {
        "status": "ok",
        "model_loaded": resistance_service.is_loaded,
    }
