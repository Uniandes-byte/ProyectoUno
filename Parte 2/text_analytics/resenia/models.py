from django.db import models
import uuid

MODELS=(("NB", "MultinomialNB"), ("LR", "LogisticRegression"), ("NN", "NeuralNetwork"))

class Resenia(models.Model):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    contenido = models.TextField("Content", max_length=10000, blank=False)
    modelo = models.CharField("Modelo", max_length=20, choices=MODELS)