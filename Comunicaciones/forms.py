from django import forms
from .models import *
from Bases.validators import MaxSizeFileValidator
from django.forms.widgets import SelectMultiple

# class Select2EmailWidget(SelectMultiple):
#     def render_option(self, selected_choices, option_value, option_label):
#         email = option_label.email
#         option_attrs = {
#             'selected': 'selected' if str(option_value) in selected_choices else '',
#             'value': option_value,
#         }
#         return self.option_template.render({
#             'widget': self,
#             'email': email,
#             'attrs': option_attrs,
#         })

#     def format_value(self, value):
#         if value is None:
#             return []
#         return [self.queryset.get(pk=pk).email for pk in value]

class ComunicacionesForm(forms.ModelForm):
    archivos = forms.FileField(
        required=False, 
        label="Adjuntos", 
        validators=[MaxSizeFileValidator(max_file_size=2)],
    )

    grupo_de_destinatarios = forms.MultipleChoiceField(required=False,widget=forms.SelectMultiple(),
    choices=[('Base Fiscales', 'Base Fiscales'),('Base Voluntarios', 'Base Voluntarios'),('Base General', 'Base General'),])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        destinatarios = Perfiles.objects.filter(email__isnull=False, activo=True)
        self.fields['destinatarios'].queryset = destinatarios
        # destinatarios = Perfiles.objects.filter(email__isnull=False, activo=True).values_list('id', 'email')
        # self.fields['destinatarios'].choices = destinatarios


    class Meta:
        model = Comunicaciones
        exclude = ('creado',)
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 5, 'placeholder': ''}),
            # 'destinatarios': Select2EmailWidget(attrs={'class': 'select2 w-100'}),
        }
        labels = {
            'titulo': 'Título del mensaje',
            'asunto': 'Asunto del email',
        }

    # Sobrescribir label_from_instance para mostrar el correo electrónico en el select2
    # def label_from_instance(self, obj):
    #     return obj.email

