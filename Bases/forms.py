from django import forms
from .models import *
from .validators import MaxSizeFileValidator
from django.core.validators import MinValueValidator, MaxValueValidator


class PerfilesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            perfil=Perfiles.objects.get(id=self.instance.pk)
            self.fields['barrio'].initial = perfil.barrio
            self.fields['comuna'].initial = perfil.comuna
    
    class Meta:
        model = Perfiles
        exclude = ('creado','modificado','fecha_inactivo', 'motivo_inactivo')
        widgets = {
            'es_empleadoGCBA' :     forms.Select(choices=[(True, 'SI'), (False, 'NO')]),
            'es_militante' :        forms.Select(choices=[(True, 'SI'), (False, 'NO')]),
            'observaciones' :       forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
            'socio_futbol' :        forms.Select(choices=[(True, 'SI'), (False, 'NO')]),
            'matriculado' :         forms.Select(choices=[(True, 'SI'), (False, 'NO')]),
            'fecha_nacimiento' :    forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),     
            
        }
        labels = {
            'tipo_doc': 'Tipo',
            'es_empleadoGCBA': 'Es empleado/a del GCBA?',
            'es_militante': 'Es militante?',
            'equipo_futbol': 'Equipo de Fútbol',
            'socio_futbol': 'Es socio del Club?',
            'profesion' : "Profesión/Actividad",
            'matriculado' : "Matriculado en CABA?",
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
            'grupo_wsp' :           forms.Select(choices=[(True, 'SI'), (False, 'NO')]),
            'gen_23' :              forms.Select(choices=[(True, 'SI'), (False, 'NO')]),
            'eventos' :             forms.Select(choices=[(True, 'SI'), (False, 'NO')]),
            'observaciones_v' :     forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
        }
        labels = {
            'grupo_wsp': 'Está en grupo de Wsp JXC?',
            'gen_23': 'Está en gen 23?',
            'eventos': 'Participa en eventos del local?',            
            'otro_afinidad': 'Cual?',
            'observaciones_v': 'Observaciones',
        }


class BaseFiscalesPerfilesForm(forms.ModelForm):
   
    class Meta:
        model = BaseFiscalesPerfiles
        exclude = ('creado','modificado',)
        widgets = {
            'fue_fiscal' :          forms.Select(choices=[(True, 'SI'), (False, 'NO')]),
            'fecha_fiscal' :        forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
            'observaciones_f' :     forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
        }
        labels = {
            'fue_fiscal': 'Fué fiscal antes?',
            'fecha_fiscal': 'Última fecha en que fue fiscal',
            'rol_fiscal': 'Rol ejercido',            
            'disp_jornada': 'Disponibilidad',
            'desempeno': 'Desempeño',
            'observaciones_f': 'Observaciones',
        }