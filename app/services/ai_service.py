"""
Service layer that wraps calls to the Gemini API.
Keeping this separate from the routers means the routers stay thin
(just validation + calling the service) and the AI logic / prompts
live in one place.
"""

import logging

from google import genai

from app.core.config import settings
from app.core.exceptions import AIServiceError

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=settings.gemini_api_key)


def _call_gemini(prompt: str) -> str:
    """Single shared entry point for all Gemini calls, with consistent
    error handling so routers don't need to know about the SDK at all."""
    try:
        response = _client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
        if not response or not response.text:
            raise AIServiceError("AI provider returned an empty response.")
        return response.text.strip()
    except AIServiceError:
        raise
    except Exception as exc:
        logger.exception("Gemini API call failed")
        raise AIServiceError(f"Failed to get a response from the AI provider: {exc}")


def summarize_text(text: str, max_words: int) -> str:
    prompt = (
        f"Summarize the following text in no more than {max_words} words. "
        f"Be concise and preserve the key points only.\n\n"
        f"Text:\n{text}"
    )
    logger.info("Calling Gemini for summarization (max_words=%s)", max_words)
    return _call_gemini(prompt)


def translate_text(text: str, target_language: str) -> str:
    prompt = (
        f"Translate the following text into {target_language}. "
        f"Return ONLY the translated text, with no extra commentary.\n\n"
        f"Text:\n{text}"
    )
    logger.info("Calling Gemini for translation (target_language=%s)", target_language)
    return _call_gemini(prompt)


def generate_email(purpose: str, tone: str, recipient_name: str | None) -> dict:
    recipient_part = f" addressed to {recipient_name}" if recipient_name else ""
    prompt = (
        f"Write a {tone} email{recipient_part} for the following purpose: {purpose}.\n"
        f"Respond strictly in this format, with no extra text before or after:\n"
        f"SUBJECT: <subject line>\n"
        f"BODY:\n<email body>"
    )
    logger.info("Calling Gemini for email generation (tone=%s)", tone)
    raw = _call_gemini(prompt)

    subject = "Generated Email"
    body = raw

    if "SUBJECT:" in raw and "BODY:" in raw:
        try:
            subject_part = raw.split("SUBJECT:", 1)[1].split("BODY:", 1)[0].strip()
            body_part = raw.split("BODY:", 1)[1].strip()
            subject = subject_part or subject
            body = body_part or body
        except IndexError:
            logger.warning("Could not parse SUBJECT/BODY from Gemini response, returning raw text.")

    return {"subject": subject, "body": body}
