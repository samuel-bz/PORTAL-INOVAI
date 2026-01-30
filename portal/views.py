from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    noticias = NewsPost.objects.all()[:3]

    context = {
        'news_posts': noticias
    }
    return render(request, 'index.html', context)

def mulheres(request):
    return render(request, 'mulheres.html')

def criar_noticia(request):
    return render(request, 'index.html')