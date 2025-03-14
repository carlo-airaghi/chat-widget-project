# app.py
from flask import Flask
from flask_cors import CORS
from pathlib import Path
import logging

# Import our modules.
from config import Config
from indexers import index_pdf_documents, index_csv_documents
from pipelines import create_pipeline
from utils import ConversationManager
from haystack.document_stores.in_memory import InMemoryDocumentStore
from routes import create_blueprint

# Initialize logging.
logging.basicConfig(level=logging.INFO)

# Create the Flask app and configure it.
app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
CORS(app)

# Initialize the in-memory document store.
document_store = InMemoryDocumentStore()

# Index all PDF and CSV documents on startup.
index_pdf_documents(Config.DOCUMENTS_FOLDER, document_store)
index_csv_documents(Config.DOCUMENTS_FOLDER, document_store)

# Read prompt templates from files in the prompts folder.
prompts_folder = Config.PROMPTS_FOLDER
prompt_template_path = prompts_folder / "prompt_template.txt"
rephrase_prompt_template_path = prompts_folder / "rephrase_prompt_template.txt"

with prompt_template_path.open("r", encoding="utf-8") as f:
    prompt_template = f.read()

with rephrase_prompt_template_path.open("r", encoding="utf-8") as f:
    rephrase_prompt_template = f.read()

# Create the pipelines.
rag_pipeline = create_pipeline(prompt_template, Config.OPENAI_API_KEY, document_store)
rephrase_pipeline = create_pipeline(rephrase_prompt_template, Config.OPENAI_API_KEY, document_store)

# Initialize the conversation manager.
conversation_manager = ConversationManager()

# Register the Blueprint containing our routes.
chat_bp = create_blueprint(rag_pipeline, rephrase_pipeline, conversation_manager)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
