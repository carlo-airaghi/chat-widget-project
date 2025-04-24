# app.py
import os
import logging
from pathlib import Path

from flask import Flask
from flask_cors import CORS

from config import Config
from indexers import index_pdf_documents, index_csv_documents
from pipelines import create_pipeline
from utils import ConversationManager
from haystack.document_stores.in_memory import InMemoryDocumentStore
from routes import create_blueprint

# ——— Logging ————————————————————————————
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ——— Flask App Setup —————————————————————
app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
CORS(app)

# ——— Document Store & Indexing ——————————————————
document_store = InMemoryDocumentStore()
index_pdf_documents(Config.DOCUMENTS_FOLDER, document_store)
index_csv_documents(Config.DOCUMENTS_FOLDER, document_store)

# ——— Prompt Template ——————————————————————
prompt_template_path = Config.PROMPTS_FOLDER / "prompt_template.txt"
with prompt_template_path.open("r", encoding="utf-8") as f:
    prompt_template = f.read()

# ——— Pipeline ———————————————————————————
pipeline = create_pipeline(
    prompt_template,
    Config.OPENAI_API_KEY,
    document_store,
    model_name=Config.OPENAI_MODEL
)

# ——— Conversation Manager & Routes ——————————
conversation_manager = ConversationManager()
chat_bp = create_blueprint(pipeline, conversation_manager)
app.register_blueprint(chat_bp)

# ——— Run —————————————————————————————
if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port)