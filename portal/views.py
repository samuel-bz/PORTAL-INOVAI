from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    context = {
        'news_posts': NewsPost.objects.all()
    }
    return render(request, 'index.html', context)

def mulheres(request):
    return render(request, 'mulheres.html')

def criar_noticia(request):
    return render(request, 'index.html')