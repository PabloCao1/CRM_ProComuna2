from datetime import date
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from Bases.choices import *
from Bases.models import *
from Eventos.models import Bases


#---------TABLA EVENTOS------------------
class Comunicaciones(models.Model):
    nombre = models.CharField(max_length=250, null=False, blank=False)
    texto = models.CharField (max_length= 500, null=True, blank=True)
    foto = models.ImageField(upload_to="img_comunicaciones", default='default.png')
    activo = models.BooleanField(default=True)
    invitados_individuales = models.ManyToManyField(Perfiles, blank=True)
    grupos_invitados = models.ManyToManyField(Bases, blank=True)
    creado     = models.DateField(auto_now_add=True)
    enviado = models.DateField(null=True, blank=True)
    modificado = models.DateField(auto_now=True)

    def delete(self):
        if not (self.foto.name.endswith('default.png')):
            self.foto.delete() # borra la imagen fisica
        return super().delete()

    def soft_delete(self):
        self.activo = False
        self.save()

    def restore(self):
        self.activo = True
        self.save()
    
    class Meta:
        ordering = ['creado']
        verbose_name = 'Comunicacion'
        verbose_name_plural = 'comunicaciones'

    def get_absolute_url(self):
        return reverse('comunicaciones_ver', kwargs={'pk': self.pk})