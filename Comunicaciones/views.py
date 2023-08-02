from typing import Any
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from Usuarios.mixins import PermisosMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 
from django.http import JsonResponse

class ComunicacionesListView(PermisosMixin, ListView):    
    permission_required = ('Usuarios.rol_admin')  
    model = Comunicaciones

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
    
class ComunicacionesDetailView(PermisosMixin,DetailView):
    permission_required = ('Usuarios.rol_admin')    
    model = Comunicaciones

class ComunicacionesDeleteView(PermisosMixin,SuccessMessageMixin,DeleteView):   
    permission_required = ('Usuarios.rol_admin')  
    model = Comunicaciones
    success_url= reverse_lazy("comunicaciones_listar")
    success_message = "El registro fue eliminado correctamente"   

class ComunicacionesCreateView(PermisosMixin,SuccessMessageMixin,CreateView):    
    permission_required = ('Usuarios.rol_admin') 
    model = Comunicaciones
    form_class = ComunicacionesForm
    success_message = "%(nombre)s fue registrado correctamente"  

class ComunicacionesUpdateView(PermisosMixin,SuccessMessageMixin,UpdateView):
    permission_required = ('Usuarios.rol_admin')  
    model = Comunicaciones
    form_class = ComunicacionesForm    
    success_message = "%(nombre)s fue editado correctamente"
    

def buscar_individuos(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        res = None
        busqueda = request.POST.get("busqueda")
        if len(busqueda) > 3:
            individuos = (
                Perfiles.objects.filter((Q(apellidos__contains=busqueda) | Q(nombres__contains=busqueda))))

            data = [
                {
                    'pk': individuo.pk,
                    'nombre': individuo.nombres,
                    'apellido':individuo.apellidos
                }
                for individuo in individuos
            ]
            res = data
        return JsonResponse({"data": res})

    return JsonResponse({"data": "this is data"})

def EnviarCorreo(request, pk):
    subject = "Email Pro Comuna 2"
    event = Comunicaciones.objects.get(pk=pk)
    grupo = event.grupos_invitados.all()
    invitados = event.invitados_individuales.all()
    nombre = event.nombre
    texto = event.texto
    foto = event.foto
    
    template = render_to_string('Eventos/correo_template.html', {
        'nombre': nombre,
        'texto': texto,
        'foto': foto,
    })
    
    for g in grupo:
        print(g)
    
    for i in invitados:
        #mail = i.email
        print (i.email)

    email = EmailMessage (
        subject,
        template,
        ['pablocao@gmail.com']
    )
    email.fail_silently = False
    email.send()

    print(grupo, invitados,  nombre, texto, foto)
    return render(request, 'Comunicaciones/correo.html')