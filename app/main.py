"""
Application entrypoint.
Run with: uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs for interactive API documentation.
"""

import logging
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import AIServiceError, ai_service_error_handler, generic_exception_handler
from app.core.logging_config import setup_logging
from app.routers import ai_routes

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description=(
        "REST API exposing three AI-powered endpoints: text summarization, "
        "translation, and email generation. Built with FastAPI and Google Gemini."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(static_dir / "index.html")

# ---------- Middleware: simple request logging + timing ----------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info("Incoming request: %s %s", request.method, request.url.path)

    response = await call_next(request)

    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(
        "Completed request: %s %s -> status=%s duration=%sms",
        request.method, request.url.path, response.status_code, duration_ms,
    )
    return response


# ---------- Global exception handlers ----------

app.add_exception_handler(AIServiceError, ai_service_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, generic_exception_handler)


# ---------- Routes ----------

app.include_router(ai_routes.router)


@app.get("/health", tags=["Health"], summary="Health check")
def health_check():
    return {"success": True, "message": f"{settings.app_name} is running."}
