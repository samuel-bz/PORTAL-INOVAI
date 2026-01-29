from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    path('mulheres/', mulheres, name='mulheres'),
    path('login/', PortalLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]