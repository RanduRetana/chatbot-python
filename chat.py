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

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "botberto"
awaiting_name_email = False


def get_response(sentence):
    global awaiting_name_email
    response = ""

    if awaiting_name_email:
        try:
            # Asume que el usuario proporciona los datos separados por comas
            name, email = sentence.split(",")
            save_user_data(name.strip(), email.strip())
            response = f"{bot_name}: Datos guardados exitosamente."
            awaiting_name_email = False
        except ValueError:
            response = f"{bot_name}: Por favor, proporciona tu nombre y correo electrónico separados por una coma."
        finally:
            awaiting_name_email = False
    else:
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)
        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            if tag == "save_data":
                awaiting_name_email = True
                response = f"{bot_name}: Por favor, dame tu nombre y correo electrónico."
            else:
                for intent in intents['intents']:
                    if tag == intent["tag"]:
                        response = f"{bot_name}: {random.choice(intent['responses'])}"
        else:
            response = f"{bot_name}: No entiendo..."

    return response
