from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    path('home/', index, name='home'),
    path('mulheres/', mulheres, name='mulheres'),
    path('editor/', news_editor, name='news_editor'),
    path('editor/<int:news_id>/', news_editor, name='news_editor_edit'),
    path('login/', PortalLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('news/', news_list, name='news_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
