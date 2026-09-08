from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.v1 import health
from app.core.config import settings
from app.services.resistance_service import resistance_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager to handle application startup and shutdown events."""
    logger.info("Initializing BioHub FastAPI application startup...")
    try:
        resistance_service.load_model()
        logger.info("Module 4 Logistic Regression model successfully loaded.")
    except Exception as e:
        logger.error("Failed to load Module 4 model on startup: %s", e)
    yield
    logger.info("BioHub FastAPI application shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "BioHub API — End-to-End Automated Platform for Microbial Image Analytics, "
        "Genomic Data Pipelines, and Resistance Phenotype Prediction."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(health.router)  # Expose /health at root level
app.include_router(api_router, prefix=settings.API_V1_STR)  # Expose /api/v1 routes
