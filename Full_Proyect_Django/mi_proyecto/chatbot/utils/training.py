import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from numpy.f2py.crackfortran import word_pattern

lemmatizer = WordNetLemmatizer()

import os
print("Directorio actual:", os.getcwd())

# carga de archivo .json
try:
    intents = json.loads(open(r'D:\RESPALDO_ESCRITORIO\Portfolio\Martin\Full_Froyect_Django\mi_proyecto\chatbot\utils\data\intents.json').read())
except:
    print("no esta el archivo intents.json")
#descarga de archivos necesarios
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# listas necesarias

words =[]
classes =[]
documents =[]
ignore_letters =['?', '!','¿', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['intent']))
        if intent['intent'] not in classes:
            classes.append(intent['intent'])
            
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

# Ruta de los archivos JSON
words_path = 'words.json'
classes_path = 'classes.json'

# Guardar 'words' en un archivo JSON
with open(words_path, 'w') as file:
    json.dump(words, file)
print(f"Words guardado en {words_path}")

# Guardar 'classes' en un archivo JSON
with open(classes_path, 'w') as file:
    json.dump(classes, file)
print(f"Classes guardado en {classes_path}")

training = []
output_empty = [0]*len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
    
random.shuffle(training)
# Convertir a NumPy arrays
training = np.array(training, dtype=object)
train_x = np.array([entry[0] for entry in training])
train_y = np.array([entry[1] for entry in training])

train_x = list(training[:,0])
train_y = list(training[:,1])      

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]), ), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))  

sgd = SGD(learning_rate=0.001, decay=1e-6, momentum=0.9, nesterov=True)

#compilamos el modelo
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

train_process = model.fit(np.array(train_x), np.array(train_y), epochs=150, batch_size=5, verbose = False)
model.save('data/chatbot_model.h5')




