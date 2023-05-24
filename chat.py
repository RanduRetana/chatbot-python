import random
import json
import torch
from database import save_user_data, get_user_url


chat_state = "initial"
user_data = {}


awaiting_name_email = False

chat_state = {}  # Cambiar a un diccionario


def get_response(sentence, session_id, bot_name, saludo, despedida):
    global chat_state, user_data

    userId = session_id.split("_")[0]
    user_url = get_user_url(userId)
    if session_id not in chat_state:
        chat_state[session_id] = "initial"

    if chat_state[session_id] == "initial":
        response = saludo
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
        response = despedida
        chat_state[session_id] = "initial"
    else:
        response = "No entiendo..."

    return response


