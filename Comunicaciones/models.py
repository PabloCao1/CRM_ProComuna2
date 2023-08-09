from datetime import date
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from Bases.choices import *
from Bases.models import *
from Eventos.models import Bases


#---------TABLA COMUNICACIONES------------------
class Comunicaciones(models.Model):
    asunto                  = models.CharField(max_length=250)
    titulo                  = models.CharField(max_length=250)
    mensaje                 = models.CharField (max_length= 1000)
    fallo                   = models.CharField (max_length= 500, null=True, blank=True)
    destinatarios           = models.ManyToManyField(Perfiles,blank=True)
    creado                  = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.asunto
    
    class Meta:
        ordering = ['creado']
        verbose_name = 'Comunicacion'
        verbose_name_plural = 'comunicaciones'

    def get_absolute_url(self):
        return reverse('comunicaciones_ver', kwargs={'pk': self.pk})

class ComunicacionesArchivos(models.Model):
    fk_comunicacion = models.ForeignKey(Comunicaciones, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='comunicaciones/archivos/')
    tipo = models.CharField(max_length=12)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Archivo {self.id} de la comunicación {self.fk_comunicacion}"