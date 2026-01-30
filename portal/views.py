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

def news_editor(request):
    return render(request, 'news_editor.html')