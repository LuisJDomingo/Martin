import random
import json
import pickle
import numpy as np

import nltk
from sklearn.preprocessing import LabelEncoder

from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()

# Cargar datos
words = pickle.load(open(r'Martin\ProyectMartin\chatbot\utils\words.pkl', 'rb'))
classes = pickle.load(open(r'Martin\ProyectMartin\chatbot\utils\classes.pkl', 'rb'))

# cargar el modelo
model = load_model(r'Martin\ProyectMartin\chatbot\utils\chatbot_model.h5')

# Cargar el encoder
le = LabelEncoder()
le.fit(classes)

def cleanUpsentence(sentence):
    print(f"Limpiando la oración: {sentence}")  # Debugging: Imprimir la oración original
    sentence_words = nltk.word_tokenize(sentence)
    print(f"Palabras tokenizadas: {sentence_words}")  # Debugging: Ver las palabras tokenizadas
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    print(f"Palabras lematizadas: {sentence_words}")  # Debugging: Ver las palabras lematizadas
    return sentence_words

def bagOfwords(sentence):
    sentence_words = cleanUpsentence(sentence)
    bag = [0] * len(words)
    print(f"Longitud de la bolsa de palabras: {len(words)}")  # Debugging: Ver el tamaño de la bolsa de palabras
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1    
                print(f"Palabra encontrada: {w}, actualizando índice {i}")  # Debugging: Ver cada palabra que coincide y su índice
    print(f"Bolsa de palabras final: {bag}")  # Debugging: Mostrar la bolsa de palabras final
    return np.array(bag)  

def predictClass(sentence):
    bow = bagOfwords(sentence)
    print(f"Bolsa de palabras para la predicción: {bow}")  # Debugging: Ver la bolsa de palabras para la predicción
    res = model.predict(np.array([bow]))[0]
    print(f"Resultados de la predicción: {res}")  # Debugging: Ver los resultados crudos de la predicción

    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    print(f"Resultados filtrados por umbral de error: {results}")  # Debugging: Mostrar resultados después del umbral

    results.sort(key=lambda x: x[1], reverse=True)
    print(f"Resultados ordenados: {results}")  # Debugging: Mostrar resultados ordenados

    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        print(f"Intent identificado: {classes[r[0]]}, con probabilidad: {r[1]}")  # Debugging: Ver cada intento identificado
    return return_list

def getResponse(intents_list, intents_json):
    # Asegúrate de que intents_list tiene al menos un elemento
    if not intents_list:
        return "Lo siento, no puedo identificar ninguna intención."

    # Obtén el nombre de la intención desde intents_list
    intent_name = intents_list[0]['intent']
    print(f"Intent identificado: {intent_name}")  # Debugging print

    # Verifica la estructura de intents_json
    print(f"Estructura de intents_json: {intents_json}")  # Verificación de la estructura completa

    # Verifica que 'intents' esté presente en intents_json
    if 'intents' not in intents_json:
        return "Lo siento, la estructura de datos no es válida."

    # Itera sobre la lista de 'intents' dentro de intents_json
    for intent in intents_json['intents']:  # Aquí accedemos a la clave 'intents'
        print(f"Intent procesado: {intent}")  # Debugging print

        # Compara el 'tag' de cada intent con el intent_name
        if intent['intent'] == intent_name:  # Compara con 'tag'
            print(f"Respuesta encontrada: {intent['responses']}")  # Debugging print
            return random.choice(intent['responses'])

    # Si no se encuentra el intent
    return "Lo siento, no entiendo lo que dices."
'''
if __name__ == "__main__":
    # Ejemplo de prueba de las funciones
    sentence = "Hola, ¿cómo estás?"
    print("Limpieza de la oración:", cleanUpsentence(sentence))
    print("Bolsa de palabras:", bagOfwords(sentence))
    tag = "saludo"  # Esto es solo un ejemplo; usa el tag que se predice
    response = getResponse(tag, {"intents": [
        {"tag": "saludo", "responses": ["¡Hola!", "¡Hola, cómo estás?"]},
        {"tag": "agradecimiento", "responses": ["De nada", "¡Con gusto!"]}
    ]})
    print("Respuesta del chatbot:", response)
'''