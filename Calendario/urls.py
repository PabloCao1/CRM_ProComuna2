from .views import *
from django.urls import path


urlpatterns = [
    #---------- LINKS CALENDARIO  -----------------
    path('calendario',Calendario, name='calendario'),
]