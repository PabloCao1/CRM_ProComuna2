from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator, Page
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *
from .forms import *
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json

class ComunicacionesListView(PermissionRequiredMixin, ListView):    
    permission_required = ('Comunicaciones.view_comunicaciones')  
    model = Comunicaciones
    template_name = 'Comunicaciones/comunicaciones_list.html'

    #Funcion de busqueda
    def get_queryset(self):
        query = self.request.GET.get('busqueda')
        if query:
            object_list = self.model.objects.filter(
                Q(asunto__icontains=query)
            ).distinct()
        else:
            object_list = self.model.objects.all()

        # Crear un objeto Paginator para paginar los resultados
        paginator = Paginator(object_list, 25)
        
        # Obtener el número de página actual desde el parámetro 'page' en la URL
        page_number = self.request.GET.get('page')
        
        # Obtener la página actual desde el objeto Paginator
        page = paginator.get_page(page_number)

        return page
    
class ComunicacionesDetailView(PermissionRequiredMixin,DetailView):
    permission_required = ('Comunicaciones.view_comunicaciones')    
    model = Comunicaciones

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(ComunicacionesDetailView, self).get_context_data(**kwargs)
        archivos = ComunicacionesArchivos.objects.filter(fk_comunicacion=pk)
        context['files_img'] = archivos.filter(fk_comunicacion=pk, tipo="Imagen")
        context['files_docs'] = archivos.filter(fk_comunicacion=pk, tipo="Documento")
        context['archivos'] = True if archivos.exists() else False
        return context

class ComunicacionesDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):   
    permission_required = ('Comunicaciones.delete_comunicaciones')  
    model = Comunicaciones
    success_url= reverse_lazy("comunicaciones_listar")
    success_message = "El registro fue eliminado correctamente"   

class ComunicacionesCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):    
    permission_required = ('Comunicaciones.add_comunicaciones') 
    model = Comunicaciones
    form_class = ComunicacionesForm
    success_message = "Comunicación enviada correctamente"  


    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        grupo_de_destinatarios = form.cleaned_data['grupo_de_destinatarios']
        destinatarios = form.cleaned_data['destinatarios']
        asunto = form.cleaned_data['asunto']
        titulo = form.cleaned_data['titulo']
        mensaje = form.cleaned_data['mensaje']
        files = self.request.FILES.getlist('archivos')  # Acceder a los archivos enviados desde Dropzone
        
        # Obtener todos los perfiles de destinatarios individuales
        perfiles_destinatarios = destinatarios.all().distinct()

        # Filtrar perfiles según grupos de destinatarios seleccionados
        q = Q()
        if grupo_de_destinatarios:
            if 'Base General' in grupo_de_destinatarios:
                q &= ~Q(es_voluntario=True) & ~Q(es_fiscal=True)
            if 'Base Fiscales' in grupo_de_destinatarios:
                q |= Q(es_fiscal=True)
            if 'Base Voluntarios' in grupo_de_destinatarios:
                q |= Q(es_voluntario=True)
            perfiles_grupo_destinatarios = Perfiles.objects.filter(email__isnull=False, activo=True).filter(q).distinct()
        else:
            perfiles_grupo_destinatarios = Perfiles.objects.none()

        # Combinar perfiles de destinatarios individuales y de grupo
        perfiles_combinados = perfiles_destinatarios | perfiles_grupo_destinatarios
        # Obtener una lista única de correos electrónicos de los perfiles combinados
        lista_correos = list(set([perfil.email for perfil in perfiles_combinados]))

        obj = form.save()
        obj.destinatarios.set(perfiles_combinados)
        obj.save()

        # contexto para renderizar los datos en el template
        context = {
        'titulo': titulo,
        'mensaje': mensaje,
        }

        email_html_message = render_to_string('Comunicaciones/correo_comunicaciones_template.html', context)
        email_plain_message = strip_tags(email_html_message)

       # Utiliza perfiles_combinados para enviar el correo
        email = EmailMultiAlternatives(asunto, email_plain_message, settings.EMAIL_HOST_USER, lista_correos)

        email.attach_alternative(email_html_message, "text/html")

        for f in files:
            if f:
                file_extension = f.name.split('.')[-1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                    tipo = 'Imagen'
                else:
                    tipo = 'Documento'

                comunicacion_archivo = ComunicacionesArchivos.objects.create(
                    fk_comunicacion=obj,
                    archivo=f,
                    tipo=tipo
                )
                # Abrir el archivo en modo binario y adjuntarlo al correo
                with f.open(mode='rb') as file:
                    email.attach(f.name, file.read(), f.content_type)

        try:
            email.send()  # Enviar el correo con los archivos adjuntos
        except Exception as e:
            if obj.fallo:
                obj.fallo += ', ' + ', '.join([destinatario.email for destinatario in destinatarios.all()])
            else:
                obj.fallo = ', '.join([destinatario.email for destinatario in destinatarios.all()])
            obj.save()

        if obj.fallo:
            messages.error(self.request, f"Error al enviar el correo a: {obj.fallo}")

        return super().form_valid(form)


