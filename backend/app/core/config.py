from pathlib import Path
from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "BioHub API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Base repository directory (4 levels up from this file)
    BASE_DIR: Path = Path(__file__).resolve().parents[3]

    # Model artifact paths
    MODEL_PATH: Path = BASE_DIR / "amr_analysis" / "models" / "logistic_regression_model.pkl"
    METADATA_PATH: Path = BASE_DIR / "amr_analysis" / "models" / "model_metadata.json"


settings = Settings()
