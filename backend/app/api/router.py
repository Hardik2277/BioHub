from fastapi import APIRouter
from app.api.v1 import health, predictions

api_router = APIRouter()

# Include endpoints
api_router.include_router(predictions.router)
