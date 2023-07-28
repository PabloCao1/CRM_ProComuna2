from django import forms
from .models import *
from Bases.validators import MaxSizeFileValidator
from .choices import *

class EventosForm(forms.ModelForm):
    
    foto = forms.ImageField(required=False, label="Foto evento", validators=[MaxSizeFileValidator(max_file_size=2)])

    class Meta:
        model = Eventos
        exclude = ('creado','modificado',)
        widgets = {
            'activo' :              forms.CheckboxInput(attrs={'class': 'btn-check btn-lg"', 'autocomplete':"off"}),
            'observaciones' :       forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
            'grupos_invitados' :           forms.CheckboxSelectMultiple(attrs={"class": "custom-control-input"},),
            'invitados_individuales' :           forms.CheckboxSelectMultiple(attrs={"class": "custom-control-input"},),
            'fecha' :    forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
            'modo': forms.Select(choices=CHOICE_MODO),
            'WEB': forms.URLInput(),
            'hora': forms.Select(choices=CHOICE_HORA),
            'minutos': forms.Select(choices=CHOICE_MINUTOS),
        }
        labels = {
            'foto': '',
            'grupos_invitados': '',
            'invitados_individuales': '',
        }