import random
import json
import numpy as np
from .utils.utils import predictClass, getResponse
from tensorflow.keras.models import load_model, save_model
import os

# Inicializar el lematizador
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Ruta base del directorio actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carga de archivos
intents_path = os.path.join(BASE_DIR, 'utils', 'data', 'intents.json')
model_path = os.path.join(BASE_DIR, 'utils', 'data', 'chatbot_model.h5')

# Cargar los datos y el modelo
intents = json.loads(open(intents_path).read())
model = load_model(model_path)

def chatbot_response(message):
    """
    Genera la respuesta del chatbot dado un mensaje.
    """
    try:
        # Predecir la clase del mensaje
        ints = predictClass(message)
        # Obtener la respuesta basada en la intención
        response = getResponse(ints, intents)
        return response
    except Exception as e:
        return f"Error procesando la solicitud: {str(e)}"
