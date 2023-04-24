from .models import Resenia
from .serializers import ReseniaSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils import *
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer

# Create your views here.
class ReseniaList(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        resenias = Resenia.objects.all()
        serializer = ReseniaSerializer(resenias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReseniaSerializer(data=request.data)
        if serializer.is_valid():       
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReseniaDetails(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, uid):
        resenia = get_object(uid)
        serializer = ReseniaSerializer(resenia)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uid):
        resenia = get_object(uid)
        serializer = ReseniaSerializer(resenia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid):
        resenia = get_object(uid)
        resenia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReseniaPredict(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, uid):
        resenia = get_object(uid)
        data = DataModel(review_es=resenia.contenido)
        sas = make_predictions(data)
        return Response(sas, status=status.HTTP_200_OK)
