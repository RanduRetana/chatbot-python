import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from database import save_user_data

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]
chat_state = "initial"
user_data = {}


model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

awaiting_name_email = False

chat_state = {}  # Cambiar a un diccionario

def get_response(sentence, session_id, bot_name, empresa_name):
    global chat_state, user_data

    if session_id not in chat_state:
        chat_state[session_id] = "initial"

    if chat_state[session_id] == "initial":
        response = f"Hola soy {bot_name} asesor virtual de {empresa_name}, ¿cómo puedo ayudarte?"
        chat_state[session_id] = "awaiting_assistance"
    elif chat_state[session_id] == "awaiting_assistance":
        # Código para manejar la respuesta del usuario
        response = "Te voy a asignar un asesor, dame tu nombre por favor."
        chat_state[session_id] = "awaiting_name"
    elif chat_state[session_id] == "awaiting_name":
        user_data["name"] = sentence
        response = "Ahora dame tu correo o WhatsApp."
        chat_state[session_id] = "awaiting_contact"
    elif chat_state[session_id] == "awaiting_contact":
        user_data["contact"] = sentence
        # Guardar nombre y contacto en la base de datos
        save_user_data(session_id, user_data["name"], user_data["contact"])
        response = "Excelente! Te pondré en contacto con un asesor, si necesitas algo más solo dime."
        chat_state[session_id] = "initial"
    else:
        response = "No entiendo..."

    return response


