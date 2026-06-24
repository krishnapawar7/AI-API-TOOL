"""
API routes for the three required endpoints:
POST /summarize
POST /translate
POST /generate-email

Each route only does: validate input (via Pydantic schema) -> call the
service layer -> return a shaped response. Business/AI logic lives in
app/services/ai_service.py.
"""

import logging

from fastapi import APIRouter

from app.schemas.ai_schemas import (
    GenerateEmailRequest,
    GenerateEmailResponse,
    SummarizeRequest,
    SummarizeResponse,
    TranslateRequest,
    TranslateResponse,
)
from app.services import ai_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["AI Endpoints"])


@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    summary="Summarize a block of text",
)
def summarize(request: SummarizeRequest):
    logger.info("Received /summarize request (text length=%s)", len(request.text))
    summary = ai_service.summarize_text(request.text, request.max_words)
    return SummarizeResponse(summary=summary)


@router.post(
    "/translate",
    response_model=TranslateResponse,
    summary="Translate text into a target language",
)
def translate(request: TranslateRequest):
    logger.info("Received /translate request (target_language=%s)", request.target_language)
    translated = ai_service.translate_text(request.text, request.target_language)
    return TranslateResponse(
        translated_text=translated,
        target_language=request.target_language,
    )


@router.post(
    "/generate-email",
    response_model=GenerateEmailResponse,
    summary="Generate an email draft for a given purpose and tone",
)
def generate_email(request: GenerateEmailRequest):
    logger.info("Received /generate-email request (tone=%s)", request.tone)
    result = ai_service.generate_email(
        purpose=request.purpose,
        tone=request.tone,
        recipient_name=request.recipient_name,
    )
    return GenerateEmailResponse(subject=result["subject"], body=result["body"])
