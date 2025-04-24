# config.py
import os
from pathlib import Path

class Config:
    # Choose LLM provider: "openai" or "deepseek"
    LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai").lower()

    # API Key (same env var for both providers)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("No OPENAI_API_KEY found in environment variables.")

    # Base URL depends on provider
    if LLM_PROVIDER == "deepseek":
        OPENAI_API_BASE_URL = os.environ.get(
            "OPENAI_API_BASE_URL",
            "https://api.deepseek.com/v1"
        )
    else:
        OPENAI_API_BASE_URL = os.environ.get(
            "OPENAI_API_BASE_URL",
            "https://api.openai.com/v1"
        )

    # Default model name, overridable via env var
    OPENAI_MODEL = os.environ.get(
        "OPENAI_MODEL",
        "deepseek-chat" if LLM_PROVIDER == "deepseek" else "gpt-4o"
    )

    # Cost constants
    PROMPT_COST = 2.5 / 1_000_000
    OUTPUT_COST = 10  / 1_000_000

    # Local folders
    STATIC_FOLDER    = "static_theapeshape"
    DOCUMENTS_FOLDER = Path(STATIC_FOLDER) / "documents"
    PROMPTS_FOLDER   = Path("prompts")