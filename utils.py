import random
import json
import numpy as np
import os

import nltk
from sklearn.preprocessing import LabelEncoder
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()

# Ruta absoluta al archivo words.json
words_path = os.path.join(os.path.dirname(__file__), 'words.json')
# Ruta absoluta al archivo classes.json
classes_path = r'D:\RESPALDO_ESCRITORIO\Portfolio\Martin\classes.json'
# Ruta absoluta al archivo chatbot_model.h5
model_path = os.path.join(os.path.dirname(__file__), 'chatbot_model.h5')

# Cargar datos desde archivos JSON
with open('words.json', 'r') as file:
    words = json.load(file)
with open(classes_path, 'r') as file:
    classes = json.load(file)
# cargar el modelo
model = load_model(model_path)

# Cargar el encoder
le = LabelEncoder()
le.fit(classes)

def cleanUpsentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bagOfwords(sentence):
    sentence_words = cleanUpsentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1    
    return np.array(bag)  

def predictClass(sentence):
    bow = bagOfwords(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(intents_list, intents_json):
    # Asegúrate de que intents_list tiene al menos un elemento
    if not intents_list:
        return "Lo siento, no puedo identificar ninguna intención."

    # Obtén el nombre de la intención desde intents_list
    intent_name = intents_list[0]['intent']
    # Verifica que 'intents' esté presente en intents_json
    if 'intents' not in intents_json:
        return "Lo siento, la estructura de datos no es válida."
    # Itera sobre la lista de 'intents' dentro de intents_json
    for intent in intents_json['intents']:  # Aquí accedemos a la clave 'intents'
        # Compara el 'intent' de cada intent con el intent_name
        if intent['intent'] == intent_name:  # Compara con 'tag'
            return random.choice(intent['responses'])
    # Si no se encuentra el intent
    return "Lo siento, no entiendo lo que dices."