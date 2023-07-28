from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission

#region-----------USUARIOS---------------------------------------------------------------------------------------

class UsuariosInline(admin.StackedInline):
    model = Usuarios
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsuariosInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(Permission)
admin.site.register(User, UserAdmin)

#endregion-----------USUARIOS---------------------------------------------------------------------------------------

