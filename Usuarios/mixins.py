from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin, UserPassesTestMixin


class PermisosMixin(PermissionRequiredMixin):
    '''
    Verifica al mismo tiempo usuario logeado y permisos.
    Requiere agregar un atributo 'permission_required' en la vista, colocando un permiso o una lista de los mismos.
    '''

    def get_required_permissions(self):
        # Obtiene los permisos requeridos de la vista
        required_permissions = super().get_required_permissions()

        # Obtiene los permisos individuales del usuario
        user_individual_permissions = self.request.user.user_permissions.all()

        # Obtiene los permisos de los grupos del usuario
        user_group_permissions = self.request.user.get_group_permissions()

        # Combina todos los permisos en una única lista
        all_permissions = required_permissions.union(
            user_individual_permissions, user_group_permissions
        )

        return all_permissions

    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        self.permission_denied_message = 'No posee permisos para realizar la acción'
        return super().handle_no_permission()

    

class EsStaffoUsusarioActual(LoginRequiredMixin, UserPassesTestMixin):
    '''
    Verifica si el usuario logeado es staff o si la petición la realiza sobre sí mismo.
    '''
    def test_func(self):
    # accede a la vista de detalle si es staff o si es el mismo usuario
       if self.request.user.is_authenticated:
            usuario_actual = self.request.user.id
            usuario_solicitado= int(self.kwargs['pk'])
            if (usuario_actual == usuario_solicitado) or self.request.user.is_staff:
                return True
       else:
           return False 