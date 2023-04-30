from .models import Resenia
from rest_framework.response import Response
from rest_framework import status
from typing import Optional
from joblib import load
import pandas as pd
import json
from nltk.corpus import stopwords
from .DataModel import DataModel
import numpy as np
from collections import Counter
from .transformer import TextPreProcessing
#import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import SnowballStemmer

def get_object(uid):
    try:
        return Resenia.objects.get(uid=uid)
    except Resenia.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
def make_predictions(dataModel: DataModel, resenia):
    df = pd.DataFrame(dataModel.dict(),
                      columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    trans=TextPreProcessing()
    data= trans.transform(df)
    data = [str(x) for x in data]
    data.pop()
    data = np.array(data)
    model = load("static/pipelines/pipeline_neuronalNetwork.joblib")    
    x=model.predict(data)
    clasificacion=x.tolist()[0]
    num = str(num_carac(resenia))
    filtrada = (remove_stopwords(resenia))
    rep = moda(filtrada)
    info = {
    "clasificacion": clasificacion,
    "num": num,
    "moda": rep
    }
    return info

def remove_stopwords(words):    
    """Remove stop words from list of tokenized words"""
    stop_words = set(stopwords.words('spanish'))
    new_words = []
    words = words.split(' ')
    for word in words:
        if (word not in stop_words):
            new_words.append(word)
    return new_words

def moda(data):
    return Counter(data).most_common(1)[0][0]


def num_carac(data_str):
    palabras = data_str.split() 
    caracteres = len(' '.join(palabras))
    return caracteres