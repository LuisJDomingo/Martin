from django.shortcuts import render
from .utils.utils import predictClass
from .utils.utils import getResponse


# Create your views here.

from django.http import JsonResponse
from django.shortcuts import render
import json
import numpy as np
from .utils import predictClass, getResponse
from keras.models import load_model

# Cargar el modelo y los intents
intents = json.loads(open(r'Martin\ProyectMartin\chatbot\utils\intents.json').read())
model = load_model(r'Martin\ProyectMartin\chatbot\utils\chatbot_model.h5')

# Vista para el chatbot
def chatbot_response(request):
    if request.method == 'POST':
        user_message = json.loads(request.body).get('message')
        if not user_message:
            return JsonResponse({'error': 'No se recibió ningún mensaje'}, status=400)

        # Predicción y respuesta
        ints = predictClass(user_message)
        response = getResponse(ints, intents)
        return JsonResponse({'response': response})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

# función para renderizar la interfaz web
def chatbot_home(request):
    return render(request, 'chatbot/chat.html')


