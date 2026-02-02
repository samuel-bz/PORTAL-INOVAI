from django.contrib import admin
from django.urls import path
from .views import *

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