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
    nombre                  = models.CharField(max_length=250)
    fecha                   = models.DateField()
    hora                    = models.CharField(max_length= 2, null=True, blank=True)
    minutos                 = models.CharField(max_length= 2, null=True, blank=True)
    lugar                   = models.CharField(max_length=250, null=True, blank=True)
    calle                   = models.CharField(max_length=250, null=True, blank=True)
    altura                  = models.PositiveSmallIntegerField(null=True, blank=True)
    piso                    = models.CharField(max_length=10, null=True, blank=True)
    departamento            = models.CharField(max_length=20, null=True, blank=True)
    telefono                = models.PositiveIntegerField(null=True, blank=True)
    web                     = models.URLField(max_length=250, null=True, blank=True)
    modo                    = models.CharField(max_length=15, null=True, blank=True)
    mensaje                 = models.CharField (max_length= 1000, null=True, blank=True)
    flyer                   = models.ImageField(upload_to="eventos/", default='default.png')
    invitados               = models.ManyToManyField(Perfiles,blank=True)
    fallo                   = models.CharField (max_length= 1000, null=True, blank=True)
    creado                  = models.DateField(auto_now_add=True)
    modificado              = models.DateField(auto_now=True)

    def delete(self):
        if not (self.foto.name.endswith('default.png')):
            self.foto.delete() # borra la imagen fisica
        return super().delete()

    @property
    def estado(self):
        if self.fecha < date.today():
            return "Finalizado"
        elif self.fecha == date.today():
            return "Vigente"
        else:
            return "Pendiente"

    class Meta:
        ordering = ['fecha']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def get_absolute_url(self):
        return reverse('eventos_ver', kwargs={'pk': self.pk})
