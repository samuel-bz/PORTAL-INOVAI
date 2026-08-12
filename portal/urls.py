from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    path('sobre/', sobre, name='sobre'),
    path('home/', index, name='home'),
    path('mulheres/', mulheres, name='mulheres'),
    path('editor/', news_editor, name='news_editor'),
    path('editor/<int:news_id>/', news_editor, name='news_editor_edit'),
    path('login/', PortalLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # Destaque CRUD (login required)
    path('destaques/', DestaqueListView.as_view(), name='destaque_list'),
    path('destaque/<int:pk>/', DestaqueDetailView.as_view(), name='destaque_detail'),
    path('novo-destaque/', DestaqueCreateView.as_view(), name='destaque_create'),
    path('destaque/<int:pk>/edit/', DestaqueUpdateView.as_view(), name='destaque_update'),
    path('destaque/<int:pk>/delete/', DestaqueDeleteView.as_view(), name='destaque_delete'),
    path('news/', news_list, name='news_list'),
    path('noticia/<int:pk>/', news_detail, name='news_detail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
