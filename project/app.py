import logging
import os

from flask import Flask
from flask_cors import CORS
from openai import OpenAI, OpenAIError

from config import Config
from utils import ConversationManager
from routes import create_blueprint

# ── Logging ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)

# ── Flask App ────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
CORS(app)

# ── OpenAI client ────────────────────────────────────────────────────────
client = OpenAI(
    api_key  = Config.OPENAI_API_KEY,
    base_url = Config.OPENAI_API_BASE_URL,
)

# ── Verifica vector‑store una sola volta all’avvio ───────────────────────
try:
    vs = client.vector_stores.retrieve(Config.OPENAI_VECTOR_STORE_ID)

    counts = (
        vs.file_counts.model_dump()
        if hasattr(vs.file_counts, "model_dump")          # pydantic ≥2
        else vs.file_counts.dict()                       # pydantic 1.x
    )

    logging.info(
        "Vector‑store «%s» trovato – %d file (completati: %d, falliti: %d, stato: %s)",
        vs.id,
        counts.get("total", 0),
        counts.get("completed", 0),
        counts.get("failed", 0),
        vs.status,
    )
except OpenAIError as e:
    logging.critical("Vector‑store %s inesistente o inaccessibile: %s",
                     Config.OPENAI_VECTOR_STORE_ID, e)
    raise

# ── Blueprint & helpers ──────────────────────────────────────────────────
conversation_manager = ConversationManager()
chat_bp = create_blueprint(client, conversation_manager, app.config)
app.register_blueprint(chat_bp)

# ── Run (dev) ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port, debug=True)
