from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def mulheres(request):
    return render(request, 'mulheres.html')

def criar_noticia(request):
    return render(request, 'index.html')