from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

def index(request):
    return render(request, 'index.html')

def mulheres(request):
    return render(request, 'mulheres.html')

class PortalLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


def logout_view(request):
    """Log out and redirect; no template."""
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

def criar_noticia(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')


def news_list_view(request):
    return render(request, 'noticias.html')


def projects_view(request):
    return render(request, 'projetos.html')
