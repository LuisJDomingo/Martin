import random
import json
import pickle
import numpy as np
from utils import predictClass
from utils import getResponse

import nltk

from nltk.stem import WordNetLemmatizer

from keras.models import load_model

# carga de archivo .json
intents = json.loads(open(r'D:\RESPALDO_ESCRITORIO\Portfolio\Martin\Martin\intents.json').read())

import h5py

# Carga el archivo .h5
file_path = r"D:\RESPALDO_ESCRITORIO\Portfolio\Martin\Martin\chatbot_model.h5"
with h5py.File(file_path, 'r') as h5_file:
    # Listar todos los grupos (estructuras internas del archivo)
    # print("Grupos dentro del archivo:")
    def print_attrs(name, obj):
        print(name, obj)
    h5_file.visititems(print_attrs)

    # Opcional: explorar un dataset específico
    # if 'model_weights' in h5_file:
        # print("\nPesos del modelo:")
        # print(h5_file['model_weights'])

while True:

    message = input("Tú:")
    ints = predictClass(message)
    res = getResponse(ints, intents)
    print('Martin: ',res)
