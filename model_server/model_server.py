import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)

# Get model name from environment variable or default to GPT-2
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt2')

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.eval()

# Move to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Example of maintaining conversation history
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

    # Append assistant reply to history
    conversation_history.append(f"Assistant: {assistant_reply}")

    return jsonify({'reply': assistant_reply})


if __name__ == '__main__':
    port = int(os.getenv('MODEL_SERVER_PORT', 8000))
    app.run(host='0.0.0.0', port=port)

