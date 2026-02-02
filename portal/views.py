from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Destaque
from .forms import DestaqueForm


def index(request):
    destaques = Destaque.objects.filter(portal="portal_inovai")
    context = {
        'destaques': destaques
    }
    return render(request, 'index.html', context=context)

def mulheres(request):
    destaques = Destaque.objects.filter(portal="portal_mulheres_ciencia")
    context = {
        'destaques': destaques
    }
    return render(request, 'mulheres.html', context=context)

class PortalLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


def logout_view(request):
    """Log out and redirect; no template."""
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

def news_editor(request):
    return render(request, 'news_editor.html')


# --- Destaque CRUD (login required) ---

class DestaqueListView(LoginRequiredMixin, ListView):
    model = Destaque
    context_object_name = 'destaques'
    template_name = 'portal/destaque/list.html'
    login_url = reverse_lazy('portal:login')

    def get_queryset(self):
        return Destaque.objects.order_by('portal', '-created_at')


class DestaqueDetailView(LoginRequiredMixin, DetailView):
    model = Destaque
    context_object_name = 'destaque'
    template_name = 'portal/destaque/detail.html'
    login_url = reverse_lazy('portal:login')


class DestaqueCreateView(LoginRequiredMixin, CreateView):
    model = Destaque
    form_class = DestaqueForm
    template_name = 'portal/destaque/form.html'
    success_url = reverse_lazy('portal:destaque_list')
    login_url = reverse_lazy('portal:login')


class DestaqueUpdateView(LoginRequiredMixin, UpdateView):
    model = Destaque
    form_class = DestaqueForm
    context_object_name = 'destaque'
    template_name = 'portal/destaque/form.html'
    success_url = reverse_lazy('portal:destaque_list')
    login_url = reverse_lazy('portal:login')


class DestaqueDeleteView(LoginRequiredMixin, DeleteView):
    model = Destaque
    success_url = reverse_lazy('portal:destaque_list')
    login_url = reverse_lazy('portal:login')

    def get(self, request, *args, **kwargs):
        return redirect('portal:destaque_detail', pk=kwargs['pk'])