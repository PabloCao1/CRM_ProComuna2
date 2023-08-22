from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView,LoginView
from django.contrib.auth import login as auth_login
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,FormView
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage

from .models import *
from .forms import *


#region---------------------------------------------------------------------------------------USUARIOS
from django.http import JsonResponse

def set_dark_mode(request):
    if request.method == 'POST':
        dark_mode = request.POST.get('dark_mode')
        user = request.user
        if user.usuarios.darkmode:
            user.usuarios.darkmode=False
        else:
            user.usuarios.darkmode=True
        user.usuarios.save()
        return JsonResponse({'status': 'ok'})
    
    
class UsuariosLoginView(LoginView):
    template_name='login.html'

    def form_valid(self, form):
        """
        Security check complete. Log the user in.
        Según el rol redirecciona a determinada pagina.
        Por default es Inicio.        
        """
        user=form.get_user()
        auth_login(self.request, user)
        permisos= user.get_all_permissions()
        return redirect('index')


class UsuariosListView(PermissionRequiredMixin, ListView ):    
    permission_required = ('auth.view_user')   
    model = Usuarios

    #Funcion de busqueda
    def get_queryset(self):
        query = self.request.GET.get('busqueda')
        if query:
            object_list = self.model.objects.filter(
                Q(usuario__username__icontains=query) |
                Q(usuario__first_name__icontains=query) |
                Q(usuario__last_name__icontains=query) |
                Q(usuario__email__icontains=query) |
                Q(telefono__icontains=query)
            ).distinct()
        else:
            object_list = self.model.objects.all().exclude(usuario_id__is_superuser =True)
        return object_list
   
   
class UsuariosDetailView(UserPassesTestMixin,DetailView):
    model = Usuarios
    template_name = 'Usuarios/usuarios_detail.html'

    def test_func(self):
    # accede a la vista de detalle si es admin o si es el mismo usuario
       if self.request.user.is_authenticated:
            usuario_actual = self.request.user.usuarios.id
            usuario_solicitado= int(self.kwargs['pk'])
            if (usuario_actual == usuario_solicitado) or self.request.user.has_perm('auth..base_admin') or self.request.user.has_perm('auth_user.view_user'):
                return True
       else:
           return False 


class UsuariosDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):   
    permission_required = ('auth.delete_user')   
    model = Usuarios
    template_name = 'Usuarios/usuarios_confirm_delete.html'
    success_url= reverse_lazy("usuarios_listar")
    success_message = "El registro fue eliminado correctamente"   

    
class UsuariosCreateView(PermissionRequiredMixin,SuccessMessageMixin,FormView):    
    permission_required = ('auth.add_user')  
    template_name = 'Usuarios/usuarios_create_form.html'
    form_class = UsuariosCreateForm    
    
    def form_valid(self, form): 
        dni = form.cleaned_data['dni']   
        img=self.request.FILES.get('imagen')
        telefono = form.cleaned_data['telefono']        
        if form.is_valid(): 
            user=form.save()               
            usuario=Usuarios.objects.get(usuario_id=user.id)
            if dni:
                usuario.dni = dni
            if telefono:
                usuario.telefono = telefono
            if img:         
                fs = FileSystemStorage()
                filename = fs.save('usuarios/'+img.name, img)
                usuario.imagen= filename  
            usuario.save()    
            messages.success(self.request, ('Usuario creado con éxito.'))
            return redirect('usuarios_ver',user.usuarios.id)
        else:
            messages.error(self.request, ('No fue posible crear el usuario.'))
            return redirect('usuarios_listar')


class UsuariosUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    permission_required = ('auth.change_user')   
    model = User
    form_class = UsuariosUpdateForm      
    template_name = 'Usuarios/usuarios_update_form.html'

    def form_valid(self, form): 
        dni = form.cleaned_data['dni']        
        img=self.request.FILES.get('imagen')
        telefono = form.cleaned_data['telefono'] 
        if form.is_valid():  
            user=form.save()     
            usuario=Usuarios.objects.get(usuario_id=user.id)
            if dni:
                usuario.dni = dni
            if telefono:
                usuario.telefono = telefono
            if img:         
                fs = FileSystemStorage()
                filename = fs.save('usuarios/'+img.name, img)
                usuario.imagen= filename  
            usuario.save()    
            messages.success(self.request, ('Usuario modificado con éxito.'))
        else:
            messages.error(self.request, ('No fue posible modificar el usuario.'))
        return redirect('usuarios_ver', pk=user.usuarios.id)

#endregion------------------------------------------------------------------------------------------


#region---------------------------------------------------------------------------------------PASSWORDS

class UsuariosResetPassView(PermissionRequiredMixin,SuccessMessageMixin,PasswordResetView):
    '''
    Permite al usuario staff resetear la clave a otros usuarios del sistema mediante el envío de un token por mail. 
    IMPORTANTE: el mail  al que se envía el token de recupero debe coincidir con el mail que el usuario tiene 
    almacenado en su perfil, por lo cual es imprescindible chequear que sea correcto.

    De la documentación de Django: 
        Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
    '''
    permission_required = ('auth.change_user')   
    template_name='Passwords/password_reset.html'
    form_class = MyResetPasswordForm
    success_url = reverse_lazy('usuarios_listar')
    success_message = "Mail de reseteo de contraseña enviado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id =self.kwargs['pk']
        user = User.objects.get(id=user_id)
        email=user.email
        context.update(
            {
                "email": email, 
                "usuario": user, 
            }
        )
        return context

    def get_form_kwargs(self):
        """Devuelve los argumentos de palabras (kwargs) clave para instanciar el formulario."""
        user_id =self.kwargs['pk']
        user = User.objects.get(id=user_id)
        email=user.email
        kwargs = {
            "initial": {'email': email},
            "prefix": self.get_prefix(),
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

#endregion


#region---------------------------------------------------------------------------------------PERFILES DE USUARIOS     

class PerfilUpdateView(UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    '''
    Vista para que los usuarios logueados (no staff) realicen cambios en sus datos de perfil.
    De la tabla USER: Nombre de usuario, Nombre, Apellido o email.
    De la tabla USUARIOS(extensión del modelo USER): telefono.
    '''
    model = User
    form_class = PerfilUpdateForm      
    template_name = 'Perfiles/perfil_update_form.html'
    success_message = "Perfil editado con éxito."  

    def test_func(self):
        # accede a la vista si es el mismo usuario
        if self.request.user.is_authenticated:
                usuario_actual = self.request.user.id
                usuario_solicitado= int(self.kwargs['pk'])
                if (usuario_actual == usuario_solicitado):
                    return True
        else:
            return False 

    def form_valid(self, form): 
        img=self.request.FILES.get('imagen')
        telefono = form.cleaned_data['telefono']    
        dni = form.cleaned_data['dni']    
        if form.is_valid():  
            user=form.save()            
            usuario=Usuarios.objects.get(usuario_id=user.id)
            if dni:
                usuario.dni = dni
            if telefono:
                usuario.telefono = telefono
            if img:         
                fs = FileSystemStorage()
                filename = fs.save('usuarios/'+img.name, img)
                usuario.imagen= filename  
            usuario.save()   
            messages.success(self.request, ('Perfil modificado con éxito.'))
        else:
            messages.error(self.request, ('No fue posible modificar el perfil.'))      
        return redirect('usuarios_ver', pk=user.usuarios.id)
    
class PerfilChangePassView(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):
    '''
    Vista para que los usuarios logueados (no staff) realicen cambios de clave. 
    Es requisito conocer su clave anterior e introducir una nueva contraseña que cumpla con los requisitos del sistema.
    '''
    template_name='Perfiles/perfil_change_password.html'
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('index')
    success_message = "La contraseña fue modificada con éxito."  

#endregion

