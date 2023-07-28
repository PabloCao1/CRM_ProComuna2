from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,render
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,FormView,View
from Usuarios.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage
from django.urls import reverse_lazy




#region ############################################################### Base General (Perfiles)

class PerfilesListView(LoginRequiredMixin, ListView):
    model = Perfiles

    def get_queryset(self):
        today = date.today()
        palabra = self.request.GET.get('busqueda')
        if self.request.GET:
            base_general = self.request.GET.get('base_general', None)
            base_voluntarios = self.request.GET.get('base_voluntarios', None)
            base_fiscal = self.request.GET.get('base_fiscal', None)
            con_email = self.request.GET.get('con_email', None)
            con_celular = self.request.GET.get('con_celular', None)
            con_domicilio = self.request.GET.get('con_domicilio', None)
            hasta_30_anios = self.request.GET.get('hasta_30_anios', None)
            de_31_a_45_anios = self.request.GET.get('de_31_a_45_anios', None)
            mas_de_46_anios = self.request.GET.get('mas_de_46_anios', None)
            sexo_f = self.request.GET.get('sexo_f', None)
            sexo_m = self.request.GET.get('sexo_m', None)
            sexo_x = self.request.GET.get('sexo_x', None)
            activo = self.request.GET.get('activo', None)
            inactivo = self.request.GET.get('inactivo', None)
        else:
            base_general = None
            base_voluntarios = None
            base_fiscal = None
            con_email = None
            con_celular = None
            con_domicilio = None
            hasta_30_anios = None
            de_31_a_45_anios = None
            mas_de_46_anios = None
            sexo_f = None
            sexo_m = None
            sexo_x = None
            activo = None
            inactivo = None
           
        if palabra:
            object_list = self.model.objects.filter(
            Q(nombres__icontains=palabra) |
            Q(apellidos__icontains=palabra) |   
            Q(documento__icontains=palabra) |
            Q(telefono__iexact=palabra) |
            Q(observaciones__icontains=palabra)
    )
        else: object_list = self.model.objects.all()

        if base_general:  object_list = object_list.filter(es_voluntario=False).filter(es_fiscal=False)
        if base_voluntarios:  object_list = object_list.filter(es_voluntario=True)
        if base_fiscal:  object_list = object_list.filter(es_fiscal=True)
        if con_email:  object_list = object_list.filter(email__isnull=False)
        if con_celular:  object_list = object_list.filter(telefono__isnull=False)
        if con_domicilio:  object_list = object_list.filter(calle__isnull=False)
        if sexo_f:  object_list = object_list.filter(sexo="Femenino")
        if sexo_m:  object_list = object_list.filter(sexo="Masculino")
        if sexo_x:  object_list = object_list.filter(sexo="X")
        if hasta_30_anios:  
            age_threshold = today.year - 30
            object_list = object_list.filter(fecha_nacimiento__gte=date(age_threshold, today.month, today.day))
        if de_31_a_45_anios:
            today = date.today()
            age_threshold_1 = today.year - 31
            age_threshold_2 = today.year - 45
            object_list = object_list.filter(
                fecha_nacimiento__lte=date(age_threshold_1, today.month, today.day),
                fecha_nacimiento__gte=date(age_threshold_2, today.month, today.day)
            )
        if mas_de_46_anios:
            today = date.today()
            age_threshold = today.year - 46
            object_list = object_list.filter(fecha_nacimiento__lte=date(age_threshold, today.month, today.day))        
        if activo:  object_list = object_list.filter(activo=True)
        if inactivo:  object_list = object_list.filter(activo=False)

        object_list = object_list.distinct()

        return object_list


class PerfilesDetailView(LoginRequiredMixin,DetailView):  
    model = Perfiles

    def get_context_data(self, **kwargs):
        context = super(PerfilesDetailView, self).get_context_data(**kwargs)
        context['voluntario'] = BaseVoluntariosPerfiles.objects.filter(fk_perfil_v=self.get_object().pk).first()
        context['fiscal'] = BaseFiscalesPerfiles.objects.filter(fk_perfil_f=self.get_object().pk).first()
        return context
    

class PerfilesDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):  
    model = Perfiles
    success_url= reverse_lazy("perfiles_listar")
    success_message = "El registro fue eliminado correctamente"  


class PerfilesCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):    
    model = Perfiles
    form_class = PerfilesForm
    success_message = "Registrado correctamente"  


class PerfilesUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Perfiles
    form_class = PerfilesForm    
    success_message = "Editado correctamente"   


class EdicionMultipleFormView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
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
class VoluntariosCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):    
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
class FiscalesCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):    
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

