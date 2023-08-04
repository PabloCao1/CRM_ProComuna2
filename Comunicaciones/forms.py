from django import forms
from .models import *
from Bases.validators import MaxSizeFileValidator

class ComunicacionesForm(forms.ModelForm):
    archivos = forms.FileField(
        required=False, 
        label="Adjuntos", 
        validators=[MaxSizeFileValidator(max_file_size=2)],
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        destinatarios=Perfiles.objects.filter(email__isnull=False)
        self.fields['destinatarios'].queryset = destinatarios #solo envio los perfiles que tienen mail

    class Meta:
        model = Comunicaciones
        exclude = ('creado',)
        widgets = {
            'mensaje' :   forms.Textarea(attrs={'rows':5, 'placeholder': ''}),
        }
        labels = {
            'titulo': 'Título del mensaje',
            'asunto': 'Asunto del email',
        }
