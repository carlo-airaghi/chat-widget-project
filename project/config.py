import os
from pathlib import Path

class Config:
    # ── OpenAI ────────────────────────────────────────────────────────────
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY env‑var is required")

    OPENAI_API_BASE_URL = os.environ.get(
        "OPENAI_API_BASE_URL",
        "https://api.openai.com/v1"
    )

    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
    OPENAI_VECTOR_STORE_ID = os.environ.get("OPENAI_VECTOR_STORE_ID", "")

    # ── Pricing (USD/token) ───────────────────────────────────────────────
    PROMPT_COST = 2.5 / 1_000_000     # adjust for your plan / model
    OUTPUT_COST = 10  / 1_000_000

    # ── Local folders ─────────────────────────────────────────────────────
    STATIC_FOLDER  = "static_theapeshape"
    PROMPTS_FOLDER = Path("prompts")
