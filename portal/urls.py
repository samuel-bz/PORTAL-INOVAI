from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    path('home/', index, name='home'),
    path('mulheres/', mulheres, name='mulheres'),
    path('editor/', news_editor, name='news_editor'),
    path('login/', PortalLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # Destaque CRUD (login required)
    path('destaques/', DestaqueListView.as_view(), name='destaque_list'),
    path('destaque/<int:pk>/', DestaqueDetailView.as_view(), name='destaque_detail'),
    path('novo-destaque/', DestaqueCreateView.as_view(), name='destaque_create'),
    path('destaque/<int:pk>/edit/', DestaqueUpdateView.as_view(), name='destaque_update'),
    path('destaque/<int:pk>/delete/', DestaqueDeleteView.as_view(), name='destaque_delete'),
]