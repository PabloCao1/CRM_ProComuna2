from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
from email.mime.image import MIMEImage


class EventosListView(PermissionRequiredMixin, ListView):
    permission_required = ('Eventos.view_eventos')
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

class EventosDetailView(PermissionRequiredMixin,DetailView):
    permission_required = ('Eventos.view_eventos')
    model = Eventos

class EventosDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    permission_required = ('Eventos.delete_eventos')
    model = Eventos
    success_url= reverse_lazy("eventos_listar")
    success_message = "El registro fue eliminado correctamente"

class EventosCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    permission_required = ('Eventos.add_eventos')
    model = Eventos
    form_class = EventosForm
    success_message = "%(nombre)s fue registrado correctamente"

    def form_valid(self, form):
        grupo_de_invitados = form.cleaned_data['grupo_de_invitados']
        invitados = form.cleaned_data['invitados']
        asunto = form.cleaned_data['nombre']
        mensaje = form.cleaned_data['mensaje']
        flyer = self.request.FILES.get('flyer')  # Acceder a los archivos enviados desde Dropzone
        
        # Obtener todos los perfiles de invitados individuales
        perfiles_invitados = invitados.all().distinct()

        # Filtrar perfiles según grupos de invitados seleccionados
        q = Q()
        if grupo_de_invitados:
            if 'Base General' in grupo_de_invitados:
                q &= ~Q(es_voluntario=True) & ~Q(es_fiscal=True)
            if 'Base Fiscales' in grupo_de_invitados:
                q |= Q(es_fiscal=True)
            if 'Base Voluntarios' in grupo_de_invitados:
                q |= Q(es_voluntario=True)
            perfiles_grupo_invitados = Perfiles.objects.filter(email__isnull=False, activo=True).filter(q).distinct()
        else:
            perfiles_grupo_invitados = Perfiles.objects.none()

        # Combinar perfiles de invitados individuales y de grupo
        perfiles_combinados = perfiles_invitados | perfiles_grupo_invitados
        # Obtener una lista única de correos electrónicos de los perfiles combinados
        lista_correos = list(set([perfil.email for perfil in perfiles_combinados]))

        obj = form.save()
        obj.invitados.set(perfiles_combinados)
        obj.save()
        
        email_html_message = render_to_string('Eventos/eventos_email_template.html', {'evento': obj})
        email_plain_message = strip_tags(email_html_message)

        email = EmailMultiAlternatives(asunto, email_plain_message, settings.EMAIL_HOST_USER, lista_correos)
        email.attach_alternative(email_html_message, "text/html")

        if flyer:
            email.mixed_subtype = 'related'  # Permite embeber contenido en el correo
            # Adjunta la imagen al correo como archivo adjunto
            email.attach(flyer.name, flyer.read(), flyer.content_type)

            # Embeber la imagen en el correo utilizando MIMEImage
            with flyer.open(mode='rb') as file:
                img_data = file.read()
                extension = flyer.name.split('.')[-1]  # Obtener la extensión de la imagen
                img = MIMEImage(img_data, _subtype=extension)
                img.add_header('Content-Id', '<myimage>')  # ID de contenido para embeber la imagen
                img.add_header('Content-Disposition', 'inline', filename='myimage')  # Establecer como embebida
                email.attach(img)

       
        try:
            email.send()  # Enviar el correo con los archivos adjuntos
        except Exception as e:
            if obj.fallo:
                obj.fallo += ', ' + ', '.join([destinatario.email for destinatario in invitados.all()])
            else:
                obj.fallo = ', '.join([destinatario.email for destinatario in invitados.all()])
            obj.save()

        if obj.fallo:
            messages.error(self.request, f"Error al enviar el correo a: {obj.fallo}")

        return super().form_valid(form)

# class EventosUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
#     permission_required = ('Eventos.change_eventos')
#     model = Eventos
#     form_class = EventosForm
#     success_message = "%(nombre)s fue editado correctamente"

#     def form_invalid(self, form):
#         # Agrega un mensaje de error para cada campo con errores
#         for field, errors in form.errors.items():
#             for error in errors:
#                 messages.error(self.request, f"{form.fields[field].label}: {error}")
#         return super().form_invalid(form)

    