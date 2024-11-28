from flask import Flask, request, jsonify, send_from_directory
import os
import openai

app = Flask(__name__, static_folder='static')

# Enable CORS
from flask_cors import CORS
CORS(app)

# Set up OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'reply': 'Per favore, scrivi un messaggio.'})

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use your preferred model
            messages=[
                {"role": "user", "content": message}
            ]
        )
        assistant_reply = response['choices'][0]['message']['content']

        return jsonify({'reply': assistant_reply})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'reply': 'Spiacenti, si è verificato un errore. Per favore riprova più tardi.'})

# Route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
