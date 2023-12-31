from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect,render,get_object_or_404
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,FormView,View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage
from django.urls import reverse_lazy
from datetime import date
from django.http import JsonResponse
from .resources import *
from .models import *
from .admin import *
from .forms import *
from .choices import *
from django.utils.encoding import smart_bytes
import json


#region ############################################################### Base General (Perfiles)

class PerfilActivarView(View):
    def post(self, request, perfil_id):
        perfil = get_object_or_404(Perfiles, pk=perfil_id)
        perfil.activo = True
        perfil.motivo_inactivo = ""  # Vaciamos el motivo al activar
        perfil.fecha_inactivo = None  # Vaciamos la fecha al activar
        perfil.save()
        return redirect('perfiles_ver', pk=perfil_id)

class PerfilDesactivarView(View):
    def post(self, request, perfil_id):
        perfil = get_object_or_404(Perfiles, pk=perfil_id)
        motivo = request.POST.get('motivo')
        perfil.activo = False
        perfil.motivo_inactivo = motivo
        perfil.fecha_inactivo = date.today()  # Guarda la fecha actual
        perfil.save()
        return redirect('perfiles_ver', pk=perfil_id)


class PerfilesListView(PermissionRequiredMixin, ListView):
    permission_required = ('Bases.view_perfiles') 
    model = Perfiles

    def get_queryset(self):
        today = date.today()
        palabra = self.request.GET.get('busqueda')
        object_list = self.model.objects.all()

        if palabra:
            object_list = object_list.filter(
                Q(nombres__icontains=palabra) |
                Q(apellidos__icontains=palabra) |
                Q(documento__icontains=palabra) |
                Q(telefono__iexact=palabra) |
                Q(observaciones__icontains=palabra)
            )

        if self.request.GET:
            q = Q()

            if self.request.GET.get('base_general', None):
                q &= ~Q(es_voluntario=True) & ~Q(es_fiscal=True)

            if self.request.GET.get('base_voluntarios', None):
                q |= Q(es_voluntario=True)

            if self.request.GET.get('base_fiscal', None):
                q |= Q(es_fiscal=True)

            if self.request.GET.get('con_email', None):
                q &= ~Q(email__isnull=True)

            if self.request.GET.get('con_celular', None):
                q &= ~Q(telefono__isnull=True)

            if self.request.GET.get('con_domicilio', None):
                q &= ~Q(calle__isnull=True)

            if self.request.GET.get('con_instagram', None):
                q &= ~Q(instagram__isnull=True)

            if self.request.GET.get('con_facebook', None):
                q &= ~Q(facebook__isnull=True)

            # Variables separadas para los campos "sexo" y "fecha_nacimiento"
            sexo_f_q = Q()
            if self.request.GET.get('sexo_f', None):
                sexo_f_q |= Q(sexo="Femenino")

            sexo_m_q = Q()
            if self.request.GET.get('sexo_m', None):
                sexo_m_q |= Q(sexo="Masculino")

            sexo_x_q = Q()
            if self.request.GET.get('sexo_x', None):
                sexo_x_q |= Q(sexo="X")

            sexo_null_q = Q()
            if self.request.GET.get('sexo_desconocido', None):
                sexo_x_q |= Q(sexo__isnull=True)

            # Combinar las variables de sexo en una sola variable
            q &= (sexo_f_q | sexo_m_q | sexo_x_q)

            edad_h30_q = Q()
            if self.request.GET.get('hasta_30_anios', None):
                age_threshold = today.year - 30
                edad_h30_q |= Q(fecha_nacimiento__gte=date(age_threshold, today.month, today.day))

            edad_h45_q = Q()
            if self.request.GET.get('de_31_a_45_anios', None):
                age_threshold_1 = today.year - 31
                age_threshold_2 = today.year - 45
                edad_h45_q |= Q(fecha_nacimiento__lte=date(age_threshold_1, today.month, today.day)) & \
                          Q(fecha_nacimiento__gte=date(age_threshold_2, today.month, today.day))

            edad_m46_q = Q()
            if self.request.GET.get('mas_de_46_anios', None):
                age_threshold = today.year - 46
                edad_m46_q |= Q(fecha_nacimiento__lte=date(age_threshold, today.month, today.day))

            edad_null = Q()
            if self.request.GET.get('edad_desconocida', None):
                edad_null |= Q(fecha_nacimiento__isnull=True)

            # Combinar las variables para tener en cuenta las opciones excluyentes
            q &= (edad_h30_q | edad_h45_q | edad_m46_q | edad_null)

            # Variables separadas para activo e inactivo
            activo_q = Q()
            if self.request.GET.get('estado_activo', None):
                activo_q |= Q(activo=True)

            inactivo_q = Q()
            if self.request.GET.get('estado_inactivo', None):
                inactivo_q |= Q(activo=False)

            # Combinar las variables para tener en cuenta ambas condiciones
            q &= (activo_q | inactivo_q)

            object_list = object_list.filter(q)

        object_list = object_list.distinct()

        return object_list


    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = export_to_xls(queryset)
        return response


class PerfilesDetailView(PermissionRequiredMixin,DetailView): 
    permission_required = ('Bases.view_perfiles')  
    model = Perfiles

    def get_context_data(self, **kwargs):
        context = super(PerfilesDetailView, self).get_context_data(**kwargs)
        context['voluntario'] = BaseVoluntariosPerfiles.objects.filter(fk_perfil_v=self.get_object().pk).first()
        context['fiscal'] = BaseFiscalesPerfiles.objects.filter(fk_perfil_f=self.get_object().pk).first()
        return context
    

class PerfilesDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):  
    permission_required = ('Bases.delete_perfiles') 
    model = Perfiles
    success_url= reverse_lazy("perfiles_listar")
    success_message = "El registro fue eliminado correctamente"  


class PerfilesCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):   
    permission_required = ('Bases.add_perfiles')  
    model = Perfiles
    form_class = PerfilesForm
    success_message = "Registrado correctamente"  

    
    def get_context_data(self, **kwargs):
        context = super(PerfilesCreateView, self).get_context_data(**kwargs)
        context['barrios_comunas_map'] = BARRIOS_COMUNAS_MAP
        return context


class PerfilesUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    permission_required = ('Bases.change_perfiles') 
    model = Perfiles
    form_class = PerfilesForm    
    success_message = "Editado correctamente"   

    def get_context_data(self, **kwargs):
        context = super(PerfilesUpdateView, self).get_context_data(**kwargs)
        context['barrios_comunas_map'] = BARRIOS_COMUNAS_MAP
        return context


class EdicionMultipleFormView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    permission_required = ('Bases.change_perfiles') 
    model= Perfiles
    template_name = 'Bases/edicionmultiple_form.html'
    form_class = PerfilesForm
    form_voluntarios = BaseVoluntariosPerfilesForm
    form_fiscales = BaseFiscalesPerfilesForm
    success_message = "Editado correctamente" 

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(EdicionMultipleFormView, self).get_context_data(**kwargs)
        voluntario = BaseVoluntariosPerfiles.objects.filter(fk_perfil_v=pk).first()
        fiscal = BaseFiscalesPerfiles.objects.filter(fk_perfil_f=pk).first()
        
        context['barrios_comunas_map'] = BARRIOS_COMUNAS_MAP
        context['es_voluntario'] = True if voluntario else False
        context['es_fiscal'] = True if fiscal else False
        context['form_voluntarios'] = self.form_voluntarios(instance=voluntario)
        context['form_fiscales'] = self.form_fiscales(instance=fiscal)
        return context
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        pk = self.kwargs.get('pk')
        voluntario = BaseVoluntariosPerfiles.objects.filter(fk_perfil_v=pk).first()
        fiscal = BaseFiscalesPerfiles.objects.filter(fk_perfil_f=pk).first()
        form_voluntarios = self.form_voluntarios(self.request.POST)
        form_fiscales = self.form_fiscales(self.request.POST)

        if fiscal and form_fiscales.is_valid():
            update_fiscal =form_fiscales.save(commit=False)
            fiscal.fue_fiscal=update_fiscal.fue_fiscal  
            fiscal.rol_fiscal=update_fiscal.rol_fiscal  
            fiscal.desempeno=update_fiscal.desempeno  
            fiscal.disp_jornada=update_fiscal.disp_jornada  
            fiscal.observaciones_f=update_fiscal.observaciones_f 
            fiscal.save()
            return super().form_valid(form)
            
        if voluntario and form_voluntarios.is_valid():
            update_voluntario =form_voluntarios.save(commit=False)
            voluntario.grupo_wsp=update_voluntario.grupo_wsp
            voluntario.gen_23=update_voluntario.gen_23
            voluntario.eventos=update_voluntario.eventos
            voluntario.afinidad=update_voluntario.afinidad
            voluntario.otro_afinidad=update_voluntario.otro_afinidad
            voluntario.observaciones_v=update_voluntario.observaciones_v
            voluntario.save()
            return super().form_valid(form)
                
        else:
            return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     voluntario = BaseVoluntariosPerfiles.objects.filter(fk_perfil=pk).first()
    #     fiscal = BaseFiscalesPerfiles.objects.filter(fk_perfil=pk).first()
    #     form_perfil = self.form_class(request.POST)
    #     form_voluntarios = self.form_voluntarios(request.POST)
    #     form_fiscales = self.form_fiscales(request.POST)
        
    #     if(voluntario and fiscal):
    #         if form_perfil.is_valid() and form_voluntarios.is_valid() and form_fiscales.is_valid():
    #             # Do something with the form data
    #             return self.form_valid(form_perfil)
    #         else:
    #             return self.form_invalid(form_perfil)

    #     elif (fiscal and not voluntario):
    #         if form_perfil.is_valid() and form_fiscales.is_valid():
    #             # Do something with the form data
    #             return self.form_valid(form_perfil)
    #         else:
    #             return self.form_invalid(form_perfil)
            
    #     elif(voluntario and not fiscal):
    #         if form_perfil.is_valid() and form_voluntarios.is_valid():
    #             return self.form_valid(form_perfil)
    #         else:
    #             return self.form_invalid(form_perfil)
    #     else:
    #         messages.error('no')
    #         return self.form_invalid(form_perfil)

#endregion


#region ############################################################### Base Voluntarios
class VoluntariosCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView): 
    permission_required = ('Bases.add_basevoluntariosperfiles')    
    model = BaseVoluntariosPerfiles
    form_class = BaseVoluntariosPerfilesForm
    success_message = "Registrado correctamente"  

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        pk = self.kwargs.get('pk')
        if pk:       
            form.fields['fk_perfil_v'].initial = pk
        return form
    
    def form_valid(self, form):
        form.save()
        pk = self.kwargs.get('pk')
        perfil = Perfiles.objects.get(id=pk)
        perfil.es_voluntario=True
        perfil.save()
        return redirect('perfiles_ver',pk)

#endregion


#region ############################################################### Base Fiscales 
class FiscalesCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):  
    permission_required = ('Bases.add_basefiscalesperfiles')   
    model = BaseFiscalesPerfiles
    form_class = BaseFiscalesPerfilesForm
    success_message = "Registrado correctamente"  

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        pk = self.kwargs.get('pk')
        if pk:       
            form.fields['fk_perfil_f'].initial = pk
        return form
    
    def form_valid(self, form):
        form.save()
        pk = self.kwargs.get('pk')
        perfil = Perfiles.objects.get(id=pk)
        perfil.es_fiscal=True
        perfil.save()
        return redirect('perfiles_ver',pk)

#endregion

