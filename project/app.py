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

# Expanded prompt template to include all user data
prompt_template = """
Reply in italian 
Use the following customer data to contextualize the answer:

Customer ID: {{customer_id}}
Name: {{customer_name}}
Surname: {{customer_surname}}
Age: {{customer_age}}
Gender (Sesso): {{customer_sesso}}
Weight: {{customer_weight}}
Height: {{customer_height}}
Body Fat % (PercentualeMassaGrassa): {{customer_percentuale_massa_grassa}}
Caloric Expenditure (DispendioCalorico): {{customer_dispendio_calorico}}
I valori del dispendio calorico hanno il seguente significato
- circa 1.2 => Nessun allenamento, cammini poco e lavori da seduto. Circa 4000 passi al giorno; 
- circa 1.35 => Allenamento 3 volte a settimana, cammini poco e lavori da seduto. Da 4000 a 8000 passi al giorno; 
- circa 1.58 => Allenamento 3 o 4 volte a settimana, cammini abbastanza e lavori in piedi. Da 8000 a 12000 passi al giorno; 
- circa 1.78 => Allenamento 4 volte o più a settimana, cammini molto e lavori in piedi. Da 12000 a 16000 passi al giorno.
Diet Type: {{customer_diet_type}}
I valori del Diet Type hanno il seguente significato 
- 1: Perdere massa grassa; 
- 2: Aumentare massa magra
Macro Fase: {{customer_macro_fase}} indica il blocco di tredici settimane in cui si trova il cliente
Week: {{customer_week}}  
Day: {{customer_day}}
DistrettoCarente1: {{customer_distretto_carente1}}
DistrettoCarente2: {{customer_distretto_carente2}}
ExerciseSelected: {{customer_exercise_selected}} indica se l'utente ha selezionato gli esercizi per il piano di allenamento
Country: {{customer_contry}}
City: {{customer_city}}
Province: {{customer_province}}
Subscription Expiration (subExpire): {{customer_sub_expire}}
Subscription Type (SubType): {{customer_sub_type}}
- 0 -> prova gratuita, 
- 1 -> mensile, 
- 2 -> trimestrale, 
- 3 -> annuale

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

    # Retrieve all relevant fields from user_data (adjust or add as needed)
    customer_id = user_data.get('Customer_ID', None)
    customer_name = user_data.get('Name', '')
    customer_surname = user_data.get('Surname', '')
    customer_age = user_data.get('Age', '')
    customer_sesso = user_data.get('Sesso', '')
    customer_weight = user_data.get('Weight', '')
    customer_height = user_data.get('Height', '')
    customer_percentuale_massa_grassa = user_data.get('PercentualeMassaGrassa', '')
    customer_dispendio_calorico = user_data.get('DispendioCalorico', '')
    customer_diet_type = user_data.get('DietType', '')
    customer_macro_fase = user_data.get('MacroFase', '')
    customer_week = user_data.get('Week', '')
    customer_day = user_data.get('Day', '')
    customer_distretto_carente1 = user_data.get('DistrettoCarente1', '')
    customer_distretto_carente2 = user_data.get('DistrettoCarente2', '')
    customer_exercise_selected = user_data.get('ExerciseSelected', '')
    customer_contry = user_data.get('Contry', '')  # spelled as in the sample
    customer_city = user_data.get('City', '')
    customer_province = user_data.get('Province', '')
    customer_sub_expire = user_data.get('subExpire', '')
    customer_sub_type = user_data.get('SubType', '')

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
        # Run the pipeline with the user's question and the user data
        results = rag_pipeline.run({
            "retriever": {
                "query": question
            },
            "prompt_builder": {
                "question": question,
                "customer_id": customer_id,
                "customer_name": customer_name,
                "customer_surname": customer_surname,
                "customer_age": customer_age,
                "customer_sesso": customer_sesso,
                "customer_weight": customer_weight,
                "customer_height": customer_height,
                "customer_percentuale_massa_grassa": customer_percentuale_massa_grassa,
                "customer_dispendio_calorico": customer_dispendio_calorico,
                "customer_diet_type": customer_diet_type,
                "customer_macro_fase": customer_macro_fase,
                "customer_week": customer_week,
                "customer_day": customer_day,
                "customer_distretto_carente1": customer_distretto_carente1,
                "customer_distretto_carente2": customer_distretto_carente2,
                "customer_exercise_selected": customer_exercise_selected,
                "customer_contry": customer_contry,
                "customer_city": customer_city,
                "customer_province": customer_province,
                "customer_sub_expire": customer_sub_expire,
                "customer_sub_type": customer_sub_type,
                "conversation_history": recent_messages
            }
        })
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
