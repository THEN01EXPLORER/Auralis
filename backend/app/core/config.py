from pydantic_settings import BaseSettings
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auralis API"
    ALLOWED_ORIGINS: List[Union[str, AnyHttpUrl]] = ["*"]

    # Security
    SECRET_KEY: str = "changethis"  # Should be changed in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    # AWS / Bedrock
    AWS_REGION: str = "us-east-1"
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    BEDROCK_TIMEOUT: int = 25
    ENABLE_AI_ANALYSIS: bool = True
    AI_ANALYSIS_REQUIRED: bool = False

    # Git
    GIT_AVAILABLE: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None
    
    # Observability
    SENTRY_DSN: Optional[str] = None

    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
