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

# Create two separate in-memory document stores.
diet_document_store = InMemoryDocumentStore()
general_document_store = InMemoryDocumentStore()

# Index documents from the specific folders.
index_pdf_documents(Config.DIET_DOCUMENTS_FOLDER, diet_document_store)
index_csv_documents(Config.DIET_DOCUMENTS_FOLDER, diet_document_store)
index_pdf_documents(Config.GENERAL_DOCUMENTS_FOLDER, general_document_store)
index_csv_documents(Config.GENERAL_DOCUMENTS_FOLDER, general_document_store)

# Read prompt templates from files in the prompts folder.
prompts_folder = Config.PROMPTS_FOLDER
diet_prompt_template_path = prompts_folder / "diet_prompt_template.txt"
prompt_template_path = prompts_folder / "prompt_template.txt"

with diet_prompt_template_path.open("r", encoding="utf-8") as f:
    diet_prompt_template = f.read()

with prompt_template_path.open("r", encoding="utf-8") as f:
    prompt_template = f.read()

# Create the pipelines with the appropriate model names and document stores.
diet_pipeline = create_pipeline(diet_prompt_template, Config.OPENAI_API_KEY, diet_document_store, model_name="o3-mini")
final_pipeline = create_pipeline(prompt_template, Config.OPENAI_API_KEY, general_document_store, model_name="gpt-4o-mini")

# Initialize the conversation manager.
conversation_manager = ConversationManager()

# Register the Blueprint containing our routes.
chat_bp = create_blueprint(diet_pipeline, final_pipeline, conversation_manager)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
