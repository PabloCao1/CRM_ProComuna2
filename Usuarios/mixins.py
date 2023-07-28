from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin, UserPassesTestMixin


class PermisosMixin(PermissionRequiredMixin):
    '''
    Verifica al mismo tiempo usuario logeado y permisos.
    Requiere agregar un atributo 'permission_required ' en la vista, colocando un permiso o una lista de los mismos
    '''
    def handle_no_permission(self):
        self.raise_exception = self.request.user.is_authenticated
        self.permission_denied_message = 'No posee permisos para realizar la acción'
        return super(PermisosMixin, self).handle_no_permission()
    

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