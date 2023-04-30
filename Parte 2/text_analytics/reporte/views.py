from .models import Reporte
from .serializers import ReporteSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .utils import *
from django.http import HttpResponse
from django.http import FileResponse

# Create your views here.
class ReporteList(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        reportes = Reporte.objects.all()
        serializer = ReporteSerializer(reportes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReporteSerializer(data=request.data)
        if serializer.is_valid():       
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReportePredict(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, uid):
        reporte = get_object(uid)
        modelo = reporte.modelo

        if(modelo=='NB'):
            modelo = "MultinomialNB"

        elif(modelo=='LR'):
            modelo = "LogisticRegression"

        else:
            modelo = "NeuralNetwork"

        PredictReviews(modelo, reporte.file)
        return Response({'message': 'success'}, status=status.HTTP_200_OK)

class ReporteResults(APIView):

    def post(self, request):
            with open('static/results/reporte.pdf', 'rb') as pdf_file:
                pdf_output = pdf_file.read()
                # devuelve el archivo PDF como una respuesta HTTP
                response = HttpResponse(pdf_output, content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="reporte_1.pdf"'    
                return response

class PrediccionesResults(APIView):

    def post(self, request):
            with open('static/results/predicciones.csv', 'rb') as pdf_file:
                pdf_output = pdf_file.read()
                # devuelve el archivo PDF como una respuesta HTTP
                response = HttpResponse(pdf_output, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="tu_archivo.csv"'  
                return response