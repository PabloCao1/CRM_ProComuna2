from datetime import date
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from Bases.choices import *
from Bases.models import *


class Bases(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
#---------TABLA EVENTOS------------------

class Eventos(models.Model):
    nombre = models.CharField(max_length=250, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    hora = models.CharField(max_length= 2, null=True, blank=True)
    minutos = models.CharField(max_length= 2, null=True, blank=True)
    lugar = models.CharField(max_length=250, null=True, blank=True)
    calle = models.CharField(max_length=250, null=True, blank=True)
    altura = models.PositiveSmallIntegerField(null=True, blank=True)
    telefono = models.PositiveIntegerField(null=True, blank=True)
    WEB = models.URLField(max_length=250, null=True, blank=True)
    modo = models.CharField(max_length=15, null=True, blank=True)
    observaciones = models.CharField (max_length= 500, null=True, blank=True)
    foto = models.ImageField(upload_to="img_eventos", default='default.png')
    activo = models.BooleanField(default=True)
    invitados_individuales = models.ManyToManyField(Perfiles, null=True, blank=True)
    grupos_invitados = models.ManyToManyField(Bases, null=True, blank=True)
    creado     = models.DateField(auto_now_add=True)
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
        ordering = ['fecha']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def get_absolute_url(self):
        return reverse('eventos_ver', kwargs={'pk': self.pk})
