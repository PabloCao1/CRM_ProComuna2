from django import forms
from .models import *
from Bases.validators import MaxSizeFileValidator
from .choices import *

class EventosForm(forms.ModelForm):

    flyer = forms.ImageField(required=False, label="Flyer evento", validators=[MaxSizeFileValidator(max_file_size=2)])
    grupo_de_invitados = forms.MultipleChoiceField(required=False,widget=forms.SelectMultiple(),
    choices=[('Base Fiscales', 'Base Fiscales'),('Base Voluntarios', 'Base Voluntarios'),('Base General', 'Base General'),])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        invitados = Perfiles.objects.filter(email__isnull=False, activo=True)
        self.fields['invitados'].queryset = invitados
        self.fields['minutos'].widget.attrs.update({'disabled': 'disabled'})

        if 'hora' in self.data and self.data['hora']:
            self.fields['minutos'].required = True
            self.fields['minutos'].widget.attrs.update({'disabled': ''})
    
    class Meta:
        model = Eventos
        exclude = ('creado','modificado',)
        widgets = {
            'mensaje' :               forms.Textarea(attrs={'rows':5, 'placeholder': ''}),
            'fecha' :                       forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
            'modo':                         forms.Select(choices=CHOICE_MODO),
            'hora':                         forms.Select(choices=CHOICE_HORA),
            'minutos':                      forms.Select(choices=CHOICE_MINUTOS),
        }
        labels = {
            'departamento': 'Depto./Oficina',
            'nombre': 'Nombre del evento',
        }

        