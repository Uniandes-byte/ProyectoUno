from .models import Resenia
from rest_framework.response import Response
from rest_framework import status
from typing import Optional
from joblib import load
import pandas as pd
from .DataModel import DataModel
import numpy as np
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
    
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(),
                      columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    trans=TextPreProcessing()
    data= trans.transform(df)
    data = [str(x) for x in data]
    data = np.array(data)
    model = load("static/pipelines/pipeline_neuronalNetwork.joblib")
    print(model)
    #x=model.predict(data)
    #sas=x.tolist()
    #print(data)
    #return sas

