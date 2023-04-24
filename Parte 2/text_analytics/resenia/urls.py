from django.urls import path, include
from .views import (
    ReseniaList,
    ReseniaDetails,
    ReseniaPredict
)

urlpatterns = [
    path("resenias", ReseniaList.as_view()), 
    path("resenias/<uuid:uid>", ReseniaDetails.as_view()),
    path("resenias-predict/<uuid:uid>", ReseniaPredict.as_view()),
]
