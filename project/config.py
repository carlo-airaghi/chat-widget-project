# config.py
import os
from pathlib import Path

class Config:
    # Read the OpenAI API key from environment variables.
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise ValueError("No OPENAI_API_KEY found in environment variables.")

    # Define folders for static files, documents, and prompts.
    STATIC_FOLDER = 'static_theapeshape'
    DOCUMENTS_FOLDER = Path(STATIC_FOLDER) / 'documents'
    PROMPTS_FOLDER = Path("prompts")

    # New: separate folders for diet and general documents
    DIET_DOCUMENTS_FOLDER = DOCUMENTS_FOLDER / "diet"
    GENERAL_DOCUMENTS_FOLDER = DOCUMENTS_FOLDER / "general"
