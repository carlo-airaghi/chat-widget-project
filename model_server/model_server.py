import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import (
    AutoModelForCausalLM,
    AutoModelForMaskedLM,
    AutoTokenizer,
)
import torch

app = Flask(__name__)
CORS(app)

# Get model name and type from environment variables
MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_TYPE = os.getenv('MODEL_TYPE')  # 'causal' or 'masked'

if not MODEL_NAME:
    raise ValueError("MODEL_NAME environment variable not set.")

if not MODEL_TYPE:
    raise ValueError("MODEL_TYPE environment variable not set.")

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('./model')
if MODEL_TYPE == 'causal':
    model = AutoModelForCausalLM.from_pretrained('./model')
elif MODEL_TYPE == 'masked':
    model = AutoModelForMaskedLM.from_pretrained('./model')
else:
    raise ValueError("Invalid MODEL_TYPE. Choose 'causal' or 'masked'.")


model.eval()

# Move to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Initialize conversation history
conversation_history = []

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    user_message = data.get('message', '')

    # Append user message to history
    conversation_history.append(f"User: {user_message}")

    # Prepare the prompt
    prompt = "\n".join(conversation_history) + "\nAssistant:"

    # Tokenize input
    inputs = tokenizer.encode(prompt, return_tensors='pt').to(device)

    # Generate text
    with torch.no_grad():
        if MODEL_TYPE == 'causal':
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 100,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                early_stopping=True
            )
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract assistant's reply
            assistant_reply = generated_text[len(prompt):].strip()
        elif MODEL_TYPE == 'masked':
            assistant_reply = "Masked language models are not suitable for text generation in this context."
        else:
            assistant_reply = "Invalid MODEL_TYPE specified."

    # Append assistant reply to history
    conversation_history.append(f"Assistant: {assistant_reply}")

    return jsonify({'reply': assistant_reply})

if __name__ == '__main__':
    port = int(os.getenv('MODEL_SERVER_PORT', 8000))
    app.run(host='0.0.0.0', port=port)
