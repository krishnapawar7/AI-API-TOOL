"""
Custom exception types used across the app, plus the global handlers
registered in main.py. Keeping these separate makes error handling
consistent and easy to extend.
"""

from fastapi import Request
from fastapi.responses import JSONResponse


class AIServiceError(Exception):
    """Raised when the upstream AI provider (Gemini) fails or errors out."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


async def ai_service_error_handler(request: Request, exc: AIServiceError):
    return JSONResponse(
        status_code=502,
        content={
            "success": False,
            "error": "AI_SERVICE_ERROR",
            "message": exc.message,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Something went wrong. Please try again later.",
        },
    )
