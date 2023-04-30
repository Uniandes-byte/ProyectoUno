from .models import Reporte
from rest_framework import status
from .transformer import TextPreProcessing, applyModel
from .make_pdf import generacion_pdf
import pandas as pd
import scipy

def get_object(uid):
    try:
        return Reporte.objects.get(uid=uid)
    except Reporte.DoesNotExist:
        return Reporte(status=status.HTTP_404_NOT_FOUND)
    
resultado = 'static/results/predicciones.csv'

def PredictReviews(model: str, data_file: str):
    # Paso 1: Carga de los datos
    data = pd.read_csv(data_file, sep=',')[:10]
    print(data)
    # Paso 2: Pasar los datos por el procesador de texto
    text_ = TextPreProcessing()
    datos = text_.fit_transform(data)

    # El sol es lo que se le va a pasar a los modelos para que diga
    # si la reseña es positiva o negativa
    
    sol = datos[0]

    # Esto es para el pdf
    data_pdf = datos[1]

    pipeline = modelo(model)
    print("------------------------------------------")
    print(model)
    print(pipeline)
    print(sol)

    # Función que aplica el modelo
    applyModel(pipeline, sol)

    # Función que genera el pdf
    generacion_pdf(model, pipeline, data_pdf, resultado)

def modelo(model: str):
    apply_model = None
    if (model == 'MultinomialNB'):
        pipeline = "static/pipelines/pipeline_logisticRegression.joblib"
        apply_model = pipeline
    elif (model == 'LogisticRegression'):
        pipeline = "static/pipelines/pipeline_logisticRegression.joblib"
        apply_model = pipeline
    elif (model == 'NeuralNetwork'):
        pipeline = "static/pipelines/pipeline_neuronalNetwork.joblib"
        apply_model = pipeline
    return apply_model