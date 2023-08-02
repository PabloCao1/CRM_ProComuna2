from django import forms
from .models import *
from .validators import MaxSizeFileValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class PerfilesForm(forms.ModelForm):
    
    class Meta:
        model = Perfiles
        exclude = ('creado','modificado',)
        widgets = {
            'activo' :              forms.CheckboxInput(attrs={'class': 'btn-check btn-lg"', 'autocomplete':"off"}),
            'observaciones' :       forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
            'fecha_nacimiento' :    forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
            'fecha_ingreso' :    forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
            'es_empleadoGCBA': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'es_militante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),        
            
        }
        labels = {
            'tipo_doc': 'Tipo',
            'fecha_ingreso': 'Fecha de ingreso en la base',
            'es_empleadoGCBA': 'Es empleado/a del GCBA?',
            'es_militante': 'Es militante?',
        }

    def clean_telefono(self):
        instance = self.instance  # Obtener la instancia del objeto actual
        telefono = self.cleaned_data['telefono']
        if telefono and telefono != instance.telefono and Perfiles.objects.filter(telefono=telefono).exists():
            raise forms.ValidationError("Ya existe un perfil con este número de teléfono en la base de datos.")
        return telefono


class BaseVoluntariosPerfilesForm(forms.ModelForm):
   
    class Meta:
        model = BaseVoluntariosPerfiles
        exclude = ('creado','modificado',)
        widgets = {
            'grupo_wsp' :           forms.CheckboxInput(attrs={'class': 'btn-check btn-lg', 'autocomplete':"off"}),
            'gen_23' :              forms.CheckboxInput(attrs={'class': 'btn-check btn-lg', 'autocomplete':"off"}),
            'eventos' :             forms.CheckboxInput(attrs={'class': 'btn-check btn-lg', 'autocomplete':"off"}),
            'observaciones_v' :       forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
        }
        labels = {
            'grupo_wsp': 'Está en grupo de Wsp JXC?',
            'gen_23': 'Está en gen 23?',
            'eventos': 'Participa en eventos del local?',            
            'otro_afinidad': 'Cual?',
        }


class BaseFiscalesPerfilesForm(forms.ModelForm):
   
    class Meta:
        model = BaseFiscalesPerfiles
        exclude = ('creado','modificado',)
        widgets = {
            'fue_fiscal' :          forms.CheckboxInput(attrs={'class': 'btn-check btn-lg', 'autocomplete':"off"}),
            'fecha_fiscal' :        forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
            'observaciones_f' :       forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
        }
        labels = {
            'fue_fiscal': 'Fué fiscal antes?',
            'fecha_fiscal': 'Última fecha en que fue fiscal',
            'rol_fiscal': 'Rol ejercido',            
            'disp_jornada': 'Disponibilidad',
            'desempeno': 'Desempeño',
        }