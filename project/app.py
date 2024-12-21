import os
from flask import Flask, request, jsonify, send_from_directory
from haystack import Pipeline
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from flask_cors import CORS
from pathlib import Path
from haystack.components.converters import PyPDFToDocument

widget_name = 'static_theapeshape'

app = Flask(__name__, static_folder=widget_name)
CORS(app)

# Read the API key from environment variables
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables.")

# Set up the in-memory document store
document_store = InMemoryDocumentStore()

# Define the directory containing PDFs (within the 'static_theapeshape/documents' folder)
pdf_dir = Path(app.static_folder) / 'documents'

def index_pdf_documents(directory: Path):
    """
    Converts all PDFs in the specified directory to Document objects 
    and writes them to the in-memory document store.
    """
    converter = PyPDFToDocument()
    documents = []
    for pdf_file in directory.glob('*.pdf'):
        # Convert PDF to Document
        result = converter.run(sources=[pdf_file])
        docs = result.get('documents', [])
        # Add metadata to each document
        for doc in docs:
            doc.meta['filename'] = pdf_file.name
        documents.extend(docs)
    # Write documents into the document store
    document_store.write_documents(documents)

# Index all PDFs at startup (only once)
index_pdf_documents(pdf_dir)

# Define the prompt template for the PromptBuilder
prompt_template = """
Use the following customer data to contextualize the answer:
Customer Name: {{customer_name}}
Customer Height: {{customer_height}}
Customer Weight: {{customer_weight}}

Here are the last messages of the conversation (from oldest to newest):
{% for msg in conversation_history %}
- {{msg.role}}: {{msg.content}}
{% endfor %}

Given these documents, answer the question.
Documents:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}

Question: {{question}}
Answer:
"""

retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = PromptBuilder(template=prompt_template)
llm = OpenAIGenerator(api_key=Secret.from_token(api_key))

# Create a pipeline that retrieves documents, builds a prompt, then calls the LLM
rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")

# A dictionary to store conversation histories in memory
# Key: customer_id, Value: list of messages, each as { "role": ..., "content": ... }
conversation_histories = {}

@app.route('/chat', methods=['POST'])
def chat():
    """
    Receives JSON data (with 'message' and 'user' fields), processes it, 
    and returns an AI-generated response.
    """
    data = request.get_json()

    # Extract the question/message from the JSON
    question = data.get('message', '')

    # Extract user data (the entire user object) from the JSON
    user_data = data.get('user', {})

    # Example of how to fetch some specific fields:
    customer_id = user_data.get('Customer_ID', None)
    customer_name = user_data.get('Name', '')
    customer_height = user_data.get('Height', '')
    customer_weight = user_data.get('Weight', '')

    # Check for necessary fields
    if not customer_id:
        return jsonify({'reply': 'Please provide a valid Customer_ID.'}), 400

    if not question:
        return jsonify({'reply': 'Please provide a message.'}), 400

    # Initialize a conversation history for this customer if none exists
    if customer_id not in conversation_histories:
        conversation_histories[customer_id] = []

    # Append the user's message to conversation history
    conversation_histories[customer_id].append({"role": "user", "content": question})
    if len(conversation_histories[customer_id]) > 10:
        conversation_histories[customer_id] = conversation_histories[customer_id][-10:]

    # Get the most recent messages (last 10)
    recent_messages = conversation_histories[customer_id]

    try:
        # Run the pipeline with the user's question
        results = rag_pipeline.run(
            {
                "retriever": {"query": question},
                "prompt_builder": {
                    "question": question,
                    "customer_name": customer_name,
                    "customer_height": customer_height,
                    "customer_weight": customer_weight,
                    "conversation_history": recent_messages
                },
            }
        )
        reply = results["llm"]["replies"][0]

        # Add the assistant's response to the conversation history
        conversation_histories[customer_id].append({"role": "assistant", "content": reply})
        if len(conversation_histories[customer_id]) > 10:
            conversation_histories[customer_id] = conversation_histories[customer_id][-10:]

        return jsonify({'reply': reply})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'reply': 'Sorry, an error occurred. Please try again later.'})

@app.route('/history/<customer_id>', methods=['GET'])
def get_conversation_history(customer_id):
    """
    Returns the conversation history for the specified customer_id.
    If none is found, it returns an empty list.
    """
    if customer_id not in conversation_histories:
        return jsonify({"history": []}), 200
    return jsonify({"history": conversation_histories[customer_id]}), 200

@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Serves static files (e.g., images, CSS, PDF documents) from the 'static' folder.
    """
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
