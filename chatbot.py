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
intents = json.loads(open('intents.json').read())



while True:

    message = input("Tú:")
    ints = predictClass(message)
    res = getResponse(ints, intents)
    print('Martin: ',res)
