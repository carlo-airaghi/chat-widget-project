import os
from flask import Flask, request, jsonify, send_from_directory
from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from flask_cors import CORS

widget_name = 

app = Flask(__name__, static_folder='static_theapeshape')
CORS(app)

# Read the API key from environment variables
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables.")

# Write documents to InMemoryDocumentStore
document_store = InMemoryDocumentStore()
document_store.write_documents([
    Document(content="Il mio nome è Jean e vivo a Parigi."),
    Document(content="Il mio nome è Mark e vivo a Berlino."),
    Document(content="Il mio nome è Giorgio e vivo a Roma.")
])

# Build a RAG pipeline
prompt_template = """
Dato questi documenti, rispondi alla domanda.
Documenti:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}
Domanda: {{question}}
Risposta:
"""

retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = PromptBuilder(template=prompt_template)

# Initialize the OpenAI generator
llm = OpenAIGenerator(api_key=Secret.from_token(api_key))

rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('message', '')

    if not question:
        return jsonify({'reply': 'Per favore, scrivi un messaggio.'})

    try:
        # Run the RAG pipeline
        results = rag_pipeline.run(
            {
                "retriever": {"query": question},
                "prompt_builder": {"question": question},
            }
        )
        reply = results["llm"]["replies"][0]  # Get the generated reply
        return jsonify({'reply': reply})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'reply': 'Spiacenti, si è verificato un errore. Per favore riprova più tardi.'})

# Route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
