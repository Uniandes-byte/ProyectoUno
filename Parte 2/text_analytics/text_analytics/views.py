from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')

def resenia(request):
    return render(request, 'resenia.html')

def reporte(request):
    return render(request, 'reporte.html')

def prep_datos(request):
    return render(request, 'prep_datos.html')