from rest_framework import serializers
from .models import Resenia

class ReseniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resenia
        fields = ["uid",
                  "contenido"]  