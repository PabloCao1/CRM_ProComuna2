from typing import Any
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy

class EventosListView(PermisosMixin, ListView):    
    permission_required = ('Usuarios.rol_admin')  
    model = Eventos

    #Funcion de busqueda
    def get_queryset(self):
        query = self.request.GET.get('busqueda')
        if query:
            object_list = self.model.objects.filter(
                Q(nombre__icontains=query)
            ).distinct()
        else:
            object_list = self.model.objects.all()
        return object_list
    
class EventosDetailView(PermisosMixin,DetailView):
    permission_required = ('Usuarios.rol_admin')    
    model = Eventos

class EventosDeleteView(PermisosMixin,SuccessMessageMixin,DeleteView):   
    permission_required = ('Usuarios.rol_admin')  
    model = Eventos
    success_url= reverse_lazy("eventos_listar")
    success_message = "El registro fue eliminado correctamente"   

class EventosCreateView(PermisosMixin,SuccessMessageMixin,CreateView):    
    permission_required = ('Usuarios.rol_admin') 
    model = Eventos
    form_class = EventosForm
    success_message = "%(nombre)s fue registrado correctamente"  

class EventosUpdateView(PermisosMixin,SuccessMessageMixin,UpdateView):
    permission_required = ('Usuarios.rol_admin')  
    model = Eventos
    form_class = EventosForm    
    success_message = "%(nombre)s fue editado correctamente"   
