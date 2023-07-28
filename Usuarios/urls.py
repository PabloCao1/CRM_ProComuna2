from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', UsuariosLoginView.as_view(),name='login'),
    # path('', auth_views.LoginView.as_view(template_name='login.html',authentication_form = CustomAuthenticationForm),name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='login.html'),name='logout'),

    # Usuarios
    path('usuarios/crear', login_required(UsuariosCreateView.as_view()),name='usuarios_crear'), 
    path('usuarios/listar', login_required(UsuariosListView.as_view()),name='usuarios_listar'), 
    path('usuarios/ver/<pk>', login_required(UsuariosDetailView.as_view()),name='usuarios_ver'), 
    path('usuarios/editar/<pk>', login_required(UsuariosUpdateView.as_view()),name='usuarios_editar'), 
    path('usuarios/eliminar/<pk>', login_required(UsuariosDeleteView.as_view()),name='usuarios_eliminar'),
    path('set_dark_mode/', login_required(set_dark_mode), name='set_dark_mode'),  
    
    # Password
    path('usuarios/password-reset/<pk>', login_required(UsuariosResetPassView.as_view()),name='password_reset'), 
    path('usuarios/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Passwords/password_reset_done.html'),name='password_reset_done'),
    path('usuarios/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Passwords/password_reset_confirm.html',form_class =MySetPasswordFormm),name='password_reset_confirm'),
    path('usuarios/password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='Passwords/password_reset_complete.html'),name='password_reset_complete'),

    # Perfil: acciones que realiza el usuario logeado
    path('usuarios/perfil/editar/<pk>', login_required(PerfilUpdateView.as_view()),name='perfil_editar'), 
    path('usuarios/perfil/cambiar_password', login_required(PerfilChangePassView.as_view()) ,name='cambiar_password'),

]

