from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('eventos/listar', login_required(EventosListView.as_view()),name='eventos_listar'),
    path('eventos/crear', login_required(EventosCreateView.as_view()),name='eventos_crear'),
    path('eventos/ver/<pk>', login_required(EventosDetailView.as_view()),name='eventos_ver'), 
    path('eventos/eliminar/<pk>', login_required(EventosDeleteView.as_view()),name='eventos_eliminar'),
    # path('eventos/editar/<pk>', login_required(EventosUpdateView.as_view()),name='eventos_editar'), 
    # path('eventos/enviarcorreo/<pk>', login_required(EnviarCorreo),name='enviar_correo'),
    # path('eventos/individuos/buscar/', login_required(buscar_individuos), name='individuos_buscar'),
]