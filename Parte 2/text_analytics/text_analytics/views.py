from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')

def resenia(request):
    return render(request, 'resenia.html')