from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from .chatbot_logic import chatbot_response
import json

'''
# Vista para la interfaz de usuario (renderizar template)
@csrf_exempt
def chatbot_view(request):
    return render(request, 'chatbot/index_ver2.html')
'''

# Vista para la API del chatbot (JSON)
@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            # Obtener el mensaje del cuerpo de la solicitud
            body = json.loads(request.body)
            print('body: ', body)
            message = body.get('message', '')
            print('message: ', message)

            # Generar la respuesta del chatbot
            response = chatbot_response(message)
            print(response)

            # Retornar la respuesta en formato JSON
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
