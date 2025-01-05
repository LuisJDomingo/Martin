from django.urls import path
from django.shortcuts import render
from . import views

def chat_page(request):
    return render(request, 'chatbot/index_ver2.html')

urlpatterns = [
    path('', chat_page, name='chatbot'),  # Ruta para la vista de inicio del chatbot
    path('chatbot/', views.chatbot_api, name='chatbot_api'),  # Ruta para la API del chatbot
]

'''def chat_page(request):
    return render(request, 'chatbot/index_ver2.html')'''