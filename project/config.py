import os
from pathlib import Path

class Config:
    # --------------------------------------------------
    # DeepSeek (OpenAI-compatible) settings
    # --------------------------------------------------
    OPENAI_API_KEY      = os.environ.get("OPENAI_API_KEY")
    OPENAI_API_BASE_URL = os.environ.get(
        "OPENAI_API_BASE_URL",
        "https://api.deepseek.com/v1"      # DeepSeek’s OpenAI-compatible endpoint
    )

    PROMPT_COST = 2.5 / 1_000_000
    OUTPUT_COST = 10  / 1_000_000

    if not OPENAI_API_KEY:
        raise ValueError("No OPENAI_API_KEY found in environment variables.")

    # --------------------------------------------------
    # Local folders
    # --------------------------------------------------
    STATIC_FOLDER   = "static_theapeshape"
    DOCUMENTS_FOLDER = Path(STATIC_FOLDER) / "documents"
    PROMPTS_FOLDER   = Path("prompts")
