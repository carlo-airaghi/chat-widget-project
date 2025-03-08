import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path

from haystack import Pipeline
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack.components.converters import PyPDFToDocument

# Custom PromptBuilder che ignora la validazione degli input extra
class LenientPromptBuilder(PromptBuilder):
    def validate_inputs(self, **kwargs):
        # Sovrascriviamo il metodo di validazione per non lanciare errori per input extra.
        return

    def build_prompt(self, **inputs):
        # Filtra solo le chiavi usate nel template, così eventuali valori mancanti non verranno considerati
        allowed_keys = set(self.template_variables) if hasattr(self, "template_variables") else set()
        filtered_inputs = {k: v for k, v in inputs.items() if k in allowed_keys}
        return super().build_prompt(**filtered_inputs)

widget_name = 'static_theapeshape'

app = Flask(__name__, static_folder=widget_name)
CORS(app)

# Legge l'API key dalle variabili d'ambiente
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables.")

# Setup del document store in memoria
document_store = InMemoryDocumentStore()

# Directory contenente i PDF (dentro 'static_theapeshape/documents')
pdf_dir = Path(app.static_folder) / 'documents'

def index_pdf_documents(directory: Path):
    """
    Converte tutti i PDF nella directory in Document e li scrive nel document store.
    """
    converter = PyPDFToDocument()
    documents = []
    for pdf_file in directory.glob('*.pdf'):
        result = converter.run(sources=[pdf_file])
        docs = result.get('documents', [])
        for doc in docs:
            doc.meta['filename'] = pdf_file.name
        documents.extend(docs)
    document_store.write_documents(documents)

# Indicizza tutti i PDF all'avvio
index_pdf_documents(pdf_dir)

# Template per il prompt (lo stesso di prima)
prompt_template = """
Reply in Italian.

### Dati del Cliente
- **ID**: {{customer_id}}
- **Nome e Cognome**: {{customer_name}} {{customer_surname}}
- **Età**: {{customer_age}}
- **Sesso**: {{customer_sesso}}
- **Peso**: {{customer_weight}}
- **Altezza**: {{customer_height}}
- **Distretto Carente 1**: {{customer_distretto_carente1}}
- **Distretto Carente 2**: {{customer_distretto_carente2}}
- **Percentuale Massa Grassa**: {{customer_percentuale_massa_grassa}}
- **Dispendio Calorico**: {{customer_dispendio_calorico}}
  - **Valori di riferimento**:
    - circa 1.2: Nessun allenamento, cammini poco, lavori da seduto (circa 4000 passi/giorno);
    - circa 1.35: Allenamento 3 volte a settimana, cammini poco, lavori da seduto (4000-8000 passi/giorno);
    - circa 1.58: Allenamento 3-4 volte a settimana, cammini abbastanza, lavori in piedi (8000-12000 passi/giorno);
    - circa 1.78: Allenamento 4 o più volte a settimana, cammini molto, lavori in piedi (12000-16000 passi/giorno).

### Dieta
- **Tipo di Dieta**: {{customer_diet_type}}
  - 1 => Perdere massa grassa  
  - 2 => Aumentare massa magra
- **Istruzioni Dieta**:
  - Prima di proporre una dieta, chiedi al cliente se ha patologie o condizioni mediche rilevanti.
  - Se suggerisci una dieta, basati sul documento "alimentazione".
  - Per domande relative a una dieta completa, informa il cliente che è possibile prenotare un appuntamento con il nutrizionista nella sezione "Macro".

### Programma di Allenamento
- **Macroblocco**: {{customer_macroblocco}} (blocco di 13 settimane)
- **Settimana**: {{customer_week}}
- **Giorno**: {{customer_day}}
- **Esercizio Selezionato**: {{customer_exercise_selected}}
- **Istruzioni Allenamento**:
  - Suggerisci **soltanto esercizi presenti nell'app**, consultando il documento "lista esercizi".
  - Se il cliente esprime reticenza a causa di un infortunio, invitalo a eseguire l'esercizio per valutare la presenza di dolore.
    - Se il dolore risulta non gestibile, proponi un esercizio alternativo secondo le indicazioni del documento "allenamento".

### Dati Nutrizionali Aggiuntivi
- **Kcal**: {{customer_kcal}}
- **Grassi (g)**: {{customer_fats}}
- **Proteine (g)**: {{customer_proteins}}
- **Carboidrati (g)**: {{customer_carbs}}

### Impostazioni di Test
- **Settimana Test Esercizi**: {{customer_settimana_test_esercizi}}
- **Settimana Test Pesi**: {{customer_settimana_test_pesi}}
- **Workout della Settimana (se rilevante)**:
  {{customer_workout_della_settimna}}

### Abbonamento e Localizzazione
- **Luogo**: {{customer_city}}, {{customer_province}}, {{customer_country}}
- **Abbonamento**:
  - **Scadenza**: {{customer_sub_expire}}
  - **Tipo**: {{customer_sub_type}}
    - 0 => Prova gratuita
    - 1 => Mensile
    - 2 => Trimestrale
    - 3 => Annuale

### Cronologia Conversazione
Ultimi messaggi (dal più vecchio al più recente):
{% for msg in conversation_history %}
- {{msg.role}}: {{msg.content}}
{% endfor %}

### Documenti di Riferimento
I seguenti documenti contengono le informazioni necessarie:
{% for doc in documents %}
- {{ doc.content }}
{% endfor %}

### Domanda
Question: {{question}}

---

Provide a detailed answer taking into account all the above data and instructions.
"""

# Istanzio i componenti della pipeline usando il prompt builder leniente
retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = LenientPromptBuilder(template=prompt_template)
llm = OpenAIGenerator(api_key=Secret.from_token(api_key))

rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")

conversation_histories = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('message', '')
    user_data = data.get('user', {})

    customer_id = user_data.get('Customer_ID') or None
    customer_name = user_data.get('Name') or ''
    customer_surname = user_data.get('Surname') or ''
    customer_age = user_data.get('Age') or ''
    customer_sesso = user_data.get('Sesso') or ''
    customer_weight = user_data.get('Weight') or ''
    customer_height = user_data.get('Height') or ''
    customer_percentuale_massa_grassa = user_data.get('PercentualeMassaGrassa') or ''
    customer_dispendio_calorico = user_data.get('DispendioCalorico') or ''
    customer_diet_type = user_data.get('DietType') or ''
    customer_macroblocco = user_data.get('Macroblocco') or ''
    customer_week = user_data.get('Week') or ''
    customer_day = user_data.get('Day') or ''
    # Anche se vengono passati questi campi extra, il nostro prompt builder leniente li ignorerà.
    customer_exercise_selected = user_data.get('ExerciseSelected') or ''
    customer_country = user_data.get('Country') or ''
    customer_city = user_data.get('City') or ''
    customer_province = user_data.get('Province') or ''
    customer_sub_expire = user_data.get('subExpire') or ''
    customer_sub_type = user_data.get('SubType') or ''

    customer_kcal = user_data.get('Kcal') or ''
    customer_fats = user_data.get('Fats') or ''
    customer_proteins = user_data.get('Proteins') or ''
    customer_carbs = user_data.get('Carbs') or ''
    customer_settimana_test_esercizi = user_data.get('SettimanaTestEsercizi') or ''
    customer_settimana_test_pesi =user_data.get('SettimanaTestPesi') or ''
    customer_workout_della_settimna = user_data.get('WorkoutDellaSettimna') or {}
    customer_distretto_carente1 = user_data.get('customerDistrettoCarente1') or ''
    customer_distretto_carente2 = user_data.get('customerDistrettoCarente2') or ''

    if not customer_id:
        return jsonify({'reply': 'Please provide a valid Customer_ID.'}), 400
    if not question:
        return jsonify({'reply': 'Please provide a message.'}), 400

    if customer_id not in conversation_histories:
        conversation_histories[customer_id] = []
    conversation_histories[customer_id].append({"role": "user", "content": question})
    if len(conversation_histories[customer_id]) > 10:
        conversation_histories[customer_id] = conversation_histories[customer_id][-10:]

    recent_messages = conversation_histories[customer_id]

    try:
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
                "customer_macroblocco": customer_macroblocco,
                "customer_week": customer_week,
                "customer_day": customer_day,
                "customer_exercise_selected": customer_exercise_selected,
                "customer_country": customer_country,
                "customer_city": customer_city,
                "customer_province": customer_province,
                "customer_sub_expire": customer_sub_expire,
                "customer_sub_type": customer_sub_type,
                "customer_kcal": customer_kcal,
                "customer_fats": customer_fats,
                "customer_proteins": customer_proteins,
                "customer_carbs": customer_carbs,
                "customer_settimana_test_esercizi": customer_settimana_test_esercizi,
                "customer_settimana_test_pesi": customer_settimana_test_pesi,
                "customer_workout_della_settimna": customer_workout_della_settimna,
                "conversation_history": recent_messages,
                "customer_distretto_carente1": customer_distretto_carente1,
                "customer_distretto_carente2": customer_distretto_carente2
            }
        })

        reply = results["llm"]["replies"][0]

        conversation_histories[customer_id].append({"role": "assistant", "content": reply})
        if len(conversation_histories[customer_id]) > 10:
            conversation_histories[customer_id] = conversation_histories[customer_id][-10:]

        return jsonify({'reply': reply})

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'reply': 'Sorry, an error occurred. Please try again later.'})

@app.route('/history/<customer_id>', methods=['GET'])
def get_conversation_history(customer_id):
    if customer_id not in conversation_histories:
        return jsonify({"history": []}), 200
    return jsonify({"history": conversation_histories[customer_id]}), 200

@app.route('/deleteHistory/<customer_id>', methods=['DELETE'])
def delete_history(customer_id):
    if customer_id in conversation_histories:
        del conversation_histories[customer_id]
        return jsonify({"success": True, "message": "Conversation history deleted."}), 200
    else:
        return jsonify({"success": False, "message": "No conversation history found for this user."}), 404

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
