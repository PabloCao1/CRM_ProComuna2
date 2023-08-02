from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('comunicaciones/listar', login_required(ComunicacionesListView.as_view()),name='comunicaciones_listar'),
    path('comunicaciones/crear', login_required(ComunicacionesCreateView.as_view()),name='comunicaciones_crear'),
    path('comunicaciones/ver/<pk>', login_required(ComunicacionesDetailView.as_view()),name='comunicaciones_ver'), 
    path('comunicaciones/editar/<pk>', login_required(ComunicacionesUpdateView.as_view()),name='comunicaciones_editar'), 
    path('comunicaciones/eliminar/<pk>', login_required(ComunicacionesDeleteView.as_view()),name='comunicaciones_eliminar'),
    path('comunicaciones/enviarcorreo/<pk>', login_required(EnviarCorreo),name='enviar_comunicacion'), 
    path('comunicaciones/individuos/buscar/', login_required(buscar_individuos), name='com_individuos_buscar'),
]