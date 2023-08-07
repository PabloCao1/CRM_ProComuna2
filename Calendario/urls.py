from .views import *
from django.urls import path

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    #---------- LINKS CALENDARIO  -----------------
    # path('calendario',Calendario, name='calendario'),
    # path('calendario/',login_required(Calendario.as_view()),name='calendario'),


    path('calendario/', login_required(CalendarioView.as_view()), name='calendario'),
    path('eventos/', login_required(EventosJsonView.as_view()), name='eventos_json'),


]