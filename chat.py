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

def get_response(sentence, user_id, bot_name):
    global chat_state, user_data

    if chat_state == "initial":
        response = f"Hola soy {bot_name} asesor virtual, ¿cómo puedo ayudarte?"
        chat_state = "awaiting_assistance"
    elif chat_state == "awaiting_assistance":
        # Código para manejar la respuesta del usuario
        response = "Te voy a asignar un asesor, dame tu nombre por favor."
        chat_state = "awaiting_name"
    elif chat_state == "awaiting_name":
        user_data["name"] = sentence
        response = "Ahora dame tu correo o WhatsApp."
        chat_state = "awaiting_contact"
    elif chat_state == "awaiting_contact":
        user_data["contact"] = sentence
        # Guardar nombre y contacto en la base de datos
        save_user_data(user_id, user_data["name"], user_data["contact"])
        response = "Excelente! Te pondré en contacto con un asesor, si necesitas algo más solo dime."
        chat_state = "initial"
    else:
        response = "No entiendo..."

    return response

