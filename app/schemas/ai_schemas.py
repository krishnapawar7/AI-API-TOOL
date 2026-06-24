"""
Pydantic models used to validate incoming requests and shape outgoing
responses. FastAPI uses these automatically to return 422 errors for
bad input, and to generate the OpenAPI/Swagger docs.
"""

from pydantic import BaseModel, Field, field_validator


# ---------- /summarize ----------

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=20000,
                       description="The text to summarize (min 20 characters).")
    max_words: int = Field(100, ge=10, le=500,
                            description="Approximate maximum length of the summary in words.")

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank or whitespace only")
        return v


class SummarizeResponse(BaseModel):
    success: bool = True
    summary: str


# ---------- /translate ----------

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000,
                       description="The text to translate.")
    target_language: str = Field(..., min_length=2, max_length=50,
                                  description="Target language, e.g. 'French', 'Hindi', 'es'.")

    @field_validator("text", "target_language")
    @classmethod
    def must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("field must not be blank or whitespace only")
        return v


class TranslateResponse(BaseModel):
    success: bool = True
    translated_text: str
    target_language: str


# ---------- /generate-email ----------

class GenerateEmailRequest(BaseModel):
    purpose: str = Field(..., min_length=5, max_length=2000,
                          description="What the email is about, e.g. 'follow up after interview'.")
    tone: str = Field("professional", min_length=2, max_length=30,
                       description="Tone of the email, e.g. 'professional', 'friendly', 'formal'.")
    recipient_name: str | None = Field(None, max_length=100,
                                        description="Optional recipient name to personalize the email.")

    @field_validator("purpose")
    @classmethod
    def purpose_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("purpose must not be blank or whitespace only")
        return v


class GenerateEmailResponse(BaseModel):
    success: bool = True
    subject: str
    body: str
