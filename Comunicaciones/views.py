from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from Usuarios.mixins import PermisosMixin
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

class ComunicacionesListView(PermisosMixin, ListView):    
    permission_required = ('Usuarios.rol_admin')  
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
    
class ComunicacionesDetailView(PermisosMixin,DetailView):
    permission_required = ('Usuarios.rol_admin')    
    model = Comunicaciones

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(ComunicacionesDetailView, self).get_context_data(**kwargs)
        archivos = ComunicacionesArchivos.objects.filter(fk_comunicacion=pk)
        context['files_img'] = archivos.filter(fk_comunicacion=pk, tipo="Imagen")
        context['files_docs'] = archivos.filter(fk_comunicacion=pk, tipo="Documento")
        context['archivos'] = True if archivos.exists() else False
        return context

class ComunicacionesDeleteView(PermisosMixin,SuccessMessageMixin,DeleteView):   
    permission_required = ('Usuarios.rol_admin')  
    model = Comunicaciones
    success_url= reverse_lazy("comunicaciones_listar")
    success_message = "El registro fue eliminado correctamente"   

class ComunicacionesCreateView(PermisosMixin, SuccessMessageMixin, CreateView):    
    permission_required = ('Usuarios.rol_admin') 
    model = Comunicaciones
    form_class = ComunicacionesForm
    success_message = "Comunicación enviada correctamente"  

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        asunto = form.cleaned_data['asunto']
        titulo = form.cleaned_data['titulo']
        mensaje = form.cleaned_data['mensaje']
        destinatarios = form.cleaned_data['destinatarios']
        files = self.request.FILES.getlist('archivos')  # Acceder a los archivos enviados desde Dropzone

        obj = form.save()
        context = {
        'titulo': titulo,
        'mensaje': mensaje,
        }

        email_html_message = render_to_string('Comunicaciones/correo_comunicaciones_template.html', context)
        email_plain_message = strip_tags(email_html_message)

        email = EmailMultiAlternatives(asunto, email_plain_message, settings.EMAIL_HOST_USER, [destinatario.email for destinatario in destinatarios.all()])
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

        

def envio_mails(email_from, email_to,asunto,template_path,context):
    template = get_template(template_path)
    content = template.render(context)

    mail = EmailMultiAlternatives(
        subject = asunto,
        body = '',
        from_email = settings.EMAIL_HOST_USER,
        to=[email_to],
        cc='',
    )
    mail.attach_alternative(content,'text/html')
    return mail

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