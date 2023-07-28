from django import forms
from .models import *
from Bases.validators import MaxSizeFileValidator

class ComunicacionesForm(forms.ModelForm):
    
    foto = forms.ImageField(required=False, label="Archivo", validators=[MaxSizeFileValidator(max_file_size=2)])

    class Meta:
        model = Comunicaciones
        exclude = ('creado','modificado',)
        widgets = {
            'activo' :              forms.CheckboxInput(attrs={'class': 'btn-check btn-lg"', 'autocomplete':"off"}),
            'texto' :       forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
            'grupos_invitados' :           forms.CheckboxSelectMultiple(attrs={"class": "custom-control-input"},),
            'invitados_individuales' :           forms.CheckboxSelectMultiple(attrs={"class": "custom-control-input"},),
            'fecha' :    forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
        }
        labels = {
            'texto': 'Mensaje',
            'grupos_invitados': '',
            'invitados_individuales': '',
        }