from django.urls import path, include
from .views import (
    ReporteList,
    ReportePredict,
    ReporteResults,
    PrediccionesResults
)

urlpatterns = [
    path("reportes", ReporteList.as_view()), 
    path("reportes-predict/<uuid:uid>", ReportePredict.as_view()),
    path("reportes-results", ReporteResults.as_view()), 
    path("predicciones-results", PrediccionesResults.as_view()), 
]
