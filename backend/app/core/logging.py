import logging
import sys
import structlog
from typing import Any
from app.core.config import settings

def configure_logging() -> logging.Logger:
    """Configure logging with structlog and environment settings."""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if settings.LOG_FORMAT == "json" else structlog.dev.ConsoleRenderer(), # Simple for now
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False
    )

    # Standard library logging
    numeric_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        format=settings.LOG_FORMAT,
        level=numeric_level,
        stream=sys.stdout,
        force=True
    )
    
    logger = logging.getLogger("auralis")
    logger.setLevel(numeric_level)
    
    # Also set uvicorn loggers
    logging.getLogger("uvicorn.access").setLevel(numeric_level)
    logging.getLogger("uvicorn.error").setLevel(numeric_level)
    
    return logger
