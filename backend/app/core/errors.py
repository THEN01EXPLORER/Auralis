from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Any, Dict, Optional
import time
import uuid
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: str
    detail: Optional[Any] = None

class AuralisError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, detail: Any = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code=str(exc.status_code), # Fallback code
            message=exc.detail if isinstance(exc.detail, str) else "Request processing failed",
            request_id=request_id,
            detail=exc.detail if not isinstance(exc.detail, str) else None
        ).model_dump(exclude_none=True)
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            request_id=request_id,
            detail=exc.errors()
        ).model_dump(exclude_none=True)
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    # Log the error here if not already logged via middleware
    # logger.error(f"Unhandled exception: {exc}", exc_info=True) 
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            request_id=request_id
        ).model_dump(exclude_none=True)
    )
