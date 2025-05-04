import logging
import os

from flask import Flask
from flask_cors import CORS
from openai import OpenAI

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

# ── OpenAI client & helpers ──────────────────────────────────────────────
client = OpenAI(
    api_key  = Config.OPENAI_API_KEY,
    base_url = Config.OPENAI_API_BASE_URL,
)

conversation_manager = ConversationManager()

# Pass app.config to avoid current_app lookups during import
chat_bp = create_blueprint(client, conversation_manager, app.config)
app.register_blueprint(chat_bp)

# ── Run (dev) ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port, debug=True)
