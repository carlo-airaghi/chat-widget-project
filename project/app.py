from flask import Flask
from flask_cors import CORS
from pathlib import Path
import logging

from config import Config
from indexers import index_pdf_documents, index_csv_documents
from pipelines import create_pipeline
from utils import ConversationManager
from haystack.document_stores.in_memory import InMemoryDocumentStore
from routes import create_blueprint

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Create the Flask app and configure it.
app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)
CORS(app)

# Create an in-memory document store.
document_store = InMemoryDocumentStore()

# Index documents from the specific folders.
index_pdf_documents(Config.DOCUMENTS_FOLDER, document_store)
index_csv_documents(Config.DOCUMENTS_FOLDER, document_store)

# Read prompt template from file.
prompts_folder = Config.PROMPTS_FOLDER
prompt_template_path = prompts_folder / "prompt_template.txt"

with prompt_template_path.open("r", encoding="utf-8") as f:
    prompt_template = f.read()

# Create the pipeline.
pipeline = create_pipeline(prompt_template, Config.OPENAI_API_KEY, document_store, model_name="gpt-4o")

# Initialize the conversation manager.
conversation_manager = ConversationManager()

# Register the Blueprint.
chat_bp = create_blueprint(pipeline, conversation_manager)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
