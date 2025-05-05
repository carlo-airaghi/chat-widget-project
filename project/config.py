import os
from pathlib import Path

class Config:
    # ── OpenAI ────────────────────────────────────────────────────────────
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY env‑var is required")

    OPENAI_API_BASE_URL = os.getenv(
        "OPENAI_API_BASE_URL",
        "https://api.openai.com/v1"
    )

    # Vector‑store obbligatorio
    OPENAI_VECTOR_STORE_ID = os.getenv("OPENAI_VECTOR_STORE_ID")
    if not OPENAI_VECTOR_STORE_ID:
        raise ValueError("OPENAI_VECTOR_STORE_ID env‑var is required")

    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # ── Pricing (USD/token) ───────────────────────────────────────────────
    PROMPT_COST  = 2.5 / 1_000_000
    OUTPUT_COST  = 10  / 1_000_000

    # ── Local folders ─────────────────────────────────────────────────────
    STATIC_FOLDER  = "static_theapeshape"
    PROMPTS_FOLDER = Path("prompts")
