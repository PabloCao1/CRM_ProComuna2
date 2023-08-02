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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil'] = Perfiles.objects.all()
        return context

class EventosUpdateView(PermisosMixin,SuccessMessageMixin,UpdateView):
    permission_required = ('Usuarios.rol_admin')
    model = Eventos
    form_class = EventosForm
    success_message = "%(nombre)s fue editado correctamente"

def EnviarCorreo(request, pk):
    subject = "Email Pro Comuna 2"
    event = Eventos.objects.get(pk=pk)
    grupo = event.grupos_invitados.all()
    invitados = event.invitados_individuales.all()
    nombre = event.nombre
    fecha = event.fecha
    hora = event.hora
    minutos = event.minutos
    lugar = event.lugar
    calle = event.calle
    altura = event.altura
    telefono = event.telefono
    web = event.WEB
    modo = event.modo
    foto = event.foto
    observaciones = event.observaciones
    
    template = render_to_string('Eventos/correo_template.html', {
        'nombre': nombre,
        'modo': modo,
        'url': web,
        'lugar': lugar,
        'calle': calle,
        'altura': altura,
        'fecha': fecha,
        'hora': hora,
        'minutos': minutos,
        'telefono': telefono,
        'observaciones': observaciones
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

    print(grupo, invitados,  fecha, hora, minutos, lugar, calle, altura, telefono, web, modo, foto)
    return render(request, 'Eventos/correo.html')


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