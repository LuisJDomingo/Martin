import random
import json
import numpy as np
import os
import nltk
from sklearn.preprocessing import LabelEncoder
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Ruta base de la carpeta actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas de los archivos
words_path = os.path.join(BASE_DIR, 'data', 'words.json')
classes_path = os.path.join(BASE_DIR, 'data', 'classes.json')
model_path = os.path.join(BASE_DIR, 'data', 'chatbot_model.h5')

# Cargar datos desde archivos JSON
with open(words_path, 'r') as file:
    words = json.load(file)

with open(classes_path, 'r') as file:
    classes = json.load(file)

# Cargar el modelo
model = load_model(model_path)

# Inicializar el encoder
le = LabelEncoder()
le.fit(classes)

def cleanUpsentence(sentence):
    #print('empieza la limpieza')
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bagOfwords(sentence):
    #print('empieza la bolsa')
    sentence_words = cleanUpsentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1    
    return np.array(bag)  

def predictClass(sentence):
    print('empieza la prediccion')
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
    print('empieza la get response')
    if not intents_list:
        return "Lo siento, no puedo identificar ninguna intención."

    intent_name = intents_list[0]['intent']
    if 'intents' not in intents_json:
        return "Lo siento, la estructura de datos no es válida."

    for intent in intents_json['intents']:
        if intent['intent'] == intent_name:
            return random.choice(intent['responses'])
    return "Lo siento, no entiendo lo que dices."
