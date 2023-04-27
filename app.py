from flask import send_from_directory
from flask import Flask, render_template, request, jsonify
from chat import get_response
from flask_cors import CORS
import uuid
import os

app = Flask(__name__)
CORS(app)


def generate_unique_id():
    return str(uuid.uuid4())


@app.route('/register_chatbot_user', methods=['POST'])
def register_chatbot_user():
    user_data = request.get_json()
    user_id = generate_unique_id()
    # Guarda el ID único y los demás datos del usuario en la base de datos
    # ...
    return jsonify({"user_id": user_id})


@app.get('/')
def index_get():
    return render_template('base.html')


@app.post('/predict')
def predict():
    data = request.get_json()
    text = data.get("message")
    user_id = data.get("user_id")
    response = get_response(text, user_id)
    return jsonify({"response": response})


@app.route('/chatbot_loader.js')
def chatbot_loader():
    return send_from_directory('static', 'chatbot_loader.js')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

