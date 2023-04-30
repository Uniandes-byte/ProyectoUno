from django.db import models
import uuid
from rest_framework.response import Response
from rest_framework import status

MODELS=(("NB", "MultinomialNB"), ("LR", "LogisticRegression"), ("NN", "NeuralNetwork"))

class Reporte(models.Model):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    modelo = models.CharField("Modelo", max_length=20, choices=MODELS)
    file = models.FileField("file", upload_to="files")
