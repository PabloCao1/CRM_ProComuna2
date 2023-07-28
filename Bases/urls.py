from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [

    # Perfiles
    path('bases/perfiles/crear', login_required(PerfilesCreateView.as_view()),name='perfiles_crear'), 
    path('bases/perfiles/listar', login_required(PerfilesListView.as_view()),name='perfiles_listar'), 
    path('bases/perfiles/ver/<pk>', login_required(PerfilesDetailView.as_view()),name='perfiles_ver'), 
    path('bases/perfiles/editar/<pk>', login_required(PerfilesUpdateView.as_view()),name='perfiles_editar'), 
    path('bases/perfiles/eliminar/<pk>', login_required(PerfilesDeleteView.as_view()),name='perfiles_eliminar'), 

    path('bases/perfiles/edicion/<pk>', login_required(EdicionMultipleFormView.as_view()),name='edicion_multiple'), 

    #base voluntarios
    path('bases/perfiles/voluntarios/crear/<pk>', login_required(VoluntariosCreateView.as_view()),name='voluntarios_crear'), 

    #base fiscales
    path('bases/perfiles/fiscales/crear/<pk>', login_required(FiscalesCreateView.as_view()),name='fiscales_crear'), 

]
